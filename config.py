
import os
BASE_STORE_PATH='/home/admin1/data/ui_builder'
BASE_PROJ_PATH=lambda proj_id:os.path.join(BASE_STORE_PATH,proj_id)
COMPONENT_STORE_PATH= lambda proj_id:os.path.join(BASE_STORE_PATH,proj_id,'components')
PAGE_STORE_PATH= lambda proj_id:os.path.join(BASE_STORE_PATH,proj_id,'page')
COMP_FILES_EXT='.mm'
class FLEX_CONIG():
      MARGIN_DEVIATION =0.05

