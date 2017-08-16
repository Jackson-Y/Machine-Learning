# -*- coding: utf-8 -*-
'''
Description:
    Extract the feature from the text.
Version:
    python3
'''
from sklearn.feature_extraction.text import CountVectorizer

VECTORIZER = CountVectorizer(min_df=1)

CORPUS = [
    'This is the first document.',
    'This is the second second document.',
    'And the third one.',
    'Is this the first document?'
]

X = VECTORIZER.fit_transform(CORPUS)
FEATURE_NAMES = VECTORIZER.get_feature_names()

print(FEATURE_NAMES)
print(X.toarray())
