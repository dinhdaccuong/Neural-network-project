import os
import numpy as np

#Chuan hoa chuoi loai cua peptits
#Loại bỏ các kí tự dấu cách và kí tự xuống dòng
def Chuan_Hoa_KQ(string):
    i = 0
    for char in string:
        if((char != '+') & (char != '-') & (char != ' ')):
            break
        else:
            i = i + 1
    string_stand = string[0:i:2]
    return string_stand

#Chia va chuan hoa du lieu thanh 2 file chua mau và loại của mẫu
#data_path_name "Duong dan den du lieu dau vao"  dữ liệu copy từ file .pdf
#data_file_name "ten file chua du lieu tho"
#data_input "ten file chua cac chuoi peptits"
#data_result "ten file chua cac chuoi ket qua"
def Data_Process(data_path_name, data_file_name, data_input, data_result): #van con tham so
    os.chdir(data_path_name)
    f_read = open(data_file_name, "r")
    f_write_ip =  open(data_input, "w")
    f_write_rs = open(data_result, "w")
    s_result = ["", "", "", ""] #list luu cac chuoi ket qua s1, s2, s3, 4
    i = 0 
    for line in f_read:
        line_len = len(line)
        if(line_len > 9):
            if(line_len > 60):
                string_stand = Chuan_Hoa_KQ(line) #chuan hoa chuoi ket qua
                for i_ in range(4):
                    if(i_ == i):
                        s_result[i_] = s_result[i_] + string_stand
                i = i + 1
            else:
                i = 0
                f_write_ip.write(line)
                
    for i_ in range(4):
        f_write_rs.write(s_result[i_])
        f_write_rs.write("\n")    
    f_read.close()
    f_write_ip.close()
    f_write_rs.close()
    
#Chia dữ liệu thành 5 phần bằng nhau.
def Div_Data(path_data, name_data, name_lable, path_save):
    path_old = os.getcwd()
    data_part1 = "data1.txt"
    data_part2 = "data2.txt"
    data_part3 = "data3.txt"
    data_part4 = "data4.txt"
    data_part5 = "data5.txt"
    
    lable_part1 = "lable1.txt"
    lable_part2 = "lable2.txt"
    lable_part3 = "lable3.txt"
    lable_part4 = "lable4.txt"
    lable_part5 = "lable5.txt"
    
    
    n_sample1234 = 1278    #Số mẫu của tập 1, 2, 3, 4
    n_sample5 = 1281       #Số mẫu của tập 5
    n_sample = 6393        #Tổng sỗ mẫu
    #Mở file dữ liệu và nhãn của dữ liệu từ file data ban đầu
    os.chdir(path_data)
    f_read_data = open(name_data, "r")
    f_read_lable = open(name_lable, "r")
    
    #Mở file dữ liệu để ghi vào
    os.chdir(path_save)
    
    #Ghi dữ liệu
    f_write_data1 = open(data_part1, "w")
    f_write_data2 = open(data_part2, "w")
    f_write_data3 = open(data_part3, "w")
    f_write_data4 = open(data_part4, "w")
    f_write_data5 = open(data_part5, "w")
    
    #Ghi nhãn
    f_write_lable1 = open(lable_part1, "w")
    f_write_lable2 = open(lable_part2, "w")
    f_write_lable3 = open(lable_part3, "w")
    f_write_lable4 = open(lable_part4, "w")
    f_write_lable5 = open(lable_part5, "w")
    
    list_lable = ["", "", "", ""]
    list_f_w_lable = [f_write_lable1, f_write_lable2, f_write_lable3, f_write_lable4, f_write_lable5]
    
    #Đọc dữ liệu từ file chứa lable vào list
    i = 0
    for line in f_read_lable:
        list_lable[i] += "" + line
        i += 1
        
    #Ghi nhãn dữ liệu từ list lable vào các file part lable
    index = 0
    c = 0
    for j in range(6394):
        if(((j % 1278 == 0) & (j != 6390) & (j != 0)) | (j == 6393)):
            z = 0
            for z in range(4):
                list_f_w_lable[c].write(list_lable[z][index:j])
                list_f_w_lable[c].write("\n")
            index = j
            c += 1
            
            
    i = 0
    #Ghi dữ liệu vào file đã phân loại
    for line in f_read_data:
        if(i < 1278):  #Ghi du lieu vao data1  
            f_write_data1.write(line)
        elif(i < 2556):
            f_write_data2.write(line)
        elif(i < 3834):
            f_write_data3.write(line)
        elif(i < 5112):
            f_write_data4.write(line)
        else:
            f_write_data5.write(line)
        i += 1
    os.chdir(path_old)   
    f_read_data.close() 
    f_read_lable.close()
    
    f_write_data1.close() 
    f_write_data2.close() 
    f_write_data3.close() 
    f_write_data4.close() 
    f_write_data5.close() 
    
    f_write_lable1.close() 
    f_write_lable2.close() 
    f_write_lable3.close() 
    f_write_lable4.close() 
    f_write_lable5.close() 
    
#Phân loại dữ liệu vào các nhóm s1, s2, s3, s4, Có cả phân chia vào negative và positive
def Phan_Loai(file_path, file_name_data, file_name_type, file_path_save):
    s1_name_pos = "s1_pos.txt"
    s1_name_neg = "s1_neg.txt"
    
    s2_name_pos = "s2_pos.txt"
    s2_name_neg = "s2_neg.txt"

    s3_name_pos = "s3_pos.txt"
    s3_name_neg = "s3_neg.txt"

    s4_name_pos = "s4_pos.txt"
    s4_name_neg = "s4_neg.txt"
    
    os.chdir(file_path)
    f_read_data = open(file_name_data, "r")
    f_read_type = open(file_name_type, "r")
    os.chdir(file_path_save)
    f_write_s1_pos = open(s1_name_pos, "w")
    f_write_s2_pos = open(s2_name_pos, "w")
    f_write_s3_pos = open(s3_name_pos, "w")
    f_write_s4_pos = open(s4_name_pos, "w")
    
    f_write_s1_neg = open(s1_name_neg, "w")
    f_write_s2_neg = open(s2_name_neg, "w")
    f_write_s3_neg = open(s3_name_neg, "w")
    f_write_s4_neg = open(s4_name_neg, "w")
    type_string = ["", "", "", ""]
    i = 0
    
    file_pos = [f_write_s1_pos, f_write_s2_pos, f_write_s3_pos, f_write_s4_pos]
    file_neg = [f_write_s1_neg, f_write_s2_neg, f_write_s3_neg, f_write_s4_neg]
    #load du lieu ket qua vao string
    for line in f_read_type:
        type_string[i] = line[0: len(line) - 1]
        i = i + 1
    #Bat dau phan loai
    j = 0 #thu tu cua chuoi trong file data_input
    for line in f_read_data:
        for i in range(4):
            if(type_string[i][j] == '+'):
                file_pos[i].write(line)
            else:
                file_neg[i].write(line)
        j = j + 1
    
    f_read_data.close()
    f_read_type.close()
    f_write_s1_pos.close()
    f_write_s2_pos.close()
    f_write_s3_pos.close()
    f_write_s4_pos.close()
    f_write_s1_neg.close()
    f_write_s2_neg.close()
    f_write_s3_neg.close()
    f_write_s4_neg.close()
