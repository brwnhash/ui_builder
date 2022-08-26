





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
    from  UxParser import FigmaParser
    import joblib
    input_file='/home/admin1/data/ui_builder/file_data.json'
    data=joblib.load(input_file)
    fc=FigmaParser(None,None)
    fc.parse(data)   

def test_figma_pages_parser():
    from  UxParser import FigmaParser
    import joblib
    input_file='/home/admin1/data/ui_builder/file_data.json'
    data=joblib.load(input_file)
    fc=FigmaParser(None,None)
    fc.parsePages(data)
    pass
#test_figma_Canvas_parser()
#test_figma_file_parser()
#test_figma_pages_parser()
#get_figma_data_dump()
test_figma_parser()
#dump_figma_data()
#test_figma_reader()







