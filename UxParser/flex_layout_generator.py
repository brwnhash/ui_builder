import math
from nodes import Rectange

def getRowWeight(rect1,rect2):
    return 1-(math.abs(rect1.top-rect2.top)/min([rect1.height,rect2.height]))

def getColumnWeight(rect1,rect2):
    return 1-(math.abs(rect1.left-rect2.left)/min([rect1.width,rect2.width]))

class FNode():
    def __init__(self,next_row_node,next_col_node,row_edge_wt,col_edge_wt,row_idx,col_idx):
        self.next_row_node=next_row_node
        self.next_col_node=next_col_node
        self.row_edge_wt=row_edge_wt
        self.col_edge_wt=col_edge_wt
        self.row_idx=row_idx 
        self.col_idx=col_idx 
        

class GroupBoxes():
    def __init__(self,rects):
        self.rects=rects
        self.last_row_cluster_id=0
        self.last_col_cluster_id=0
        self.row_cluster_map={}
        self.col_cluster_map={}

     
    def getClusterId(self,idx,cmap,last_id):
        if(cmap.get(idx,-1)==-1):
            curr_id=last_id+1
            cmap[idx]=last_id
        else:
            curr_id=cmap[idx]
        return curr_id
        
    def getRowClusterId(self,row_idx):
        self.last_row_cluster_id= self.getClusterId(row_idx,self.row_cluster_map,self.last_row_cluster_id)
        return self.last_row_cluster_id

        
    def getColumnClusterId(self,col_idx):
        self.last_col_cluster_id= self.getClusterId(col_idx,self.col_cluster_map,self.last_col_cluster_id)
        return self.last_col_cluster_id

    def assignRowColIdxs(self,rw_idx,rw_id,col_idx,cl_id):
        self.row_cluster_map[rw_idx]=rw_id
        self.col_cluster_map[col_idx]=cl_id

    def getNearestElementInRowColumn(self):
        """
        use sorted rects by absolute position 
        for a box check forward in row and column directions what is nearest element.
        """
        node_list=[]
        rects=sorted(self.rects, key=lambda rect: ((rect.top*rect.width)+rect.left))
        total_rects=len(rects)
        for idx in range(total_rects-1):
            rect=rects[idx]

            nearest_row_idx,nearest_col_idx=-1,-1
            best_x_diff,best_y_diff=1e5,1e5

            for c_idx,rect1 in enumerate(rects[idx+1:]):
                if Rectange.is_row_intersection(rect,rect1):
                    diff=Rectange.get_x_diff(rect,rect1)
                    if diff<best_x_diff:
                        best_x_diff=diff
                        nearest_row_idx=idx+1+c_idx
                if Rectange.is_col_intersection(rect,rect1):
                    diff=Rectange.get_y_diff(rect,rect1)
                    if diff<best_y_diff:
                        best_y_diff=diff
                        nearest_col_idx=idx+1+c_idx

            rw_id,cl_id=-1,-1
            row_wt,col_wt=-1,-1
            if nearest_row_idx!=-1:
                rw_id=self.getRowClusterId(idx)
                row_wt=getRowWeight(rect,rects[nearest_row_idx])
            if nearest_col_idx!=-1:
                cl_id=self.getColumnClusterId(idx)
                col_wt=getColumnWeight(rect,rects[nearest_col_idx])

            nd=FNode(nearest_row_idx,nearest_col_idx,row_wt,col_wt,rw_id,cl_id)
            self.assignRowColIdxs(nearest_row_idx,nearest_col_idx,rw_id,cl_id)
            node_list.append(nd)

        return node_list
            


class FlexLayoutGenerator():
    def __init__(self,rects):
        """
        
        """
        self.rects=[rect for rect in rects if rect.name]
        self.parent_rect=rects[0].parent
        self.orientation=None
        self.margin=''
        self.justification,self.flex_flow,self.alignment,self.flex_property_list=None,None,None,None

    def update_orientation(self):
        for rect in self.rects:
            rect.direction=self.orientation

    def find_row_col_groups(self,rects,variation=0.2):
        """
        find row and column groups, whats the best way to generate grouping.
        calculate for every node row and col group score .
        """


        pass

    def _get_alignment(self):
        """
        alignement is done on vertical axis (by using direction u can move)
        strecth,flex_start,flex_end,center
        """
        rects=self.rects
        min_rect=min(rects, key=lambda rect: rect.area)
        top_margin=(min_rect.top_dir(self.orientation)-self.parent_rect.top_dir(self.orientation))/self.parent_rect.height_dir(self.orientation)
        bottom_margin=(self.parent_rect.bottom_dir(self.orientation) - min_rect.bottom_dir(self.orientation))/self.parent_rect.height_dir(self.orientation)
        top_margin_bigger=True if top_margin>bottom_margin else False
        div= top_margin/bottom_margin  if top_margin_bigger else bottom_margin/top_margin

        #if top and bottom both have less than 10%margin its mostly 
        # biggest margin / smaller margin if greater than 2 its not centered
        if top_margin<=0 and bottom_margin<=0:
            alignment='stretch' 
        else:
            if div<=2:
                alignment='center'
            else:
                if top_margin_bigger:
                    alignment='flex-end'
                else:
                    alignment='flex-start'
        return alignment

    def _get_rect_margins(self,parent_rect,rects,orientation):       
        idx=1
        all_rects=[parent_rect]
        all_rects.extend(rects)
        last_idx=len(all_rects)-1
        right_margin,left_margin,top_margin,bottom_margin=0,0,0,0
        for rect in all_rects[1:]:
            left_rect=all_rects[idx-1]
            if orientation==ROW: #for row orientation
                if idx==1:
                    left_margin=rect.left-left_rect.left  # first diff w.r.t parent
                else:
                    left_margin=rect.left-left_rect.right #rest diff are within 
                top_margin=rect.top-parent_rect.top
                #right margin only for last rectangle...
                if idx==last_idx:
                    right_margin=parent_rect.right-rect.right

            else:  #for col orientation.
                left_margin=rect.left-parent_rect.left
                if idx==1:
                    top_margin=rect.top-parent_rect.top 
                else:
                    top_margin=rect.top-left_rect.bottom
                if idx==last_idx:
                   bottom_margin=parent_rect.bottom-rect.bottom

            rect.margin['left']=left_margin
            rect.margin['top']=top_margin
            rect.margin['right']=right_margin 
            rect.margin['bottom']=bottom_margin            
            idx+=1
        
        
      
    def _get_justification(self):
        """
        justificaiton: flex-start,flex-end,center,space-around,space-between,space-evenly
        """
        justification=''
        margin=''
        rects=self.rects
        #left to right sorted rects
        sorted_rects = sorted(rects, key=lambda rect: rect.left) if self.orientation==ROW else sorted(rects,key=lambda rect: rect.top)
        #self.rects=sorted_rects
        self._get_rect_margins(self.parent_rect,sorted_rects,self.orientation)
        #primary rect to first distance
        first_rect=sorted_rects[0]
        parent_rect=self.parent_rect
        second_rect=sorted_rects[1]  if len(sorted_rects)>1 else first_rect
        second_last_rect=sorted_rects[len(rects)-2] if len(sorted_rects)>1 else first_rect
        last_rect=sorted_rects[len(rects)-1]
        left_margin=first_rect.left_dir(self.orientation)-parent_rect.left_dir(self.orientation)
        right_margin=parent_rect.right_dir(self.orientation)-last_rect.right_dir(self.orientation)
        middle_margin=second_rect.left_dir(self.orientation)-first_rect.right_dir(self.orientation)
        second_last_margin=last_rect.left_dir(self.orientation)-second_last_rect.right_dir(self.orientation)
        #detect flex-start and end

        #lr_margin_diff=math.fabs(left_margin-right_margin)/(min([left_margin,right_margin]))
        #fs_margin_diff=math.fabs(left_margin-middle_margin)/(min([left_margin,middle_margin]))
        #middle_margins_diff=math.fabs(middle_margin-second_last_margin)/(min([second_last_margin,middle_margin]))
        lr_margin_diff=max([left_margin,right_margin])/(min([left_margin,right_margin]))
        if len(sorted_rects)>=2:
            min_val=min([left_margin,middle_margin])
            fs_margin_diff=0 if min_val==0 else max([left_margin,middle_margin])/min_val
        else:
            fs_margin_diff=-1
        if len(sorted_rects)>=3:
            min_val=min([second_last_margin,middle_margin])
            middle_margins_diff=0 if min_val==0 else max([middle_margin,second_last_margin])/min_val
        else:
            middle_margins_diff=-1
        #left right distance is greater than 3 or only one box present
        if lr_margin_diff>JUST_START_END_MIN_SCALE:           
            justification= 'flex-end' if left_margin> right_margin else 'flex-start'
            print('justification is '+str(justification))
            return justification,'1'
        #left right distance is less than 1.5 or almost equal condition this is
        if lr_margin_diff<=JUST_SPACE_AROUND_MIN_SCALE: #almost equal    
            #first and second diff almost equal                         
            if fs_margin_diff!=-1 and fs_margin_diff<=JUST_SPACE_AROUND_MIN_SCALE: 
                justification='space-evenly'
                print('justification is '+str(justification))
                
            #middle margins should be almost equal and first second margin diff should be almost double
            #first second differnce between 1.5 to 3 
            elif (fs_margin_diff>=JUST_SPACE_AROUND_MIN_SCALE and fs_margin_diff <=JUST_SPACE_AROUND_MAX_SCALE):
                 if left_margin<middle_margin:
                     justification='space-around'
                     print('justification is '+str(justification))
        #middle margins are equal and (Quite big diff first and second
        #left marign smaller space between else center)
        if not justification:
            if middle_margins_diff<=JUST_CENTER_MAX_SCALE:
                if left_margin<middle_margin:
                    justification='space-between'
                else:
                    justification='center'
        if not justification:
            print('using default justification')
            justification,margin='flex-start','1'
        return justification,margin

    def __detect_flex_direction(self):
        """
        direction:rect with bigger side is direction. 
        for keeping things simple row col reverse not supported
        wrap: not a good idea to support wrap if we want to do automatic formatting.
        """
        return PRectange.is_1D_orientation(self.rects[0],rect[len(self.rects)-1])
    
  
    def _get_flex_property(self):
        """
        grow,shrink,flex_basis
        only grow property is calcualted rest is default
        in direction of alignment only we will check how big one entry w.r.t other
        """
        property_list={}
        var_rects=self.rects
        #var_rects=[rect for rect in self.rects if not rect.is_static() ]
        #change it dicection is on all rect intesection which side....
        min_rect=min(var_rects,key=lambda rect:rect.width) if var_rects else 1
        for rect in self.rects:
            if rect.is_static():
                property_list[rect.name]=('0','1','auto')
            else:
                grow=rect.width/min_rect.width
                grow=int(grow+0.5)
                property_list[rect.name]=(str(grow),'1','auto')
        return property_list
        
        
    def _get_flex_flow(self):
        self.orientation=PRectange.is_1D_orientation(self.rects)
        self.update_orientation()
        return 'row nowrap' if self.orientation==ROW else 'column nowrap'
     
         
    def detect_patterns(self):
        """
        sketch_rect: rect drawn by sketches..
        """
        self.flex_flow=self._get_flex_flow()
        self.flex_property_list=self._get_flex_property()
        self.justification,self.margin=self._get_justification()
        self.alignment=self._get_alignment()

    def _get_margin_css(self):
        """
        margins are w.r.t width if u take % ,why it makes sense if its w.r.t width and height
        respectively ,u will see unequal size when u use short hands for margin ,for all margins
        
        """
        margin_props_list=[]
        for rect in self.rects:
            margin=[]
            if self.orientation==ROW:   
                if self.justification in ['flex-start','flex-end','center','space-between','space-around']:
                    m_l=round((rect.margin['left']*100),2)
                    margin.append('margin-left:'+str(m_l)+'vw')
                if self.alignment in ['flex-start','flex-end','space-around','space-evenly']:
                    m_l=round((rect.margin['top']*100),2)
                    margin.append('margin-top:'+str(m_l)+'vh') 
                if self.justification not in ['space-evenly']:
                    if rect.margin['right']!=0:
                       m_l=round((rect.margin['right']*100),2)
                       margin.append('margin-right:'+str(m_l)+'vw') 
               
            else:
                if self.justification in ['flex-start','flex-end','center','space-between']:
                    m_l=round((rect.margin['top']*100),2)
                    margin.append('margin-top:'+str(m_l)+'vh')
                if self.alignment in ['flex-start','flex-end']:
                    m_l=round((rect.margin['left']*100),2)
                    margin.append('margin-left:'+str(m_l)+'vw')
                    if rect.margin['right']!=0:
                        m_l=round((rect.margin['right']*100),2)
                        margin.append('margin-right:'+str(m_l)+'vw')
                if rect.margin['bottom']!=0:
                    m_l=round((rect.margin['bottom']*100),2) 
                    margin.append('margin-bottom:'+str(m_l)+'vh')    
                
            margin_str=";\n".join(margin)
            margin_prop='.{class_name}{{\n {margin_str} \n}}'.format(class_name=rect.name,margin_str=margin_str)
            margin_props_list.append(margin_prop)
        return "\n ".join(margin_props_list)

    def to_css(self,lvl):
        container=".{class_name}{{\n\
        display:flex; \n\
        flex-flow:{flex_flow};\n\
        justify-content:{justification};\n \
        align-items:{alignment};\n\
        }}".format(class_name=self.parent_rect.name,flex_flow=self.flex_flow \
                        ,justification=self.justification,alignment=self.alignment)
  
        rect_props={}
        for rect in self.rects:
            rect_props[rect.name]=rect
        class_prop_list=[] 
        scale_width,scale_height=1,1
        #if lvl:
        #    #scale_width= 1/self.parent_rect.width
        #    #scale_height=1/self.parent_rect.height
        #    scale_width= 1/vw
        #    scale_height=1/vh
        
        margins=self._get_margin_css()
        color=DEFAULT_COLOR_LVL[lvl+1]
        for name,flex_prop in self.flex_property_list.items():
            if ENABLE_OUTLINE_BORDER:
                class_prop=".{class_name}{{border: 1px solid green;flex: {flex_prop};width:{width}vw;height:{height}vh}}".format(class_name=name,width=round((rect_props[name].width*scale_width*100),2),height=round((rect_props[name].height*scale_height*100),2),flex_prop=" ".join(flex_prop))
            else:
                class_prop=".{class_name}{{flex: {flex_prop};width:{width}vw;height:{height}vh}}".format(class_name=name,width=round((rect_props[name].width*scale_width*100),2),height=round((rect_props[name].height*scale_height*100),2),flex_prop=" ".join(flex_prop))                
            class_prop_list.append(class_prop)
        child_props="\n ".join(class_prop_list)
        child_css=container+'\n'+'\n'+child_props+'\n'+margins
        return child_css