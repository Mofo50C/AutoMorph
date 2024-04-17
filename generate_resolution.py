import pandas as pd
import os
import glob
import shutil

BASE_PATH = "./images"

if os.path.exists('./images/.ipynb_checkpoints'):
    shutil.rmtree('./images/.ipynb_checkpoints')

# image_list = sorted(os.listdir('./images/'))
image_list = [os.path.normpath(os.path.relpath(x, BASE_PATH)) for x in glob.iglob(BASE_PATH + "/**/**/*")]
img_list = []
# import image resolution here
res_list = []

for i in image_list:
    img_list.append(i)
    res_list.append(0.008)
    
Data4stage2 = pd.DataFrame({'fundus':img_list, 'res':res_list})
Data4stage2.to_csv('resolution_information.csv', index = None, encoding='utf8')
