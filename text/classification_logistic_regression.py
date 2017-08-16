#-*- coding: utf-8 -*-
'''
Description:
    Text Classification Based on Logistic Regression.
Version:
    python3
'''
import scipy as sp
import numpy as np
from matplotlib import pyplot
from matplotlib import pylab
from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import precision_recall_curve, roc_curve, auc
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
import time

start_time = time.time()

# 绘制 P/R 曲线
def plot_pr(auc_score, precision, recall, label=None):
    pylab.figure(num=None, figsize=(6, 5))
    pylab.xlim([0.0, 1.0])
    pylab.ylim([0.0, 1.0])
    pylab.xlabel('Recall')
    pylab.ylabel('Precision')
    pylab.title('P/R (AUC=%0.2f) / %s' % (auc_score, label))
    pylab.fill_between(recall, precision, alpha=0.5)
    pylab.grid(True, linestyle='-', color='0.75')
    pylab.plot(recall, precision, lw=1)
    pylab.show()
    pylab.savefig('classification_pr.png')

# 加载并保存数据.
# 数据在endata/ 目录下，
# endata/neg 下存放所有负面评论文本， endata/pos 下存放所有正面评论文本.
# 第一次运行时需要打开以下三行注释，以后只需读取.npy文件即可.
# movie_reviews = load_files('endata')
# sp.save('my_data.npy', movie_reviews.data)
# sp.save('my_target.npy', movie_reviews.target)

# 读取已保存的数据
movie_data = sp.load("my_data.npy")
movie_target = sp.load("my_target.npy")
x = movie_data
y = movie_target

count_vec = TfidfVectorizer(binary=False, decode_error='ignore', stop_words='english')
average = 0
testNum = 10
for i in range(testNum):
    # 将数据切分，80%用来训练，20%用来测试。
    x_train, x_test, y_train, y_test \
            = train_test_split(movie_data, movie_target, test_size=0.2)

    # 特征提取 & 向量化 & 加权
    x_train = count_vec.fit_transform(x_train)
    x_test = count_vec.transform(x_test)

    # 创建逻辑回归模型
    clf = LogisticRegression()

    # 使用训练数据，训练模型
    clf.fit(x_train, y_train)

    # 使用测试数据，进行预测
    y_pred = clf.predict(x_test)

    # 判断预测的准确率
    p = np.mean(y_pred == y_test)
    print(p)
    average += p

# 对 x_test（测试数据的特征矩阵/向量）进行预测
answer = clf.predict_proba(x_test)[:,1]
precision, recall, thresholds = precision_recall_curve(y_test, answer)
report = answer > 0.5
print(classification_report(y_test, report, target_names=['neg', 'pos']))
print("average precision: ", average/testNum)
print("time spent: ", time.time() - start_time)

# 这里进绘制正面评论的 P/R 图.
# 如果是在shell或者终端中运行，只能生成图片文件，不能直接显示图形。
plot_pr(0.5, precision, recall, "pos")

# 以下是对训练好的模型进行应用，判断其他文本属于那一分类（neg/pos）
test = [b'nb movie!\n']
test1 = count_vec.transform(test)
result = clf.predict_proba(test1)[:,1]
print("result: ", result)
if result > 0.5:
    print(test, "\nThis is a positive comment!")
else:
    print(test, "\nThis is a negative comment!")

test2 = [b'waste life!\n']
test3 = count_vec.transform(test2)
result1 = clf.predict_proba(test3)[:,1]
print("result: ", result1)
if result1 > 0.5:
    print(test2, "\nThis is a positive comment!")
else:
    print(test2, "\nThis is a negative comment!")
