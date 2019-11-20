from program.relAlg import select, join
from program.relAlg import project
from program.display import displayTable, write_query

supplier_string = "Suppliers"
product_string = "Products"
supply_string = "Supply"
sid_attr = "sid"
pid_attr = "pid"
query_result_txt = "queryResult.txt"

# result = select(supplier_string,sid_attr,"=","s23")
# print(result)
# file = project(result,"sname")
# print(file)
# write_query("Find the name for the supplier ‘s23’ when a B+_tree exists on Suppliers.sid.")
# displayTable(file,query_result_txt)



# result = select(supplier_string,sid_attr,"=","s23")
# print(result)
# file = project(result,"sname")
# print(file)
# write_query("Find the name for the supplier ‘s23’ when a B+_tree does not exists on Suppliers.sid.")
# displayTable(file,query_result_txt)


result = join(supplier_string,"sid",supply_string,"sid")
print(result)
file = select(result,"pid","=","p15")
print(file)
res = project(file,"address")
write_query("Find the address of the suppliers who supplied ‘p15’.")
displayTable(res,query_result_txt)




#
# from program.remove import removeTree
#
# removeTree(supplier_string,sid_attr)
# result = select(supplier_string,pid_attr,"=","s23")
# displayTable(result,query_result_txt)


# result = join(supplier_string,sid_attr,supply_string,sid_attr)
# file_content = read_file_content(schemas_path,"Suppliers_Supply_1574143652.txt")






