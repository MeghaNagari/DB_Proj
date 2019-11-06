import os
from pathlib import Path
import json
import ast

supplier_string = "Suppliers"
product_string = "Products"
supply_string = "Supply"
path = ""
path = os.getcwd()
my_path = os.path.dirname(path)


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


myResultArray = []
supplierObjList = []
productObjList = []
supplyObjList = []
finalArray = []


def convert_str_to_float(args):
    return float(args)


def check_record(op, val, record, compare_attr, my_result_array):
    try:
        if compare_attr >= val:
            print("exception")
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



def select(rel, att, op, val):
    result = []
    if rel == supplier_string:
        data_folder = Path(my_path + "/data/Suppliers")
        file_names = get_files(data_folder)
        # print("fileNames = ", file_names)
        my_result_array = []
        for i in file_names:
            file_to_open = data_folder / i
            file_content = file_to_open.read_text()
            my_json = convert_file_content_to_json(file_content)
            h = ast.literal_eval(my_json)
            # j = one record, j has sid,sname and address
            if att == "sid":
                compare_obj_idx = 0
            elif att == "sname":
                compare_obj_idx = 1
            elif att == "address":
                compare_obj_idx = 2
            for j in h:
                # print("j = ", j)
                compare_obj = j[compare_obj_idx]
                check_record(op, val, j, compare_obj, my_result_array)
        result = my_result_array

    elif rel == product_string:
        data_folder = Path(my_path + "/data/Products")
        file_names = get_files(data_folder)
        # print("fileNames = ", file_names)
        my_result_array = []
        for i in file_names:
            # print("i = ", i)
            file_to_open = data_folder / i
            file_content = file_to_open.read_text()
            my_json = convert_file_content_to_json(file_content)
            h = ast.literal_eval(my_json)
            # j = one record, j has sid,sname and address
            if att == "pid":
                compare_obj_idx = 0
            elif att == "pname":
                compare_obj_idx = 1
            elif att == "color":
                compare_obj_idx = 2
            for j in h:
                compare_obj = j[compare_obj_idx]
                check_record(op, val, j, compare_obj, my_result_array)
        result = my_result_array

    elif rel == supply_string:
        data_folder = Path(my_path + "/data/Supply")
        file_names = get_files(data_folder)
        # print("fileNames = ", file_names)
        my_result_array = []
        for i in file_names:
            # print("i = ", i)
            file_to_open = data_folder / i
            file_content = file_to_open.read_text()
            my_json = convert_file_content_to_json(file_content)
            h = ast.literal_eval(my_json)
            # j = one record, j has sid,sname and address
            if att == "sid":
                compare_obj_idx = 0
            elif att == "pid":
                compare_obj_idx = 1
            elif att == "cost":
                compare_obj_idx = 2
            for j in h:
                compare_obj = j[compare_obj_idx]
                check_record(op, val, j, compare_obj, my_result_array)
        result = my_result_array

    for r in result:
        print(r)


select(supply_string, "cost", "<", "50")

# def project(rel, *attList):
