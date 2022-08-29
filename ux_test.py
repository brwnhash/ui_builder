





def test_figma_reader():
    import FigmaPy

    token = 'figd_6OS0WhuNuZw79Nkmolp_efuVsvxJ3AVVtUNCziVy'  # can be found in your figma user profile page
    file_key = 'jJPaQGoE6vIq1bxJyePiij'  # can be found in the URL of the file
    figmaPy = FigmaPy.FigmaPy(token=token)
    ids=['61%3A29']
    #figmaPy.get_file_nodes(file_key,ids)
    file = figmaPy.get_file(key=file_key)
    print([x.name for x in file.document.children])
    # ['Page 1', 'Page 2']
    for page in file.document.children:
        if page.name!='interact':
            continue
        for comps in page.children:
            for comp in comps.children:
                print(comp.name)

def dump_figma_data():
    import FigmaPy
    import json
    out_file='/home/admin1/data/figma/all_pages.json'
    token = 'figd_6OS0WhuNuZw79Nkmolp_efuVsvxJ3AVVtUNCziVy'  # can be found in your figma user profile page
    file_key = 'jJPaQGoE6vIq1bxJyePiij'  # can be found in the URL of the file
    figmaPy = FigmaPy.FigmaPy(token=token)
    ids=['25%3A45']
    data=figmaPy.get_file_nodes(file_key,ids)
    #data = figmaPy.get_file(key=file_key,return_raw_data=True)
    # comp_id='61%3A29'
    # data=figmaPy.get_file_components(file_key,comp_id)
    with open(out_file,'w') as fp:
        json.dump(data,fp)

def get_figma_data_dump():
    from  UxParser import FigmaParser,FigmaParseType
    import joblib
    token = 'figd_6OS0WhuNuZw79Nkmolp_efuVsvxJ3AVVtUNCziVy' 
    file_key = 'jJPaQGoE6vIq1bxJyePiij'
    page_id='56%3A108'
    fp=FigmaParser(token,file_key)
    #data=fp.fetch()
    data=fp.fetchAll(page_id)
    out_file='/home/admin1/data/ui_builder/file_data.json'
    joblib.dump(data,out_file)

def test_figma_file_parser():
    from  UxParser import FigmaParser,FigmaParseType
    import json
    token = 'figd_6OS0WhuNuZw79Nkmolp_efuVsvxJ3AVVtUNCziVy'
    out_file='/home/admin1/data/figma/sample_comp.json'
    data=None
    file_key = 'jJPaQGoE6vIq1bxJyePiij'
    page_ids=['56%3A108']
    with open(out_file,'r') as fp:
        data=json.load(fp)
        pid=page_ids[0].replace('%3A',':')
        data.update(data['nodes'][pid])
        del data['nodes']

    fp=FigmaParser(token,file_key,FigmaParseType.PAGE,page_ids)
    parsed_data=fp.figma.parse_file_data(fp.req_key,data)
    pass

def test_figma_Canvas_parser():
    from  UxParser import FigmaParser
    import joblib
    input_file='/home/admin1/data/ui_builder/file_data.json'
    data=joblib.load(input_file)
    fc=FigmaParser(None,None)
    fc.parseCanvasNode(data)

def test_figma_parser():
    from  UxParser import FigmaParser,DataStore
    import joblib
    
    proj_id='sample_proj'
    input_file='/home/admin1/data/ui_builder/file_data.json'
    data=joblib.load(input_file)
    fc=FigmaParser(None,None)
    fc.parse(data)
    store=DataStore(proj_id)
    store.storeComponents(fc.getComponents())
    print('cool')   

def test_flex_layout_generator():
    from  UxParser import DataStore
    
    proj_id='sample_proj'
    store=DataStore(proj_id)
    for id,comp in store.getComponents():
        pass

def get_fake_box_props(name,x,y,width,height,view_x=None,view_y=None,view_width=None,view_height=None):
    import random
    view_x= view_x   if view_x else x
    view_y=view_y if view_y else y
    view_width=view_width if view_width else width
    view_height=view_height if view_height else height
    props={'width':width,'height':height,'x':x,'y':y,
            'name':name,'uid':name,'parent':None,
            'view_x':view_x,'view_y':view_y,
            'x_offset':0,'y_offset':0,'view_width':view_width,'view_height':view_height}
    return props

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
    return bb
def get_2d_perfect_overlap_row():
    bb=[]
    bb.append(get_fake_box_props('1',10,10,40,40))
    bb.append(get_fake_box_props('2',10,60,40,40)) #at offset of 10
    bb.append(get_fake_box_props('3',60,10,40,40))
    bb.append(get_fake_box_props('4',60,60,40,40))
    bb.append(get_fake_box_props('5',110,10,40,40))#at offset of 10
    bb.append(get_fake_box_props('6',110,60,40,40))
    return bb

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

def symmetric_1d_row_col_boxes_check():
    from UxParser.flex_layout_generator import GroupBoxes
    from UxParser.nodes import Rectange
    #col boxes
    #box_list=[get_row_boxes(),get_col_boxes(),get_non_sym_row_boxes(),get_partial_col_overlap()]
    box_list=[get_non_sym_row_boxes()]
    for idx,(box1,box2,box3) in enumerate(box_list):
        bb1=Rectange(box1)
        bb2=Rectange(box2)
        bb3=Rectange(box3)
        gb=GroupBoxes([bb1,bb2,bb3])
        node_list=gb.getNearestElementInRowColumn()
        print( f'idx is {idx}')
        for node in node_list:
            print(f'nid {node.uid} row_idx {node.row_grp_idx} and col_idx {node.col_grp_idx} row wt {node.row_edge_wt} and col wt {node.col_edge_wt}')
        

def symmetric_2d_row_col_boxes_check():
    from UxParser.flex_layout_generator import GroupBoxes
    from UxParser.nodes import Rectange

    #box_lil=[get_2d_perfect_overlap_col(),get_2d_partial_overlap1(),get_2d_non_overlap(),get_2d_perfect_overlap_row()]
    box_lil=[get_2d_partial_overlap1()]
    for idx,box_list in enumerate(box_lil):
        rect_list=[Rectange(bb) for bb in box_list]
        gb=GroupBoxes(rect_list)
        node_list=gb.getNearestElementInRowColumn()
        print( f'idx is {idx}')
        for node in node_list:
            print(f'nid  {node.uid} row_idx {node.row_grp_idx} and col_idx {node.col_grp_idx} row wt {node.row_edge_wt} and col wt {node.col_edge_wt}')
               
    

    


def test_box_groupings():
    from UxParser.flex_layout_generator import GroupBoxes
    from UxParser.nodes import Rectange
    #test 1 equal 

    rect=Rectange()


def test_figma_pages_parser():
    from  UxParser import FigmaParser
    import joblib
    input_file='/home/admin1/data/ui_builder/file_data.json'
    data=joblib.load(input_file)
    fc=FigmaParser(None,None)
    fc.parsePages(data)
    pass

#symmetric_1d_row_col_boxes_check()
symmetric_2d_row_col_boxes_check()

#test_figma_Canvas_parser()
#test_figma_file_parser()
#test_figma_pages_parser()
#get_figma_data_dump()
#test_figma_parser()
#test_flex_layout_generator()
#dump_figma_data()
#test_figma_reader()







