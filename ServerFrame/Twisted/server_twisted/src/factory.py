#encoding:utf-8

'''
Created on 2015/3/7

@author: Axiezhou
'''

from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

from app.net.protocol import GameProtocol
from app.data import gameglobal
from app.net.connectionManager import ConnectionManager
from app.game import gameWorld

reactor = reactor

class GameFactory(Factory):
    
    '''
    连接工厂
    '''
    def __init__(self):
        self.connManager = ConnectionManager() # 连接管理器
        gameWorld.start(self)
        
        
    def buildProtocol(self, addr):
        p = GameProtocol(self, addr)
        connID = self.connManager.put(p)
        p.id = connID
        return p
    
if __name__ == '__main__':
    endpoint = TCP4ServerEndpoint(reactor, gameglobal.SERVER_PORT)
    gf = GameFactory()
    endpoint.listen(gf)
    reactor.run()
    
    