


import joblib
import os


class ComponentBuilder():
    def __init__(self,ref_file,comp_dir,ext):
        """
        ref file : can have root node with all nodes or it single component .
        """
        self.ref_file=ref_file
        self.comp_dir=comp_dir
        self.ext=ext

    def _readComponent(self,id):
        path=os.path.join(self.comp_dir,str(id)+self.ext)
        return joblib.load(path)

    def buildComponentStack(self,nodes,stack):
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
            self.buildComponentStack(comps,stack)
            
    def run(self):
        node_data=joblib.load(self.ref_file)
        stack=[]
        self.buildComponentStack([node_data],stack)
        print('cool')

        pass
