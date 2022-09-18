from re import L
from xml.dom.expatbuilder import parseString
from .nodes import Rectangle,RECT_INTERSECT
from collections import defaultdict
import numpy as np
from config import FLEX_CONIG
from .common import DictVect
import math

def getRowWeight(rect1,rect2):
    return 1-(abs(rect1.top-rect2.top)/min([rect1.height,rect2.height]))

def getColumnWeight(rect1,rect2):
    """
    to give more weight to column assignments we subtract 0.05 from there
    """
    return 1-(abs(rect1.left-rect2.left)/min([rect1.width,rect2.width]))

class FNode():
    def __init__(self,uid,next_row_node,next_col_node,row_edge_wt,col_edge_wt,row_idx,col_idx):
        self.uid=uid
        self.nearest_row_node=next_row_node
        self.nearest_col_node=next_col_node
        self.row_edge_wt=row_edge_wt
        self.col_edge_wt=col_edge_wt
        self.row_grp_idx=row_idx 
        self.col_grp_idx=col_idx 



class GroupBoxes():
    ROW_COL=0
    ROW_ONLY=1
    COL_ONLY=2  
    def __init__(self,rects,grouping_type=ROW_COL,row_extra_wt=0.05,col_extra_wt=0):
        self.rects=rects
        self.grouping_type=grouping_type
        self.row_extra_wt=row_extra_wt
        self.col_extra_wt=col_extra_wt
        self.last_row_cluster_id=-1
        self.last_col_cluster_id=-1
        self.row_cluster_map={}
        self.col_cluster_map={}
        
    def groupElements(self,node_id_map):
        grps=defaultdict(list)
        for rect in self.rects:
            grp_id,orientation=node_id_map[rect.uid]
            grps[grp_id].append((rect,orientation))
        return grps


     
    def getClusterId(self,idx,nidx,cmap,last_id):
        curr_id= min([cmap.get(idx,1e6),cmap.get(nidx,1e6),last_id+1])
        cmap[idx]=curr_id
        cmap[nidx]=curr_id
        return curr_id

    def getRowClusterId(self,row_idx,nearest_idx):
        self.last_row_cluster_id= self.getClusterId(row_idx,nearest_idx,self.row_cluster_map,self.last_row_cluster_id)
        return self.last_row_cluster_id

        
    def getColumnClusterId(self,col_idx,nearest_idx):
        self.last_col_cluster_id= self.getClusterId(col_idx,nearest_idx,self.col_cluster_map,self.last_col_cluster_id)
        return self.last_col_cluster_id

    def assignRowColIdxs(self,node_list):
        row_grp_wts,col_grp_wts={},{}
        row_grp_cnt,col_grp_cnt={},{}
        for node in node_list:
            row_grp_wts[node.row_grp_idx]=row_grp_wts.get(node.row_grp_idx,0)+node.row_edge_wt
            row_grp_cnt[node.row_grp_idx]=row_grp_cnt.get(node.row_grp_idx,0)+1
            col_grp_wts[node.col_grp_idx]=col_grp_wts.get(node.col_grp_idx,0)+node.col_edge_wt
            col_grp_cnt[node.col_grp_idx]=col_grp_cnt.get(node.col_grp_idx,0)+1

        #assign more weight to bigger group..
        node_uid_map={}
        for node in node_list:
            rw_grp_idx,col_grp_idx=node.row_grp_idx,node.col_grp_idx
            if rw_grp_idx==-1 and col_grp_idx==-1:
                continue
            max_cnt=max(row_grp_cnt[rw_grp_idx],col_grp_cnt[col_grp_idx])
            rval=(row_grp_wts[rw_grp_idx]/row_grp_cnt[rw_grp_idx])+0.3*(row_grp_cnt[rw_grp_idx]/max_cnt)
            cval=col_grp_wts[col_grp_idx]/col_grp_cnt[col_grp_idx]+0.3*(col_grp_cnt[col_grp_idx]/max_cnt)
            # invalidate row or col grp values
            rval+=self.row_extra_wt
            cval+=self.col_extra_wt
            if rval>cval:
                node.col_grp_idx=-1
                node_uid_map[node.uid]=(node.row_grp_idx,RECT_INTERSECT.ROW)
            else:
                node.row_grp_idx=-1
                node_uid_map[node.uid]=(node.col_grp_idx,RECT_INTERSECT.COL)
            
        return node_uid_map



    def getNearestElementInRowColumn(self):
        """
        use sorted rects by absolute position 
        for a box check forward in row and column directions what is nearest element.

        """
        node_list=[]
        rects=sorted(self.rects, key=lambda rect: ((rect.top*rect.width)+rect.left))
        total_rects=len(rects)
        for idx in range(total_rects):
            rect=rects[idx]

            nearest_row_idx,nearest_col_idx=-1,-1
            best_x_diff,best_y_diff=1e5,1e5

            for c_idx,rect1 in enumerate(rects):
                if idx==c_idx:
                    continue

                if (self.grouping_type!=GroupBoxes.COL_ONLY) and (Rectangle.is_row_intersection(rect,rect1)):
                    diff=Rectangle.get_x_diff(rect,rect1)
                    if diff<best_x_diff:
                        best_x_diff=diff
                        nearest_row_idx=c_idx

                if (self.grouping_type!=GroupBoxes.ROW_ONLY) and (Rectangle.is_col_intersection(rect,rect1)):
                    diff=Rectangle.get_y_diff(rect,rect1)
                    if diff<best_y_diff:
                        best_y_diff=diff
                        nearest_col_idx=c_idx

            rw_id,cl_id=-1,-1
            row_wt,col_wt=-1,-1
            if nearest_row_idx!=-1:
                rw_id=self.getRowClusterId(idx,nearest_row_idx)
                row_wt=getRowWeight(rect,rects[nearest_row_idx])
            if nearest_col_idx!=-1:
                cl_id=self.getColumnClusterId(idx,nearest_col_idx)
                col_wt=getColumnWeight(rect,rects[nearest_col_idx])

            nd=FNode(rect.uid,nearest_row_idx,nearest_col_idx,row_wt,col_wt,rw_id,cl_id)
            node_list.append(nd)

        node_uid_map=self.assignRowColIdxs(node_list)

        return node_list,node_uid_map

    def group(self):
        node_list,uid_map=self.getNearestElementInRowColumn()
        grps=self.groupElements(uid_map)
        return grps






class FlexLayoutGenerator():
    def __init__(self,rects,orientation):
        """
        It deals with 1D layout only . nowrap property is set..
        """
        self.rects=[rect for rect in rects if rect.name]
        self.parent_rect=rects[0].parent
        self.orientation=orientation
        self.margin=''
        self.justification,self.flex_flow,self.alignment,self.flex_property_list=None,None,None,None
        self._initialize()

    def _initialize(self):
        self.justification_model= DictVect(['lr','mid','lmid','rmid','mid2l','mid2r'],[1,1,1,1,2,2])
        #consider lr,lmid,rmid order
        train_feature_list=[
            ([1,0,0,0,0,0],'center'),
            ([0,1,0,0,0,0],'space_between'),
            ([1,1,0,0,1,1],'space_around'),
            ([1,1,1,1,0,0],'space_even')
        ]

        self.justification_model.train(train_feature_list)

    def getAlignment(self):
        """
        alignement is done on vertical axis (by using direction u can move)
        stretch,flex_start,flex_end,center
        """
        rects=self.rects
        rect_props=[]
        for rect in self.rects:
            top_margin=(rect.top_dir(self.orientation)-self.parent_rect.top_dir(self.orientation))/self.parent_rect.height_dir(self.orientation)
            bottom_margin=(self.parent_rect.bottom_dir(self.orientation) - rect.bottom_dir(self.orientation))/self.parent_rect.height_dir(self.orientation)
            top_margin_bigger=True if top_margin>bottom_margin else False
            div= top_margin/bottom_margin  if top_margin_bigger else bottom_margin/top_margin
            alignment='flex-start'
            if top_margin<=0 and bottom_margin<=0:
                alignment='stretch' 
            else:
                if div>=1-FLEX_CONIG.margin_dev and div<=1+FLEX_CONIG.margin_dev:
                    alignment='center'
                else:
                    if top_margin_bigger:
                        alignment='flex-end'
                    else:
                        alignment='flex-start'
            rect_props.append(alignment)
        all_same_prop=True
        for prop in rect_props[1:]:
            if rect_props[0]!=prop:
                all_same_prop=False
        if all_same_prop:
            self.parent_rect.addChildProps({'alignment':alignment},'flex')
        else:
            for rect in self.rects:
                rect.addOwnProps({'alignment':alignment},'flex')
        
        
           

    def _get_rect_margins(self,parent_rect,rects,orientation): 
        """
        margin of rect from left and right
        we push parent in list as well to have conistent loop and loop starts from first item
        """

        idx=1
        all_rects=[parent_rect]
        all_rects.extend(rects)
        last_idx=len(all_rects)-1
        right_margin,left_margin,top_margin,bottom_margin=0,0,0,0
        for rect in all_rects[1:]:
            left_rect=all_rects[idx-1]
            if orientation==RECT_INTERSECT.ROW: #for row orientation
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
            rect.addOwnProps({'left':left_margin,'top':top_margin,'right':right_margin,'bottom':bottom_margin},'margin')         
            idx+=1
        

    def _middleElmMargins(self,rects):
        if len(rects)<2:
            return False,-1
        size=len(rects)
        diff_list=[]
        for idx in range(1,size-1):
            left_rect=rects[idx-1]
            right_rect=rects[idx]
            middle_margin=right_rect.left_dir(self.orientation)-left_rect.right_dir(self.orientation)
            diff_list.append(middle_margin)
        norm_diff=np.array(diff_list)/np.max(diff_list)
        val=np.std(norm_diff)
        if val<FLEX_CONIG['margin_dev']:
            return True,float(np.mean(diff_list))
        return False,-1

    def _getMarginDiff(self,left,right):
        return max([left,right])/(min([left,right]))

    def getJustification(self):
        """
        its justify content
        justificaiton: flex-start,flex-end,center,space-around,space-between,space-evenly

        justify content wont work if grow property set as all space already taken
        ---
        left,right and middle margins are needed to find property

        """

        rects=self.rects
        #left to right sorted rects
        sorted_rects = sorted(rects, key=lambda rect: rect.left) if self.orientation==RECT_INTERSECT.ROW else sorted(rects,key=lambda rect: rect.top)
  
        self._get_rect_margins(self.parent_rect,sorted_rects,self.orientation)
        #primary rect to first distance
        first_rect=sorted_rects[0]
        parent_rect=self.parent_rect
        last_rect=sorted_rects[len(rects)-1]

        left_margin=first_rect.left_dir(self.orientation)-parent_rect.left_dir(self.orientation)
        right_margin=parent_rect.right_dir(self.orientation)-last_rect.right_dir(self.orientation)
        mid_valid,middle_margin=self._middleElmMargins(sorted_rects)

        
        lr_margin_diff=self._getMarginDiff(left_margin,right_margin)
        lmid_margin_diff=self._getMarginDiff(left_margin,middle_margin)
        rmid_margin_diff=self._getMarginDiff(middle_margin,right_margin)

        mid2l=lmid_margin_diff
        mid2r=rmid_margin_diff
        

        feature={'mid2l':mid2l,'mid2r':mid2r,'lr':lr_margin_diff,'mid':mid_valid,'lmid':lmid_margin_diff,'rmid':rmid_margin_diff}
        justification,score=self.justification_model.predict(feature)
        if score>0.9:
            parent_rect.addChildFlexProps({'justification':justification},'flex')
        else:
            print(f'justification score is less for {parent_rect.name} ',score)
        return justification


  
    def getFlexProperty(self):
        """
        grow,shrink,flex_basis
        grow shrink works only in main axis.
        assumption:
        grow shrink with margins can define whole flex box we dont even need any other property

        """
        property_list={}
        min_rect=min(self.rects,key=lambda rect:rect.width) if self.rects else 1
        for rect in self.rects:
            grow=rect.width_dir(self.orientation)/min_rect.width_dir(self.orientation)
            grow=round(grow,3)
            # we kept both same for default properties..
            rect.addOwnProps({'grow':grow,'shrink':grow},'flex')
            property_list[rect.name]={'grow':grow}
        return property_list
              
    def detect_patterns(self):
        """
        sketch_rect: rect drawn by sketches..
        """
        self.flex_property_list=self.getFlexProperty()
        self.justification,self.margin=self.getJustification()
        self.alignment=self.getAlignment()

class GridCreator():
    """
    By default we divide rows and columns to 12 grid layout.
    """
    def __init__(self):
        self.css_blocks=[]
        self.html_block=''
        self.container='container'

    def add_container(self,name,default_height=True,default_frame=True):
        if default_height:
            block=".{class_name} {{ display: grid;\n \
                   grid-template-columns:repeat({row_div}, 1fr);\n \
                   grid-template-rows:repeat({col_div}, 1fr);\n\
                   height:calc(100vh - 17px);\
                    }}"\
                   .format(class_name=name,row_div=int(css_grid_props['num_rows']),col_div=int(css_grid_props['num_cols']))
        else:
           block=".{class_name} {{ display: grid;\n \
                   grid-template-columns:repeat({row_div}, 1fr);\n \
                   grid-template-rows:repeat({col_div}, 1fr);\
                    }}"\
                   .format(class_name=name,row_div=int(css_grid_props['num_rows']),col_div=int(css_grid_props['num_cols']))
        if ENABLE_OUTLINE_BORDER:
            frame="\n.{class_name}{{border : 1px solid blue }}\n.{class_name} > * {{border : 1px solid red }}\n".format(class_name=name) 
            block=frame+block
        self.css_blocks.append(block)
        self.container=name


    def _build_item_css(self,item):
        block=".{class_name}{{grid-column-start: {col_start};\n \
                grid-column-end: {col_end};\n \
                grid-row-start: {row_start};\n \
                grid-row-end: {row_end};}}\
              ".format(class_name=item.name,col_start=math.ceil(item.col_start),col_end=math.ceil(item.col_end),\
                        row_start=math.ceil(item.row_start),row_end=math.ceil(item.row_end))
        return block


    def add_items_to_grid(self,items_list):
        for item in items_list:
            if not item.name:
                continue
            block=self._build_item_css(item)
            self.css_blocks.append(block)
        html_block=create_html_div_layout(items_list)
        self.html_block= add_css_class_to_div(self.container,html_block)

    @property       
    def css(self):
        return " \r\n".join(self.css_blocks)

    @property
    def html(self):
        return self.html_block
                        


class GridCreator():
    def __init__(self):
        self.row_div=0
        self.col_div=0

    def getElmProps(self,rect):
        """
        row start move to left floor  ; row end move to ceil
        indexing starts from 1 so add 1 to final results.
        """
        rnd=lambda val:int(math.floor(1+val))
        rel_rect=rect.getRelativeNode()
        col_start=rnd(rel_rect.left/self.col_div)
        row_start=rnd(rel_rect.top/self.row_div)
        col_span=rnd((rel_rect.left+rel_rect.width)/self.col_div)
        row_span=rnd((rel_rect.top+rel_rect.height)/self.row_div)
        
        return {'grid-row-start':row_start,'grid-row-end':row_span,'grid-column-start':col_start,'grid-column-end':col_span}

    def getBestMatch(self,min_val,targets,max_error=2):
        best_match,min_err=1,1e5
        for i in range(min_val,101,1):
            err_list=[]
            for target in targets:              
                err_list.append(target%i)
            err=max(err_list)
            if err<min_err:
                min_err=err
                best_match=i
            if min_err==0:
                break
        if min_err<max_error:
            best_match=-1 
        return best_match


    def calculateNumRowsCols(self,rects):
        """
        calculate biggest size with 0 error and minimum with in desired limit.
        we assume grid design and minimum grid 1
        """
        min_wt=min(rects,key=lambda rect:rect.width)
        min_ht=min(rects,key=lambda rect:rect.height)
        max_row_div=self.getBestMatch(min_wt,[rect.width for rect in rects])
        max_col_div=self.getBestMatch(min_ht,[rect.height for rect in rects])


        # self.row_div=1/num_rows
        # self.col_div=1/num_cols
        pass

    def create_css_grid(self,rect_list):


        css_rects=[]
        for rect in rect_list:
            elm_props=self.getElmProps(rect)
            rect.addOwnProps(elm_props,'item_grid')
    