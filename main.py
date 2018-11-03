import os
import re
import shutil
import chardet


class VerilogAutoChecker(object):
    """
    自动检查verilog代码的基本语法错误
    """

    def __init__(self):
        self.current_path = os.getcwd().replace('\\', '/')  # 获取当前路径并换成unix格式
        file_names = self.get_wanted_checked_code_name()
        if file_names is None:
            file_names = self.get_source_code_path()
        print(file_names)
        self.back_up_files(file_names)  # 备份源文件
        for file in file_names:
            print('==' * 30)
            print('检查文件 %s ...' % file)

            self.read_file(file)

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
            back_up_code = file_path + '/' + file
            shutil.copyfile(source_code, back_up_code)
        print('源文件备份完成，如有错误，请从备份目录中恢复...')

    def get_wanted_checked_code_name(self):
        """
        读取希望检查的verilog源代码
        """
        files = input('输入你想检查的.v文件名字,如果有多个文件，用空格分开, 默认为当前文件夹下所有源文件，按回车继续')
        print(files)
        if not files:
            return None
        if files[0].isspace():
            return None
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
        return v_file

    def read_file(self, filename):
        """
        一次读取整个文件并检查错误
        """
        file_path = self.get_cur_file_path(filename)
        text = ''  # 用来临时保存文件
        data = None
        with open(file_path, 'rb') as f:
            data = chardet.detect(f.read())
        code_format = data['encoding']  # 获取编码格式(str)
        format_possibility = data['confidence']  # 获取该编码格式的可能性(float类型)

        get_code_format = True
        if format_possibility >= 0.8:  # 编码可能性大于0.8， 尝试解码
            try:
                with open(file_path, 'r', encoding=code_format) as f:
                    text = f.read()
            except UnicodeDecodeError as e:
                get_code_format = False
                print('尝试自动判断编码， 概论为%f, 过低，尝试强制解码...' % format_possibility)

        if format_possibility < 0.8 or not get_code_format:  # 自动判断概论过低或者自动解码错误
            get_code_format = True
            try:
                get_code_format = True
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            except UnicodeDecodeError as e:
                get_code_format = False
                print('尝试UTF-8解码， 错误... 更换解码方式...')

            if not get_code_format:
                try:
                    get_code_format = True
                    with open(file_path, 'r', encoding='ANSI') as f:
                        text = f.read()
                except UnicodeDecodeError as e:
                    get_code_format = False
                    print('尝试ANSI解码， 错误... 更换解码方式...')

            if not get_code_format:
                try:
                    get_code_format = True
                    with open(file_path, 'r', encoding='') as f:
                        text = f.read()
                except UnicodeDecodeError as e:
                    get_code_format = False
                    print('尝试GBK解码， 错误... 更换解码方式...')

            if not get_code_format:
                try:
                    get_code_format = True
                    with open(file_path, 'r', encoding='GBK2312') as f:
                        text = f.read()
                except UnicodeDecodeError as e:
                    get_code_format = False
                    print('尝试GBK2312解码， 错误... 更换解码方式...')

        if not get_code_format:
            print('该文件无法解码，请忽略以下错误提示... 更换解码方式...')

        text = self.run_checker(text)
        self.write_back_file(file_path, text)

    def run_checker(self, text):
        text = self.check_chinese_characters(text)  # 检查错误
        text = self.check_case(text)  # 检查关键字大小写
        self.check_begin_and_end(text)  #检查begin end
        self.check_module_and_endmodule(text)  # 检查 module endmodule
        self.check_module_instantiation(text)  # 检查模块实例化
        return text

    def write_back_file(self, file_path, text):
        with open(file_path, 'w') as f:
            f.write(text)  # 将文件重新写回

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

    def check_case(self, text):
        """
        检查关键字的大小写，统一为小写
        """
        for word in ['always', 'and', 'assign', 'wor', 'xor',
                     'automatic', 'begin', 'case', 'casex', 'casez',
                     'cell', 'deassign', 'default', 'defparam', 'design',
                     'disable', 'edge', 'else', 'end', 'endcase',
                     'endconfig', 'endfunction', 'endgenerate', 'endmodule', 'endprimitive',
                     'endtable', 'endtask', 'event', 'for', 'force',
                     'forever', 'fork', 'function', 'inout', 'input',
                     'integer', 'reg', 'wire', 'while', 'xnor',
                     ]:
            text = re.sub(word, word, text, flags=re.IGNORECASE)
        return text

    def check_module_and_endmodule(self, text):
        """
        检查module和 endmodule
        Error (10171)
        """
        modules = re.findall('module\s', text)
        endmodules = re.findall('endmodule', text)

        n1 = len(modules)
        n2 = len(endmodules)

        if n1 == 0 or n2 == 0:
            if n1 == 0:
                print('未检出module 或者module未与其他单词分开')
            if n2 == 0:
                print('未检出关键字endmodule 或者endmodule未与其他单词分开')
        else:
            if n1 < n2:
                print('缺少关键字module 或者module未与其他单词分开')
            elif n1 > n2:
                print('缺少关键字endmodule 或者endmodule未与其他单词分开')

    def check_begin_and_end(self, text):
        """
        检查 begin 和 end
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
        error_cnt_1 = len(re.findall('> =', text))
        error_cnt_2 = len(re.findall('< =', text))
        error_cnt_3 = len(re.findall('= =', text))
        error_cnt_4 = len(re.findall('! =', text))

        if error_cnt_1:
            print('错误："> = " 分开 数量: %d 已修复...' % error_cnt_1)
        if error_cnt_2:
            print('错误："< = " 分开 数量: %d 已修复...' % error_cnt_2)
        if error_cnt_3:
            print('错误："= = " 分开 数量: %d 已修复...' % error_cnt_3)
        if error_cnt_4:
            print('错误："! = " 分开 数量: %d 已修复...' % error_cnt_4)

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
        # parentheses = re.findall('[(](.*)[)]', text)
        ptn = re.compile(r'(?<==)\(.*\)(?=\s*\w+\s*=)', re.DOTALL)
        parentheses = ptn.findall(re.sub(r'(?<==)\s*(?=\()', '', text))

        num = 0  # 记录是第几个模块实例
        print(parentheses)

        for item in parentheses:
            num = num + 1
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


if __name__ == '__main__':
    demo = VerilogAutoChecker()
