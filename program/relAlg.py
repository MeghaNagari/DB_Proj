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

sid_idx = 0
sname_idx = 1
address_idx = 2
pid_idx = 0
pname_idx = 1
color_idx = 2
supply_sid_idx = 0
supply_pid_idx = 1
supply_cost_idx = 2


def get_files(data_folder_path):
    page_link_file = data_folder_path / "pageLink.txt"
    file_names = page_link_file.read_text()
    # print(fileNames)
    file_array = json.loads(file_names)
    return file_array


# def convert_file_content_to_json(file_content):
#     lis = ast.literal_eval(file_content)
#     my_json = json.dumps(lis)
#     return my_json


# myResultArray = []
# supplier_list = []
# product_list = []
# supply_list = []
# finalArray = []


def convert_str_to_float(args):
    return float(args)


def check_record(op, val, record, compare_attr, my_result_array):
    try:
        if compare_attr >= val:
            pass
    except TypeError:
        compare_attr = convert_str_to_float(compare_attr)
        val = convert_str_to_float(val)

    if op == ">=":
        if compare_attr >= val:
            my_result_array.append(record)
    if op == "<=":
        if compare_attr <= val:
            my_result_array.append(record)
    if op == ">":
        if compare_attr > val:
            my_result_array.append(record)
    if op == "<":
        if compare_attr < val:
            my_result_array.append(record)
    if op == "=":
        if compare_attr == val:
            my_result_array.append(record)


def read_file_content(data_folder, i):
    file_to_open = data_folder / i
    file_content = file_to_open.read_text()
    return json.loads(file_content)


def readSchemas():
    global sid_idx,sname_idx,address_idx,pid_idx,pname_idx,color_idx,supply_sid_idx,supply_pid_idx,supply_cost_idx
    h = read_file_content(schemas_path, "schemas.txt")
    # print(h)
    for i in h:
        # print(i)
        if i[0] == supplier_string:
            if i[1] == "sid":
                sid_idx = int(i[3])
            if i[1] == "sname":
                sname_idx = int(i[3])
            if i[1] == "address":
                address_idx = int(i[3])
        elif i[0] == product_string:
            if i[1] == "pid":
                pid_idx = int(i[3])
            if i[1] == "pname":
                pname_idx = int(i[3])
            if i[1] == "color":
                color_idx = int(i[3])
        elif i[0] == product_string:
            if i[1] == "sid":
                supply_sid_idx = int(i[3])
            if i[1] == "pid":
                supply_pid_idx = int(i[3])
            if i[1] == "cost":
                supply_cost_idx = int(i[3])


def is_bplustree_existing(rel, att):
    f = open(str(page_pool__index_folder) + "\\directory.txt", "r")
    if rel in str(f.readlines()) and att in str(f.readlines()):
        return True
    else:
        return False



def select(rel, att, op, val):
    is_tree_existing = is_bplustree_existing(rel,att)



    result = []
    readSchemas()
    if rel == supplier_string:
        file_names = get_files(supplier_data_folder)
        # print("fileNames = ", file_names)
        my_result_array = []
        for i in file_names:
            h = read_file_content(supplier_data_folder, i)
            if att == "sid":
                compare_obj_idx = sid_idx
            elif att == "sname":
                compare_obj_idx = sname_idx
            elif att == "address":
                compare_obj_idx = address_idx
            for j in h:
                # print("j = ", j)
                # supplier_list.append(j)
                compare_obj = j[compare_obj_idx]
                check_record(op, val, j, compare_obj, my_result_array)
        result = my_result_array

    elif rel == product_string:
        file_names = get_files(product_data_folder)
        # print("fileNames = ", file_names)
        my_result_array = []
        for i in file_names:
            # print("i = ", i)
            h = read_file_content(product_data_folder, i)
            if att == "pid":
                compare_obj_idx = pid_idx
            elif att == "pname":
                compare_obj_idx = pname_idx
            elif att == "color":
                compare_obj_idx = color_idx
            for j in h:
                # product_list.append(j)
                compare_obj = j[compare_obj_idx]
                check_record(op, val, j, compare_obj, my_result_array)
        result = my_result_array

    elif rel == supply_string:
        file_names = get_files(supply_data_folder)
        # print("fileNames = ", file_names)
        my_result_array = []
        for i in file_names:
            # print("i = ", i)
            h = read_file_content(supply_data_folder, i)
            if att == "sid":
                compare_obj_idx = supply_sid_idx
            elif att == "pid":
                compare_obj_idx = supply_pid_idx
            elif att == "cost":
                compare_obj_idx = supply_cost_idx
            for j in h:
                # supply_list.append(j)
                compare_obj = j[compare_obj_idx]
                check_record(op, val, j, compare_obj, my_result_array)
        result = my_result_array

    for r in result:
        print(r)


def addToFinalResult(record, obj, my_result_list, indexes_to_add):
    for i in indexes_to_add:
        obj.append(record[i])
    my_result_list.append(obj)


def project(rel, *att_list):
    if rel == supplier_string:
        file_names = get_files(supplier_data_folder)
        my_result_list = []
        indexes_to_add = []
        if att_list.__contains__("sid"):
            indexes_to_add.append(sid_idx)
        if att_list.__contains__("sname"):
            indexes_to_add.append(sname_idx)
        if att_list.__contains__("address"):
            indexes_to_add.append(address_idx)
        for i in file_names:
            h = read_file_content(supplier_data_folder, i)
            # print(h)
            # print(h[0])
            for j in h:
                obj = []
                addToFinalResult(j, obj, my_result_list, indexes_to_add)

    elif rel == product_string:
        file_names = get_files(product_data_folder)
        my_result_list = []
        indexes_to_add = []
        if att_list.__contains__("pid"):
            indexes_to_add.append(pid_idx)
        if att_list.__contains__("pname"):
            indexes_to_add.append(pname_idx)
        if att_list.__contains__("color"):
            indexes_to_add.append(color_idx)
        for i in file_names:
            h = read_file_content(product_data_folder, i)
            for j in h:
                obj = []
                addToFinalResult(j, obj, my_result_list, indexes_to_add)

    elif rel == supply_string:
        file_names = get_files(supply_data_folder)
        my_result_list = []
        indexes_to_add = []
        if att_list.__contains__("sid"):
            indexes_to_add.append(supply_sid_idx)
        if att_list.__contains__("pid"):
            indexes_to_add.append(supply_pid_idx)
        if att_list.__contains__("cost"):
            indexes_to_add.append(supply_cost_idx)
        for i in file_names:
            h = read_file_content(supply_data_folder, i)
            # print(h)
            # print(h[0])
            for j in h:
                obj = []
                addToFinalResult(j, obj, my_result_list, indexes_to_add)

        for r in my_result_list:
            print(r)


def join(rel1, att1, rel2, att2):
    if att1 != att2:
        raise AttributeError('Sorry, attributes must be same')
    supplier_file_names = get_files(supplier_data_folder)
    supplier_list = []
    for i in supplier_file_names:
        h = read_file_content(supplier_data_folder, i)
        for j in h:
            supplier_list.append(j)
    product_file_names = get_files(product_data_folder)
    product_list = []
    for i in product_file_names:
        h = read_file_content(product_data_folder, i)
        for j in h:
            product_list.append(j)
    supply_file_names = get_files(supply_data_folder)
    supply_list = []
    for i in supply_file_names:
        h = read_file_content(supply_data_folder, i)
        for j in h:
            supply_list.append(j)
    index_attr_1 = 0
    index_attr_2 = 0
    if rel1 == supplier_string:
        rel1 = supplier_list
        if att1 == "sid":
            index_attr_1 = sid_idx
        elif att1 == "sname":
            index_attr_1 = sname_idx
        elif att1 == "address":
            index_attr_1 = address_idx
    elif rel1 == product_string:
        rel1 = product_list
        if att1 == "pid":
            index_attr_1 = pid_idx
        elif att1 == "pname":
            index_attr_1 = pname_idx
        elif att1 == "color":
            index_attr_1 = color_idx
    elif rel1 == supply_string:
        rel1 = supply_list
        if att1 == "sid":
            index_attr_1 = supply_sid_idx
        elif att1 == "pid":
            index_attr_1 = supply_pid_idx
        elif att1 == "cost":
            index_attr_1 = supply_cost_idx
    if rel2 == supplier_string:
        rel2 = supplier_list
        if att2 == "sid":
            index_attr_2 = sid_idx
        elif att2 == "sname":
            index_attr_2 = sname_idx
        elif att2 == "address":
            index_attr_2 = address_idx
    elif rel2 == product_string:
        rel2 = product_list
        if att2 == "pid":
            index_attr_2 = pid_idx
        elif att2 == "pname":
            index_attr_2 = pname_idx
        elif att2 == "color":
            index_attr_2 = color_idx
    elif rel2 == supply_string:
        rel2 = supply_list
        if att2 == "sid":
            index_attr_2 = supply_sid_idx
        elif att2 == "pid":
            index_attr_2 = supply_pid_idx
        elif att2 == "cost":
            index_attr_2 = supply_cost_idx

    result = []
    for x in rel1:
        for y in rel2:
            if x[index_attr_1] == y[index_attr_2]:
                myobj = []
                try:
                    for idx in range(3):
                        if idx != index_attr_1:
                            myobj.append(x[idx])
                        if idx != index_attr_2:
                            myobj.append(y[idx])
                    result.append(myobj)
                except Exception as e:
                    print(e)

    print(result)


# under_22 = [rider for rider in people if rider[1] < 22]

# select(product_string, "color", "=", "white")
select(supplier_string, "sname", "=", "Carter")

# project(supplier_string, "sid", "sname")


# join(product_string, "pid", supply_string, "pid")
