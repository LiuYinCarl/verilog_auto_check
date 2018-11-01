import os
import re
import shutil


class VerilogAutoChecker(object):
    """
    自动检查verilog代码的基本语法错误
    """

    def __init__(self):
        self.current_path = os.getcwd().replace('\\', '/')  # 获取当前路径并换成unix格式
        pass

    def get_cur_file_path(self, filename):
        """
        返回 filename 文件的绝对路径
        """
        return self.current_path + '/' + filename

    def back_up_files(self, file_list):
        """
        备份源文件
        """
        file_path = self.get_cur_file_path('备份源文件目录_可删除')

        is_exist = os.path.exists(file_path)  # 判断备份目录是否存在

        if not is_exist:  # 如果备份目录不存在则创建
            print('备份目录不存在，创建备份目录...')
            os.makedirs(file_path)

        print('源文件备份中...')
        for file in file_list:  # 将所有源文件复制到备份目录中
            source_code = self.get_cur_file_path(file)
            shutil.copyfile(source_code, file_path)
        print('源文件备份完成，如有错误，请从备份目录中恢复...')

    def get_wanted_checked_code_name(self):
        """
        读取希望检查的verilog源代码
        :return:
        """
        files = input('输入你想检查的.v文件名字,如果有多个文件，用空格分开')
        files = files.split(' ')
        file_name = []
        for file in files:
            if file[-2:] == '.v':  # 如果输入的文件名带了拓展名
                file_name.append(file)
            else:  # 如果输入的文件没有带拓展名
                file_name.append(file + '.v')
        return file_name

    def get_source_code_path(self):
        """
        获取目录下所有 Verilog 源文件的路径
        :return:
        """

        files = os.listdir(self.current_path)  # 得到文件夹下所有文件名字
        v_file = []  # 保存 verilog源文件路径
        for file in files:
            if os.path.isfile(file):  # 判断是否是文件，是才继续操作
                if file[-2:] == '.v':  # 判断是否是verilog源文件，是才继续操作
                    v_file.append(file)

    def read_file(self, filename):
        """
        一次读取整个文件并检查错误
        """
        file_path = self.get_cur_file_path(filename)
        text = ''  # 用来临时保存文件
        with open(file_path, 'r') as f:
            text = f.readlines()  # 读取整个文件

        text1 = self.check_chinese_characters(text)  # 检查错误
        self.check_begin_and_end(text1)
        self.check_module_and_endmodule(text1)

        with open(file_path, 'w') as f:
            f.write(text1)  # 将文件重新写回

    def read_one_line(self, filename):
        tmp_file_name = self.current_path + '/' + 'my_tmp_file_fadfafdfa'
        tmp_f = open(tmp_file_name, 'a')
        file_path = self.current_path + '/' + filename
        with open(file_path, 'r') as f:
            line = f.readline()

    def check_the_semicolon(self):
        """
        检查分号
        Error (10170)
        :return:
        """
        pass

    def check_chinese_characters(self, text):
        """
        检查中文符号并替换为英文符号
        """
        table = {ord(f): ord(t) for f, t in zip(
            '，。！？【】（）％＃＠＆１２３４５６７８９０',
            ',.!?[]()%#@&1234567890')}
        return text.translate(table)

    def check_module_and_endmodule(self, text):
        """
        检查module和 endmodule
        Error (10171)
        :return:
        """
        modules = re.findall('[^d]module', text)
        endmodules = re.findall('\sendmodule', text)

        n1 = len(modules)
        n2 = len(endmodules)

        if n1 == 0 or n2 == 0:
            if n1 == 0:
                print('缺少关键字module 或者module未与其他单词分开')
            if n2 == 0:
                print('缺少关键字endmodule 或者endmodule未与其他单词分开')
        else:
            if n1 < n2:
                print('缺少关键字module 或者module未与其他单词分开')
            elif n1 > n2:
                print('缺少关键字endmodule 或者endmodule未与其他单词分开')

    def check_begin_and_end(self, text):
        """
        检查 begin 和 end
        :return:
        """
        begins = re.findall('\sbegin\s', text)
        ends = re.findall('[;\s]end\s', text)

        n1 = len(begins)
        n2 = len(ends)

        if n1 < n2:
            print('关键字begin的数目小于end 或begin未与其他单词分开')
        if n1 > n2:
            print('关键字end的数目小于begin 或 end未与其他单词分开')

    def check_error_spaces(self, text):
        """
        检查错误的空格，比如将 ">=" 分开
        :return:
        """
        text1 = text.replace('> =', '>=')
        text2 = text1.replace('< =', '<=')
        text3 = text2.replace('= =', '==')
        text4 = text3.replace('! =', '!=')

        return text4

    def check_module_instantiation(self, text):
        """
        检查模块实例化中 没带"."或者","的错误
        :return:
        """
        parentheses = re.findall('\((.*)\)', text)
        num = 1  # 记录是第几个模块实例
        for item in parentheses:
            p1 = re.findall('\.', item)
            p2 = re.findall('\(', item)
            p3 = re.findall('\)', item)
            p4 = re.findall(',', item)

            if not len(p1) or not len(p2):
                if len(p2) != len(p3):  # 处理左右括号缺失
                    if len(p2) < len(p3):
                        print('源文件中"("（左括号）缺失')
                    if len(p2) > len(p3):
                        print('源文件中")"（右括号）缺失')
                if len(p1) < len(p2):  # 处理句号缺失
                    print('第 %d 个模块实例中 "."（英文句号） 缺失 %d 个' % (num, len(p2) - len(p1)))

                if len(p2) > (len(p4) + 1):  # 处理逗号缺失
                    print('第 %d 个模块实例中 ","（逗号）缺失 %d 个' % (num, len(p2) - (len(p4) + 1)))
