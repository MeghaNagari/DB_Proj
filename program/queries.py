from program.buildTree import build
from program.relAlg import select
from program.display import displayTree
from program.display import displayTable
from program.relAlg import read_file_content
from program.relAlg import schemas_path
from program.relAlg import join

supplier_string = "Suppliers"
product_string = "Products"
supply_string = "Supply"
sid_attr = "sid"
pid_attr = "pid"
query_result_txt = "queryResult.txt"

result = select(supplier_string,sid_attr,"=","s23")
displayTable(result,query_result_txt)
#
# from program.remove import removeTree
#
# removeTree(supplier_string,sid_attr)
# result = select(supplier_string,pid_attr,"=","s23")
# displayTable(result,query_result_txt)


# result = join(supplier_string,sid_attr,supply_string,sid_attr)
# file_content = read_file_content(schemas_path,"Suppliers_Supply_1574143652.txt")














print(bt)
