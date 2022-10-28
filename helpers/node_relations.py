
from asyncio.log import logger
from .nodes import *
from collections import defaultdict

def findNodeRelations(nodes):
    fn=FindNodeRelationship()
    fn.run(nodes)
    
class FindNodeRelationship():
    def __init__(self):
        self.fun_elm_contians_elm = {
            ElmType.RECTANGLE+'_'+ElmType.RECTANGLE: self._rectContainsRect,
            ElmType.RECTANGLE+'_'+ElmType.ELLIPSE:None

        }

    def _rectContainsRect(self, left_block, right_block):
        """
        left block contains right block
        """
        if left_block.left > right_block.left:
            return False
        width_in = True if (
            left_block.left <= right_block.left and left_block.right >= right_block.right) else False

        height_in = True if (
            left_block.top <= right_block.top and left_block.bottom >= right_block.bottom) else False
        return True if (width_in and height_in) else False



    def run(self,nodes):
        """
        sort nodes by area then check in ascending order ,break for first parent found as that is immediate parent
        for last node parent is Null.
        """
        node_map=defaultdict(list)
        for nn in nodes:
            nn.parent=None
            node_map[int(nn.area)].append(nn)
        
        sorted_list = sorted(node_map.items(), key=lambda item: item[0])
        sorted_nodes=[]
        for (area,items) in sorted_list:
            sorted_nodes.extend(items[::-1])

        total_boxes=len(sorted_nodes)
        for i in range(0, total_boxes-1):
            first_rect = sorted_nodes[i]
            for j in range(i+1, total_boxes):
                second_rect = sorted_nodes[j]
                rel_name=second_rect.root_type+'_'+first_rect.root_type
                if rel_name not in self.fun_elm_contians_elm:
                    logger.error(f'relation function is not implemented {rel_name}')
                if self.fun_elm_contians_elm[rel_name](second_rect,first_rect):
                    first_rect.parent=second_rect
                    break
        