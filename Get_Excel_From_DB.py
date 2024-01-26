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
query = "SELECT excel_1 FROM dart.corp_table WHERE stock_name = '진에어'"
 
# Execute the query to get the file
cursor.execute(query)
 
data = cursor.fetchall()
 
# The returned data will be a list of list
image = data[0][0]
 
# Decode the string
binary_data = base64.b64decode(image)
 
# 엑셀 파일 저장할 떄
#f = open("test.xlsx", 'wb')
#f.write(binary_data)
#f.close

 
# OpenPyxl로 열 떄

workbook_xml = io.BytesIO(binary_data)
workbook_xml.seek(0)
wb = openpyxl.load_workbook(workbook_xml)
ws_src = wb.active
#wb.save('xlsave.xlsx')

wb_dest = Workbook() # 새 워크북 생성
ws_dest = wb_dest.active # 현재 활성화된 sheet 가져옴
ws_dest.title = "원본" # sheet 의 이름을 변경

# wb_dest.save("sample.xlsx")
# wb_dest.close()