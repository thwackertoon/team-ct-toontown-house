from __init__ import *
from tth.avatar.toon import rgb2p

class BookPage:
    def __init__(self,book):
        self.book = book  
        self.frame = book.bg.attachNewNode('pageFrame')
        
    def destroy(self):
        self.frame.removeNode()