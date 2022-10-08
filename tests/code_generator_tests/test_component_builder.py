from code_generator import ComponentBuilder

def test_simple_comp_builder():
    base='/home/admin1/data/ui_builder/first_project'
    file=base+'/page/1:2.mm'
    component_folder=base+'/components'
    cb=ComponentBuilder(file,component_folder,'.mm')
    cb.run()



