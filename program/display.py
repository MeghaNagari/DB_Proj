import ast
import json
import os
from pathlib import Path

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
query_output_folder = Path(my_path+"/queryOutput")


def get_files(data_folder_path):
    page_link_file = data_folder_path / "pageLink.txt"
    file_names = page_link_file.read_text()
    # print(fileNames)
    file_array = ast.literal_eval(file_names)
    return file_array


def convert_file_content_to_json(file_content):
    lis = ast.literal_eval(file_content)
    my_json = json.dumps(lis)
    return my_json


def read_file_content(data_folder, i):
    file_to_open = data_folder / i
    file_content = file_to_open.read_text()
    my_json = convert_file_content_to_json(file_content)
    h = ast.literal_eval(my_json)
    return h


def write_file_content(file_content,root_page,my_page,folder):
    f = open(str(folder) + "\\"+root_page, "a")
    if file_content[0] == "I"and file_content[1] != "Nil":
        f.write("\t"+my_page + ":"+json.dumps(file_content)+"\n")
    elif file_content[0] == "L":
        f.write("\t\t"+my_page + ":"+json.dumps(file_content)+"\n")
    else:
        f.write(my_page + ":"+json.dumps(file_content)+"\n")
    f.close()


def read_page_write_content(page_to_read,root_file_name,folder):
    file_content = read_file_content(page_pool__index_folder,page_to_read)
    write_file_content(file_content,root_file_name,page_to_read,folder)
    for i in file_content[2]:
        if ".txt" in i:
            read_page_write_content(i, root_file_name,folder)

def create_test_tree(rel, root_file_name):
    file_content = read_file_content(page_pool__index_folder, root_file_name)
    file_name_for_creation = rel + "Temp.txt"
    if os.path.exists(str(tree_pic_folder) + "\\" + file_name_for_creation):
        os.remove(str(tree_pic_folder) + "\\" + file_name_for_creation)
    write_file_content(file_content, file_name_for_creation, root_file_name,page_pool__index_folder)
    for i in file_content[2]:
        if ".txt" in i:
            read_page_write_content(i, file_name_for_creation,page_pool__index_folder)
    # print(file_name_for_creation)

def displayTree(root_file_name):
    file_content = read_file_content(page_pool__index_folder,root_file_name)
    file_name_for_creation = ""
    if "s0" in str(file_content):
        file_name_for_creation = supplier_string+"_sid.txt"
    else:
        file_name_for_creation = supply_string+"_pid.txt"
    if os.path.exists(str(tree_pic_folder) + "\\" + file_name_for_creation):
        os.remove(str(tree_pic_folder) + "\\" + file_name_for_creation)
    write_file_content(file_content,file_name_for_creation,root_file_name,tree_pic_folder)
    for i in file_content[2]:
        if ".txt" in i:
            read_page_write_content(i,file_name_for_creation,tree_pic_folder)
    print(file_name_for_creation)


supplier_list = []
product_list = []
supply_list = []


def write_query(string):
    f = open(str(query_output_folder) + "\\" + "queryResult.txt", "a")
    f.write("\n\n"+json.dumps(string, ensure_ascii=False) + "\n\n")
    f.close()
    return



def displayTable(rel, fname):

    if rel == supplier_string:
        file_names = get_files(supplier_data_folder)
        for i in file_names:
            h = read_file_content(supplier_data_folder, i)
            for idx, j in enumerate(h):
                supplier_list.append(j)
        data = supplier_list

    elif rel == product_string:
        file_names = get_files(product_data_folder)
        for i in file_names:
            h = read_file_content(product_data_folder, i)
            for j in h:
                product_list.append(j)
        data = product_list


    elif rel == supply_string:
        file_names = get_files(supply_data_folder)
        for i in file_names:
            h = read_file_content(supply_data_folder, i)
            for idx, j in enumerate(h):
                supply_list.append(j)
        data = supply_list

    else:
        file_content = read_file_content(schemas_path, rel)
        f = open(str(query_output_folder) + "\\" + fname, "a")
        for i in file_content:
            f.write(json.dumps(i, ensure_ascii=False) + "\n")
        # print(file_content)
        # f.write(json.dumps(file_content, ensure_ascii=False) + "\n\n\n")
        f.close()
        return

    # f = open(fname, "w+")
    # f.write(json.dumps(data, ensure_ascii=False))
    # f.close()



# displayTree("pg00.txt")
# displayTable(supply_string,"Supply.txt")
