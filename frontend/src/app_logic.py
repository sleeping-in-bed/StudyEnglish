import os
from bs4 import BeautifulSoup
from pyecharts import options as opts
from pyecharts.charts import Line, Bar
import base64
import hashlib
from cryptography.fernet import Fernet

import network_util
from psplpy import data_access
from base import Base

base_dir = os.path.dirname(os.path.abspath(__file__))

'''
user:
{'name': str, 'password': str}
user_data:
{date->'yyyy-mm-dd': {'new': int, 'review': int, 'periods': [{'start_time': 'hhmmss', 'end_time': 'hhmmss'}, ...]},
 ...}
'''


class Crypto:
    def __init__(self, key: str):
        self.key = self.generate_key(key)

    @staticmethod
    def generate_key(text: str):
        key = hashlib.sha256(text.encode()).digest()
        key = base64.urlsafe_b64encode(key)
        return key

    def encrypt_message(self, message: str) -> bytes:
        cipher_suite = Fernet(self.key)
        encrypted_message = cipher_suite.encrypt(message.encode())
        return encrypted_message

    def decrypt_message(self, encrypted_message: bytes) -> str:
        cipher_suite = Fernet(self.key)
        decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
        return decrypted_message


class User:
    user_path = os.path.join(base_dir, r'data\user.json')

    def __init__(self):
        self.user = self.load_user()
        self.user.setdefault('name', '')
        self.user.setdefault('password', '')
        self.crypto = Crypto(self.user['name'])

    def get_name(self) -> str:
        return self.user['name']

    def set_name(self, name: str):
        self.user['name'] = name
        self.dump_user()

    def get_password(self) -> str:
        if self.user['password']:
            b = base64.b64decode(self.user['password'])
            return self.crypto.decrypt_message(b)
        else:
            return ''

    def set_password(self, password: str):
        b = self.crypto.encrypt_message(password)
        self.user['password'] = base64.b64encode(b).decode()
        self.dump_user()

    def load_user(self) -> dict:
        return data_access.load_json_maybe_null(self.user_path, dict)

    def dump_user(self) -> None:
        data_access.dump_json_human_friendly(self.user, self.user_path)


class UserData:
    user_data_path = os.path.join(base_dir, r'data\user_data.json')

    def __init__(self):
        self.user_data = self.load_user_data()
        self.today = Base.get_today_zero_time().strftime(Base.day_fmt)

    def get_new_num(self, date: str):
        return self.user_data[date]['new']

    def get_today_new_num(self):
        return self.get_new_num(self.today)

    def get_total_new_num(self):
        total = 0
        for date in self.user_data:
            total += self.get_new_num(date)
        return total

    def get_review_num(self, date):
        return self.user_data[date]['review']

    def get_today_review_num(self):
        return self.get_review_num(self.today)

    def get_total_review_num(self):
        total = 0
        for date in self.user_data:
            total += self.get_review_num(date)
        return total

    def _get_study_time(self, date: str):
        day_fmt = '%H%M%S'
        total_seconds = 0
        for period in self.user_data[date]['periods']:
            start_time = period[0].strptime(day_fmt)
            end_time = period[1].strptime(day_fmt)
            time_difference = end_time - start_time
            seconds_difference = time_difference.total_seconds()
            total_seconds += seconds_difference
        return total_seconds

    def get_today_study_time(self):
        return self._get_study_time(self.today)

    def get_total_study_time(self):
        total_seconds = 0
        for date in self.user_data:
            total_seconds += self._get_study_time(date)
        return total_seconds

    def load_user_data(self) -> dict:
        return data_access.load_json_maybe_null(self.user_data_path, dict)

    def dump_user_data(self) -> None:
        data_access.dump_json_human_friendly(self.user_data, self.user_data_path)


def get_chart_html():
    user_data = UserData()
    date_list = list(user_data.user_data.keys())[-7:]
    print(date_list)
    date_new_list = [user_data.get_new_num(date) for date in date_list]
    date_review_list = [user_data.get_review_num(date) for date in date_list]

    bar = (
        Bar()
            .add_xaxis(xaxis_data=date_list)
            .add_yaxis(
            series_name="新单词学习数量",
            y_axis=date_new_list,
        )
            .add_yaxis(
            series_name="复习单词数量",
            y_axis=date_review_list,
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="用户数据"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
        )
    )
    bar.width = "800px"
    bar.height = "500px"
    html_string = bar.render_embed()

    style = """
        body {
            background-color: rgb(249, 249, 249);
        }
    """
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_string, "html.parser")
    # 在<head>标签中查找现有的内容
    head_tag = soup.head
    # 创建一个新的style标签，并将样式添加到其中
    style_tag = soup.new_tag("style")
    style_tag.string = style
    # 将新的style标签添加到<head>中的末尾
    head_tag.append(style_tag)
    # 打印或使用包含样式的HTML字符串
    html_with_style = str(soup)
    # print(html_with_style)
    return html_with_style


# 服务器配置
HOST = '127.0.0.1'
PORT = 12345
client_socket = network_util.ClientSocket(HOST, PORT)


def login_authentication(username: str, password: str) -> bool:
    client_socket.connect()
    client_socket.send_obj({'command': 'login', 'username': username, 'password': password})
    response = client_socket.recv_obj()
    client_socket.close()
    return response


def retrieve_user_data(username: str) -> str:
    client_socket.connect()
    client_socket.send_obj({'command': 'retrieve_user_data', 'username': username})
    file_path = client_socket.receive_file(os.path.join(base_dir, rf'data\{username}.zip'))
    client_socket.close()
    data_access.extract_file(file_path, os.path.join(base_dir, 'data'))
    return file_path


def upload_user_data(username: str) -> str:
    file_list = ['words.json', 'user_data.json']
    file_abspath_list = [os.path.join(base_dir, rf'data\{file_name}') for file_name in file_list]
    zip_file_path = data_access.compress_file(file_abspath_list, os.path.join(base_dir, rf'data\{username}.zip'),
                                              os.path.join(base_dir, 'data'))

    client_socket.connect()
    client_socket.send_obj({'command': 'upload_user_data', 'username': username})
    client_socket.recv_obj()
    client_socket.send_file(zip_file_path)
    client_socket.close()
    return zip_file_path



if __name__ == '__main__':
    print(retrieve_user_data('1'))