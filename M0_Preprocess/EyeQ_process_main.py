import fundus_prep as prep
import os
import glob
import pandas as pd
from PIL import ImageFile
import shutil
ImageFile.LOAD_TRUNCATED_IMAGES = True

BASE_PATH = "../images"

def process(image_list, save_path):
    
    radius_list = []
    centre_list_w = []
    centre_list_h = []
    name_list = []
    list_resolution = []
    scale_resolution = []
    
    resolution_list = pd.read_csv('../resolution_information.csv')
    
    for image_path in image_list:
        
        image_path = os.path.normpath(image_path)
        rel_path = os.path.normpath(os.path.relpath(image_path, BASE_PATH))
        name, ext = os.path.splitext(os.path.basename(rel_path))
        dir_name = os.path.dirname(rel_path)
        # print(f"image_path: {image_path}")
        # print(f"rel_path: {rel_path}")
        # print(f"dir_name: {dir_name}")
        # print(f"base_name: {name}")
        # print()

        save_img_path = os.path.normpath(os.path.join(save_path, dir_name, name + ".png"))
        print(save_img_path)
    
        if os.path.exists(save_img_path):
            print('continue...')
            continue

        if not os.path.exists(os.path.join(save_path, dir_name)):
            os.makedirs(os.path.join(save_path, dir_name))

        try:
            resolution_ = resolution_list['res'][resolution_list['fundus']==rel_path].values[0]
            list_resolution.append(resolution_)
            img = prep.imread(image_path)
            r_img, borders, mask, r_img, radius_list,centre_list_w, centre_list_h = prep.process_without_gb(img,img,radius_list,centre_list_w, centre_list_h)
            prep.imwrite(save_img_path, r_img)
            name_list.append(rel_path)
        except Exception as e:
            print(e.with_traceback(e.__traceback__))

    scale_list = [a*2/912 for a in radius_list]
    scale_resolution = [a*b*1000 for a,b in zip(list_resolution,scale_list)]
    Data4stage2 = pd.DataFrame({'Name':name_list, 'centre_w':centre_list_w, 'centre_h':centre_list_h, 'radius':radius_list, 'Scale':scale_list, 'Scale_resolution':scale_resolution})
    Data4stage2.to_csv('../Results/M0/crop_info.csv', index = None, encoding='utf8')


if __name__ == "__main__":
    if os.path.exists(BASE_PATH + "/.ipynb_checkpoints"):
        shutil.rmtree(BASE_PATH + "/.ipynb_checkpoints")
    image_list = glob.glob(BASE_PATH + "/**/*.*", recursive=True)
    save_path = '../Results/M0/images/'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    process(image_list, save_path)

        




