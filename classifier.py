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
分类
"""

from training_bayes import *


def classify_bayes(message_vec, p0_vec, p1_vec, p_spam):
    """
    输入文本向量，预测分类结果
    :param message_vec: 文本向量
    :param p0_vec: [p(F1|0),p(F2|0),p(F3|0),p(F4|0)...p(Fn|0)]
    :param p1_vec: [p(F1|1),p(F2|1),p(F3|1),p(F4|1)...p(Fn|1)]
    :param p_spam: p(1) 垃圾短信的概率
    :return: 预测分类结果
    """
    p0 = sum(message_vec * p0_vec) + np.log(1 - p_spam)
    p1 = sum(message_vec * p1_vec) + np.log(p_spam)
    if p1 > p0:
        return 1
    else:
        return 0


def get_test_score(real_list, predict_list):
    """
    评分 =   0.7 × (0.65 × 垃圾短信准确率 + 0.35 × 垃圾短信查全率）
            + 0.3 × （0.65 × 普通短信准确率 + 0.35 × 普通短信查全率）
    :param real_list: 真实结果
    :param predict_list: 预测结果
    :return:
    """
    num = len(predict_list)
    A = 0.
    B = 0.
    C = 0.
    D = 0.
    for i in range(num):
        real_list[i] = int(real_list[i])
        predict_list[i] = int(predict_list[i])
        if real_list[i] == predict_list[i]:
            if real_list[i] == 0:
                A += 1
            else:
                D += 1
        else:
            if real_list[i] == 0:
                C += 1
            else:
                B += 1
    print "垃圾短信准确率:", D / (B + D)
    print "垃圾短信查全率:", D / (C + D)
    print "普通短信准确率:", A / (A + C)
    print "普通短信查全率:", A / (A + B)
    print "评分:", 0.7 * (0.65 * (D / (B + D)) + 0.35 * (D / (C + D))) + 0.3 * (
        0.65 * (A / (A + C)) + 0.35 * (A / (A + B)))

if __name__ == '__main__':
    data = load_file('dataSet/note_unknown.txt')[:1000]
    vocab = load_file('dataSet/new_vocab.txt')
    messages_unknown = [i.split()[1] for i in data]
    messages_unknown_cut = cut_sentence(messages_unknown)
    p0_vec = np.load('classifier/done/p0_vec.npy')
    p1_vec = np.load('classifier/done/p1_vec.npy')
    p_spam = np.load('classifier/done/p_spam.npy')
    predict_result = []  # 保存预测结果列表
    for index, message in enumerate(messages_unknown_cut):
        sys.stdout.write('\r classing....%i' % index)
        message_vec = create_vector(message, vocab)
        # 使用测试集多次测试后，将p_spam调至0.006
        predict_result.append(classify_bayes(message_vec, p0_vec=p0_vec, p1_vec=p1_vec, p_spam=0.006))
        del message_vec  # 回收内存
    sys.stdout.write('\r')

    # 获得预测结果的评分
    real_result = [i.split(',')[1] for i in load_file('dataSet/result_answer.txt')]
    get_test_score(real_list=real_result, predict_list=predict_result)

    # 预测结果写入txt
    write_lines = []
    for i in range(len(predict_result)):
        write_lines.append("%i,%i" % (i+800001, predict_result[i]))
    write_file('dataSet/result_predict.txt', write_lines)
