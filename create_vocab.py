# coding=utf-8
#        ┏┓　　　┏┓+ +
# 　　　┏┛┻━━━┛┻┓ + +
# 　　　┃　　　　　　 ┃ 　
# 　　　┃　　　━　　　┃ ++ + + +
# 　　 ████━████ ┃+
# 　　　┃　　　　　　 ┃ +
# 　　　┃　　　┻　　　┃
# 　　　┃　　　　　　 ┃ + +
# 　　　┗━┓　　　┏━┛
# 　　　　　┃　　　┃　　　　　　　　　　　
# 　　　　　┃　　　┃ + + + +
# 　　　　　┃　　　┃　　　　Codes are far away from bugs with the animal protecting　　　
# 　　　　　┃　　　┃ + 　　　　神兽保佑,代码无bug　　
# 　　　　　┃　　　┃
# 　　　　　┃　　　┃　　+　　　　　　　　　
# 　　　　　┃　 　　┗━━━┓ + +
# 　　　　　┃ 　　　　　　　┣┓
# 　　　　　┃ 　　　　　　　┏┛
# 　　　　　┗┓┓┏━┳┓┏┛ + + + +
# 　　　　　　┃┫┫　┃┫┫
# 　　　　　　┗┻┛　┗┻┛+ + + +
"""
Author = Eric_Chan
Create_Time = 2016/05/29
构建词库
"""

import jieba
import sys
jieba.initialize()  # 手动启动jieba模块


def load_file(file_name, charset='utf-8'):
    """
    读取文件，按列返回列表
    :param file_name: 文件路径
    :param charset: 文本内容decode的编码，默认为utf-8
    :return: 文本内容列表
    """
    f1 = open(file_name)
    line = f1.readline().decode(charset).strip()
    line_list = []
    while line:
        line = line.strip()
        if line:
            line_list.append(line)
            line = f1.readline().decode(charset)
        else:
            line = f1.readline().decode(charset)
    return line_list


def cut_sentence(sentence_list):
    """
    对句子列表进行分词并除去停用词
    :param sentence_list: 待分词的句子列表
    :return: 每个句子的已分词后的二维列表
    """
    sentence_cut_list = []
    for sentence in sentence_list:
        sentence_cut_list.append(jieba.cut(sentence))
    return sentence_cut_list


def write_file(file_name, line_list, charset='utf-8', mode='w'):
    """
    新建文件将line_list中每个元素按行写入
    :param mode: 打开文件的规格， 'w' 表示新建， 'a' 表示添加， 'r' 表示只读
    :param file_name: 新建文件的文件名和路径
    :param line_list: 写入文件的列表
    :param charset: 写入文件是encode的编码， 默认为utf-8
    :return: void
    """
    f1 = open(file_name, mode=mode)
    for line in line_list:
        line = line.encode(charset)
        f1.write(line + '\n')
    f1.flush()
    f1.close()


def create_vocab_list(sentence_cut_list):
    """
    构建词库
    :param sentence_cut_list: 已分词的二维列表
    :return:
    """
    print "creating vocab..."
    t = 1.
    total_num = len(sentence_cut_list)
    vocab_set = set([])
    for sentence_cut in sentence_cut_list:
        for word in sentence_cut:
            if word not in vocab_set:
                vocab_set.add(word)
        # vocab_set = vocab_set | set(sentence_cut)  # 消重取并集
        sys.stdout.write('\r           %5.2f%%' % (t / total_num * 100))
        sys.stdout.flush()
        t += 1
    sys.stdout.write('\r')
    print "creating vocab done"
    return list(vocab_set)

if __name__ == '__main__':
    import time
    t1 = time.time()
    data = load_file('dataSet/note_training.txt')
    messages = [i.split('\t')[2] for i in data]
    messages_cut = cut_sentence(messages)
    vocab = create_vocab_list(messages_cut)
    vocab.sort()
    write_file('dataSet/vocab.txt', vocab)
    t2 = time.time()
    print "\n finished   use time: %5.2fs" % (t2-t1)
