#coding:utf-8

'''
Created on 2015/03/07

@author: Axiezhou
'''



from twisted.internet import reactor
from twisted.internet.protocol import Protocol

import jsonpickle


import struct
import json
import threading

from app.common.mixin import MixinClass

from app.log.logger import debug, error, info
from app.net.circularBuffer import CircularBuffer
from app.tools import charUtils

from app.net.imp.impCombatSoldierHandle import ImpCombatSoldierHandle
from app.net.imp.impAuthHandle import ImpAuthHandle
from app.net.imp.impMatchHandle import ImpMatchHandle
from app.net.imp.impLoadPacket import ImpLoadPacket

from app.data import const
from app.data.config import cmd_handle_data as CHD
from app.data.config import handle_cmd_data as HCD



reactor = reactor



class ProtocolHead(object):
    
    def __init__(self, magic, packLen, cmdID, retCode):
        self.magic = magic # 标记
        self.packLen = packLen # 包长度
        self.cmdID = cmdID # 指令ID
        self.retCode = retCode # 返回码（服务器返回执行的结果）

class NetworkMsg(object):

    def __init__(self, pHead, pData):
        self.pHead = pHead # 包头
        self.pData = pData # 包正文
        
    def pack(self):
        packData = struct.pack('!HHHH', self.pHead.magic, self.pHead.packLen, self.pHead.cmdID, self.pHead.retCode) + self.pData
        return packData
    
    def getHandle(self):
        '''
        根据指令ID，获取其处理句柄名称
    @note: 找不到该指令代码对应的句柄时，返回None
        '''
        return CHD.data.get(self.pHead.cmdID, None)
        
    def __str__(self):
        return '{"Head" : {"magic":%d, "packLen":%d, "cmdID":%d, "retCode":%d}, ' % (self.pHead.magic, self.pHead.packLen, self.pHead.cmdID,
                    self.pHead.retCode) + '"Data" : %s' % self.pData






class GameProtocol(Protocol, object):
    

    def __init__(self, factory, ip):
        #debug('GameProtocol.__init__')
        self.factory = factory
        self.ip = ip
        self.ringBuff = CircularBuffer() # 客户端网络数据缓冲
        self.curClientMsg = None # 当前接收到的客户端消息
        self.curClientMsgHandled = False # 当前客户端消息是否已处理（是否已从数据缓冲中取出）
        
        self.buffLock = threading.Lock() # 缓冲数据的同步锁
        
        
        
    def onJsonReceived(self, hd, jsonStr):
        '''
    @param hd: 处理句柄字符串
    @param jsonStr: json字符串 
        '''
        #debug('onJsonReceived, jsonStr: ', jsonStr)
        try: 
            data = None
            if jsonStr and jsonStr != '':
                data = json.loads(jsonStr)
        except:
            error('loads jsons string failed.')
            return 
        
        # ...
        
    
        
    
    def handleRequest(self, hd, data, printLog = True):
        '''
        向客户端发送请求
    @param hd: 请求句柄
    @param data: 请求参数
        '''
        cmdID = HCD.data.get(hd, None)
        if not cmdID:
            error("don't has this request handle:", hd)
            return 
        self.sendNetworkMsg(cmdID, data, 0, printLog)
        
    def sendNetworkMsg(self, cmdID, data, retCode, printLog = True):
        '''
        向客户端发送消息
        '''
        pData = ''
        try:
            if data and data != '':
                pData = jsonpickle.encode(data, unpicklable = False)
        except:
            error("can't encode this obj:", data)
            return 
        pHead = ProtocolHead(0, len(pData) + 8, cmdID, retCode)
        serverMsg = NetworkMsg(pHead, pData)
        if printLog:
            info('send server msg to %s:' % (self.ip, ), serverMsg)
        self.transport.write(serverMsg.pack())
        

    
    
    def __isCompleteMsgRecv(self):
        '''
        判断是否已从客户端接收到一条完整的消息
        '''
        if self.buffLock.acquire():
            ret = self.__realIsCompleteMsgRecv()
            self.buffLock.release()
            return ret
            
    def __realIsCompleteMsgRecv(self):
        if self.ringBuff.size >= 4:
            packLen = charUtils.bytes2INT16(self.ringBuff.copy(2, offset = 2))
            if self.ringBuff.size >= packLen:
                self.__packNetworkMsgFromBuff()
                return True
        return False
    
    
    def __packNetworkMsgFromBuff(self):
        '''
        从客户端接收缓存数据中打包一个网络消息
        调用此方法时，__isCompleteMsgeRecv()必须返回为True
        '''
        pHead = self.__packProtocolHeadFromBuff()
        pData = charUtils.bytes2Str(self.ringBuff.get(pHead.packLen - 8))
        self.curClientMsg = NetworkMsg(pHead, pData)
        self.curClientMsgHandled = False
        
    def __packProtocolHeadFromBuff(self):
        '''
        打包包头
        '''
        magic = charUtils.bytes2INT16(self.ringBuff.get(2))
        packLen = charUtils.bytes2INT16(self.ringBuff.get(2))
        cmdID = charUtils.bytes2INT16(self.ringBuff.get(2))
        retCode = charUtils.bytes2INT16(self.ringBuff.get(2))
        return ProtocolHead(magic, packLen, cmdID, retCode)
    
    
    def connectionMade(self):
        debug('%s connected to server.' %  self.ip)
        self.status = const.CONNECTION_STATUS_MADE
        #self.transport.write('success')
        
        
    def connectionLost(self, reason):
        info(self.ip, 'connectionLost.')
        if self.avatar is not None:
            self.avatar.connectionLost()
            
        self.factory.connManager.remove(self.id)
        
    
    
        
    def dataReceived(self, data):
        Protocol.dataReceived(self, data)
        
        self.buffLock.acquire()
        self.ringBuff.put(data)
        self.buffLock.release()
        
        if self.__isCompleteMsgRecv():
            debug('received client msg from %s : %s' % (self.ip, self.curClientMsg))
            self.curClientMsgHandled = True
            hd = self.curClientMsg.getHandle()
            if not hd:
                error("don't has this cmd :", self.curClientMsg.pHead.cmdID)
                return 
            self.onJsonReceived(hd, self.curClientMsg.pData)
        
    
        
    

    

