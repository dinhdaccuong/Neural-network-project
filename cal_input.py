#Lớp tính số lần xuất hiện của các kí tự
#Lớp sẽ tính toán số lần xuất hiện của các kí tự tại các vị trí khác nhau trên toàn bộ các chuỗi có trong file
import numpy as np
import os
#Chuyển đổi kí tự sang dạng số
def Convert(char):
    char_dir = {'A':0, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8, 'K':10, 'L':11, 'M':12, 'N':13, 'P':15, 'Q':16, 'R':17, 'S':18, 'T':19, 'V':21, 'W':22, 'Y':24}        
    return char_dir[char]

class Count:
    def __init__(self, file_path, file_data):
        self.freq_appear_X = np.zeros((25, 27), dtype = int) #freq_appear_X[3][4][5] Kí tự 3 xuất hiện ở vị trí thứ 4
                                                             #và kí tự 5 xuất hiện ở vị trí thú 4 + 1 5 lần
        self.freq_appear_XY = np.zeros((25, 27, 27), dtype = int)
        self.file_path = file_path
        self.file_data = file_data
        self.sum_line = 0
    def Count_(self):
        path_old = os.getcwd()
        os.chdir(self.file_path)
        f_read = open(self.file_data, "r")
        self.sum_line = sum(1 for i in f_read)
        f_read.close()
        f_read = open(self.file_data, "r")
        for line in f_read:
            line_stand = line[0: len(line)-1]
            i = 0
            for char in line_stand:
                num = Convert(char)
                self.freq_appear_X[num][i] += 1
                i = i + 1
            for i_ in range(len(line_stand)-1):
                num1 = Convert(line_stand[i_])
                num2 = Convert(line_stand[i_+1])
                self.freq_appear_XY[num1][i_][num2] += 1
        os.chdir(path_old)
        f_read.close()
        
        
        
#Lớp xác xuất có thuộc tính chứa ma trận xác xuất đầu vào cho mạng
#Số cột của ma trận đầu vào là số 

#THAM SỐ
    #file_path: Đường dẫn đến file cần tính xác xuất
    #file_name_train: Tên file chứa chuỗi cần tính xác xuất
    #file_name_pos: Tên file postive
    #file_name_neg: Tên file negative
    #file_path_pro: Đường dẫn đến file làm mẫu để tính xác xuất
#Lớp xác xuất có thuộc tính chứa ma trận xác xuất đầu vào cho mạng
#Số cột của ma trận đầu vào là số 
class Probability:
    def __init__(self, file_path, file_name_train, file_name_pos, file_name_neg, file_path_pro):
        self.file_path = file_path
        self.file_name_train = file_name_train
        self.file_name_pos = file_name_pos
        self.file_name_neg = file_name_neg
        self.file_path_pro = file_path_pro
        self.count_pos = Count(self.file_path_pro, self.file_name_pos)
        self.count_neg = Count(self.file_path_pro, self.file_name_neg)
    def Cal_Probability(self):
        os.chdir(self.file_path) 
        f_read = open(self.file_name_train, "r") #Mở file để đọc
        sum_line = sum(1 for i in f_read) #Số dãy trong tập train ~ số mẫu ~ số cột của ma trận xác xuất
        f_read.close()
        
        self.prop_matrix = np.zeros((26, sum_line)) #ma tran xac xuat cua tap train doi voi loai Sx
        self.count_pos.Count_() #Tính số lần xuất hiện của các kí tự trong tập negative
        self.count_neg.Count_() #Tính số lần xuất hiện của các kí tự trong tập positive
        j = 0
        
        os.chdir(self.file_path)
        f_read1 = open(self.file_name_train, "r")
        for line in f_read1:
            i = 0
            for i in range(len(line)-1):
                num1 = Convert(line[i])
                if(i <= 12):
                    if( i == 12):     #vi tri R-1
                        prop_pos = float(self.count_pos.freq_appear_X[num1][i])/self.count_pos.sum_line
                        prop_neg = float(self.count_neg.freq_appear_X[num1][i])/self.count_neg.sum_line
                    else:
                        num2_1 = Convert(line[i+1])
                        if(self.count_pos.freq_appear_X[num2_1][i+1] != 0):
                            prop_pos = float(self.count_pos.freq_appear_XY[num1][i][num2_1])/self.count_pos.freq_appear_X[num2_1][i+1]
                        else:
                            prop_pos = 0
                        if(self.count_neg.freq_appear_X[num2_1][i+1] != 0):
                            prop_neg = float(self.count_neg.freq_appear_XY[num1][i][num2_1])/self.count_neg.freq_appear_X[num2_1][i+1]
                        else:
                            prop_neg = 0
                    self.prop_matrix[i][j] = prop_pos-prop_neg
                elif(i >= 14):
                    if(i == 14):
                        prop_pos = float(self.count_pos.freq_appear_X[num1][i])/self.count_pos.sum_line
                        prop_neg = float(self.count_neg.freq_appear_X[num1][i])/self.count_neg.sum_line
                    else:
                        num2_2 = Convert(line[i-1])
                        if(self.count_pos.freq_appear_X[num2_2][i-1] != 0):
                            prop_pos = float(self.count_pos.freq_appear_XY[num2_2][i-1][num1])/self.count_pos.freq_appear_X[num2_2][i-1]          
                        else:
                            prop_pos = 0
                        if(self.count_neg.freq_appear_X[num2_2][i-1] != 0):
                            prop_neg = float(self.count_neg.freq_appear_XY[num2_2][i-1][num1])/self.count_neg.freq_appear_X[num2_2][i-1]
                        else:
                            prop_neg = 0
                    self.prop_matrix[i-1][j] = prop_pos-prop_neg
            j += 1
        f_read1.close()
        self.prop_matrix = self.prop_matrix.T
        return self.prop_matrix