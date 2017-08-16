#-*- coding: utf-8 -*-
'''
Description:
    Text Classification Based on Naive Bayes.
Version:
    python3
'''

import scipy as sp
import numpy as np
from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import classification_report

# 从 tokens/ 目录下加载数据（已分类）并保存到文件中
# tokens/pos 下存放正面评论文本， tokens/neg 下存放负面评论文本.
# 第一次运行次脚本时需要把一下三行注释打开.
# movie_reviews = load_files('tokens')
# sp.save('movie_data.npy', movie_reviews.data)
# sp.save('movie_target.npy', movie_reviews.target)

# 读取数据
movie_data = sp.load('movie_data.npy')
movie_target = sp.load('movie_target.npy')
x = movie_data
y = movie_target

# 创建 tf-idf对象，用于特征提取、向量化、加权
count_vec = TfidfVectorizer(binary=False, decode_error='ignore', stop_words='english')

x_train, x_test, y_train, y_test \
    = train_test_split(movie_data, movie_target, test_size=0.2)
x_train = count_vec.fit_transform(x_train)
x_test = count_vec.transform(x_test)

clf = MultinomialNB().fit(x_train, y_train)
doc_class_predicted = clf.predict(x_test)

print(np.mean(doc_class_predicted == y_test))

precision, recall, thresholds = precision_recall_curve(y_test, clf.predict(x_test))
answer = clf.predict_proba(x_test)[:,1]
report = answer > 0.5
print(classification_report(y_test, report, target_names=['neg', 'pos']))




