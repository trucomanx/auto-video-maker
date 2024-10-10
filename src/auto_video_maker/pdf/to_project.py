#!/usr/bin/python3

import os
import json
from .to_image   import to_images
from .annotation import annotations

CONFIG_DEFAULT = {
    "transition": {"enable": True, "type": "fading", "time":1.0},
    "time_minimum": 1.0
}

def to_project(pdf_path, output_dir, image_name_format, dpi=300, shape=(800,600)):
    '''
    '''
    image_dir = os.path.join(output_dir,'images');
    
    image_paths     = to_images(pdf_path, image_dir, image_name_format, dpi);
    all_annotations = annotations(pdf_path)
    
    data={"width": shape[0], "height": shape[1], "clips":[]  }
    
    for k,img_path in enumerate(image_paths):
        elem_v={"enable": False};
        elem_t={"enable": False};
        
        if img_path.strip()!="":
            elem_v={"enable": True, "source": os.path.relpath(img_path, output_dir)}
            
        text=""
        for annot in all_annotations[k]:
            text = text + annot['content'] + "\n\n";
        if text.strip()!="":
            elem_t={"enable": True, "source": text};
        
        data["clips"].append({ "textual": elem_t, "visual": elem_v });
    with open(os.path.join(output_dir,"data.json"), "w") as outfile: 
        json.dump(data, outfile,indent=4,ensure_ascii=False)  
        
    with open(os.path.join(output_dir,"config.json"), "w") as outfile: 
        json.dump(CONFIG_DEFAULT, outfile,indent=4,ensure_ascii=False)  
