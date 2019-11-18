import json
import os
from pathlib import Path
import re


supplier_string = "Suppliers"
product_string = "Products"
supply_string = "Supply"
path = ""
path = os.getcwd()
my_path = os.path.dirname(path)
supplier_data_folder = Path(my_path + "/data/Suppliers")
product_data_folder = Path(my_path + "/data/Products")
supply_data_folder = Path(my_path + "/data/Supply")
schemas_path = Path(my_path + "/data")
page_pool__index_folder = Path(my_path+"/index")
tree_pic_folder = Path(my_path+"/treePic")



def get_files(data_folder_path):
    page_link_file = data_folder_path / "pageLink.txt"
    file_names = page_link_file.read_text()
    # print(fileNames)
    file_array = json.loads(file_names)
    return file_array


# def convert_file_content_to_json(file_content):
#     lis = json.loads(file_content)
#     my_json = json.dumps(lis)
#     return my_json


def read_file_content(data_folder, i):
    file_to_open = data_folder / i
    file_content = file_to_open.read_text()
    h = json.loads(file_content)
    return h


def write_file_content(file_content,root_page,my_page):
    f = open(str(tree_pic_folder) + "\\"+root_page, "a")
    f.write(my_page + ":"+json.dumps(file_content)+"\n")
    f.close()


def put_page_in_page_pool(file_array,page_pool_file):
    f = open(page_pool_file, "w")
    f.write(json.dumps(file_array, ensure_ascii=False))
    f.close()


def delete_page_and_put_in_page_pool(page_name,data_folder,data_forlder_path_for_rel):
    if data_forlder_path_for_rel != None:
        if os.path.exists(str(data_forlder_path_for_rel) + "\\" + page_name):
            os.remove(str(data_forlder_path_for_rel) + "\\" + page_name)
    try:
         if os.path.exists(str(data_folder)+"\\"+page_name):
          os.remove(str(data_folder)+"\\"+page_name)
          page_pool_file = data_folder / "pagePool.txt"
          page_names = page_pool_file.read_text()
          file_array = json.loads(page_names)
          file_array.append(page_name)
          put_page_in_page_pool(file_array,page_pool_file)

    except Exception as e:
        print(e)



def get_indexes(string):
    return [m.start() for m in re.finditer('pg', string)]


def read_page_and_get_indexes(page_folder,page_name):
    file_to_open = read_file_content(page_folder,page_name)
    read_contents = str(file_to_open)
    li = get_indexes(read_contents)
    return li


def delete_entry_from_directory(rel, att):
    f = open(str(page_pool__index_folder) + "\\directory.txt","r+")
    lines = f.readlines();
    lines_to_write = []
    for i in lines:
        if rel not in str(i) or att not in str(i):
            lines_to_write.append(i)
    for k in lines_to_write:
        f.write(k+"\n")
    f.close()



def removeTree(rel, att):
    file_to_open = rel+"_"+att+".txt"
    try:
        file_content =  open(str(tree_pic_folder) + "\\"+file_to_open, "r")
        lines = file_content.readlines()
        for i in lines:
            file_array = i.strip().split(":")
            page_to_del = file_array[0]
            if page_to_del != "":
                delete_page_and_put_in_page_pool(file_array[0],page_pool__index_folder,None)
        print("deleted all pages and put back to page pool")
        delete_entry_from_directory(rel,att)
    except Exception as e:
        print(e)

# removeTree("Supplier", "sid")
# removeTree("Supply","pid")


def delete_from_Schemas(rel):
    file_content = read_file_content(schemas_path, "schemas.txt")
    lines_to_write = []
    for i in file_content:
        if rel not in str(i):
            lines_to_write.append(i)
    f = open(str(schemas_path) + "\\"+"schemas.txt", "w")
    f.write(json.dumps(lines_to_write))





def removeTable(rel):
    if rel == supplier_string:
        folder_path = supplier_data_folder
        page_link_files = get_files(supplier_data_folder)
    elif rel == product_string:
        folder_path = product_data_folder
        page_link_files = get_files(product_data_folder)
    elif rel == supply_string:
        folder_path = supply_data_folder
        page_link_files = get_files(supply_data_folder)
    for i in page_link_files:
        delete_page_and_put_in_page_pool(i, schemas_path,folder_path)
    delete_from_Schemas(rel)



removeTable(supplier_string)



