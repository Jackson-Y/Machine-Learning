#-*- coding: utf-8 -*-
'''
Description:
    Vectorize the features of the text and get the tf-idf term weighting.
Version:
    python3
'''
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

VECTORIZER = CountVectorizer(min_df=1)

CORPUS = [
    'This is the first document.',
    'This is the second second document.',
    'And the third one.',
    'Is this the first document?'
]

# Feature extraction & vectorize（特征提取及向量化）
X = VECTORIZER.fit_transform(CORPUS)
FEATURE_NAMES = VECTORIZER.get_feature_names()

print(FEATURE_NAMES)
print(X.toarray())

# Tf–idf term weighting（特征加权, 使其大小范围在 [0.0, 1.0] 之间）
TRANSFORMER = TfidfTransformer(smooth_idf=False)
TFIDF = TRANSFORMER.fit_transform(X)

print(TFIDF.toarray())

# 以上两步可以用一个函数（TfidfVectorizer）代替，将在classification.py中给出。
