from openpyxl import Workbook, load_workbook
import re
wb = Workbook()
ws = wb.active()
ws.title = "동종업종"
data = []

def same_area(): #파일 갯수 만큼 -> 한 업체당 엑셀 표 3개
    filename = re.compile("^ETFI")
    b = load_workbook(filename)
    bs = b["동종업종"] # Dict 로 sheet 접근
    
    j=3 # 3행 부터
    while True:
        data.append(
            [
                bs["B{}".format(j)].value, 
                bs["C{}".format(j)].value, 
                bs["D{}".format(j)].value, 
                bs["E{}".format(j)].value
            ]
        )
        j = j+1
        if bs["B{}".format(j)].value == None:
            break
# print(data)

wb["동종업종"]["B2"] = "판매코드"
wb["동종업종"]["C2"] = "지점"
wb["동종업종"]["D2"] = "종류"
wb["동종업종"]["E2"] = "가격"
for i in range(len(data)):
    wb["동종업종"]["B{}".format(i+3)] = data[i][0]
    wb["동종업종"]["C{}".format(i+3)] = data[i][1]
    wb["동종업종"]["D{}".format(i+3)] = data[i][2]
    wb["동종업종"]["E{}".format(i+3)] = data[i][3]

wb.save("동종업종.xlsx")
wb.close()