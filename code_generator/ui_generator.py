

def choiceLookUp(type,choices):
    if type not in choices:
        raise Exception(f'Invalid {type} Choice options are {choices}')


class UiGenerator():
    """
    config contains all the choice for parsers etc.
    ux parser: fetch and parse ux 
    layout parser : parse layout based on selected choice 
    """
    def __init__(self,config):
        self.layout_parser_map={}
        self.ux_parser_map={}
        self.ux_parser=None
        self.layout_parser=None

        
    def getLayoutChoices(self):
        return list(self.addLayoutParser.keys())
    
    def addLayoutParser(self,layout_type):
        choiceLookUp(layout_type,self.layout_parser_map)
        self.layout_parser=self.layout_parser_map[layout_type]

    def addUxParser(self,ux_type):
        choiceLookUp(ux_type,self.ux_parser_map)
        self.ux_parser=self.ux_parser_map[ux_type]
        

    def run(self):
        """
        request can be to build page and all interactions or a single component
        1.select UX and do parsing .
        2.Adapter to convert to format which generator can understand
        3.generate layout ,generate style sheet ,generate components in JS frameworks

        """
        

        pass

    
    