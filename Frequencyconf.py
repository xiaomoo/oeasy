#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.getconf import getConfig
import tornado
import pymysql
from pymysql.cursors import DictCursor
import json
from compare import Compare

conf_area = list(set(getConfig('compare', 'area').split(',')) - {''})
conf_device = list(set(getConfig('compare', 'device').split(",")) - {''})
conf_dimension = int(getConfig('compare', 'dimension'))
conf_model_path = getConfig('compare', 'model_path')
conf_image_size = eval(getConfig('compare', 'image_size'))
conf_detect_url = getConfig('compare', 'detect_url')
conf_gpu_idx = int(getConfig('compare', 'gpu_idx'))

filepath = "./face_compare_server/conf/conf.txt"

class Frequence(tornado):
    def __init__(self):
        self.area = conf_area
        self.dev = conf_device
        self.dimension = conf_dimension
        self._model_path = conf_model_path
        self._detect_url = conf_detect_url
        self.con1, self.con2, self.con3 = 0
        self.uid = ""

    def getPost(self):
        self.con1 = self.get_body_argument("con1")
        self.con2 = self.get_body_argument("con2")
        self.con3 = self.get_body_argument("con3")
        if self.con1 < 0 and 0 < self.con2 < 30 and 0 < self.con3 < 90:
            self.write("con1 in [0-15]")
        elif self.con1 < 0 and self.con2 < 0 and 0 < self.con3 < 90:
            self.write("con1 in [0-15] and con2 in [0-30]")
        elif self.con1 < 0 and self.con2 > 30 and 0 < self.con3 < 90:
            self.write("con1 in [0-15] and con2 in [0-30]")
        elif self.con1 < 0 and 0 < self.con2 < 30 and self.con3 < 0:
            self.write("con1 in [0-15] and con3 in [0-90] ")
        elif self.con1 < 0 and 0 < self.con2 < 30 and self.con3 > 90:
            self.write("con1 is in [0-15] and con3 is in [0-90]")
        elif self.con1 < 0 and self.con2 < 0 and self.con3 > 90:
            self.write("con1 is in [0-15] and con2 is in [0-30] and con3 is in [0-90]")
        elif self.con1 < 0 and self.con2 > 30 and self.con3 < 0:
            self.write("con1 is in [0-15] and con2 is in [0-30] and con3 is in [0-90]")
        elif self.con1 < 0 and self.con2 < 0 and self.con3 < 0:
            self.write("con1 is in [0-15] and con2 is in [0-30] and con3 is in [0-90]")
        elif self.con1 < 0 and self.con2 > 30 and self.con3 > 90:
            self.write("con1 is in [0-15] and con2 is in [0-30] and con3 is in [0-90]")
        elif self.con1 > 15 and 0 < self.con2 < 30 and 0 < self.con3 < 90:
            self.write("con1 is in [0-15]")
        elif self.con1 > 15 and self.con2 < 0 and 0 < self.con3 < 90:
            self.write("con1 is in [0-15] and con2 is in [0-30]")
        elif self.con1 > 15 and self.con2 > 30 and 0 < self.con3 < 90:
            self.write("con1 is in [0-15] and con2 is in [0-30]")
        elif self.con1 > 15 and 0 < self.con2 < 30 and self.con3 < 0:
            self.write("con1 is in [0-15] and con3 is in [0-90]")
        elif self.con1 > 15 and 0 < self.con2 < 30 and self.con3 > 90:
            self.write("con1 is in [0-15] and con3 is in [0-90]")
        elif self.con1 > 15 and self.con2 < 0 and self.con3 < 0:
            self.write("con1 is in [0-15] and con2 is in [0-30] and con3 is in [0-90]")
        elif self.con1 > 15 and self.con2 > 30 and self.con3 > 90:
            self.write("con1 is in [0-15] and con2 is in [0-30] and con3 is in [0-90]")
        elif self.con1 > 15 and self.con2 < 0 and self.con3 > 90:
            self.write("con1 is in [0-15],con2 is in [0-30] and con3 is in [0-90]")
        elif self.con1 > 15 and self.con2 > 30 and self.con3 < 0:
            self.write("con1 is in [0-15] and con2 is in [0-30] and con3 is in [0-90]")
        elif 0 < self.con1 < 15 and self.con2 < 0 and 0 < self.con3 < 90:
            self.write("con2 is in [0-30]")
        elif 0 < self.con1 < 15 and self.con2 > 30 and 0 < self.con3 < 90:
            self.write("con2 is in [0-30]")
        elif 0 < self.con1 < 15 and 0 < self.con2 < 30 and self.con3 < 0:
            self.write("con3 is in [0-90]")
        elif 0 < self.con1 < 15 and 0 < self.con2 < 30 and self.con3 > 90:
            self.write("con3 is in [0-90]")
        elif 0 < self.con1 < 15 and self.con2 < 0 and self.con3 > 90:
            self.write("con2 is in [0-30] and con3 is in [0-90]")
        elif 0 < self.con1 < 15 and self.con2 < 0 and self.con3 < 0:
            self.write("con2 is in [0-30] and con3 is in [0-90]")
        elif 0 < self.con1 < 15 and self.con2 > 30 and self.con3 < 0:
            self.write("con2 is in [0-30] and con3 is in [0-90]")
        elif 0 < self.con1 < 15 and self.con2 > 30 and self.con3 > 90:
            self.write("con2 is in [0-30] and con3 is in [0-90]")
        elif 0 < self.con1 < 15 and 0 < self.con2 < 30 and 0 < self.con3 < 90:
            con_dic = {
                'con1': self.con1,
                'con2': self.con2,
                'con3': self.con3
            }
            with open(filepath, 'w') as json_files:
                json_files.write(json.dump(con_dic))
            json_files.close()
            self.write(json.load(open(filepath)))
        else:
            self.write("Please input a number")

    def screen(self):
        stranger_list = []
        total = 0
        self.uid = self.get_body_arguement("uid")
        db = pymysql.connect(host='192.168.4.189', port='3306', database='strange_list', user='syncdb', passwd='syncdb_list')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        if self.uid == "":
            sql = "select item_id, pic_url, frequency, uid from stranger_list"
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                total += 1
                stranger_list.append(row)
            self.write(total, stranger_list)
        else:
            sql = "select item_id, pic_uri, frequence, uid from stranger_list where uid == self.uid"
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                total += 1
                stranger_list.append(row)
            self.write(total, stranger_list)
        db.close()

if __name__ == '__main__':
   pass