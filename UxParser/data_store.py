

from config import COMPONENT_STORE_PATH,BASE_PROJ_PATH
import joblib
import os
#Session component Manager manages components in current session
#also stores components to store

class DataStore():
    def __init__(self,proj_id):
        self.proj_id=proj_id
        self.file_ext='.mm'
        proj_path=BASE_PROJ_PATH(proj_id)
        if not os.path.exists(proj_path):
            os.mkdir(proj_path)

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

