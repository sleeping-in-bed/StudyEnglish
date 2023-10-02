import copy
import multiprocessing
import os
import re
import zipfile
from datetime import datetime, timedelta
import random

from psplpy import data_access, file_util, timing

'''
words: {word->str: {'ch_trans': str, 'study_record': {'last_study_time': yyyy-mm-dd->str,
        'study_times': int, 'word_status': 'mastered' | 'studying' | 'obsolete' | 'finished'->str
        [, 'meaning_study_times': int, 'not_know_flag': bool, 'interesting': bool, 'aliases': [str]]}}}
words_info: {word->str: {'ch_trans': {part_of_speech->str: trans->str, ...}, 
                         'phonetic': {'uk': {'symbol': str, 'pronunciation': path->str}, 'us': ...}}
'''


class Base:
    review_time_table = {0: 0, 1: 1, 2: 3, 3: 7, 4: 14, 5: 30, 6: 60, 7: 120, 8: 240}
    every_turn_study_words_num = 10
    day_fmt = '%Y-%m-%d'

    obsolete_status = 'obsolete'
    mastered_status = 'mastered'
    finished_status = 'finished'
    studying_status = 'studying'

    project_dir = os.path.dirname(os.path.abspath(__file__))
    backup_dir = file_util.create_dir(os.path.join(project_dir, 'backup'))
    pronunciation_dir = file_util.create_dir(os.path.join(project_dir, r'data\pronunciation'))
    words_path = os.path.join(project_dir, r'data\words.json')
    words_info_path = os.path.join(project_dir, r'data\words_info.json')
    words_txt_path = os.path.join(project_dir, r'word.txt')

    def __init__(self, debug: bool = False, load_words: bool = True, load_words_info: bool = True,
                 words_dict: dict = None, words_info_dict: dict = None):
        # 使用前先备份项目
        # self.backup_project()
        self.debug = debug
        if load_words:
            if words_dict:
                self.words_dict = words_dict
            else:
                self.words_dict = self.load_words_dict()
            self.using_words_dict = copy.deepcopy(self.words_dict)
        if load_words_info:
            if words_info_dict:
                self.words_info_dict = words_info_dict
            else:
                self.words_info_dict = self.load_words_info_dict()

    @timing.timing_decorator()
    def _group_words_by_time(self, words_items_list: list) -> dict:
        """data_format: {time_index->int: [word_item->tuple, ...], ...}"""
        # 创建一个空字典，用于存储分组后的时间字符串
        grouped_word_dict_by_time = {}
        # 遍历时间字符串列表
        for word_item in words_items_list:
            # 将上次复习时间字符串转换为 datetime 对象
            last_study_date = datetime.strptime(word_item[1]['study_record']['last_study_time'], self.day_fmt)
            # 计算当前时间与上次复习时间之间的天数差
            days_diff = (self.get_today_zero_time() - last_study_date).days
            # 获取当前单词的复习天数间隔，新单词为0
            review_days = self.review_time_table[word_item[1]['study_record']['study_times']]
            if review_days != 0:
                # 计算天数差与复习天数间隔，得出比率，比率越大，越应该先复习
                ratio = days_diff / review_days
            else:
                # 如果复习天数间隔为0，说明是新单词，设置比率为 -1
                ratio = -1
            if ratio in grouped_word_dict_by_time:
                grouped_word_dict_by_time[ratio].append(word_item)
            else:
                grouped_word_dict_by_time[ratio] = [word_item]
        if self.debug:
            print(grouped_word_dict_by_time)
        return grouped_word_dict_by_time

    @timing.timing_decorator()
    def shuffle_using_words_dict(self) -> dict:
        # 将字典的键值对转化为列表，然后打乱顺序
        words_items = list(self.using_words_dict.items())
        # 将单词进行分组
        grouped_items = self._group_words_by_time(words_items)
        for group_index in grouped_items:
            random.shuffle(grouped_items[group_index])
        # 降序排序，比率大的先学习
        iterate_order = sorted(grouped_items.keys(), reverse=True)
        if self.debug:
            print({i: len(grouped_items[i]) for i in iterate_order})
        new_order_items = []
        for group_index in iterate_order:
            for item in grouped_items[group_index]:
                new_order_items.append(item)
        # 重新构造字典
        new_dict = dict(new_order_items)
        if self.debug:
            print(new_dict)
        return new_dict

    def is_need_study(self, word: str) -> bool:
        no_need_study_statuses = [self.mastered_status, self.obsolete_status, self.finished_status]
        if self.using_words_dict[word]['study_record']['word_status'] not in no_need_study_statuses:
            return True

    def is_new(self, word: str) -> bool:
        if self.is_need_study(word) and self.using_words_dict[word]['study_record']['study_times'] == 0:
            return True

    def is_need_review(self, word: str) -> bool:
        if self.is_need_study(word) and not self.using_words_dict[word]['study_record']['study_times'] == 0:
            return True

    @timing.timing_decorator()
    def get_review_date_dict(self) -> dict:
        review_date_dict = {}
        # 今天0点时间
        zero_time = self.get_today_zero_time()
        zero_time_str = zero_time.strftime(self.day_fmt)
        for word in self.using_words_dict:
            # 如果不是新单词且没有不需要学习的status，那么总会在某一天复习，否则直接退出函数，返回None
            if self.is_need_review(word):
                # 上次学习完成日期的0点时间
                last_study_time = datetime.strptime(self.using_words_dict[word]['study_record']['last_study_time'],
                                                    self.day_fmt)
                # 根据study_times获得review_time_table的复习日期间隔
                interval_days = self.review_time_table[self.using_words_dict[word]['study_record']['study_times']]
                # 算出复习的日期的0点时间
                review_day = last_study_time + timedelta(days=interval_days)
                # 如果复习日在未来
                if review_day > zero_time:
                    review_day_str = review_day.strftime(self.day_fmt)
                    if not review_date_dict.get(review_day_str):
                        review_date_dict[review_day_str] = []
                    review_date_dict[review_day_str].append(word)
                # 如果复习日在今天或者过去的某一天，则都是今天该复习的
                else:
                    if not review_date_dict.get(zero_time_str):
                        review_date_dict[zero_time_str] = []
                    review_date_dict[zero_time_str].append(word)
        return review_date_dict

    @staticmethod
    def get_today_zero_time():
        return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    @timing.timing_decorator()
    def load_words_dict(self) -> dict:
        return data_access.load_json_maybe_null(self.words_path, dict)

    @timing.timing_decorator()
    def load_words_info_dict(self) -> dict:
        return data_access.load_json_maybe_null(self.words_info_path, dict)

    @timing.timing_decorator()
    def update_words_dict(self) -> None:
        # 将words_dict的新值赋给original_words_dict，从而不改变原字典顺序
        for word in self.using_words_dict:
            self.words_dict[word] = self.using_words_dict[word]

    @timing.timing_decorator()
    def dump_words_dict(self) -> None:
        data_access.dump_json_human_friendly(self.words_dict, self.words_path)

    @timing.timing_decorator()
    def dump_words_info_dict(self) -> None:
        data_access.dump_json_human_friendly(self.words_info_dict, self.words_info_path)

    def _load_words_txt(self, ret_value, loop_task):
        file_content = open(self.words_txt_path, encoding='utf-8').readlines()
        for i in range(0, len(file_content), 2):
            try:
                if word := file_content[i].strip():
                    loop_task(file_content, word, i)
            except IndexError:
                pass
        return ret_value

    @timing.timing_decorator()
    def load_words_txt_dict(self) -> dict:
        new_words_dict = {}
        loop_task = lambda file_content, word, i: new_words_dict.update({word: file_content[i + 1].strip()})
        return self._load_words_txt(new_words_dict, loop_task)

    @timing.timing_decorator()
    def load_words_txt_word_list(self) -> list:
        new_words_list = []
        loop_task = lambda file_content, word, i: new_words_list.append(word)
        return self._load_words_txt(new_words_list, loop_task)

    def _backup_project(self) -> str:
        exclude_abspath = [self.backup_dir]
        exclude_relpath = [r'data\pronunciation', 'history']
        regex_list = [re.compile(r'.*[.](?:exe|pyc)$')]
        file_list = file_util.get_files_in_dir(self.project_dir, exclude_abspath=exclude_abspath,
                                               exclude_relpath=exclude_relpath,
                                               exclude_abspath_match_compiled_regex=regex_list)
        save_path = os.path.join(self.backup_dir, file_util.get_current_time_as_file_name('zip'))
        with zipfile.ZipFile(save_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in file_list:
                zipf.write(file)
        return save_path

    @timing.timing_decorator()
    def backup_project(self):
        multiprocessing.Process(target=self._backup_project).start()

    @staticmethod
    @timing.timing_decorator()
    def process_phrase(phrase: str) -> list:
        word_list = phrase.split()
        for i in range(len(word_list)):
            # 把单词变成小写的；之后只保留英文字符
            word_list[i] = re.sub(r"[^a-z'-]", "", word_list[i].casefold())
            # 如果上述处理进行完，单词没有变成空字符串（例如原字符串只有一个逗号）
            if word_list[i]:
                # 去除's、'd一类的后缀，例如 Smith's
                word_list[i] = re.sub(r'(?:\'s|\'d)\b', '', word_list[i])

        # 清除处理后变成空字符串的单词
        return [word for word in word_list if word]

    @staticmethod
    def _2_data_to_3(data_2: dict) -> dict:
        for word in data_2:
            data_2[word]['ch_trans'] = data_2[word]["chinese_translation"]
            data_2[word].pop("chinese_translation")
            data_2[word].pop("phonetic_symbol")
            data_2[word] = {key: data_2[word][key] for key in sorted(data_2[word])}
        return data_2


if __name__ == '__main__':
    pass
