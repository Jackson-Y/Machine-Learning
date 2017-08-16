# 从零开始机器学习 Machine Learning
Machine Learning &amp; Deep Learning  
> 本文适合有一定编程经验，对机器学习零基础的同学作为入门引导。  
> 本文主要以机器学习和深度学习算法的使用案列为主，不深究算法原理。

## 1. text
文本（包括文本特征提取、向量化、加权、文本分类）
### 1) feature extraction（特征提取）
- 文本标记  
  标记即人工将已知的数据集分类：  
  e.g.   
  > 恶意网页 vs 非恶意网页、  
  > 垃圾邮件 vs 非垃圾邮件、   
  > 正面评论 vs 负面评论  
- 文本分词  
去停用词：  
e.g.   
  > 中文：的、是、啊、吖、吧、呃，以及标点等  
  > 英文：is, a, an, one, yeah, 'll, 's, 'ld...
去一些无用信息：  
e.g.  
  > 网页中的的标记文本<html><div><script>等  
  
### 2) vectorizer & tf-idf weighting
特征向量化、基于tf-idf的加权向量化算法：  
使用空间向量模型，把提取出来的特征转化为空间向量，并给不同的特征赋以不同的权重。  
  
### 3) classification
文本分类算法：  
利用转换好的带有分类标记的空间向量，对特定的数据函数模型进行训练(逐步调优函数的参数)，  
然后用训练出来的分类模型对未知数据集进行分类。  
（目前的所使用的数据集训练出来的模型，分类准确率可以达到80%左右）  
- Logistic Regression（逻辑回归分类算法）
- Naive Bayes（朴素贝叶斯分类算法）
