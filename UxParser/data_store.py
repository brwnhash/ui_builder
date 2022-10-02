

from config import COMPONENT_STORE_PATH,PAGE_STORE_PATH,BASE_PROJ_PATH
import joblib
import os
import shutil
import json

#Session component Manager manages components in current session
#also stores components to store

class DataStore():
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
        

    def storePage(self,page_id,page_data):
        path=PAGE_STORE_PATH(page_id)
        if not os.path.exists(path):
            os.mkdir(path)
        for uid,frame in page_data.items():
            joblib.dump(frame,os.path.join(path,str(uid)+self.file_ext))

    def storeComponents(self,comps):
        path=COMPONENT_STORE_PATH(self.proj_id)
        if not os.path.exists(path):
            os.mkdir(path)
        for uid,comp in comps.items():
            joblib.dump(comp,os.path.join(path,str(uid)+self.file_ext))
        
    def getComponents(self,ids):
        path=COMPONENT_STORE_PATH(self.proj_id)
        files=os.listdir(path) if not ids else [str(id)+self.file_ext for id in ids]
        for file in files:
            fpath=os.path.join(path,file)
            data=joblib.load(fpath)
            id=file.replace(self.file_ext,'').strip()
            yield id,data

