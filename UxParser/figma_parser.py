from asyncio.log import logger
import FigmaPy
import logging
from helpers import Frame,Component,Rectangle,ComponentParser,DictVect



# valid top elements

class FigmaParseType():
    PROJECT='project'
    PAGE='page'

def getDimProps(data):
    res={}
    res['name']=data.name
    box=data.absoluteBoundingBox
    render_box=data.absoluteRenderBounds
    
    res['width'],res['height'],res['x'],res['y']=box.width,box.height,box.x,box.y
    res['view_width'],res['view_height'],res['view_x'],res['view_y']=render_box['width'],\
                                                                     render_box['height'],render_box['x'],render_box['y']
    res['uid']=data.id

    return res


class FigmaComponentParser(ComponentParser):
    """
    x_offset ,y_offset : offset are fixed and w.r.t top frame
    parse component data and return Component and interaction to component 
    return: component
    """
    def __init__(self,x_offset,y_offset):
        self.x_offset=x_offset
        self.y_offset=y_offset
        self.comp_map={}
        self.parseMap={"RECTANGLE":self.parseRectangle,
        "COMPONENT":self.parseComponent,
        "INSTANCE":self.parseComponent,
        "LINE":self.parseLine,
        "ELLIPSE":self.parseEllipse

        }

        
    def getNodeDimProps(self,data,parent):
        props=getDimProps(data)
        props['parent']=parent
        props['x_offset'],props['y_offset']=self.x_offset,self.y_offset
        return props
        
    def parseElement(self,elm,parent):
        if elm.type not in self.parseMap.keys():
            logger.error(f'nested {elm.type} element is not implemented yet ')
            return
        self.parseMap[elm.type](elm,parent)


    def parseRectangle(self,data,parent):
        props=self.getNodeDimProps(data,parent)
        rect=Rectangle(props)
        for elm in rect.children:
            self.parseElement(elm,rect)


    
    def parseEllipse(self,data,parent):
        pass

    def parseLine(self,data,parent):
        pass

    def parseComponent(self,data,parent):
        props=self.getNodeDimProps(data,parent)
        comp_id= data.componentId if hasattr(data,'componentId') else None
        comp=Component(props,parent,data.type,comp_id)
        self.comp_map[comp.uid]=comp
        for elm in data.children:
            self.parseElement(elm,comp)
        return comp
        


class UNode:
    def __init__(self,elm):
        self.uid=elm.id
        self.children=[]


class FigmaParser():
    """
    Parser has data fetcher and parser 
    store component map which is per page .
    compset map is for overall projects
    page map stores all components in page and there structure 

    """

    def __init__(self,token,key,store):
        """
        """
        self.store=store
        self.req_key=key
        self.token=token
        self.x_offset,self.y_offset=0,0
        self.figma = FigmaPy.FigmaPy(token=token)
        self.parseMap={'FRAME':self.parseFrame,
                        'COMPONENT':self.parseComponent,
                        'INSTANCE':self.parseComponent}
        self.comp_list=[]
        self.compset_map={}
        self.page_map={}
        self.interaction_map={}
    
    def initializeFrame(self):
        self.comp_list=[]
        self.compset_map={}
        self.page_map={}
        self.interaction_map={}


    def isDerivedComponent(self,type):
        """
        what to be considered as derived component
        """
        if type in self.parseMap.keys():
            return True
        

    def getComponents(self):
        return self.comp_list
   

    def fetch(self,page_id=None):
        data=None
        if not page_id:
            data=self.figma.get_file(key=self.req_key,return_raw_data=True)
        else:
            data=self.figma.get_file_nodes(self.req_key,ids=[page_id])
            pid=page_id.replace('%3A',':')
            data.update(data['nodes'][pid])
            del data['nodes']

        parsed_data=self.figma.parse_file_data(self.req_key,data)

        return parsed_data
    
    def fetchComponentSets(self,data):
        """
        we do single component fetching ,this can be improved.
        """
        for uid,_ in data.componentSets.items():
            cid=uid.replace(':','%3A')
            if cid in self.compset_map:
                logger.info(f'skipping component fetch of {cid} as it already exists ')
                continue
            comp_set=self.fetch(cid)
            self.compset_map[uid]=comp_set


    def fetchAll(self,page_id=None):
        """
        Fetch page and component info both
        """
        page_data=self.fetch(page_id)
        compsets=self.fetchComponentSets(page_data)
        type=FigmaParseType.PAGE if page_id else FigmaParseType.PROJECT
        return {'doc':page_data,'type':type,'compsets':compsets}
        
        
    def parseComponent(self,elm,root):
        if elm.id in self.comp_list:
            logger(f'skipped parsing of component {elm.id} as it already exists ')
            return
        fc=FigmaComponentParser(self.x_offset,self.y_offset)
        fc.parseComponent(elm,root)
        self.comp_list.append(elm.id)
        self.store.storeComponents(fc.comp_map)


    def parseFrame(self,data,parent=None):
        """
        Inner Frames are considered a component
        """
        
        box=getDimProps(data)
        box['x_offset'],box['y_offset'],box['parent']=self.x_offset,self.y_offset,parent
        root_node=Frame(box)
        if not hasattr(data,'children'):
            return
        for element in data.children:
            #only components will be parsed 
            if element.type not in self.parseMap.keys():
                logging.error(f'Frame top element {element.type} is not supported')
                continue
            self.parseMap[element.type](element,root_node)

        #frame which has parent is inner Frame considered as component
        if parent!=None:
            self.store.storeComponents({root_node.uid:root_node})
            self.comp_list.append(root_node.uid)

    def getPageStructure(self,parent):
        """
        DOM structure with only ids
        """
        node=UNode(parent)
        if not hasattr(parent,'children'):
            return node
        for elm in parent.children:
            cnode=self.getPageStructure(elm)
            node.children.append(cnode)
        return node


    def parseNode(self,data):
        """
        Node has single frame data
        """
        frame=data.document
        self.x_offset,self.y_offset=frame.absoluteBoundingBox.x,frame.absoluteBoundingBox.y          
        self.parseFrame(frame)
        page_node=self.getPageStructure(frame)
        self.store.storePage(page_node)


    def parse(self,data):
        """
        parsing is done per page 
        """
        type,doc,compsets=data['type'],data['doc'],data['compsets']
        self.initializeFrame()
        self.parseNode(doc)
        compsets={} if not compsets else compsets
        for comp_id,comp_data in compsets.items():
            if comp_id in self.comp_list:
                continue
            self.parseNode(comp_data)
        



    

