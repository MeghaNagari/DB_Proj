from program.relAlg import select, join
from program.relAlg import project
from program.display import displayTable, write_query

supplier_string = "Suppliers"
product_string = "Products"
supply_string = "Supply"
sid_attr = "sid"
pid_attr = "pid"
query_result_txt = "queryResult.txt"


#query-1

result = select(supplier_string,sid_attr,"=","s23")
print(result)
file = project(result,"sname")
print(file)
write_query("Find the name for the supplier ‘s23’ when a B+_tree exists on Suppliers.sid.")
displayTable(file,query_result_txt)

#query-2


result = select(supplier_string,sid_attr,"=","s23")
print(result)
file = project(result,"sname")
print(file)
write_query("Find the name for the supplier ‘s23’ when a B+_tree does not exists on Suppliers.sid.")
displayTable(file,query_result_txt)


#query-3

result = join(supplier_string,"sid",supply_string,"sid")
print(result)
file = select(result,"pid","=","p15")
print(file)
res = project(file,"address")
write_query("Find the address of the suppliers who supplied ‘p15’.")
displayTable(res,query_result_txt)


#query-4
#
result = join(supplier_string,"sid",supply_string,"sid")
print(result)
file = select(result,"pid","=","p20")
print(file)
file_2 = select(file,"sname","=","Kiddie")
print(file_2)
res = project(file_2,"cost")
write_query("What is the cost of ‘p20’ supplied by ‘kiddie’")
displayTable(res,query_result_txt)


#query - 5

result = join(product_string,"pid",supply_string,"pid")
print(result)
file = select(result,"cost",">=","47")
print(file)
file2 = join(file,"sid",supplier_string,"sid")
res = project(file2,"sname","pname","cost")
write_query("For each supplier who supplied products with a cost of 47 or higher, list his/her name, product name and the cost.")
displayTable(res,query_result_txt)


#
# from program.remove import removeTree
#
# removeTree(supplier_string,sid_attr)
# result = select(supplier_string,pid_attr,"=","s23")
# displayTable(result,query_result_txt)


# result = join(supplier_string,sid_attr,supply_string,sid_attr)
# file_content = read_file_content(schemas_path,"Suppliers_Supply_1574143652.txt")






