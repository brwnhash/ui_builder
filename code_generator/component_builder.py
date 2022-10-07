


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
  
    def run(self):
        node_data=joblib.load(self.ref_file)
        print('cool')

        pass
