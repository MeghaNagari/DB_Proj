from program.relAlg import select
from program.relAlg import project


supplier_string = "Suppliers"
product_string = "Products"
supply_string = "Supply"
sid_attr = "sid"
pid_attr = "pid"
query_result_txt = "queryResult.txt"

result = select(supplier_string,sid_attr,"=","s23")
print(result)
project(result,"sname")
#
# from program.remove import removeTree
#
# removeTree(supplier_string,sid_attr)
# result = select(supplier_string,pid_attr,"=","s23")
# displayTable(result,query_result_txt)


# result = join(supplier_string,sid_attr,supply_string,sid_attr)
# file_content = read_file_content(schemas_path,"Suppliers_Supply_1574143652.txt")






