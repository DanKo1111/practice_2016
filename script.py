# -*- coding: utf-8 -*-

import os, re, json, codecs

exam_texts_dir = os.path.dirname(os.path.abspath(__file__)) + "\\Files_by_exam"
mystem = os.path.dirname(os.path.abspath(__file__)) + "\\mystem.exe"

re_lemma = re.compile("{(.*?)=")

def write_data (path, data):
    json_data = json.dumps(data, ensure_ascii=False, indent=1)  
    json_file = codecs.open (path, 'w', 'utf-8')
    json_file.write (json_data)
    json_file.close()
def read_data (path):
    data_file = codecs.open(path, 'r', 'utf-8')
    data = json.load(data_file)
    data_file.close()
    return data 

def mystem_parsing(input_path, output_path, mystem_dir="C:\\mystem.exe", options="-n -d -e utf-8 -i --eng-gr"): #Парсинг текстов
    os.system(mystem_dir + " " + options + " " + input_path + " " + output_path)

def type_token_ratio(tokens, types):
    return (types/tokens) * 100

def main(path):
    all_exams = []
    for i in os.walk(path):
        c_dir = i[0]
        c_files = i[2]
        exam_data, files_data = data_by_exam(c_dir, c_files)
        if exam_data:
            all_exams.append(exam_data)
    while len(all_exams) > 1:
        first = all_exams.pop()
        second = all_exams.pop()
        all_exams.append(summ_data(first, second))

    final_data = all_exams[0]
    final_summ = final_data[-1]
        
    l = lambda x: x[1]
    sorted_all_dicts = sorted(final_summ.items(), key=l, reverse=True)
    final_data.pop()
    final_data.append(sorted_all_dicts)
    
    write_data(exam_texts_dir + "\\" + "all_exam_data.json", final_data[1:])
    #dict_10, is_ok = quantity(10, final_summ)
    #write_data(exam_texts_dir + "\\" + "all_exam_data_10.json", dict_10)
    dict_3000 = quantity(3000, final_summ)
    write_data(exam_texts_dir + "\\" + "all_exam_data_3000.json", dict_3000)
    dict_5000 = quantity(5000, final_summ)
    write_data(exam_texts_dir + "\\" + "all_exam_data_5000.json", dict_5000)
    dict_10000 = quantity(10000, final_summ)
    write_data(exam_texts_dir + "\\" + "all_exam_data_10000.json", dict_10000)

def quantity(qtt, data):
    qtt_dict = {}
    for i in data:
        if data[i] in qtt_dict:
            qtt_dict[data[i]].append(i)
        else:
            qtt_dict.update({data[i]:[i]})

    rev_qtt_dict = []
    for i in sorted(qtt_dict):
        rev_qtt_dict.append([i, qtt_dict[i]])
    result = []
    rev_qtt_dict.reverse()
    #print(len(rev_qtt_dict))
    edge = 0
    for i in range(len(rev_qtt_dict)):
        qtt -= rev_qtt_dict[i][0]
        if qtt <= 0:
            edge = i
            break
    qtt_part = rev_qtt_dict[edge + 1:]
    qtt_sum = 0
    for i in qtt_part:
        qtt_sum += i[0]
    qtt_part.insert(0, qtt_sum)
    return qtt_part
        
##    print (len(qtt_dict))
##    
##    if len(qtt_dict) >= qtt:
##        left_qtt = 0
##        qtt_part = qtt_dict[qtt:]
##        for i in sorted(qtt_part):
##            result.append([i, qtt_dict[qtt:][i]])
##            left_qtt += len(qtt_dict[qtt:][i])
##        
##        result.append(left_qtt)
##        result.reverse()
##        return result, True
##    else:
##        left_qtt = 0
##        for i in sorted(qtt_dict):
##            result.append([i, qtt_dict[i]])
##            left_qtt += len(qtt_dict[i])
##        
##        result.append(left_qtt)
##        result.reverse()
##        return result, False
    

        
def summ_data(first, second):
    files_data = [first, second]
    exam_data = [[files_data[0][0],files_data[1][0]], files_data[0][1] + files_data[1][1]]
    exam_dict = files_data[1][-1]
    for i in files_data[0][-1]:
        if i in exam_dict:
            exam_dict[i] += files_data[0][-1][i]
        else:
            exam_dict.update({i:files_data[0][-1][i]})
    exam_data.append(len(exam_dict))
    exam_data.append(type_token_ratio(files_data[0][1] + files_data[1][1], len(exam_dict)))
    exam_data.append(exam_dict)

    return exam_data    
    

def data_by_exam(c_dir, c_files):
    if not c_files:
        return None, None
    files_data = []
    for j in c_files:
        files_data.append(data_by_file(c_dir, j))
    exam_data = [[files_data[0][0], files_data[1][0]], files_data[0][1] + files_data[1][1]]
    exam_dict = files_data[1][-1]
    for i in files_data[0][-1]:
        if i in exam_dict:
            exam_dict[i] += files_data[0][-1][i]
        else:
            exam_dict.update({i:files_data[0][-1][i]})
    exam_data.append(len(exam_dict))
    exam_data.append(type_token_ratio(files_data[0][1] + files_data[1][1], len(exam_dict)))

    l = lambda x: x[1]
    sorted_exam_dict = sorted(exam_dict.items(), key=l, reverse=True)

    exam_data.append(sorted_exam_dict)
    write_data(c_dir + "\\" + "exam_data.json", exam_data)
    exam_data.pop()
    exam_data.append(exam_dict)

##    dict_3000, is_ok = quantity(3000, exam_dict)
##    write_data(c_dir + "\\" + "exam_data_3000.json", dict_3000)
##    dict_5000, is_ok = quantity(5000, exam_dict)
##    write_data(c_dir + "\\" + "exam_data_5000.json", dict_5000)
##    dict_10000, is_ok = quantity(10000, exam_dict)
##    write_data(c_dir + "\\" + "exam_data_10000.json", dict_10000)
    
    return exam_data, files_data

def data_by_file(path, name):
    c_path = path + "\\" + name
    mystem_parsing(c_path, os.path.dirname(os.path.abspath(__file__)) + "\\parsing_flag.txt", mystem)

    file = open(os.path.dirname(os.path.abspath(__file__)) + "\\parsing_flag.txt", encoding="utf-8")
    text = file.read()
    file.close()

    tokens = re_lemma.findall(text)
    file_dict = {}
    tokens_len = len(tokens)
    
    for i in range(len(tokens)):
        next_token = tokens[i].replace("?", "")
        if next_token in file_dict:
            file_dict[next_token] += 1
        else:
            file_dict.update({next_token:1})
    types_len = len(file_dict)
    ttr = (types_len/tokens_len)*100

    l = lambda x: x[1]
    sorted_file_dict = sorted(file_dict.items(), key=l, reverse=True)
    #print(sorted_file_dict)
    
    file_data = [name, tokens_len, types_len, type_token_ratio(tokens_len, types_len), file_dict]
    #print(name, tokens_len, types_len)
    write_data(path + "\\" + name[:-3] + "json", [name, tokens_len, types_len, type_token_ratio(tokens_len, types_len), sorted_file_dict])

##    dict_3000, is_ok = quantity(3000, file_dict)
##    write_data(path + "\\" + name[:-4] + "_3000.json", dict_3000)
##    dict_5000, is_ok = quantity(5000, file_dict)
##    write_data(path + "\\" + name[:-4] + "_5000.json", dict_5000)
##    dict_10000, is_ok = quantity(10000, file_dict)
##    write_data(path + "\\" + name[:-4] + "_10000.json", dict_10000)
    return file_data
            


main(exam_texts_dir)
