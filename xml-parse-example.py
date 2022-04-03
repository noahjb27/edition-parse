from logging import root
import xml.etree.ElementTree as ET
import csv
import os
#path to folder with XML files - folder can only have xml files!
path = r'C:\Users\...'

for filename in os.listdir(path):
        if filename.endswith(".xml"):
            fullpath = os.path.join(path, filename)
        #getting the root of each file as my starting point
        for file in fullpath:
            tree = ET.parse(fullpath)
            root = tree.getroot()
            with open('FILENAME.csv', 'a', newline='',  encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f, fieldnames=['element_or_attribute', 'text_or_value']
                )
            
                # merge dictionaries of elements and attributes
                # dict keys remove namespaces and checks for NoneTypes
                # attributes are prefixed with their parent element name
                xml_dicts = [{
                    **{el.tag.split('}')[1]:(
                        el.text.strip() if el.text is not None else el.text
                    )}, 
                    **{(
                        el.tag.split('}')[1]+'_'+k.split('}')[1] 
                        if '}' in k 
                        else el.tag.split('}')[1]+'_'+k):v 
                    for k,v in el.attrib.items()}
                } for i, el in enumerate(root.findall(f'.//*'), start=1)]
                
                # combine dicts into flatter format
                csv_dicts = [
                    {'element_or_attribute': k, 'text_or_value':v} 
                    for d in xml_dicts  
                    for k, v in d.items()
                ]
                
                writer.writeheader()
                writer.writerows(csv_dicts)