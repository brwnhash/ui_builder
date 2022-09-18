
import os
BASE_STORE_PATH='/home/admin1/data/ui_builder'
BASE_PROJ_PATH=lambda proj_id:os.path.join(BASE_STORE_PATH,proj_id)
COMPONENT_STORE_PATH= lambda proj_id:os.path.join(BASE_STORE_PATH,proj_id,'components')
FLEX_CONIG={
      'margin_dev':0.05

}

