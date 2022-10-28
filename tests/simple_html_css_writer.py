
from distutils.fancy_getopt import wrap_text
import joblib
from collections import defaultdict
import os

DEFAULT_BORDER=True
border_txt='border-style: solid;\n border-color: red'


def space(num=1):
    txt=''
    for i in range(num):
        txt+=' '
    return txt

def norm_id(id):
    return id.replace(':','_')

def norm_name(name):
    return name.replace(' ','')

def tab(num=1):
    txt=''
    for i in range(num):
        txt+='  '
    return txt

enter='\n'


def start_div(name,tag='div'):
    return f'<{tag} class="{name}">'

def end_div(tag='div'):
    return f'</{tag}>'

def addCssId(id,props):
    txt=f'#{id}'+'{'+enter
    txt+=props
    return txt+enter+'}'

def addCssClass(name,props):
    txt=f'.{name}'+'{'+enter
    txt+=props
    return txt+enter+'}'


def dictToStr(data,seprator=';'):
    out=''
    for k,v in data.items():
        out+=k+space()+':'+space()+str(v)+seprator+enter
    return out

def write_to_file(text,file_name):
    with open(file_name,'w') as f:
        f.write(text)


class HtmlCssWriter():
    def __init__(self,store,out_folder):
        self.store=store
        self.html=''
        self.css=''
        self.out_folder=out_folder
        self.html_file_path=os.path.join(out_folder,'index.html')
        self.css_file_name='ref.css'
        self.css_file_path=os.path.join(out_folder,self.css_file_name)
        self.comp_map=defaultdict(list)
        self.addDefaultCss()

    def addDefaultCss(self):
        self.css+='html,body\n{\nbox-sizing: border-box;\nmargin:0;\npadding:0;\n}\n'
        self.css+='*, *:before, *:after {\n box-sizing: inherit;}\n'
        

    def addHtml(self,data,depth=1):
        self.html+=tab(depth)+enter
        self.html+=tab(depth)+start_div(norm_name(data.name))
        for child in data.children:
            self.addHtml(child,depth+1)
        self.html+=enter
        self.html+=tab(depth)+end_div()
        

    def addComponentLayout(self,data,container=False):
        """
        only top components are placed..
        """
        id,comp_data=self.store.getComponent(data.uid)
        grid_item=''
        if container:
            grid_item=comp_data.node_props.get('grid_container',{})
            #add container height
            grid_item['height']='100vh'
        else:
            grid_item=comp_data.node_props.get('grid_item',{})
        layout_txt=''
        if grid_item:
            layout_txt=dictToStr(grid_item)
        if DEFAULT_BORDER:
            layout_txt+=border_txt
        self.comp_map[norm_name(data.name)].append(layout_txt)
        for child in data.children:
            self.addComponentLayout(child)


    def addComponentCSS(self,data):
        id,comp_data=self.store.getComponent(data.uid)
        comp_txt=''
        self.comp_map[norm_name(data.name)].append(comp_txt)
        for child in data.children:
            self.addComponentCSS(child)
            
    def writeHtml(self):
        txt='<!DOCTYPE html>'+enter
        txt+='<html>'+enter      
        txt+='<head>'+enter
        txt+='<meta name="viewport" content="width=device-width, initial-scale=1.0">'+enter
        txt+=f'<link rel="stylesheet" href="{self.css_file_name}">'+enter
        txt+='</head>'+enter
        txt+='<body>'+enter
        txt+=self.html+enter
        txt+='</body>'+enter
        txt+='</html>'+enter
        self.html=txt

    def writeCss(self):
        for name,props in self.comp_map.items():
            props_txt="\n".join(props)
            self.css+=addCssClass(name,props_txt)+enter


    def writeToDisk(self):
        if not os.path.exists(self.out_folder):
            os.mkdir(self.out_folder)
        
        write_to_file(self.html,self.html_file_path)
        write_to_file(self.css,self.css_file_path)


    def parsePageStruct(self,page_file):
        data=joblib.load(page_file)
        self.addHtml(data)
        self.addComponentLayout(data,True)
        self.addComponentCSS(data)
        self.writeCss()
        self.writeHtml()
        self.writeToDisk()


def test_simple_HC_Writer():
    from helpers import LocalStore
    proj_id='grid_project'
    base=f'/home/admin1/data/ui_builder/{proj_id}'
    page_file=base+'/page/1:2.mm'
    out_folder=os.path.join(base,'output')
    store=LocalStore(proj_id)
    hc=HtmlCssWriter(store,out_folder)
    hc.parsePageStruct(page_file)
    pass
