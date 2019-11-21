import ast
import json
import os
from pathlib import Path
import time


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


sid_idx = 0
sname_idx = 1
address_idx = 2
pid_idx = 0
pname_idx = 1
color_idx = 2
supply_sid_idx = 0
supply_pid_idx = 1
supply_cost_idx = 2

cost_of_search = 0


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


def is_bplustree_existing(rel):
    string_content = Path(str(page_pool__index_folder) + "\\directory.txt").read_text()
    if rel in string_content:
        return True
    else:
        return False


def find_array_to_return(nav_array, start_idx):
    pages_array = []
    for i in range(start_idx, len(nav_array)):
        if ".txt" in nav_array[i]:
            pages_array.append(nav_array[i])
        else:
            break
    return pages_array


def get_page_to_search(nav_array,compare_number,type,rel):
    element = ""
    global cost_of_search
    cost_of_search += 1
    if rel == supply_string:
        element = "p"
    else:
        element = "s"
    for idx,i in enumerate(nav_array):
        if element in i and ".txt" not in i:
            number_from_i = int(i.replace(element,""))
            if compare_number < number_from_i:
                return nav_array[idx-1]
            if compare_number == number_from_i and type == "I":
                return nav_array[idx+1]
            if compare_number == number_from_i and type == "L" and rel == supply_string:
                return find_array_to_return(nav_array,idx+1)
    return nav_array[len(nav_array) -1]


def search_in_tree(rel, att, op, val,join_array):
    file_to_be_created = rel+"_"+str(int(time.time()))+".txt"
    global cost_of_search
    cost_of_search = 0
    my_content = ""
    schema = []
    result = []
    compare_number = 0
    if rel == supplier_string:
        compare_number = int(val.replace("s", ""))
        f = open(str(page_pool__index_folder) + "\\" + supplier_string+"Temp.txt", "r")
        schema = ["sid","sname","address"]

    if rel == supply_string:
        compare_number = int(val.replace("p", ""))
        f = open(str(page_pool__index_folder) + "\\" + supply_string + "Temp.txt", "r")
        schema = ["sid","pid","cost"]

    file_lines = f.readlines()
    page_to_search = ""
    for i in file_lines:
        node = i.strip().split(":")
        if node[0] == page_to_search or page_to_search == "":
            nav_array = ast.literal_eval(node[1])
            nav = nav_array[len(nav_array)-1]
            page_to_search = get_page_to_search(nav,compare_number,nav_array[0],rel)
            if type(page_to_search) != str:
                page_to_search = str(page_to_search)
            if "page" in page_to_search:
                page = page_to_search.split(".")
                index = page[2]
                page_name = page[0]+".txt"
                if rel == supplier_string:
                    my_content = read_file_content(supplier_data_folder,page_name)
                    if join_array != None:
                        join_array.append(my_content[int(index)])
                    # print(my_content[int(index)])
                    result.append(my_content[int(index)])
                    write_to_file(file_to_be_created,result,schema)
                    cost = cost_of_search
                    # print(
                    #     "With the B+ tree, the cost of searching " + att + " " + op + " " + " " + val + " on " + rel + " is ",
                    #     cost_of_search + 1)  # for reading the record add 1

                else:
                    try:
                        page_to_search  = ast.literal_eval(page_to_search)
                    except:
                        temp_list = []
                        temp_list.append(page_to_search)
                        page_to_search = temp_list
                    for i in page_to_search:
                        page = i.split(".")
                        index = page[2]
                        page_name = page[0] + ".txt"
                        my_content = read_file_content(supply_data_folder, page_name)
                        if join_array != None:
                            join_array.append(my_content[int(index)])
                        # print(my_content[int(index)])
                        result.append(my_content[int(index)])
                        write_to_file(file_to_be_created, result,schema)
                        cost = cost_of_search
                    # print(
                    #     "With the B+ tree, the cost of searching " + att + " " + op + " " + " " + val + " on " + rel + " is ",
                    #     cost_of_search + len(page_to_search))  # for reading the records
    return file_to_be_created


def write_to_file(file,content,schema_array):
    if schema_array != None:
           for i in content:
               for idx,j in enumerate(schema_array):
                   try:
                        i[idx] = i[idx]+":"+j
                   except TypeError:
                       i[idx] = str(i[idx]) + ":" + j
                       # print()

    f = open(str(schemas_path) + "\\" + file, "w+")
    f.write(json.dumps(content, ensure_ascii=False))
    f.close()


def get_result_for_comparison(op, file_content, att,val,cost_initial):
    global cost
    result_array = []
    if len(file_content)>0:
        for i in file_content:
            cost_initial += 1
            record = i
            for j in record:
                if att in str(j):
                    cost_to_compare = j.split(":")
                    check_record(op,val,i,cost_to_compare[0],result_array)
    cost = cost_initial
    return result_array


def select(rel, att, op, val):
    global cost_of_search
    global cost
    cost_of_search = 0
    result_schema = []
    is_tree_existing = is_bplustree_existing(rel)
    result = []
    readSchemas()
    if rel == supplier_string:
        result_schema = ["sid","sname","address"]
        if is_tree_existing and att =="sid" and op == "=":
            cost_of_search = 0
            file = search_in_tree(rel, att, op, val,None)
            print(
                "With the B+ tree, the cost of searching " + att + " " + op + " " + " " + val + " on " + rel + " is ",
                cost_of_search+1+" pages")
            print(file)
            return file
        file_names = get_files(supplier_data_folder)
        # print("fileNames = ", file_names)
        my_result_array = []
        for i in file_names:
            if len(my_result_array) != 0 and att == "sid"  and op == "=":
                break
            h = read_file_content(supplier_data_folder, i)
            cost_of_search += 1
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
        result_schema = ["pid","pname","color"]
        file_names = get_files(product_data_folder)
        # print("fileNames = ", file_names)
        my_result_array = []
        for i in file_names:
            # print("i = ", i)
            h = read_file_content(product_data_folder, i)
            cost_of_search += 1
            if len(my_result_array) != 0 and att == "pid":
                cost_of_search = cost_of_search -1
                break
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
        result_schema = ["sid","pid","cost"]
        if is_tree_existing and att =="pid":
            cost_of_search = 0
            file = search_in_tree(rel, att, op, val,None)
            print(
                "With the B+ tree, the cost of searching " + att + " " + op + " " + " " + val + " on " + rel + " is ",
                str(cost_of_search+1)+" pages")
            print(file)
            return file
        file_names = get_files(supply_data_folder)
        # print("fileNames = ", file_names)
        my_result_array = []
        for i in file_names:
            # print("i = ", i)
            h = read_file_content(supply_data_folder, i)
            cost_of_search += 1
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
    else:
        file_content = read_file_content(schemas_path, rel)
        my_result_list = []
        cost = 0
        if op != "=":
            my_result_list = get_result_for_comparison(op,file_content,att,val,cost)
        else:
            if len(file_content) > 0:
                for i in file_content:
                    cost += 1
                    if val in str(i):
                        my_result_list.append(i)
        cost_of_search = int(cost/2)
            # print("cost of "+rel+" "+att+" "+op+" "+val+" = ",int(cost/2))
        result = my_result_list
    file_to_be_created = ""
    if ".txt" not in rel:
        file_to_be_created = rel+str(int(time.time())) + ".txt"
    else:
        file_to_be_created = "test_"+str(int(time.time())) + ".txt"
    write_to_file(file_to_be_created,result,result_schema)
    print(file_to_be_created)
    print("Without the B+ tree, the cost of searching "+att+" "+op+" "+" "+val+" on "+rel+" is ", str(cost_of_search)+" pages")
    return file_to_be_created

    #
    # for r in result:
    #     print(r)
    #

def addToFinalResult(record, obj, my_result_list, indexes_to_add):
    for i in indexes_to_add:
        obj.append(record[i])
    my_result_list.append(obj)


def get_result_array(file_content, att_list):
    # TODO - project attribute lists
    final_array = []
    str(att_list)
    for i in file_content:
        result_array = []
        for j in att_list:
            for k in i:
                val = str(k)
                if j in val:
                    val = val.split(":")[0]
                    result_array.append(val)
        final_array.append(result_array)
    # print(result_array)
    return final_array

def project(rel, *att_list):
    result_array = []
    if ".txt" not in rel:
        file_to_be_created = rel+str(int(time.time())) + ".txt"
    else:
        file_to_be_created = "test_"+str(int(time.time())) + ".txt"
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
    else:
        file_content = read_file_content(schemas_path,rel)
        result_array = get_result_array(file_content,att_list)
        my_result_list = result_array

    # for r in my_result_list:
    #         print(r)
    print(file_to_be_created)
    write_to_file(file_to_be_created,my_result_list,None)
    return file_to_be_created

join_cost = 0
final_cost = 0

def join_using_tree(rel1, att1, rel2, att2,file_to_be_created):
    global join_cost
    global final_cost
    cost = 0
    p_key = None
    search_in_tree_rel = None
    join_array = []
    final_array =  []
    is_tree_existing_rel1 = is_bplustree_existing(rel1)
    if is_tree_existing_rel1:
        search_in_tree_rel = rel1
    is_tree_existing_rel2 = is_bplustree_existing(rel2)
    if is_tree_existing_rel2:
        search_in_tree_rel = rel2
    if att1 == "pid" or att2 == "pid":
        p_key = "pid"
    if att1 == "sid" or att2 == "sid":
        p_key = "sid"
    if rel1 == supplier_string or rel2 == supplier_string:
        supply_file_names = get_files(supply_data_folder)
        cost = 0
        join_cost = 0
        for i in supply_file_names:
            h = read_file_content(supply_data_folder, i)
            cost += 1
            for j in h:
                join_array = []
                search_in_tree(supplier_string, p_key, "=", j[0], join_array)
                join_cost += cost_of_search+1
                if len(join_array) > 0:
                    for m in join_array:
                        final_array.append(list(dict.fromkeys(j + m)))
    if rel1 == product_string or rel2 == product_string:
        product_file_names = get_files(product_data_folder)
        product_list = []
        join_cost = 0
        for i in product_file_names:
            h = read_file_content(product_data_folder, i)
            cost += 1
            for j in h:
                product_list.append(j)
                join_array = []
                search_in_tree(supply_string,p_key,"=",j[0],join_array)
                join_cost += cost_of_search+1
                if len(join_array) > 0:
                    for m in join_array:
                        final_array.append(list(dict.fromkeys(j+m)))
        # print("done with joining")
    final_cost = cost + join_cost
    print("cost of joining with B+ tree on "+search_in_tree_rel+ " = ",str(cost+join_cost)+" pages")
    try:
        write_to_file(file_to_be_created, final_array)
    except Exception as e:
        # print("join exception = "+e)
        pass

    return file_to_be_created


def join_all_with_sid(sid, file_content,record,cost):
    result = []
    for j in file_content:
        cost += 1
        if sid in str(j):
            j.append(record[1]+":"+"sname")
            j.append(record[2]+":"+"address")
            result.append(j)

    return result


def join_uncommon_relations(rel1, att1, rel2, att2):
    cost = 0
    file_content = []
    supplier_file_names = get_files(supplier_data_folder)
    supplier_list = []
    for i in supplier_file_names:
        h = read_file_content(supplier_data_folder, i)
        for j in h:
            supplier_list.append(j)
    if ".txt" in rel1:
        file_content = read_file_content(schemas_path,rel1)

    if ".txt" in rel2:
        file_content = read_file_content(schemas_path,rel1)
    final_res = []
    cost = 0
    for j in supplier_list:
        cost += 1
        res_array = join_all_with_sid(j[0],file_content,j,cost)
        for m in res_array:
            final_res.append(m)
    print("cost for joining "+rel1+" "+rel2, int(cost/2))
    return final_res


def join(rel1, att1, rel2, att2):
    err = False
    global final_cost
    rel1_string = rel1
    rel2_string = rel2
    if att1 != att2:
        raise AttributeError('Sorry, attributes must be same')
    file_to_be_created = rel1+"_"+rel2+"_"+str(int(time.time()))+".txt"
    tree_on = ""
    if is_bplustree_existing(rel1):
        tree_on = rel1_string
    if is_bplustree_existing(rel2):
        tree_on = rel2_string

    try:
        if is_bplustree_existing(rel1) or is_bplustree_existing(rel2):
            join_using_tree(rel1, att1, rel2, att2,file_to_be_created)
            return file_to_be_created
    except Exception as e:
        # print(e)
        err = True
        pass
    result = []
    cost = 0
    if ".txt" in rel1 or ".txt" in rel2:
        result = join_uncommon_relations(rel1,att1,rel2,att2)
        write_to_file(file_to_be_created, result, None)
        return file_to_be_created


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
    schema_1 = []
    schema_2 = []
    if rel1 == supplier_string:
        rel1 = supplier_list
        if att1 == "sid":
            index_attr_1 = sid_idx
        elif att1 == "sname":
            index_attr_1 = sname_idx
        elif att1 == "address":
            index_attr_1 = address_idx
        schema_1.append("sid")
        schema_1.append("sname")
        schema_1.append("address")
    elif rel1 == product_string:
        rel1 = product_list
        if att1 == "pid":
            index_attr_1 = pid_idx
        elif att1 == "pname":
            index_attr_1 = pname_idx
        elif att1 == "color":
            index_attr_1 = color_idx
        schema_1.append("pid")
        schema_1.append("pname")
        schema_1.append("color")
    elif rel1 == supply_string:
        rel1 = supply_list
        if att1 == "sid":
            index_attr_1 = supply_sid_idx
        elif att1 == "pid":
            index_attr_1 = supply_pid_idx
        elif att1 == "cost":
            index_attr_1 = supply_cost_idx
        schema_1.append("sid")
        schema_1.append("pid")
        schema_1.append("cost")
    if rel2 == supplier_string:
        rel2 = supplier_list
        if att2 == "sid":
            index_attr_2 = sid_idx
        elif att2 == "sname":
            index_attr_2 = sname_idx
        elif att2 == "address":
            index_attr_2 = address_idx
        schema_2.append("sid")
        schema_2.append("sname")
        schema_2.append("address")
    elif rel2 == product_string:
        rel2 = product_list
        if att2 == "pid":
            index_attr_2 = pid_idx
        elif att2 == "pname":
            index_attr_2 = pname_idx
        elif att2 == "color":
            index_attr_2 = color_idx
        schema_2.append("pid")
        schema_2.append("pname")
        schema_2.append("color")
    elif rel2 == supply_string:
        rel2 = supply_list
        if att2 == "sid":
            index_attr_2 = supply_sid_idx
        elif att2 == "pid":
            index_attr_2 = supply_pid_idx
        elif att2 == "cost":
            index_attr_2 = supply_cost_idx
        schema_2.append("sid")
        schema_2.append("pid")
        schema_2.append("cost")
    result = []
    final_schema = []
    cost_rel1 = 0
    cost_rel2 = 0
    for x in rel1:
        cost_rel1 += 1
        for y in rel2:
            cost_rel2 += 1
            if x[index_attr_1] == y[index_attr_2]:
                myobj = []
                try:
                    for idx in range(3):
                        # if idx != index_attr_1:
                        myobj.append(x[idx])
                        if schema_1[idx] not in final_schema:
                            final_schema.append(schema_1[idx])
                        if idx != index_attr_2:
                            myobj.append(y[idx])
                            if schema_2[idx] not in final_schema:
                                final_schema.append(schema_2[idx])
                    result.append(myobj)
                except Exception as e:
                    # print(e)
                    pass
    if not (is_bplustree_existing(rel1_string) or is_bplustree_existing(rel2_string)) and not err:
        print("cost of joining without B tree on "+rel1_string+" and "+rel2_string+" = ", int(int(cost_rel1)/2 +int(cost_rel2)/4))
    # if is_bplustree_existing(rel1_string) and err:
    #     print("cost of joining with B tree on "+rel1_string+ " = ", final_cost)
    # if is_bplustree_existing(rel2_string) and err:
    #     print("cost of joining with B tree on " + rel2_string + " = ", final_cost)
    print(file_to_be_created)
    write_to_file(file_to_be_created,result,final_schema)
    return file_to_be_created

