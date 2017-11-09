""" 候选生成（Candidate generation） & 排序（LTR， Learning to Ranking）"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import argparse
from operator import itemgetter
from math import sqrt

import pandas as pd
import pymysql
from sklearn.model_selection import train_test_split
# from sklearn.metrics.pairwise import pairwise_distances
# from sklearn.metrics import mean_squared_error

class UserBasedCF(object):
    """ 基于用户的协同过滤 """
    def __init__(self, n_similarity_users=20, n_recommendation_articles=10):
        self.n_similarity_users = n_similarity_users
        self.n_recomendation_articles = n_recommendation_articles

        self.train_data = {}
        self.test_data = {}

        self.user_similarity_matrix = {}
        self.article_count = 0
        print("Number of similarity users = {}".format(self.n_similarity_users))
        print("Number of recommended articles = {}".format(self.n_recomendation_articles))
    
    def store_data_mysql2csv(self):
        """Store data from mysql to csv."""
        sql = 'select uid,lid,ImportantDegree,LocalModifyTime from 20171020_rating'
        conn = pymysql.connect(host='192.168.106.231', \
                            user='root', password='cnkidras', \
                            db='recomm', charset='utf8', use_unicode=True)
        df = pd.read_sql(sql, con=conn)
        print(df.head())
        df.to_csv("data.csv", index=False)
        conn.close()

    def load_data(self):
        """Load data from csv."""
        if os.path.isfile('data.csv'):
            if os.path.getsize('data.csv') > 0:
                return
        self.store_data_mysql2csv()
        header = ['uid', 'lid', 'ImportantDegree', 'LocalModifyTime']
        df = pd.read_csv('data.csv', sep=',', names=header, low_memory=False)
        train_data, test_data = train_test_split(df, test_size=0.2)
        train_data_len = 0
        test_data_len = 0
        for line in train_data.itertuples():
            if line[1] not in self.train_data:
                self.train_data.setdefault(line[1], {})
            self.train_data[line[1]][line[2]] = line[3]
            train_data_len += 1

        for line in test_data.itertuples():
            if line[1] not in self.test_data:
                self.test_data.setdefault(line[1], {})
            self.test_data[line[1]][line[2]] = line[3]
            test_data_len += 1
        print('Train data length = %s' % train_data_len)
        print('Test data length = %s' % test_data_len)

    def calc_user_similarity(self):
        """ 计算用户相似度 """
        article_user = {}
        for uid, lids in self.train_data.items():
            for lid in lids:
                if lid not in article_user:
                    article_user[lid] = set()
                article_user[lid].add(uid)
        self.article_count = len(article_user)
        print("Total article numbers = %d" % self.article_count)
        for lid, uids in article_user.items():
            for uid1 in uids:
                for uid2 in uids:
                    if uid1 == uid2:
                        continue
                    self.user_similarity_matrix.setdefault(uid1, {})
                    self.user_similarity_matrix[uid1].setdefault(uid2, 0)
                    self.user_similarity_matrix[uid1][uid2] += 1
        
        for u, related_users in self.user_similarity_matrix.items():
            for v, count in related_users.items():
                self.user_similarity_matrix[u][v] = count / sqrt(len(self.train_data[u]) * len(self.train_data[v]))
    
    def recommendation(self, user):
        """ 为用户user推荐文献，返回推荐列表及评分。 """
        K = self.n_similarity_users
        N = self.n_recomendation_articles
        rank = {}
        print("user: ", user)
        watched_articles = self.train_data[user]

        for v, wuv in sorted(self.user_similarity_matrix[user].items(), key=itemgetter(1), reverse=True)[0:K]:
            for article in self.train_data[v]:
                if article in watched_articles:
                    continue
                rank.setdefault(article, 0)
                rank[article] += wuv
        return sorted(rank.items(), key=itemgetter(1), reverse=True)

    def evaluate(self):
        """ 计算准确率、召回率、覆盖率 """
        N = self.n_recomendation_articles
        hit = 0
        recommend_count = 0
        test_count = 0
        all_rec_article = set()

        for i, user, in enumerate(self.train_data):
            test_articles = self.test_data.get(user, {})
            recommend_articles = self.recommendation(user)
            for article, w in recommend_articles:
                if article in test_articles:
                    hit += 1
                all_rec_article.add(article)
            recommend_count += N
            test_count = len(test_articles)
        precision = hit / (1.0 * recommend_count)
        recall = hit / (1.0 * test_count)
        coverage = len(all_rec_article) / (1.0 * self.article_count)
        print('precision= %.4f\t recall=%.4f\t coverage=%.4f' % (precision, recall, coverage))
    
class PrintArticles(object):
    """ print class """
    def  __init__(self, lid_list):
        self.lid_list = lid_list
    
    def output(self):
        """ 在数据库中查找lid对应的文献标题，并打印。 """
        conn = pymysql.connect(host='192.168.106.231', \
                            user='root', password='cnkidras', \
                            db='recomm', charset='utf8', use_unicode=True)
        for score_tuple in self.lid_list:
            sql = 'select lid,UserID,title from test where lid = %s;' % score_tuple[0]
            df = pd.read_sql(sql, con=conn)
            print(df)

        conn.close()

FLAGS = None

def main(_):
    """main function"""
    user_cf = UserBasedCF(20, 10)
    user_cf.load_data()
    user_cf.calc_user_similarity()
    recommended_articled = user_cf.recommendation(FLAGS.uid)
    print(recommended_articled[0:10])
    out = PrintArticles(recommended_articled[0:10])
    out.output()
    # user_cf.evaluate()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.register("type", "bool", lambda v: v.lower() == "true")
    parser.add_argument(
        "--uid",
        type=str,
        default='80871',
        help="The user who is going to be recommended articles."
    )
    parser.add_argument(
        "--n",
        type=int,
        default=10,
        help="Number of recommended articles."
    )

    FLAGS, unparsed = parser.parse_known_args()
    print("{} {}".format(sys.argv[0], unparsed))
    print(FLAGS)
    main(FLAGS)
