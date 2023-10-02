import os.path
import sys


def replace_pyqt5(output_path):
    content = open(output_path, encoding='utf-8').read()
    content = content.replace('from PyQt5 import QtCore', 'from PyQt6 import QtCore')
    open(output_path, 'w', encoding='utf-8').write(content)


def add_rc(output_path):
    content = open(output_path, encoding='utf-8').read()
    content += 'from .. import resource_rc'
    open(output_path, 'w', encoding='utf-8').write(content)


def modification_time_of_a_is_earlier_than_b(file_a_path, file_b_path) -> bool:
    # 获取文件的最后修改时间戳
    file_a_mtime = os.path.getmtime(file_a_path)
    file_b_mtime = os.path.getmtime(file_b_path)
    # 比较两个文件的最后修改时间
    if file_a_mtime < file_b_mtime:
        return True


def transform_to_py(import_rc: bool = False):
    for file in os.listdir(ui_dir) + os.listdir(qrc_dir):
        basename, ext = os.path.splitext(file)
        if ext == '.ui':
            input_path = os.path.join(ui_dir, file)
            output_path = os.path.join(ui_output_dir, basename + "_ui.py")
            # 如果ui文件没修改，就不重新生成
            if not (os.path.exists(output_path) and modification_time_of_a_is_earlier_than_b(input_path, output_path)):
                command = f'{sys.executable} {pyuic_path} {input_path} -o {output_path}'
                print(command)
                os.system(command)
                if import_rc:
                    add_rc(output_path)
        elif ext == '.qrc':
            output_path = os.path.join(qrc_output_dir, basename + "_rc.py")
            command = f'{sys.executable} {pyrrc_path} {os.path.join(qrc_dir, file)} -o {output_path}'
            print(command)
            os.system(command)
            replace_pyqt5(output_path)


if __name__ == '__main__':
    pyuic_path = os.path.join(os.path.dirname(sys.executable), 'Scripts\\pyuic6.exe')
    pyrrc_path = os.path.join(os.path.dirname(sys.executable), 'Scripts\\pyrcc5.exe')

    ui_dir = os.path.dirname(os.path.abspath(__file__))
    ui_output_dir = ui_dir
    qrc_dir = os.path.dirname(ui_dir)
    qrc_output_dir = qrc_dir

    transform_to_py(import_rc=True)
