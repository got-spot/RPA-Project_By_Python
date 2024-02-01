import mysql.connector, base64, openpyxl, io
from openpyxl import Workbook
 
# Create a connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password='admin',
    database="dart"  # Name of the database
)
 
# Create a cursor object
cursor = mydb.cursor()
 
# Prepare the query
query = "SELECT excel_1, excel_2, excel_3 FROM dart.corp_table where excel_3 is not null limit 2;"
# query = "SELECT * FROM dart.corp_table where induty_code in (SELECT induty_code FROM dart.corp_table where corp_name like '%대한항공%') limit 2;"
 
# Execute the query to get the file
cursor.execute(query)

data = cursor.fetchall()

# data[0][0] # => excel_1 (재무상태표)
# data[0][1] # => excel_2 (손익계산서)
# data[0][2] # => excel_3 (재무분석표)
print(len(data[0]))
# The returned data will be a list of list
for i in range(len(data[0])):
    image = data[0][i]
    binary_data = base64.b64decode(image)
    f = open(f"test{i+1}.xlsx", 'wb')
    f.write(binary_data)
    f.close

# Decode the string
binary_data = base64.b64decode(image)
 
# # 엑셀 파일 저장할 때
# f = open("test.xlsx", 'wb')
# f.write(binary_data)
# f.close

# # OpenPyxl로 열 때
# workbook_xml = io.BytesIO(binary_data)
# workbook_xml.seek(0)
# wb = openpyxl.load_workbook(workbook_xml)
# ws_src = wb.active
# #wb.save('xlsave.xlsx')

# wb_dest = Workbook() # 새 워크북 생성
# ws_dest = wb_dest.active # 현재 활성화된 sheet 가져옴
# ws_dest.title = "원본" # sheet 의 이름을 변경

# # wb_dest.save("sample.xlsx")
# # wb_dest.close()