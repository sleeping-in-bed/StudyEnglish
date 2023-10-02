import datetime
import os
import traceback
import mysql.connector

from psplpy import network_util, time_util

base_dir = os.path.dirname(os.path.abspath(__file__))

# 服务器配置
HOST = '127.0.0.1'
PORT = 12345

# MySQL数据库配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'study_english',
}


def login_authentication(client_socket: network_util.ClientSocket, user_info):
    # 连接到MySQL数据库
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    # 查询数据库中是否有匹配的用户名和密码
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (user_info['username'], user_info['password']))
    result = cursor.fetchone()
    if result:
        client_socket.send_obj(True)
    else:
        client_socket.send_obj(False)
    # 关闭数据库连接
    cursor.close()
    conn.close()


def retrieve_user_data(client_socket: network_util.ClientSocket, user_info):
    user_data_dir = os.path.join(base_dir, f"user_data/{user_info['username']}")
    with open(os.path.join(user_data_dir, f'{user_info["username"]}.zip'), 'rb') as f:
        client_socket.client_socket.sendfile(f)


def upload_user_data(client_socket: network_util.ClientSocket, user_info):
    user_data_dir = os.path.join(base_dir, f"user_data/{user_info['username']}")
    user_data_path = os.path.join(user_data_dir, f'{user_info["username"]}.zip')
    client_socket.send_obj('Start upload')
    client_socket.receive_file(user_data_path)


def handler(client_socket: network_util.ClientSocket):
    data = client_socket.recv_obj()
    if data['command'] == 'login':
        login_authentication(client_socket, data)
    elif data['command'] == 'retrieve_user_data':
        retrieve_user_data(client_socket, data)
    elif data['command'] == 'upload_user_data':
        upload_user_data(client_socket, data)

    client_socket.close()


# Start Server
def main():
    server_socket = network_util.ServerSocket(HOST, PORT, backlog=100)
    print(f"Waiting for connection...")
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from: {addr}, at {datetime.datetime.now().strftime(time_util.t_fmt['milli'])}")
        try:
            server_socket.client_handler(client_socket, handler)
        except Exception as e:
            print(f"An error '{e}' occurred at {datetime.datetime.now().strftime(time_util.t_fmt['milli'])}")
            traceback.print_exc()


if __name__ == "__main__":
    main()
