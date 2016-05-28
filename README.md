### 代码说明
**create_vocab.py**
对短信进行分词并消重,获得词库,并做为特征属性。
获得的词库写入'dataSet/vocab.txt'
**feature_select.py**
进行特征选择， 排除在所有输入样本的垃圾短信中特征取值都是0的特征属性。
特征选择后新的词库写入'dataSet/new_vocab.txt'
**training_bayes.py**
训练朴素贝叶斯分类器
学习过程产生的数据保存在'classifier'
学习的结果保存在'classifier/done'
**classifier.py**
将训练完成的分类器，对短信进行分类，并获得评分。
结果保存在'dataSet/result_predict.txt'
评分 = 0.7 × (0.65 × 垃圾短信准确率 + 0.35 × 垃圾短信查全率） + 0.3 × （0.65 × 普通短信准确率 + 0.35 × 普通短信查全率）

