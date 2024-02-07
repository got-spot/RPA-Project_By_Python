import mysql.connector, base64, openpyxl, io
from openpyxl import Workbook
from appendSheet import appendSheet

def getExcelStreamByCompanyName(corp):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password='admin',
        database="dart"  # Name of the database
    )
    
    cursor = mydb.cursor()
    # query = "SELECT  excel_1, excel_2, excel_3, stock_name FROM dart.corp_table where excel_3 is not null limit 5;"
    # query = f"SELECT  excel_1, excel_2, excel_3, stock_name FROM dart.corp_table where stock_name like '%{corp}%' limit 5;"
    query = f"SELECT excel_1, excel_2, excel_3, stock_name, bizr_no FROM dart.corp_table where bizr_no in "+corp+" limit 30;"

    cursor.execute(query)

    data = cursor.fetchall()

    # data[0][0] # => excel_1 (재무상태표)
    # data[0][1] # => excel_2 (손익계산서)
    # data[0][2] # => excel_3 (재무분석표)

    wb_dest = Workbook() # 새 워크북 생성
    ws_dest = wb_dest.active # 현재 활성화된 sheet 가져옴
    ws_dest.title = "원본" # sheet 의 이름을 변경

    start_row = 1
    start_col = 1
    row_offset = 1
    col_offset = 2
    # return str(len(data))
    for company in range(len(data)):
        ws_dest.cell(row = start_row, column = start_col, value = data[company][3] )
        start_row += 1
        if company > 0: 
            col_offset = 3
        for i in range(3):
            image = data[company][i]
 
            if image == None:
                # print(data[company][3])
                continue
        # Decode the string
            binary_data = base64.b64decode(image)
        
        # # 엑셀 파일 저장할 때
        # f = open("test.xlsx", 'wb')
        # f.write(binary_data)
        # f.close

        # OpenPyxl로 열 때
            workbook_xml = io.BytesIO(binary_data)
            workbook_xml.seek(0)
            wb = openpyxl.load_workbook(workbook_xml)
            ws_src = wb.active
            end_row, end_col = appendSheet(ws_dest, start_row, start_col, ws_src, row_offset, col_offset)
            start_row = end_row
        end_col += 1
        start_col = end_col
        start_row = 1

    #wb_dest.save("merged.xlsx")
    output = io.BytesIO()
    wb_dest.save(output)
    wb_dest.close()
    return output