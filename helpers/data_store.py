

from config import COMPONENT_STORE_PATH,PAGE_STORE_PATH,BASE_PROJ_PATH,COMP_FILES_EXT
import joblib
import os
import shutil
import json
from abc import ABC, abstractmethod
from helpers import Component,CompNode

#Session component Manager manages components in current session
#also stores components to store


class DataStore(ABC):
    """
    Store Id and components per page 
    """
    @abstractmethod
    def storeProjectMeta(self,info):
        """
        info is expected a json format.
        """
        return
        
    @abstractmethod
    def storePage(self,page_id,page_data):
        return

    @abstractmethod
    def storeComponents(self,comps):
        return
        
    @abstractmethod
    def getComponents(self,ids):
        return

class LocalStore(DataStore):
    """
    Store Id and components per page 
    """
    def __init__(self,proj_id,mode='r'):
        """
        mode: read, append ,write 
        read and append wont delete existing 
        """
        self.proj_id=proj_id
        self.file_ext=COMP_FILES_EXT
        self.project_meta_file='project_info'+self.file_ext
        self.proj_path=BASE_PROJ_PATH(proj_id)
        if os.path.exists(self.proj_path):
            if mode=='w':
                shutil.rmtree(self.proj_path)
                os.mkdir(self.proj_path)
        else:
            os.mkdir(self.proj_path)

        self.comp_path=COMPONENT_STORE_PATH(self.proj_id)
        if not os.path.exists(self.comp_path):
            os.mkdir(self.comp_path)
        self.page_store_path=PAGE_STORE_PATH(self.proj_id)
        if not os.path.exists(self.page_store_path):
            os.mkdir(self.page_store_path)

    def storeProjectMeta(self,info):
        """
        info is expected a json format.
        """
        fname=os.path.join(self.proj_path,self.project_meta_file)
        if os.path.exists(fname):
            last_info=json.load(fname)
            info.update(last_info)
        with open(fname,'r') as fp:
            json.dump(info,fp)
        

    def storePage(self,page_data):
        uid=page_data.uid
        joblib.dump(page_data,os.path.join(self.page_store_path,str(uid)+self.file_ext))

    def normalizeComponentChildren(self,comp):
        ids=[]
        for child in comp.children:
            if isinstance(child,Component):
                ids.append(CompNode(child.uid))
            elif isinstance(child,CompNode):
                ids.append(child)
            else:
                pass
        comp.children=ids


    def storeComponents(self,comps):
        """
        during storage if children are of type Node ,store them in list format
        """
        for uid,comp in comps.items():
            self.normalizeComponentChildren(comp)
            joblib.dump(comp,os.path.join(self.comp_path,str(uid)+self.file_ext))

    def getComponent(self,id):
        file=str(id)+self.file_ext
        fpath=os.path.join(self.comp_path,file)
        data=joblib.load(fpath)
        return id,data
    
    def getComponents(self,ids):
        path=self.comp_path
        files=os.listdir(path) if not ids else [str(id)+self.file_ext for id in ids]
        for id,file in zip(ids,files):
            fpath=os.path.join(path,file)
            data=joblib.load(fpath)
            yield id,data

