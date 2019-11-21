from __future__ import annotations
from math import ceil, floor
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

sid_idx = 0
sname_idx = 1
address_idx = 2
pid_idx = 0
pname_idx = 1
color_idx = 2
supply_sid_idx = 0
supply_pid_idx = 1
supply_cost_idx = 2
max_height = 0


def get_files(data_folder_path):
    page_link_file = data_folder_path / "pageLink.txt"
    file_names = page_link_file.read_text()
    # print(fileNames)
    file_array = json.loads(file_names)
    return file_array


def convert_file_content_to_json(file_content):
    lis = json.loads(file_content)
    my_json = json.dumps(lis)
    return my_json


def read_file_content(data_folder, i):
    file_to_open = data_folder / i
    file_content = file_to_open.read_text()
    my_json = convert_file_content_to_json(file_content)
    h = json.loads(my_json)
    return h


myResultArray = []
supplier_list = []
product_list = []
supply_list = []
finalArray = []
supplier_file_list = []
supply_file_list = []
tree_created_on = ""



final_data = []
class FinalObject:
    def __init__(self, height, my_elements,uid,parent_uid,page_name,parent_page,left_sibling_page,right_sibling_page,is_appended):
         self.height = height
         self.my_elements = my_elements
         self.uid = uid
         self.parent_uid = parent_uid
         self.page_name = page_name
         self.parent_page = parent_page
         self.left_sibling_page = left_sibling_page
         self.right_sibling_page = right_sibling_page
         self.is_appended = is_appended




class Node:
    uid_counter = 0
    """
    Base node object.
    Attributes:
        order (int): The maximum number of keys each node can hold. (aka branching factor)
    """

    def __init__(self, order):
        self.order = order
        self.parent: Node = None
        self.keys = []
        self.values = []

        #  This is for Debugging purposes only!
        Node.uid_counter += 1
        self.uid = self.uid_counter

    def split(self) -> Node:  # Split a full Node to two new ones.
        left = Node(self.order)
        right = Node(self.order)
        mid = int(self.order // 2)

        left.parent = right.parent = self

        left.keys = self.keys[:mid]
        left.values = self.values[:mid + 1]

        right.keys = self.keys[mid + 1:]
        right.values = self.values[mid + 1:]

        self.values = [left, right]  # Setup the pointers to child nodes.

        self.keys = [self.keys[mid]]  # Hold the first element from the right subtree.

        # Setup correct parent for each child node.
        for child in left.values:
            if isinstance(child, Node):
                child.parent = left

        for child in right.values:
            if isinstance(child, Node):
                child.parent = right

        return self  # Return the 'top node'

    def get_size(self) -> int:
        return len(self.keys)

    def is_empty(self) -> bool:
        return len(self.keys) == 0

    def is_full(self) -> bool:
        return len(self.keys) == self.order - 1

    def is_nearly_underflowed(self) -> bool:  # Used to check on keys, not data!
        return len(self.keys) <= floor(self.order / 2)

    def is_underflowed(self) -> bool:  # Used to check on keys, not data!
        return len(self.keys) <= floor(self.order / 2) - 1

    def is_root(self) -> bool:
        return self.parent is None


class LeafNode(Node):

    def __init__(self, order):
        super().__init__(order)

        self.prev_leaf: LeafNode = None
        self.next_leaf: LeafNode = None

    def add(self, key, value):  # TODO: Implement improved version
        if not self.keys:  # Insert key if it doesn't exist
            self.keys.append(key)
            self.values.append([value])
            return

        for i, item in enumerate(self.keys):  # Otherwise, search key and append value.
            if key == item:  # Key found => Append Value
                self.values[i].append(value)  # Remember, this is a list of data. Not nodes!
                break

            elif key < item:  # Key not found && key < item => Add key before item.
                self.keys = self.keys[:i] + [key] + self.keys[i:]
                self.values = self.values[:i] + [[value]] + self.values[i:]
                break

            elif i + 1 == len(self.keys):  # Key not found here. Append it after.
                self.keys.append(key)
                self.values.append([value])
                break

    def split(self) -> Node:  # Split a full leaf node. (Different method used than before!)
        top = Node(self.order)
        right = LeafNode(self.order)
        mid = int(self.order // 2)

        self.parent = right.parent = top

        right.keys = self.keys[mid:]
        right.values = self.values[mid:]
        right.prev_leaf = self
        right.next_leaf = self.next_leaf

        top.keys = [right.keys[0]]
        top.values = [self, right]  # Setup the pointers to child nodes.

        self.keys = self.keys[:mid]
        self.values = self.values[:mid]
        self.next_leaf = right  # Setup pointer to next leaf

        return top  # Return the 'top node'


class BPlusTree(object):
    def __init__(self, order=5):
        self.root: Node = LeafNode(order)  # First node must be leaf (to store data).
        self.order: int = order

    @staticmethod
    def _find(node: Node, key):
        for i, item in enumerate(node.keys):
            if key < item:
                return node.values[i], i
            elif i + 1 == len(node.keys):
                return node.values[i + 1], i + 1  # return right-most node/pointer.

    @staticmethod
    def _merge_up(parent: Node, child: Node, index):
        parent.values.pop(index)
        pivot = child.keys[0]

        for c in child.values:
            if isinstance(c, Node):
                c.parent = parent

        for i, item in enumerate(parent.keys):
            if pivot < item:
                parent.keys = parent.keys[:i] + [pivot] + parent.keys[i:]
                parent.values = parent.values[:i] + child.values + parent.values[i:]
                break

            elif i + 1 == len(parent.keys):
                parent.keys += [pivot]
                parent.values += child.values
                break

    def insert(self, key, value):
        node = self.root

        while not isinstance(node, LeafNode):  # While we are in internal nodes... search for leafs.
            node, index = self._find(node, key)

        # Node is now guaranteed a LeafNode!
        node.add(key, value)

        while len(node.keys) == node.order:  # 1 over full
            if not node.is_root():
                parent = node.parent
                node = node.split()  # Split & Set node as the 'top' node.
                jnk, index = self._find(parent, node.keys[0])
                self._merge_up(parent, node, index)
                node = parent
            else:
                node = node.split()  # Split & Set node as the 'top' node.
                self.root = node  # Re-assign (first split must change the root!)

    @staticmethod
    def _borrow_left(node: Node, sibling: Node, parent_index):
        if isinstance(node, LeafNode):  # Leaf Redistribution
            key = sibling.keys.pop(-1)
            data = sibling.values.pop(-1)
            node.keys.insert(0, key)
            node.values.insert(0, data)

            node.parent.keys[parent_index - 1] = key  # Update Parent (-1 is important!)
        else:  # Inner Node Redistribution (Push-Through)
            parent_key = node.parent.keys.pop(-1)
            sibling_key = sibling.keys.pop(-1)
            data: Node = sibling.values.pop(-1)
            data.parent = node

            node.parent.keys.insert(0, sibling_key)
            node.keys.insert(0, parent_key)
            node.values.insert(0, data)

    @staticmethod
    def _borrow_right(node: LeafNode, sibling: LeafNode, parent_index):
        if isinstance(node, LeafNode):  # Leaf Redistribution
            key = sibling.keys.pop(0)
            data = sibling.values.pop(0)
            node.keys.append(key)
            node.values.append(data)
            node.parent.keys[parent_index] = sibling.keys[0]  # Update Parent
        else:  # Inner Node Redistribution (Push-Through)
            parent_key = node.parent.keys.pop(0)
            sibling_key = sibling.keys.pop(0)
            data: Node = sibling.values.pop(0)
            data.parent = node

            node.parent.keys.append(sibling_key)
            node.keys.append(parent_key)
            node.values.append(data)

    @staticmethod
    def _merge_on_delete(l_node: Node, r_node: Node):
        parent = l_node.parent

        jnk, index = BPlusTree._find(parent, l_node.keys[0])  # Reset pointer to child
        parent_key = parent.keys.pop(index)
        parent.values.pop(index)
        parent.values[index] = l_node

        if isinstance(l_node, LeafNode) and isinstance(r_node, LeafNode):
            l_node.next_leaf = r_node.next_leaf  # Change next leaf pointer
        else:
            l_node.keys.append(parent_key)  # TODO Verify dis
            for r_node_child in r_node.values:
                r_node_child.parent = l_node

        l_node.keys += r_node.keys
        l_node.values += r_node.values

    @staticmethod
    def get_prev_sibling(node: Node) -> Node:
        if node.is_root() or not node.keys:
            return None
        jnk, index = BPlusTree._find(node.parent, node.keys[0])
        return node.parent.values[index - 1] if index - 1 >= 0 else None

    @staticmethod
    def get_next_sibling(node: Node) -> Node:
        if node.is_root() or not node.keys:
            return None
        jnk, index = BPlusTree._find(node.parent, node.keys[0])

        return node.parent.values[index + 1] if index + 1 < len(node.parent.values) else None

    def show_bfs(self):
        global max_height
        if self.root.is_empty():
            print('The B+ Tree is empty!')
            return
        queue = [self.root, 0]  # Node, Height... Scrappy but it works

        while len(queue) > 0:
            node = queue.pop(0)
            height = queue.pop(0)
            final_obj = FinalObject(height,node.keys,node.uid,node.parent.uid if node.parent else None,None,None,None,None,False)
            final_data.append(final_obj)
            max_height = height
            if not isinstance(node, LeafNode):
                queue += self.intersperse(node.values, height + 1)
            # print(height, '|'.join(map(str, node.keys)), '\t', node.uid, '\t parent -> ',
            #       node.parent.uid if node.parent else None)

    def get_leftmost_leaf(self):
        if not self.root:
            return None

        node = self.root
        while not isinstance(node, LeafNode):
            node = node.values[0]

        return node

    def get_rightmost_leaf(self):
        if not self.root:
            return None

        node = self.root
        while not isinstance(node, LeafNode):
            node = node.values[-1]

    def show_all_data(self):
        node = self.get_leftmost_leaf()
        if not node:
            return None

        while node:
            for node_data in node.values:
                print('[{}]'.format(', '.join(map(str, node_data))), end=' -> ')

            node = node.next_leaf
        print('Last node')

    def show_all_data_reverse(self):
        node = self.get_rightmost_leaf()
        if not node:
            return None

        while node:
            for node_data in reversed(node.values):
                print('[{}]'.format(', '.join(map(str, node_data))), end=' <- ')

            node = node.prev_leaf
        print()

    @staticmethod
    def intersperse(lst, item):
        result = [item] * (len(lst) * 2)
        result[0::2] = lst
        return result




def is_internal(str):
    return str.__contains__(".Node")


def is_leaf_node(str):
    return str.__contains__(".LeafNode")


def get_page():
    page_pool_file = page_pool__index_folder / "pagePool.txt"
    page_names = page_pool_file.read_text()
    # print(page_names)
    file_array = json.loads(page_names)
    length_file_array = len(file_array)
    if length_file_array == 0:
        print("short of pages in page pool")
        exit()
        return
    page_taken = file_array[length_file_array-1]
    file_array.remove(page_taken)
    f = open(page_pool_file, "w")
    f.write(json.dumps(file_array, ensure_ascii=False))
    f.close()
    return page_taken


def put_in_page(element_list,page_name):
    f = open(str(page_pool__index_folder)+"\\"+page_name, "w")
    f.write(element_list)
    f.close()




def get_parent(parent_uid):
    for i in final_data:
        if i.uid == parent_uid:
            return i



def get_left_child(element, parent_uid):
    for i in final_data:
        if i.parent_uid == parent_uid and i.my_elements[0]<element:
            if i.page_name == None:
                i.page_name = get_page()
            return i
    return None

def get_right_child(element, parent_uid):
    for i in final_data:
        if i.parent_uid == parent_uid and i.my_elements[0] >= element:
            if i.page_name == None:
                i.page_name = get_page()
            return i
    return None

class InternalNode:
    def __init__(self, type, parent,my_content,my_page):
         self.type = type
         self.parent = parent
         self.my_content = my_content
         self.my_page = my_page


class LeafNodeRep:
    def __init__(self, type, parent,left_sibling_page,right_sibling_page,my_content,my_page):
         self.type = type
         self.parent = parent
         self.my_content = my_content
         self.left_sibling_page = left_sibling_page
         self.right_sibling_page = right_sibling_page
         self.my_page = my_page


list_uid = []
supply_product_list = []




def get_data_by_uid(uid):
    for i in final_data:
        if i.uid == uid:
            return i


def get_left_sibling(my_uid):
    j = 0
    while my_uid > list_uid[j]:
        j += 1
    if list_uid[j] == list_uid[0]:
        return None
    else:
        return get_data_by_uid(list_uid[j-1])



def get_right_sibling(my_uid):
    j = 0
    while list_uid[j] < my_uid:
        j += 1
    if list_uid[j] == list_uid[len(list_uid)-1]:
        return None
    else:
        return get_data_by_uid(list_uid[j+1])




def write_internal_node(node):
    list = []
    list.append(node.type)
    list.append(node.parent)
    for i in node.my_content:
        if ".txt" not in str(i):
            idx_to_replace = node.my_content.index(i)
            if tree_created_on == supplier_string:
                node.my_content.remove(i)
                node.my_content.insert(idx_to_replace,supplier_list[i-1][sid_idx])
            else:
                node.my_content.remove(i)
                node.my_content.insert(idx_to_replace, "p"+i)
    list.append(node.my_content)
    put_in_page(json.dumps(list),node.my_page)


def get_pages_list(pid):
    file_list = []
    i = 0
    for i in supply_file_list:
        if i[0] == pid:
            file_list.append(i[1])
    return file_list


def write_leaf_node(leaf):
    list = []
    list.append(leaf.type)
    list.append(leaf.parent)
    list.append(leaf.left_sibling_page)
    list.append(leaf.right_sibling_page)
    contents = leaf.my_content
    actual_contents = []
    pid_string = ""
    for i in contents:
        if ".txt" not in str(i):
                idx_to_replace = leaf.my_content.index(i)
                if tree_created_on == supplier_string:
                    leaf.my_content.remove(i)
                    leaf.my_content.insert(idx_to_replace, supplier_list[i - 1][sid_idx])
                    leaf.my_content.insert(idx_to_replace+1,supplier_file_list[i - 1])
                else:
                    pid_string = "p"+str(i)
                    actual_contents.append(pid_string)
                    pages_to_append = get_pages_list(pid_string)
                    for k in pages_to_append:
                        actual_contents.append(k)
    if tree_created_on == supplier_string:
        list.append(leaf.my_content)
    else:
        list.append(actual_contents)
    put_in_page(json.dumps(list), leaf.my_page)


def write_to_directory(rel, att, my_page):
    f = open(str(page_pool__index_folder) + "\\directory.txt", "a")
    f.write("("+rel+","+att+","+my_page+")\n")
    f.close()


supply_pid_page_list = []
class Supply_Pid_Pages:
    def __init__(self, pid, my_pages):
            self.pid = pid
            self.my_pages = my_pages


def get_first_least(compare_element):
    least = 0
    least_node = ""
    for i in final_data:
        current_element = i.my_elements[len(i.my_elements)-1]
        if int(compare_element) > int(current_element) and least < int(current_element):
            least = int(current_element)
            least_node = i
    if least_node == "":
        return None
    return least_node


def get_left_sibling_new(current_element):
    return get_first_least(current_element)




def get_right_sibling_new(compare_element):
    # first_highest =
    # highest_node = ""
    #
    # for i in final_data:
    #     current_element = i.my_elements[0]
    #     if first_highest == 0:
    #         first_highest = current_element
    #     if int(compare_element) < int(current_element) and int(current_element) > first_highest :
    #         first_highest = int(current_element)
    #         highest_node = i
    # if highest_node.my_elements[0]<compare_element:
    #     return None
    # return highest_node

    least = int(compare_element)+1
    least_node = ""
    for i in final_data:
        current_element = i.my_elements[0]
        if int(compare_element) < int(current_element) and least >= int(current_element):
            least = int(current_element)
            least_node = i
    if least_node == "":
        return None
    return least_node


root_pages = []

def is_bplustree_existing(rel):
    string_content = Path(str(page_pool__index_folder) + "\\directory.txt").read_text()
    if rel in string_content:
        return True
    else:
        return False

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

def create_temp_tree(rel,my_page):
    create_test_tree(rel,my_page)


def build(rel, att, od):
    if is_bplustree_existing(rel):
        print("Sorry, tree already exists")
        return

    global tree_created_on
    if rel == supplier_string:
        tree_created_on = supplier_string
        file_names = get_files(supplier_data_folder)
        for i in file_names:
            h = read_file_content(supplier_data_folder, i)
            for idx,j in enumerate(h):
                supplier_list.append(j)
                supplier_file_list.append(i+"."+str(idx))
        attr = sid_idx
        if att == "sname":
            attr = sname_idx
        elif att == "address":
            attr = address_idx

        bt = BPlusTree(order=(2*od+1))  # 2d+1
        for i in range(1, len(supplier_list) + 1):
            bt.insert(i, supplier_list[i - 1][attr])
        bt.show_bfs()

    elif rel == supply_string:
        tree_created_on = supply_string
        file_names = get_files(supply_data_folder)
        for i in file_names:
            h = read_file_content(supply_data_folder, i)
            for idx,j in enumerate(h):
                supply_list.append(j)
                pid = j[supply_pid_idx]
                if pid not in supply_product_list:
                    supply_product_list.append(j[supply_pid_idx])
                supply_file_list.append([pid, i+"."+str(idx)])
        attr = supply_sid_idx
        if att == "pid":
            attr = supply_pid_idx
        elif att == "cost":
            attr = supply_cost_idx

        bt = BPlusTree(order=(2 * od + 1))  # 2d+1
        for i in range(1, len(supply_product_list) + 1):
            bt.insert(supply_product_list[i-1].strip("p"), supply_product_list[i-1])
        bt.show_bfs()

    for i in final_data:
        i.page_name = get_page()

    for i in final_data:
        if i.parent_uid != None:
            parent = get_parent(i.parent_uid)
            i.parent_page = parent.page_name

    for i in final_data:
        if i.height == max_height:
            list_uid.append(i.uid)

    final_tree = []
    for i in range(len(final_data)):
        final_obj = final_data[i]
        my_elements = final_obj.my_elements
        my_uid = final_obj.uid
        my_content = []
        for x in my_elements:
            left_child = get_left_child(x, my_uid)
            right_child = get_right_child(x, my_uid)
            if left_child != None and left_child.page_name not in my_content:
                my_content.append(left_child.page_name)
            my_content.append(x)
            if right_child != None and right_child.page_name not in my_content:
                my_content.append(right_child.page_name)
        if final_obj.height == 0:
            root_node = InternalNode("I", "Nil", my_content, final_obj.page_name)
            if final_obj.is_appended == False:
                final_tree.append(root_node)
                final_obj.is_appended = True

        if left_child == None or right_child == None:
            # left_sibling = get_left_sibling(final_obj.uid)
            left_sibling = get_left_sibling_new(final_obj.my_elements[0])
            # right_sibling = get_right_sibling(final_obj.uid)
            right_sibling = get_right_sibling_new(final_obj.my_elements[len(final_obj.my_elements)-1])
            leaf_node = LeafNodeRep("L", final_obj.parent_page,
                                    left_sibling.page_name if left_sibling != None else "Nil",
                                    right_sibling.page_name if right_sibling != None else "Nil",
                                    my_content, final_obj.page_name)
            final_tree.append(leaf_node)


        else:
            intenal_node = InternalNode("I", final_obj.parent_page, my_content, final_obj.page_name)
            if final_obj.is_appended == False:
                final_tree.append(intenal_node)
                final_obj.is_appended = True

    for i in final_tree:
        if isinstance(i, InternalNode):
            write_internal_node(i)
        else:
            write_leaf_node(i)

    write_to_directory(rel,att,root_node.my_page)
    print("my root page = "+root_node.my_page)
    create_temp_tree(rel,root_node.my_page)
    return root_node.my_page





# build(supplier_string,"sid",2)
# build(supply_string,"pid",2)

