from code_generator import ComponentsBuilder

def test_simple_comp_builder():
    from code_generator import GridFlexLayoutParser
    from helpers import NodeType,LocalStore
    proj_id='grid_project'
    base=f'/home/admin1/data/ui_builder/{proj_id}'
    file=base+'/page/21:53.mm'
    component_folder=base+'/components'
    store=LocalStore(proj_id)
    layout_parser=GridFlexLayoutParser(store)
    cb=ComponentsBuilder(file,component_folder,NodeType.PAGE,layout_parser)
    cb.run()



