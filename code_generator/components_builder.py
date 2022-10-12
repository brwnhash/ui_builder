
import joblib
import os
from config import  COMPONENT_STORE_PATH,COMP_FILES_EXT
from helpers import NodeType


class ComponentsBuilder():
    def __init__(self,ref_file,comp_dir,type,layout_parser):
        """
        ref file : can have root node with all nodes or it single component .
        """
        self.ref_file=ref_file
        self.comp_dir=comp_dir
        self.type=type
        self.layout_parser=layout_parser


    def getComponentStack(self,nodes,stack):
        """
        breath first approach to explore all components .All leafs will be at end .
        """
        comps=[]
        #add first entry
        if not stack:
            stack.append(nodes[0].uid)  
        for node in nodes:
            for comp in node.children:
                stack.append(comp.uid)
                comps.append(comp)
        if comps:
            self.getComponentStack(comps,stack)
            
    def run(self):
        node_data=joblib.load(self.ref_file)
        if self.type==NodeType.PAGE:
            self.layout_parser.parsePageStructure(node_data)
        stack=[]
        self.getComponentStack([node_data],stack)
        while(stack):
            comp_id=stack.pop()
            bc=BuildComponent(self.comp_dir,comp_id,self.layout_parser)
            bc.run()




class BuildComponent():
    def __init__(self,comp_dir,comp_id,layout_parser):
        self.comp_id=comp_id
        self.comp_file=os.path.join(comp_dir,str(comp_id)+COMP_FILES_EXT)
        self.layout_parser=layout_parser

    def exists(self):
        return os.path.exists(self.comp_file) 

            
    def getStyleSheetProps(self):
        pass

    def getLayoutProps(self,comp_data):
        self.layout_parser.parseComponentStructure(comp_data)
        
    def run(self):
        if not self.exists():
            return
        comp_data=joblib.load(self.comp_file)
        self.getLayoutProps(comp_data)
        
