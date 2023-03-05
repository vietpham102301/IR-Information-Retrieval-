"""
Thông tin thành viên nhóm 5
    Lê Quang Phục - N19DCCN143
    Phạm Hoàng Việt N19DCCN226
    Nguyễn Thanh Sang N19DCCN156
"""

import re

""" 
    Bài 1 : Ma trận đánh dấu 
    A) Lưu trữ 
"""


def Bai1a(doc):
    """ Tiền xử lý văn bản từ file được định dạng từ file doc-text nên tiền xử lý sẽ xử lý theo bố cục file doc-text"""
    # Chuyển về dạng chữ thường
    doc.lower()
    # Tách số và ký tự xuống dòng  khỏi văn bản gốc
    doc = re.sub(r'\d+', ' ', doc)
    doc = re.sub(r'\n', ' ', doc)
    """ Tạo một list để lưu trữ văn bản và đánh dấu chúng """
    # Tách file thành từng đoạn văn bản và lưu vào trong list
    doc1 = doc.split("/")
    lt = []
    for i in doc1:
        if i:
            lt.append(i.split())
    """Tạo tập hợp từ xuất hiện trong tất cả văn bản và sắp xếp từ A -> Z"""
    # Tạo từ điển
    dic = re.sub(r'/', ' ', doc)
    dic = dic.split()
    dic = list(set(dic))
    dic.sort()
    """ Xử lý chính và lưu trữ chúng """
    # Lưu trữ ma trận dấu
    matrix = [[0 for j in range(len(dic))] for i in range(len(lt))]
    matrix.insert(0, dic)
    for k in lt:
        for i in k:
            for j in dic:
                if i == j:
                    matrix[lt.index(k) + 1][dic.index(j)] = 1
                    break
    return matrix


""" 
    B) Truy vấn dữ liệu 

"""


def find(matrix, text):
    kq = None
    for a in matrix[0]:
        if a == text:
            kq = [row[matrix[0].index(a)] for row in matrix]
    return kq




def find(matrix, text):
    kq = None
    for a in matrix[0]:
        if a == text:
            kq = [row[matrix[0].index(a)] for row in matrix]
    return kq



def operator(l,matrix):
    lt = l.split()
    temp = []
    i = 0
    for k in lt:
        temp.append(find(matrix,k))
    while i < len(lt):
        if lt[i] == "NOT":
            if i + 1 < len(lt):
                for a in range(len(temp[i+1])-1):
                    temp[i+1][a+1] = int(not temp[i+1][a+1])
                del lt[i]
                del temp[i]
            else:
                print("Invalid expression")
                break
        else:
            i += 1
    while len(lt) > 1:
        if lt[1] == "AND":
            for a in range(len(temp[0])-1):
                temp[0][a+1] = int(temp[0][a+1] and temp[2][a+1])
            del lt[1:3]
            del temp[1:3]
        elif lt[1] == "OR":
            for a in range(len(temp[0])-1):
                temp[0][a+1] = int(temp[0][a+1] or temp[2][a+1])
            del lt[1:3]
            del temp[1:3]
    del temp[0][0]
    temp[0].insert(0,"kq")
    return temp


if __name__ == "__main__":
    # cau a
    with open("resource/doc-text") as f:
        doc = f.read()
        matrix = Bai1a(doc)

    # cau b
    kw = "an AND for AND NOT axes AND NOT logic OR of"
    print(operator(kw, matrix))
    for i in matrix:
        print(i)
