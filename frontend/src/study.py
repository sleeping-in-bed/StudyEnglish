import copy
from datetime import datetime
import re

from psplpy import interact_util, timing
from base import Base
from word_info import WordInfo


class Study(Base):
    new_mode = 'new'
    review_mode = 'review'

    meaning_stage = 'meaning'
    spell_stage = 'spell'
    invalid_input_tip = '输入错误，请重新输入'

    def __init__(self, debug: bool = False, debug_words_dict: dict = None):
        super(Study, self).__init__(debug=debug, words_dict=debug_words_dict)
        self.init_data()

    @timing.timing_decorator()
    def init_data(self):
        self.using_words_dict = copy.deepcopy(self.words_dict)
        self.using_words_dict = self.shuffle_using_words_dict()
        self.review_date_dict = self.get_review_date_dict()
        (self.new_words_num, self.new_words_list, self.review_words_num,
            self.review_words_list) = self.get_words_num_and_list_of_new_and_review()

    @timing.timing_decorator()
    def get_words_num_and_list_of_new_and_review(self) -> (int, list, int, list):
        new_words_list = []
        for word in self.using_words_dict:
            if self.is_new(word):
                new_words_list.append(word)
        new_count = len(new_words_list)

        today_key = self.get_today_zero_time().strftime(self.day_fmt)
        if self.review_date_dict.get(today_key):
            review_words_list = self.review_date_dict[today_key]
        else:
            review_words_list = []
        review_count = len(review_words_list)

        return new_count, new_words_list, review_count, review_words_list

    def check_meaning_study_times(self, word: str, times: int) -> bool:
        return self.using_words_dict[word]['study_record'].setdefault('meaning_study_times', 0) < times

    def whether_study_finish_this_time(self, word: str, stage: str) -> bool:
        if self.is_need_study(word):
            if stage == Study.meaning_stage:
                if self.study_mode == Study.new_mode:
                    return self.check_meaning_study_times(word, 3)
                elif self.study_mode == Study.review_mode:
                    if not self.using_words_dict[word]['study_record'].setdefault('not_know_flag', False):
                        return self.check_meaning_study_times(word, 1)
                    else:
                        self.using_words_dict[word]['study_record']["study_times"] = 0
                        return self.check_meaning_study_times(word, 3)
            elif stage == Study.spell_stage:
                return self.check_meaning_study_times(word, 1)

    def set_status(self, status: str):
        self.using_words_dict[self.studying_word]['study_record']['word_status'] = status

    def zero_cleaning_meaning_study_time_and_set_not_know_true(self):
        self.using_words_dict[self.studying_word]['study_record']['meaning_study_times'] = 0
        self.using_words_dict[self.studying_word]['study_record']['not_know_flag'] = True

    def study_meaning_procedure(self) -> None:
        def _fixed_choice(inner_choice: str) -> None:
            if inner_choice == '4':
                # 设置本单词已掌握
                self.set_status(Study.mastered_status)
                print('已标记掌握')
            elif inner_choice == '5':
                # 设置本单词已废弃
                self.set_status(Study.obsolete_status)
                print('已标记废弃')

        # 打印单词和音标
        print(self.studying_word)
        print(self.study_phonetic_symbol_dict[self.studying_word])
        # 询问是否知道中文含义
        choice = interact_util.limited_input(['1', '2', '3', '4', '5'], error_tip=self.invalid_input_tip,
                                             print_str='认识输入1，不认识输入2，标记已掌握输入4，标记废弃输入5\n')
        if choice == '1':
            # 如果没记错含义，则打印中文，供用户检查是否与自己想的一致
            print(self.using_words_dict[self.studying_word]['ch_trans'])
            subchoice = interact_util.limited_input(['1', '2', '3', '4', '5'], error_tip=self.invalid_input_tip,
                                                    print_str='没记错输入1，记错了输入2，标记已掌握输入4，标记废弃输入5\n')
            if subchoice == '1':
                # 没记错含义，本次学习次数+1
                self.using_words_dict[self.studying_word]['study_record']['meaning_study_times'] += 1
            elif subchoice == '2':
                # 记错了，清零本次学习次数，并设置一个未答对标签
                self.zero_cleaning_meaning_study_time_and_set_not_know_true()
            else:
                _fixed_choice(subchoice)
        elif choice == '2':
            # 不认识，清零本次学习次数，并设置一个未答对标签
            self.zero_cleaning_meaning_study_time_and_set_not_know_true()
            # 打印中文供用户查看中文含义
            print(self.using_words_dict[self.studying_word]['ch_trans'])
            interact_util.limited_input(['1', '3'], print_str='输入1继续\n', error_tip=self.invalid_input_tip)
        else:
            _fixed_choice(choice)

    def _examine_spell(self) -> bool:
        # 打印中文含义，让用户根据其填写英文
        print(self.using_words_dict[self.studying_word]['ch_trans'])
        # 只保留英文字母，并转化为小写，从而避免一些无关因素影响检查的准确性，之后检查英文是否输入正确
        input_str = re.sub(r"[^a-zA-Z]", "", input('请输入英文\n')).casefold()
        if input_str == re.sub(r"[^a-zA-Z]", "", self.studying_word).casefold():
            # 如果正确，则打印出英文及其音标，并将本次拼写次数+1，返回True让程序知道本次拼写正确
            print(self.studying_word)
            print(self.study_phonetic_symbol_dict[self.studying_word])
            self.using_words_dict[self.studying_word]['study_record']['meaning_study_times'] += 1
            return True

    def study_spell_procedure(self) -> None:
        while True:
            # 如果拼写不正确
            if not self._examine_spell():
                # 打印英文及其音标，供用户查看
                print(f'拼写错误，正确拼写：{self.studying_word}')
                print(self.study_phonetic_symbol_dict[self.studying_word])
                choice = interact_util.limited_input(['1', '2', '3'], error_tip=self.invalid_input_tip,
                                                     print_str='输入1继续拼写，输入2跳过该拼写，输入3重新学习，并继续拼写\n')
                if choice == '2':
                    # 将本次拼写次数+1，从而跳过拼写
                    self.using_words_dict[self.studying_word]['study_record']['meaning_study_times'] += 1
                    return
                elif choice == '3':
                    # 修改words_dict和original_words_dict，并保存单词数据
                    self.using_words_dict[self.studying_word]['study_record']['study_times'] = 1
                    self.words_dict[self.studying_word]['study_record']['study_times'] = 1
                    self.dump_words_dict()
                    print('已重置')
            # 如果拼写正确，退出函数
            else:
                return

    def study_ending_clear(self) -> None:
        for word in self.study_list:
            self.using_words_dict[word]['study_record'].pop('meaning_study_times', None)
            self.using_words_dict[word]['study_record'].pop('not_know_flag', None)

    def meaning_study_ending_settle(self) -> None:
        for word in self.study_list:
            self.using_words_dict[word]['study_record']['study_times'] += 1
            self.using_words_dict[word]['study_record']['last_study_time'] = self.study_date

    def study(self, stage: str):
        # 是否所有单词都学习完成的标识
        flag = True
        while flag:
            flag = False
            for self.studying_word in self.study_list:
                if self.whether_study_finish_this_time(self.studying_word, stage):
                    # 如果经过判断，还有单词未学习完成，则将flag设置为True
                    flag = True
                    if stage == Study.meaning_stage:
                        self.study_meaning_procedure()
                    elif stage == Study.spell_stage:
                        self.study_spell_procedure()
        # 学习完成，清理临时数据
        self.study_ending_clear()
        if stage == Study.meaning_stage:
            # 如果正常完成词义学习，更新学习数据
            self.meaning_study_ending_settle()

    def _get_study_list(self) -> list:
        study_list = []
        if self.study_mode == Study.new_mode:
            words_list = self.new_words_list
        elif self.study_mode == Study.review_mode:
            words_list = self.review_words_list
        else:
            raise ValueError

        for word in words_list:
            if len(study_list) == self.every_turn_study_words_num:
                break
            study_list.append(word)
        return study_list

    def get_word_phonetic_symbol(self, word) -> str:
        try:
            phonetic_symbol = f"/{self.words_info_dict[word]['phonetic']['us']['symbol']}/"
        except KeyError:
            phonetic_symbol = '/None/'
        return phonetic_symbol

    @timing.timing_decorator()
    def get_study_phonetic_symbol_dict(self) -> dict:
        study_phonetic_symbol_dict = {}
        for phrase in self.study_list:
            word_list = self.process_phrase(phrase)
            phase_phonetic_symbol = ''
            for word in word_list:
                phonetic = self.get_word_phonetic_symbol(word)
                phase_phonetic_symbol += f'{phonetic} '
            study_phonetic_symbol_dict[phrase] = phase_phonetic_symbol.strip()
        return study_phonetic_symbol_dict

    def show_review_time_table(self):
        count = 0
        for date in sorted(self.review_date_dict.keys()):
            number = len(self.review_date_dict[date])
            count += number
            print(f'{date}: {number}')
        print(f'total: {count}')

    def main(self):
        while True:
            print(f'当前待学习单词数量：{self.new_words_num}')
            print(f'当前待复习单词数量：{self.review_words_num}')
            tip_str = '输入1学习新单词，输入2复习单词，输入3退出，输入4查看时间表，输入5添加新单词，输入6补充单词信息\n'
            choice = interact_util.limited_input(['1', '2', '3', '4', '5', '6'], print_str=tip_str,
                                                 error_tip=self.invalid_input_tip)
            if choice in ['1', '2']:
                if choice == '1':
                    self.study_mode = Study.new_mode
                elif choice == '2':
                    self.study_mode = Study.review_mode

                self.study_list = self._get_study_list()
                print(f'本次学习的单词：{self.study_list}')
                self.study_phonetic_symbol_dict = self.get_study_phonetic_symbol_dict()
                self.studying_word = None
                self.study_date = datetime.now().strftime(self.day_fmt)

                print(f'本次学习数量：{len(self.study_list)}')
                self.study(Study.meaning_stage)
                if not self.debug:
                    # 及时更新words_dict，防止数据丢失
                    self.update_words_dict()
                    self.dump_words_dict()
                else:
                    return self.using_words_dict
                choice = interact_util.limited_input(['s', '2', '3'], error_tip=self.invalid_input_tip,
                                                     print_str='学习完成！输入s开始拼写，输入2跳过拼写，输入3退出\n')
                if choice == 's':
                    self.study(Study.spell_stage)
                elif choice == '3':
                    return

                choice = interact_util.limited_input(['new', '3'], print_str='学习完成！输入new开始新一轮学习，输入3退出\n',
                                                     error_tip=self.invalid_input_tip)
                if choice == 'new':
                    self.init_data()
                elif choice == '3':
                    return

            elif choice == '3':
                return
            elif choice == '4':
                self.show_review_time_table()
            elif choice in ['5', '6']:
                word_info = WordInfo(self.debug, self.words_dict, self.words_info_dict)
                if choice == '5':
                    added_word_dict = word_info.add_word()
                    print(f'添加成功的单词：{added_word_dict}')
                    # 添加完之后，重新初始化数据，以便载入新单词
                    self.init_data()
                elif choice == '6':
                    failed_words_set = word_info.replenish_word_info()
                    print(f'添加失败的单词：{failed_words_set}')
                    # 添加后不需要重新初始化数据

    def test(self, test_words_dict: dict = None):
        def _check_result(original_words_dict: dict, words_dict: dict):
            this_time_study_word_list = []
            for word in words_dict:
                original_study_time = original_words_dict[word]['study_record']["study_times"] + 1
                if original_study_time == words_dict[word]['study_record']["study_times"]:
                    this_time_study_word_list.append(word)
            if len(this_time_study_word_list) != self.every_turn_study_words_num:
                raise AssertionError
            else:
                print(this_time_study_word_list)

        def _test():
            study = Study(debug=True, debug_words_dict=copy.deepcopy(test_words_dict))
            new_words_dict = study.main()
            _check_result(test_words_dict, new_words_dict)

        if not test_words_dict:
            test_words_dict = self.load_words_dict()
        interact_util.mock_input(['1' for _ in range(1000)], _test)
        interact_util.mock_input(['2'] + ['1' for _ in range(1000)], _test)
        print('==============================================测试成功==============================================')


class StudyGui(Study):
    def get_finished_words_num(self) -> int:
        finished_words_list = []
        for word in self.study_list:
            if not self.whether_study_finish_this_time(word, self.stage):
                finished_words_list.append(word)
        return len(finished_words_list)

    def next_word(self) -> bool:
        while True:
            self.count += 1
            if self.count == self.every_turn_study_words_num:
                self.count = 0
            self.studying_word = self.study_list[self.count]
            if self.whether_study_finish_this_time(self.studying_word, self.stage):
                return True
            if self.get_finished_words_num() == self.every_turn_study_words_num:
                return False

    def study_init(self, mode: str) -> None:
        self.study_mode = mode
        self.study_list = self._get_study_list()
        self.study_phonetic_symbol_dict = self.get_study_phonetic_symbol_dict()
        self.studying_word = None
        self.study_date = datetime.now().strftime(self.day_fmt)

        self.stage = Study.meaning_stage
        self.count = 0
        self.next_word()

    def get_studying_word_chinese(self) -> None:
        return self.using_words_dict[self.studying_word]['ch_trans']

    def studying_word_this_time_study_time_plus_one(self) -> None:
        self.using_words_dict[self.studying_word]['study_record']['meaning_study_times'] += 1


if __name__ == '__main__':
    Study().test()
