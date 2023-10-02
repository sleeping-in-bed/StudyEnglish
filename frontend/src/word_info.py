import copy
import time
import traceback
from datetime import datetime
import os
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

from psplpy import data_process, file_util, interact_util, data_access
from base import Base

"""
failed_words_dict = {word->str: number_of_failures->int, ...}
"""


class WordInfo(Base):
    failed_words_dict_path = os.path.join(Base.project_dir, r'data\failed_words.json')
    word_info_dict_template = {'ch_trans': {}, 'phonetic': {'uk': {}, 'us': {}}}

    def __init__(self, debug: bool, words_dict: dict, words_info_dict: dict):
        super(WordInfo, self).__init__(debug=debug, words_dict=words_dict, words_info_dict=words_info_dict)
        self.words_txt_dict = self.load_words_txt_dict()
        self.failed_words_set = set()
        self.failed_words_dict = self.load_failed_words_dict()

    @staticmethod
    def _word_request(url: str) -> requests.Response:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                                 ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}
        res = requests.get(url, headers=headers, timeout=(10, 15))
        return res

    def _get_word_info(self, word: str) -> dict:
        word_info_dict = copy.deepcopy(self.word_info_dict_template)
        cambridge_root_url = r'https://dictionary.cambridge.org'
        word_url = urljoin(cambridge_root_url, rf'dictionary/english/{word}')
        res = self._word_request(word_url).text

        soup = BeautifulSoup(res, 'html.parser')
        for region in ['uk', 'us']:
            info = soup.find(class_=f'{region} dpron-i')
            source_tag = info.find('source')
            rel_pronunciation_path = source_tag.get('src')[1:]
            word_info_dict['phonetic'][region]['pronunciation'] = rel_pronunciation_path
            phonetic = info.find(class_='ipa dipa lpr-2 lpl-1').text
            word_info_dict['phonetic'][region]['symbol'] = phonetic
            pronunciation_url = urljoin(cambridge_root_url, rel_pronunciation_path)

            res_data = self._word_request(pronunciation_url)
            is_reserved, pronunciation_path = file_util.process_win_reserved_name(
                os.path.join(self.pronunciation_dir, rel_pronunciation_path), restore=False)
            print(pronunciation_path)
            file_util.create_file(pronunciation_path)
            with open(pronunciation_path, 'wb') as mp3_file:
                mp3_file.write(res_data.content)

        youdao_url = rf'https://www.youdao.com/result?word={word}&lang=en'
        res = self._word_request(youdao_url).text
        soup = BeautifulSoup(res, 'html.parser')

        box = soup.find(class_='basic')
        meaning_list = box.find_all(class_='word-exp')
        for meaning in meaning_list:
            try:
                part_of_speech = meaning.find(class_='pos').text
                chinese = meaning.find(class_='trans').text
                word_info_dict['ch_trans'][part_of_speech] = [chinese]
            except AttributeError:
                pass

        return word_info_dict

    def _add_word_info(self, phrase: str, get_failed_words: bool) -> None:
        word_list = self.process_phrase(phrase)
        for word in word_list:
            if not (get_failed_words ^ (word in self.failed_words_dict or word in self.failed_words_set)):
                if word not in self.words_info_dict:
                    t = time.time()
                    print(f'\n开始获取：{word}')
                    try:
                        word_info = self._get_word_info(word)
                    except Exception:
                        traceback.print_exc()
                        self.failed_words_set.add(word)
                    else:
                        self.words_info_dict[word] = word_info
                        print(f'获取完成，用时：{time.time() - t:.2f}s')
                        print(f'{word}: {word_info}')
                        # 及时保存单词信息
                        self.dump_words_info_dict()
                else:
                    if word in self.failed_words_dict:
                        self.failed_words_dict.pop(word)

    def _update_failed_words_dict(self) -> None:
        for word in self.failed_words_set:
            if word in self.failed_words_dict:
                self.failed_words_dict[word] += 1
            else:
                self.failed_words_dict[word] = 1

    def replenish_word_info(self) -> set:
        words_list = list(self.words_txt_dict.keys())
        old_failed_words_set_length = len(self.failed_words_set)
        for i in range(len(words_list)):
            self._add_word_info(words_list[i], False)
            if len(self.failed_words_set) != old_failed_words_set_length:
                print(f'当前失败单词集合：{self.failed_words_set}')
                old_failed_words_set_length = len(self.failed_words_set)
            interact_util.overlay_print(f'进度：{i + 1}/{len(words_list)}')
        self._update_failed_words_dict()
        self.dump_failed_words_dict()
        print('\n开始尝试获取曾经失败的单词')
        for word in data_process.sorted_dict_according_to_value(self.failed_words_dict, reversed=True):
            self._add_word_info(word, True)

        return self.failed_words_set

    def add_word(self) -> dict:
        self._find_duplicated_words()
        self._check_trans_consistency()

        added_word_dict = {}
        count = 0
        today_datetime = datetime.now().strftime(self.day_fmt)
        for word, ch_trans in self.words_txt_dict.items():
            if not self.words_dict.get(word):
                value = {'ch_trans': ch_trans, 'study_record': {'last_study_time': today_datetime,
                                                                'study_times': 0, 'word_status': self.studying_status}}
                self.words_dict[word] = value
                added_word_dict[word] = value
                count += 1
        self.dump_words_dict()
        print(f'# 添加{count}个单词成功')
        return added_word_dict

    def _find_duplicated_words(self) -> None:
        duplicates = data_process.find_list_duplicates(self.load_words_txt_word_list())
        if duplicates:
            print('# Duplicated words (word: index):')
            for duplicate in duplicates:
                print(f'{duplicate}: {duplicates[duplicate]}')
            raise AssertionError('Please deal with the duplicates first')

    def _check_trans_consistency(self) -> None:
        inconsistent_word_dict = {}
        for word in self.words_dict:
            original_trans = self.words_dict[word]['ch_trans']
            new_trans = self.words_txt_dict[word]
            if original_trans != new_trans:
                inconsistent_word_dict[word] = {'original': original_trans, 'new': new_trans}
        if inconsistent_word_dict:
            print('# Inconsistent words (word: index):')
            for inconsistent in inconsistent_word_dict:
                print(f'{inconsistent}: {inconsistent_word_dict[inconsistent]}')
            raise AssertionError('Please deal with the translation inconsistency first')

    @staticmethod
    def load_failed_words_dict() -> dict:
        return data_access.load_json_maybe_null(WordInfo.failed_words_dict_path, dict)

    def dump_failed_words_dict(self) -> None:
        data_access.dump_json_human_friendly(self.failed_words_dict, WordInfo.failed_words_dict_path)