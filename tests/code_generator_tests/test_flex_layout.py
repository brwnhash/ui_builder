
from .common import get_fake_box_props,get_var_boxes

from helpers import Rectangle
from code_generator import GroupBoxes,FlexLayoutGenerator1D,FlexLayoutGenerator2D
    


def get_col_boxes():
    box1=get_fake_box_props('1',10,10,40,40)
    box2=get_fake_box_props('2',10,60,40,40) #at offset of 10
    box3=get_fake_box_props('3',10,110,40,40)
    return box1,box2,box3

def get_row_boxes():
    box1=get_fake_box_props('1',10,10,40,40)
    box2=get_fake_box_props('2',60,10,40,40) #at offset of 10
    box3=get_fake_box_props('3',110,10,40,40)
    return box1,box2,box3

def get_non_sym_row_boxes():
    box1=get_fake_box_props('1',10,10,40,40)
    box2=get_fake_box_props('2',60,20,40,40) #at offset of 10
    box3=get_fake_box_props('3',110,30,40,40)
    return box1,box2,box3    

def get_partial_col_overlap():
    box1=get_fake_box_props('1',10,10,40,40)
    box2=get_fake_box_props('2',30,60,40,40) #at offset of 10
    box3=get_fake_box_props('3',40,110,40,40)
    return box1,box2,box3       

def get_2d_perfect_overlap_col():
    bb=[]
    bb.append(get_fake_box_props('1',10,10,40,40))
    bb.append(get_fake_box_props('2',10,60,40,40)) #at offset of 10
    bb.append(get_fake_box_props('3',10,110,40,40))
    bb.append(get_fake_box_props('4',60,10,40,40))
    bb.append(get_fake_box_props('5',60,60,40,40))#at offset of 10
    bb.append(get_fake_box_props('6',60,110,40,40))
    x,y=bb[0]['x']-10,bb[0]['y']-10
    max_wt=max(bb,lambda v:v['width'])
    max_ht=max(bb,lambda v:v['height'])
    wt,ht=max_wt+10,max_ht+10
    pp=get_fake_box_props('0',x,y,wt,ht)
    return bb,pp

def get_2d_perfect_overlap_row():
    bb=[]
    
    bb.append(get_fake_box_props('1',10,10,40,40))
    bb.append(get_fake_box_props('2',10,60,40,40)) #at offset of 10
    bb.append(get_fake_box_props('3',60,10,40,40))
    bb.append(get_fake_box_props('4',60,60,40,40))
    bb.append(get_fake_box_props('5',110,10,40,40))#at offset of 10
    bb.append(get_fake_box_props('6',110,60,40,40))

    min_wt_rect=min(bb,key=lambda v:v['x'])
    min_ht_rect=min(bb,key=lambda v:v['y'])
    x,y=min_wt_rect['x']-10,min_ht_rect['y']-10

    max_wt_rect=max(bb,key=lambda v:v['x'])
    max_ht_rect=max(bb,key=lambda v:v['y'])
    wt=max_wt_rect['x']+max_wt_rect['width']+10
    ht=max_ht_rect['y']+max_ht_rect['height']+10
    pp=get_fake_box_props('0',x,y,wt,ht)
    return bb,pp

def get_2d_partial_overlap1():
    bb=[]
    bb.append(get_fake_box_props('1',10,10,40,40))
    bb.append(get_fake_box_props('2',60,20,40,40)) #at offset of 10
    bb.append(get_fake_box_props('3',110,15,40,40))
    bb.append(get_fake_box_props('4',10,60,40,40))
    bb.append(get_fake_box_props('5',60,70,40,40))#at offset of 10
    bb.append(get_fake_box_props('6',110,65,40,40))
    return bb

def get_2d_non_overlap():
    bb=[]
    bb.append(get_fake_box_props('1',10,10,40,40))
    bb.append(get_fake_box_props('2',60,60,40,40)) #at offset of 10
    bb.append(get_fake_box_props('3',110,115,40,40))
    return bb



def test_flex_justification():
    
    boxes=get_var_boxes(4,direction=0)
    fl=FlexLayoutGenerator1D(boxes,0)
    fl._get_justification()
    

def test_flex_layout_generator():
    #boxes=get_var_boxes(4,direction=0)
    box_list,pp=get_2d_perfect_overlap_row()
    parent=Rectangle(pp)
    rect_list=[Rectangle(bb,parent) for bb in box_list]
    fl=FlexLayoutGenerator2D()
    fl.detectPatterns(rect_list)

def symmetric_2d_row_col_boxes_check():

    #box_lil=[get_2d_perfect_overlap_col(),get_2d_partial_overlap1(),get_2d_non_overlap(),get_2d_perfect_overlap_row()]
    box_lil=[get_2d_perfect_overlap_col()]
    for idx,box_list in enumerate(box_lil):
        rect_list=[Rectangle(bb) for bb in box_list]
        gb=GroupBoxes(rect_list)
        grps=gb.group()
        print( f'idx is {idx}')
        for grp_id,rects in grps.items():
            names=[(rect.name,orn) for rect,orn in rects]
            print(f'nid  {grp_id}  rect names ',names)
               
    

def test_box_groupings():
    from code_generator.flex_grid_layout_parser import GroupBoxes
    from helpers.nodes import Rectangle
    #test 1 equal 

    rect=Rectangle()

def symmetric_1d_row_col_boxes_check():
    from code_generator.flex_grid_layout_parser import GroupBoxes
    from helpers.nodes import Rectangle
    #col boxes
    #box_list=[get_row_boxes(),get_col_boxes(),get_non_sym_row_boxes(),get_partial_col_overlap()]
    box_list=[get_non_sym_row_boxes()]
    for idx,(box1,box2,box3) in enumerate(box_list):
        bb1=Rectangle(box1)
        bb2=Rectangle(box2)
        bb3=Rectangle(box3)
        gb=GroupBoxes([bb1,bb2,bb3])
        node_list=gb.getNearestElementInRowColumn()
        print( f'idx is {idx}')
        for node in node_list:
            print(f'nid {node.uid} row_idx {node.row_grp_idx} and col_idx {node.col_grp_idx} row wt {node.row_edge_wt} and col wt {node.col_edge_wt}')
