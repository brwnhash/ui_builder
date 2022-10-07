
from .common import get_fake_box_props
from helpers import Rectangle

def get_2d_grid_div1():
    parent=Rectangle(get_fake_box_props('0',0,0,340,140))
    
    bb=[]
    bb.append(Rectangle(get_fake_box_props('1',10,10,40,40,parent=parent)))
    bb.append(Rectangle(get_fake_box_props('2',60,60,80,40,parent=parent))) #at offset of 10
    bb.append(Rectangle(get_fake_box_props('3',160,70,160,40,parent=parent)))
    return bb

def test_css_grid():
    from UxParser import GridCreator
    rect_list=get_2d_grid_div1()
    gc=GridCreator()
    gc.extractGridProps(rect_list)
