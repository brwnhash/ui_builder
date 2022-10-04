

from config import COMPONENT_STORE_PATH,PAGE_STORE_PATH,BASE_PROJ_PATH
import joblib
import os
import shutil
import json
from abc import ABC, abstractmethod

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
    def __init__(self,proj_id,delete_existing=True):
        self.proj_id=proj_id
        self.file_ext='.mm'
        self.project_meta_file='project_info'+self.file_ext
        self.proj_path=BASE_PROJ_PATH(proj_id)
        if os.path.exists(self.proj_path):
            if delete_existing:
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

    def storeComponents(self,comps):
        for uid,comp in comps.items():
            joblib.dump(comp,os.path.join(self.comp_path,str(uid)+self.file_ext))
        
    def getComponents(self,ids):
        path=self.comp_path
        files=os.listdir(path) if not ids else [str(id)+self.file_ext for id in ids]
        for file in files:
            fpath=os.path.join(path,file)
            data=joblib.load(fpath)
            id=file.replace(self.file_ext,'').strip()
            yield id,data

