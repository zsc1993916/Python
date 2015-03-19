#encoding:utf-8

'''
Created on 2015年3月9日

@author: Axiezhou
'''

from struct import unpack

def bytes2INT8(bytearr):
    return unpack('!B', bytes2Str(bytearr))[0]

def bytes2INT16(bytearr):
    return unpack('!H', bytes2Str(bytearr))[0]

def bytes2INT32(bytearr):
    return unpack('!I', bytes2Str(bytearr))[0]


def bytes2Str(bytearr):
    if not bytearr:
        return ''
    data = ''
    for byte in bytearr:
        data = data + byte
    return data
