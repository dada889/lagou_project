# -*- coding: utf-8 -*-
__author__ = 'dada'

from pymongo import MongoClient

class LagouDb():

    def __init__(self, local=True):
        if local:
            self.client = MongoClient('localhost', 27017)
        else:
            self.client = MongoClient('192.168.3.18', 27017)

    def db(self):
        return self.client.lagou




if __name__ == "__main__":
    a = LagouDb().db()
    d = {'3': 12}
    a['proxy'].insert_one(d)
