
from .nodes import Node

#application is build of components and every component will have multiple nodes ..
# now interaction can change either behaviour of node or completely modify it..
#interaction should define type of mutation done on object.


class Component(Node):
    def __init__(self):
        Node.__init__(self)
        self.node_list=[]
        
