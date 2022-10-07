from helpers import Rectangle

def get_fake_box_props(name,x,y,width,height,view_x=None,view_y=None,view_width=None,view_height=None,parent=None):
    import random
    view_x= view_x   if view_x else x
    view_y=view_y if view_y else y
    view_width=view_width if view_width else width
    view_height=view_height if view_height else height
    props={'width':width,'height':height,'x':x,'y':y,
            'name':name,'uid':name,'parent':parent,
            'view_x':view_x,'view_y':view_y,
            'x_offset':0,'y_offset':0,'view_width':view_width,'view_height':view_height}
    return props



def get_var_boxes(num,wt=40,ht=40,st_margin=10,end_margin=10,mid_margin=10,dev=0,direction=0):
    """
    direction : 0 for row boxes ,1 for column boxes
    st and end margin is for x and y same

    """
    bb_list=[]
    parent=None
    x,y=st_margin,st_margin
    parent_width,parent_height=0,0
    if direction==0:
        parent_width=(wt*num)+(st_margin+end_margin)+(num-1)*mid_margin
        parent_height=(ht*num)+(st_margin+end_margin)
    else:
        parent_width=(wt*num)+(st_margin+end_margin)
        parent_height=(ht*num)+(st_margin+end_margin)+(num-1)*mid_margin

    prop=get_fake_box_props('prnt',0,0,parent_width,parent_height)
    parent=Rectangle(prop)
    for i in range(num):
        bb=get_fake_box_props(str(i+1),x,y,wt,ht)
        bb['parent']=parent
        bb_list.append(Rectangle(bb))
        if direction==0:
            x+=(wt+mid_margin)
        
        else:
            y+=(ht+mid_margin)
    return bb_list

   