
import FigmaPy
#Session component Manager manages components in current session
#also stores components to store

class SessionComponentManager():
    def __init__(self,token,key):
        self.figma = FigmaPy.FigmaPy(token=token)
        self.req_key=key
        self.comp_map={}
        self.missing_comps=[]
        
    def update_comp_list(self,existing_comps,missing_comps):
        self.comp_map=existing_comps
        self.missing_comps=missing_comps
        
    def fetchComponent(self):

        
        pass