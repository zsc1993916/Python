#encoding:utf-8

'''
Created on 2015年3月10日

@author: Axiezhou
'''

import random


from app.log.logger import error, info
from app.data import const

class ConnectionManager(object):
    
    '''
    连接管理器
    '''
    
    MAX_CONN_SIZE = 10 # 最大保持的同时在线连接个数
    
    def __init__(self):
        self.conns = {}
        self.curSize = 0
        
    def put(self, conn):
        
        '''
        加入一个连接
        '''
        
        if self.curSize == self.MAX_CONN_SIZE:
            error('connected number is full while put a connection.')
            return None
        while True: 
            connID = random.randint(1, 10000)
            if not self.conns.has_key(connID):
                break 
        
        info('add a connection : %d' % connID)
        
        self.curSize = self.curSize + 1
        self.conns[connID] = conn
        
        return connID
    
    def remove(self, connID):
        '''
        删除一个连接
        '''
        if not self.conns.has_key(connID):
            error("can't remove connection by inexistence ID.")
            return 
        self.curSize = self.curSize - 1
        del self.conns[connID]
    
    def get(self, connID):
        '''
        获取一个连接
        '''
        if not self.conns.has_key(connID):
            error("can't get connection by unexistence ID.")
            return 
        return self.conns[connID]
    
    
    def serachMatchingConnection(self):
        '''
        简单返回一个正在匹配中的连接ID
    @note: 如果未找到这样的ID， 返回None
        '''
        for connID, pb in self.conns.items():
            if pb.status == const.CONNECTION_STATUS_MATCHING:
                return connID
        return None
