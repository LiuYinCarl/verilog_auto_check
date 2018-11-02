# a = 'test.v'
# print(a[-2:])

import os
import re

# print(os.getcwd().replace('\\', '/'))


fi = 'F:/github_project/verilog_auto_check/text.txt'
text = ''

with open(fi, 'r') as f:
    text = f.read()
    # print(text)
text2 = re.sub('begin', 'begin', text, flags=re.IGNORECASE)

with open(fi, 'w') as f:
    f.write(text2)

# modules = re.findall('[^d]module', text)
#
# endmodules = re.findall('\sendmodule', text)
#
# print(len(modules))
# print(len(endmodules))

# begins = re.findall('\sbegin\s', text)
# # ends = re.findall('[;\s]end\s', text)
# #
# # n1 = len(begins)
# # n2 = len(ends)
# # print(n1)
# # print(n2)

# text1 = text.replace('> =', '>=')
# text2 = text1.replace('< =', '<=')
# text3 = text2.replace('= =', '==')
# text4 = text3.replace('! =', '!=')
#
# # text += '\n hhhhhhhh'
#
# with open(fi, 'w') as f:
#     f.write(text4)

# print(re.findall('\((.*)\)', text))


# In Python3, use str.maketrans instead
# table = {ord(f): ord(t) for f, t in zip(
#     '，。！？【】（）％＃＠＆１２３４５６７８９０',
#     ',.!?[]()%#@&1234567890')}
# t = '中国，中文，标点符号！你好？１２３４５＠＃【】+=-（）'
# t2 = t.translate(table)
# print(t2)
