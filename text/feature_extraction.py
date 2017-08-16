# -*- coding: utf-8 -*-
'''
Description:
    Extract the feature from the text in English.
Version:
    python3
'''
from sklearn.feature_extraction.text import CountVectorizer

VECTORIZER = CountVectorizer(min_df=1)

# 以下代码设置了特征提取方法的参数（以1-2个单词作为滑动窗口大小，以空格作为单词的分割点，最小词频为1）
# 详细参考API介绍: 
# http://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction
# VECTORIZER = CountVectorizer(ngram_range=(1,2), token_pattern=r'\b\w+\b', min_df=1)

CORPUS = [
    'This is the first document.',
    'This is the second second document.',
    'And the third one.',
    'Is this the first document?'
]

X = VECTORIZER.fit_transform(CORPUS)
FEATURE_NAMES = VECTORIZER.get_feature_names()

print(FEATURE_NAMES)
