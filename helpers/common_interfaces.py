
from abc import ABC, abstractmethod
class ComponentParser():
    def __init__(self):
        pass

class ComponentLayoutParser():
    def __init__(self):
        pass
    @abstractmethod
    def parsePageStructure(self,node):
        pass
    @abstractmethod
    def parseComponentStructure(self,node):
        pass

class NodeType:
    PAGE=0
    COMPONENT=1



class CompNode:
    def __init__(self,uid):
        self.uid=uid

