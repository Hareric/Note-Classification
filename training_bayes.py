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
训练朴素贝叶斯分类器
"""

from feature_select import *


def train_bayes(train_matrix, train_class_vec, is_first=False, is_last=False):
    """
    朴素贝叶斯分类器的学习过程
    p0_vec: [p(F1|0),p(F2|0),p(F3|0),p(F4|0)...p(Fn|0)]
    p1_vec: [p(F1|1),p(F2|1),p(F3|1),p(F4|1)...p(Fn|1)]
    p_spam: p(1) 垃圾短信的概率
    :param is_last: 是否为最后一次训练
    :param is_first: 是否为第一次训练
    :param train_matrix: 特征矩阵
    :param train_class_vec: 对应的分类属性列表
    :return: p0_vec, p1_vec, p_spam
    """
    message_num = len(train_matrix)  # 训练集信息的数量
    words_num = len(train_matrix[0])  # 词库的大小
    if is_first:
        p0_num = np.ones(words_num)
        p1_num = np.ones(words_num)
        p0_denom = 2.0
        p1_denom = 2.0
    else:
        p0_num = np.load('classifier/p0_num.npy')
        p1_num = np.load('classifier/p1_num.npy')
        p0_denom = np.load('classifier/p0_denom.npy')
        p1_denom = np.load('classifier/p1_denom.npy')
    print "training...."
    for i in range(message_num):
        sys.stdout.write("\r   %5.2f%%" % (i * 1.0 / message_num * 100))
        sys.stdout.flush()
        if train_class_vec[i] == 0:
            p0_num += train_matrix[i]
            p0_denom += sum(train_matrix[i])
        else:
            p1_num += train_matrix[i]
            p1_denom += sum(train_matrix[i])
    sys.stdout.write("\r")
    print "\ntraining done"
    if is_last:
        p_spam = sum(train_class_vec) / float(message_num)  # 垃圾短信的概率
        p1_vec = np.log(p1_num / p1_denom)
        p0_vec = np.log(p0_num / p0_denom)
        return p0_vec, p1_vec, p_spam
    else:
        np.save('classifier/p0_num', p0_num)
        np.save('classifier/p1_num', p1_num)
        np.save('classifier/p0_denom', p0_denom)
        np.save('classifier/p1_denom', p1_denom)
        return None, None, None


def create_matrix(message_cut_list, vocab_list):
    """
    :param message_cut_list: 分词后的
    :param vocab_list:
    :return:
    """
    return_matrix = []
    total = len(message_cut_list)
    vocab_set = set(vocab_list)
    print "creating matrix..."
    for index, message in enumerate(message_cut_list):
        sys.stdout.write("\r   %5.2f%%" % (index * 1.0 / total * 100))
        sys.stdout.flush()
        return_matrix.append(create_vector(message, vocab_set, vocab_list))
    sys.stdout.write("\r")
    print "\ncreating done"
    return return_matrix


if __name__ == '__main__':
    import time
    t1 = time.time()

    data = load_file('dataSet/note_training.txt')
    vocab = load_file('dataSet/new_vocab.txt')
    part_num = len(data) / 8  # 将训练集分为8个部分进行训练
    for part in range(8):
        print "part:", part + 1
        class_result = [int(i.split('\t')[1]) for i in data[part_num * part:part_num * (part + 1)]]
        messages = [i.split('\t')[2] for i in data[part_num * part:part_num * (part + 1)]]
        messages_cut = cut_sentence(messages)
        feature_matrix = create_matrix(messages_cut, vocab)
        p0_vec, p1_vec, p_spam = train_bayes(feature_matrix, class_result, is_first=part == 0, is_last=part == 7)
        del feature_matrix, class_result, messages_cut  # 回收内存
    np.save('classifier/done/p0_vec', p0_vec)
    np.save('classifier/done/p1_vec', p1_vec)
    np.save('classifier/done/p_spam', p_spam)

    t2 = time.time()
    print "\n finished   use time: %5.2fs" % (t2-t1)
