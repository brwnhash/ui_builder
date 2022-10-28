

from abc import ABC, abstractmethod
class RECT_ORIENT():
    ROW=0
    COLUMN=1
    BOTH=2
    NONE=3

class ElmType:
    RECTANGLE="RECTANGLE"
    GROUP="GROUP"
    COMPONENT="COMPONENT"
    INSTANCE="INSTANCE"
    LINE="LINE"
    ELLIPSE="ELLIPSE"
    FRAME="FRAME"

class RectNode(ABC):
    def __init__(self,max_width,max_height,min_left,min_top,width,height,left,top,name,uid,parent,shape_type,x_offset,y_offset):
        """
        min_left and min_top : when box is out of bounding limits like scrolls
        width and height are viewport width and height
        max_width and max_height if actual width is bigger ,mostly for scroll case etc.
        Nodes have relative info w.r.t parent.

        """
        self.root_type=ElmType.RECTANGLE
        if width:
            self.width = width
            self.height = height
            self.left=left-x_offset 
            self.top=top-y_offset 
            self.left=0  if self.left<0 else self.left
            self.right=self.left+self.width
            self.top=0 if self.top<0  else self.top   
            self.bottom=self.top+self.height
        else:
            self.width,self.height,self.left,self.right,self.top,self.bottom=None,None,None,None,None,None

        self.max_width,self.max_height=max_width,max_height
        self.parent=parent 
        self.children=[]
        self.name=name
        self.type=shape_type
        self.uid=str(uid)
        self.min_left=min_left-x_offset
        self.min_top=min_top-y_offset
        self.node_props={}
                        
        if parent:
            if not self.doesChildElmExist():
                self.parent.children.append(self)

    def doesChildElmExist(self):
        for child in self.parent.children:
            if child.uid==self.uid:
                return True
        return False

    @staticmethod
    def hasParent(first_node,other_node):
        """
        check if first node has other node as recursive parent
        """
        if first_node.parent==other_node:
            return True
        if first_node.parent!=None:
            return RectNode.hasParent(first_node.parent,other_node)
        

    def addProps(self,props,key):
        """
        props is a dict of elements to be updated
        """
        if key not in self.node_props:
            self.node_props[key]={}
        self.node_props[key].update(props)
    
    def getRelativeNode(self):
        """
        Node dimension w.r.t its parent node
        """
        width=self.width/self.parent.width 
        height=self.height/self.parent.height
        left=(self.left-self.parent.left)/self.parent.width
        top=(self.top-self.parent.top)/self.parent.height

        #scaling is done w.r.t top container view port not w.r.t actual width

        max_width=self.max_width/self.parent.width 
        max_height=self.max_height/self.parent.height
        min_left=(self.min_left-self.parent.left)/self.parent.width
        min_top=(self.min_top-self.parent.top)/self.parent.height

        return RectNode(max_width,max_height,min_left,min_top,width,height,left,top,self.name,self.uid\
                ,self.parent,self.type,0,0)

    def getArea(self):
        pass


        


        
def getXMargins(rects):
    parent=rects[0].parent
    if parent==None:
        return []
    left_rect=rects[0]
    margins=[left_rect.left-parent.left]
    for rect in rects[1:]:
        diff=Rectangle.get_x_diff(left_rect,rect)
        margins.append(diff)
        left_rect=rect
    last_diff=parent.right-rects[-1].right
    margins.append(last_diff)
    return margins

def getYMargins(rects):
    parent=rects[0].parent
    if parent==None:
        return []
    top_rect=rects[0]
    margins=[top_rect.top-parent.top]
    for rect in rects[1:]:
        diff=Rectangle.get_y_diff(top_rect,rect)
        margins.append(diff)
        top_rect=rect
    last_diff=parent.bottom-rects[-1].bottom
    margins.append(last_diff)
    return margins

class Rectangle(RectNode):
    def __init__(self,props,parent=None,type='RECTANGLE'):
        
        RectNode.__init__(self,props['width'],props['height'],props['x'],props['y'],props['view_width'],\
                        props['view_height'],props['view_x'],props['view_y'],props['name'],\
                        props['uid'],parent,type,props['x_offset'],props['y_offset'])
    @staticmethod
    def is_row_intersection(rect1,rect2):
        left_rect= rect1  if rect1.top<= rect2.top else rect2
        right_rect= rect2 if left_rect==rect1 else rect1
        intersection= True if right_rect.top>=left_rect.top and right_rect.top<=left_rect.bottom else False
        return intersection

    @staticmethod
    def is_col_intersection(rect1,rect2):
        left_rect= rect1  if rect1.left<= rect2.left else rect2
        right_rect= rect2 if left_rect==rect1 else rect1
        intersection= True if right_rect.left>=left_rect.left and right_rect.left<=left_rect.right else False
        return intersection

    @staticmethod
    def get_x_diff(rect1,rect2):
        """
        x axis difference in rect1 and rect2
        """
        left_rect= rect1  if rect1.left<= rect2.left else rect2
        right_rect= rect2 if left_rect==rect1 else rect1
        return right_rect.left-left_rect.right

    @staticmethod
    def get_y_diff(rect1,rect2):   
        top_rect= rect1  if rect1.top<= rect2.top else rect2
        bottom_rect= rect2 if top_rect==rect1 else rect1    
        return bottom_rect.top-top_rect.bottom


    @staticmethod
    def is_valid_orientation(rects,func):
        """
        pass row and column function to check valid orientation.
        """
        valid_intersection=True
        total_rects=len(rects)
        for idx in range(total_rects-1):
            rect=rects[idx]
            for rect1 in rects[idx+1:]:
                valid_intersection=valid_intersection and func(rect,rect1)
            if not valid_intersection:
                break                     
        return valid_intersection

    @staticmethod
    def is_equal(rect1,rect2):
        start=rect1.left==rect2.left and rect1.top==rect2.top
        end=rect1.bottom=rect2.bottom and rect1.right==rect2.right
        return start and end


    @staticmethod
    def get_orientation(rects):
        """
        orientation won't work if there is only one block 
        we looking for row as well as column intersection 
    
        """
        
        if len(rects)<=1:
            return RECT_ORIENT.ROW  

        row=Rectangle.is_valid_orientation(rects,Rectangle.is_row_intersection)
        col=Rectangle.is_valid_orientation(rects,Rectangle.is_col_intersection)
        if row and col:
            return RECT_ORIENT.BOTH
        if row or col:
            return RECT_ORIENT.ROW if row else RECT_ORIENT.COLUMN
        return RECT_ORIENT.NONE

    @property
    def area(self):
        return self.width*self.height

    def abs_diff(self,other):
        return abs(self.left-other.left)+abs(self.right-other.right)


    def top_dir(self,direction):
        return self.top if direction==RECT_ORIENT.ROW else self.left


    def bottom_dir(self,direction):
        return self.bottom if direction==RECT_ORIENT.ROW else self.right


    def left_dir(self,direction):
        return self.left if direction==RECT_ORIENT.ROW else self.top


    def right_dir(self,direction):
        return self.right if direction==RECT_ORIENT.ROW else self.bottom

    def width_dir(self,direction):
        return self.width if direction==RECT_ORIENT.ROW else self.height

    def height_dir(self,direction):
        return self.height if direction==RECT_ORIENT.ROW else self.width

    def contains(self,other):
        """
        right_block  should be inside left block
        bottom_block should be inside top_block       
        """
        left_block= self if self.left<=other.left else other
        right_block=other if left_block==self else self
        width_in=True if (right_block.left>=left_block.left and  right_block.right<=left_block.right) else False
        top_block= self if self.top<=other.top else other
        bottom_block=other if top_block==self else self
        height_in=True if (bottom_block.top>=top_block.top and  bottom_block.bottom<=top_block.bottom) else False
        return True if (width_in and height_in) else False
    



class Frame(Rectangle):
    def __init__(self,props,parent=None,type='FRAME'):
        Rectangle.__init__(self,props,parent,type)
    
class Component(Rectangle):
    def __init__(self,props,parent=None,type='COMPONENT',comp_id=None):
        Rectangle.__init__(self,props,parent,type)
        self.comp_id=comp_id

class Line():
    def __init__(self,props,parent,type='LINE'):
        raise Exception('Line not implemented yet')
    
class Ellipse():
    def __init__(self,props,parent,type='ELLIPSE'):
        raise Exception('Ellipse not implemented yet')





NODE_CLASS_MAPPING = {
    ElmType.FRAME:Frame,
    ElmType.RECTANGLE: Rectangle,
    ElmType.GROUP: Component,
    ElmType.COMPONENT: Component,
    ElmType.INSTANCE: Component,
    ElmType.LINE: Line,
    ElmType.ELLIPSE: Ellipse

}

def isComponentType(elm):
    if elm.type in [ElmType.GROUP,ElmType.COMPONENT,ElmType.INSTANCE,ElmType.FRAME]:
        return True
    return False


def isValidParentChildStructure(parent):
    valid=True
    if not isinstance(parent,Rectangle):
        return True
    for child in parent.children:
        if not isComponentType(child,Rectangle):
            continue
        if not parent.contains(child):
            valid=False
    return valid

    

def normalizeComponent(rect):
    """
    parent and child are of same type and same dimension merge them 

    """
    if not isComponentType(rect):
        return rect
    if len(rect.children)==1:
        child=rect.children[0]
        if isComponentType(child) and Rectangle.is_equal(rect,child):
            rect.children=child.children
        normalizeComponent(child)



            