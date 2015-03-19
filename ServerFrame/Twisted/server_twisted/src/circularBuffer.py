#encoding:utf-8

'''
Created on 2015年3月8日

@author: Axiezhou
'''

from app.log.logger import info, error

BUFF_MAX_SIZE = 4000

class CircularBuffer(object):
    
    def __init__(self):
        self.buff = []
        self.head = 0
        self.size = 0
        self.tail = 0
        self.allocSize = 0
        
    def clear(self):
        self.size = 0
        self.head = 0
        self.tail = 0
    
    def put(self, data):
        for item in data:
            self.__join(item)
    
    def get(self, count = 1):
        realCount = min(count, self.size)
        dst = self.copy(count)
        self.head = (self.head + realCount) % BUFF_MAX_SIZE
        self.size -= realCount
        return dst

    def copy(self, count, offset = 0):
        realCount = min(count, self.size - offset)
        if realCount == 0:
            return []
        if realCount < 0:
            error('count required is too large or offset larger than buff size..')
            return None
        dst = []
        for i in range(realCount):
            dst.append(self.buff[(self.head + offset + i) % BUFF_MAX_SIZE])
        return dst
    
    def __join(self, item):
        if self.size == BUFF_MAX_SIZE:
            info('buff is full...')
            return 
        if self.tail >= self.allocSize:
            self.buff.append(item)
            self.allocSize = self.allocSize + 1
        else:
            self.buff[self.tail] = item
            
        self.tail = self.tail + 1
        if self.tail == BUFF_MAX_SIZE:
            self.tail = 0
            
        self.size = self.size + 1
        
        