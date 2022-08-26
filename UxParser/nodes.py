



class RECT_INTERSECT():
    ROW=0
    COLUMN=1
    BOTH=2
    NONE=3



class Node(object):
    def __init__(self,max_width,max_height,min_left,min_top,width,height,left,top,name,uid,parent,shape_type,x_offset,y_offset):
        """
        min_left and min_top : when box is out of bounding limits like scrolls
        width and height are viewport width and height
        max_width and max_height if actual width is bigger ,mostly for scroll case etc.
        Nodes have relative info w.r.t parent.

        """
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
        self.shape_type=shape_type
        self.uid=uid
        self.min_left=min_left-x_offset
        self.min_top=min_top-y_offset
        if parent:
            self.parent.children.append(self)


    def get_relative_node(self):
        """
        cases where there is scroll maxwidth and maxheight will be bigger than viewport
        """
        if self.width:
            width=self.width/self.parent.width 
            height=self.height/self.parent.height
            left=(self.left-self.parent.left)/self.parent.width
            top=(self.top-self.parent.top)/self.parent.height

        #scaling is done w.r.t top container view port not w.r.t actual width

        max_width=self.max_width/self.parent.width 
        max_height=self.max_height/self.parent.height
        min_left=(self.min_left-self.parent.left)/self.parent.width
        min_top=(self.min_top-self.parent.top)/self.parent.height

        return Node(max_width,max_height,min_left,min_top,width,height,left,top,self.name,self.uid\
                ,self.parent,self.shape_type,0,0)

        
        

class Frame(Node):
    def __init__(self,props,type='FRAME'):
        Node.__init__(self,props['width'],props['height'],props['x'],props['y'],props['view_width'],\
                        props['view_height'],props['view_x'],props['view_y'],props['name'],\
                        props['uid'],props['parent'],type,props['x_offset'],props['y_offset'])
    
class Component(Node):
    def __init__(self,props,type='COMPONENT',parent_comp_id=None):
        Node.__init__(self,props['width'],props['height'],props['x'],props['y'],props['view_width'],\
                        props['view_height'],props['view_x'],props['view_y'],props['name'],\
                        props['uid'],props['parent'],type,props['x_offset'],props['y_offset'])

        self.parent_comp_id=parent_comp_id
        
class Rectange(Node):
    def __init__(self,props,type='RECTANGLE'):
        Node.__init__(self,props['width'],props['height'],props['x'],props['y'],props['view_width'],\
                        props['view_height'],props['view_x'],props['view_y'],props['name'],\
                        props['uid'],props['parent'],type,props['x_offset'],props['y_offset'])
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
        left_rect= rect1  if rect1.top<= rect2.top else rect2
        right_rect= rect2 if left_rect==rect1 else rect1    
        return right_rect.top-left_rect.bottom


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
    def get_orientation(rects):
        """
        orientation won't work if there is only one block 
        we looking for row as well as column intersection 
    
        """
        
        if len(rects)<=1:
            return RECT_INTERSECT.ROW  

        row=Rectange.is_valid_orientation(rects,Rectange.is_row_intersection)
        col=Rectange.is_valid_orientation(rects,Rectange.is_col_intersection)
        if row and col:
            return RECT_INTERSECT.BOTH
        if row or col:
            return RECT_INTERSECT.ROW if row else RECT_INTERSECT.COLUMN
        return RECT_INTERSECT.NONE

           

    def abs_diff(self,other):
        return abs(self.left-other.left)+abs(self.right-other.right)

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

