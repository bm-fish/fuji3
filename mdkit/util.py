import os
import csv

def find_num_after_searchstr(line:str, str_to_find:str, dtype="float")->float or int:
    ## The string pattern shall be "PAW double counting   =     78293.39402329   -79313.88379173"
    ## str_to_find = "counting"
    ## Return [78293.39402329,-79313.88379173]
    s_part = line.split(str_to_find)
    if len(s_part) <= 1:
        return None
    else:
        # Check if "=" is included after the keyword, then remove "="
        if "=" in s_part[-1]:
            num_list_str = s_part[-1].split("=")[1].split()[0]
        elif ":" in s_part[-1]:
            num_list_str = s_part[-1].split(":")[1].split()[0]
        else:
            num_list_str = s_part[-1].split()[0]
        
        # print(num_list_str, type(num_list_str))
        if dtype=="float":
            num_list_num = float(num_list_str)
        elif dtype=="int":
            num_list_num = int(num_list_str)
        else:
            raise ValueError("dtype shall be 'int' or 'float'")
        return num_list_num

def make_data_dict_from_keyword_dict(input_dict):
    output_dict = {}
    for key, value in input_dict.items():
        if value is True:
            output_dict[key] = []
        else:
            output_dict[key] = value
    return output_dict

def write_data_dict_to_csv(data_dict:dict, csv_dir):
    len_list_data = []
    for key, item in data_dict.items():
        len_list_data.append(len(item))
    maxlen = max(len_list_data)
    print(maxlen)
    with open(csv_dir, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(list(data_dict.keys()))
    
        for i in range(maxlen):
            line_to_write = []
            for key in data_dict.keys():
                data_len = len(data_dict[key])
                # when the i exesed the current data_len, write empty str
                if i >= data_len:
                    line_to_write.append("")
                else:
                    line_to_write.append(data_dict[key][i])
            writer.writerow(line_to_write)

    


if __name__=="__main__":
    line = "energy without entropy =     -0.64910114  energy(sigma->0) =     -878.57396738"
    line = "  energy without entropy =     -8.39955600  energy(sigma->0) =     -878.33430269"
    line = "    kin. lattice  EKIN_LAT=         0.000000  (temperature  463.81 K)"
    # print(find_num_after_searchstr(line,"temperature",dtype="float"))
    input_dict = {
    "key1": [1,2,3],
    "key2": [10,20,30],
    "key3": [0,0,0],
    "key4": [100,100,100,100]
    }
    write_data_dict_to_csv(input_dict,"test.csv")