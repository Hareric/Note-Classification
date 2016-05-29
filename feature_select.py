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
特征选择策略：
    排除在所有输入样本中的垃圾短信中特征取值都是0的特征属性
"""
import numpy as np
from create_vocab import *


def create_vector(message_cut, vocab_set, vocab_list):
    """
    创建向量
    :param message_cut: 已分词的文本
    :param vocab_set: 词库集合，提高检索速度
    :param vocab_list: 词库
    :return: 该文本对应该词库的向量
    """
    return_vec = [0] * len(vocab_list)
    for word in message_cut:
        if word in vocab_set:
            return_vec[vocab_list.index(word)] = 1
    return return_vec


if __name__ == '__main__':
    import time
    t1 = time.time()

    data = load_file('dataSet/note_training.txt')
    vocab = load_file('dataSet/vocab.txt')
    vocab_set = set(vocab)
    class_list = [i.split('\t')[1] for i in data]
    message_list = [i.split('\t')[2] for i in data]
    message_num = len(message_list)  # 训练集的个数
    feature_num = len(vocab)  # 特征的个数
    sum_spam = np.zeros(feature_num)  # 所有垃圾短信的特征属性之和。（若为0,表示该特征没有在垃圾短信内出现过）
    for i in range(message_num):
        sys.stdout.write("\r feature selecting... %5.2f%%" % (i * 1.0 / message_num * 100))
        sys.stdout.flush()
        if class_list[i] == '1':
            sum_spam += create_vector(jieba.cut(message_list[i]), vocab_set, vocab)
    selected = np.where(sum_spam > 0)[0]  # 某个特征在垃圾短信存在过，则判定为有效特征
    new_vocab = [vocab[i] for i in selected]
    write_file("dataSet/new_vocab.txt", new_vocab)

    print "原词库大小： ", vocab.__len__()
    print "特征选取后词库大小： ", vocab.__len__()

    t2 = time.time()
    print "\n finished   use time: %5.2fs" % (t2-t1)
