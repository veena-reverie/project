import re
from pathlib import Path
from dateutil.relativedelta import relativedelta
from datetime import datetime
from enums import Language
from collections import defaultdict
def nested_dict():
    return defaultdict(nested_dict)

languages=[Language.Hindi,Language.English]
lang_dict = {"english":Language.English,'hindi':Language.Hindi}

time_dict_new=nested_dict()
num_dict_new=nested_dict()
minute_dict=nested_dict()
time_div_dict_new=nested_dict()

data_path = Path(Path(__file__).parent).parent / 'project'/'data'
relative_time_dict={'before':-1,'ago':-1,'after':+1,'bAda':+1,'pahalE':-1}


def load_data(fn):
    file_name = fn
    f = data_path / file_name

    if fn == 'minute_dict':
        dict_name = minute_dict
    elif fn == 'num_dict':
        dict_name = num_dict_new
    elif fn == 'time_dict':
        dict_name = time_dict_new
    elif fn == 'time_div_dict':
        dict_name = time_div_dict_new

    with open(f, encoding='utf-8') as fp:
        lines = fp.readlines()
    for line in lines:
        if line.startswith("#"):
            continue
        parts = line.strip().split("\t")
        if len(parts) < 13:
            print("Tab Issue")
            print(line)
            continue
        value = parts.pop(0)

        for lang in languages:
            if lang == Language.English:
                parts[lang.value] = parts[lang.value].lower()

            dict_name[lang][parts[lang.value]] = value


def time_extractor(s,lang):
    time_list=[]
    rel_flag=0
    rel_ind=0
    num=00
    hr=00
    min=00
    sec=00
    final_time=''
    time_of_day = ''

    lang_dic = lang_dict[lang]

    if lang == 'english':
        s = s.lower().strip('\n')
    else:
        #since its revcode no need to convert to lower
        s = s.strip('\n')

    s = s.split()

    for ind, item in enumerate(s):
        if item in time_dict_new[lang_dic].keys():
            time_of_day = time_dict_new[lang_dic][item]

        elif item in relative_time_dict.keys():
            rel_ind = ind
            rel_flag = 1

        elif item in time_div_dict_new[lang_dic].keys():
            key = time_div_dict_new[lang_dic][item]
            prev_word = s[ind - 1]
            if prev_word.isdigit() and int(prev_word) in list(range(13)):
                num = prev_word
            elif prev_word.isalpha() and prev_word in num_dict_new[lang_dic].keys():
                num = num_dict_new[lang_dic][prev_word]
            else:
                num = ''

            if key in ['AM','PM']:
                time_list.append(num +' '+ key)
            elif key == 'o\'clock':
                if time_of_day:
                    time_list.append(num +' '+ time_of_day)
                else:
                    time_list.append(num +' '+ key)

            elif key == 'hour' :
                hr = num
                try:
                    if time_div_dict_new[lang_dic][s[ind+2]] == 'minute' and time_div_dict_new[lang_dic][s[ind+4]] == 'seconds':
                        next_word=s[ind+1]
                        if next_word.isdigit() and int(next_word) in list(range(13)):
                            min = next_word
                        elif next_word.isalpha() and next_word in num_dict_new[lang_dic].keys():
                            min=num_dict_new[lang_dic][next_word]
                        else:
                            min='00'
                        second_word=s[ind+3]
                        if second_word.isdigit() and second_word in list(range(13)):
                            sec = second_word
                        elif second_word.isalpha() and second_word in num_dict_new[lang_dic].keys():
                            sec = num_dict_new[lang_dic][second_word]
                        else:
                            sec = '00'
                        time_list.append(hr + ':' + min +':'+sec+ ' ' + time_of_day)

                    elif time_div_dict_new[lang_dic][s[ind + 2]] == 'minute':
                        next_word = s[ind + 1]
                        if next_word.isdigit() and int(next_word) in list(range(13)):
                            min = next_word
                        elif next_word.isalpha() and next_word in num_dict_new[lang_dic].keys():
                            min = num_dict_new[lang_dic][next_word]
                        else:
                            min = '00'

                        time_list.append(hr+':'+min+' '+time_of_day)
                    else:
                        time_list.append(hr+' '+time_of_day)
                except:
                    hr=num
            elif key == 'minute':
                min = num
                try:
                    if time_div_dict_new[lang_dic][s[ind+2]] == 'seconds':
                        next_word = s[ind+1]
                        if next_word.isdigit() and int(next_word) in list(range(13)):
                            sec = next_word
                        elif next_word.isalpha() and next_word in num_dict_new[lang_dic].keys():
                            sec = num_dict_new[lang_dic][next_word]
                        else:
                            sec = '00'

                        time_list.append(min +':'+sec+ ' ' + time_of_day)
                    else:
                        time_list.append(min +' ' + time_of_day)
                except:
                    min=num
            elif key == 'seconds':
                sec = num
                time_list.append(sec + ' ' + time_of_day)



    # final_time=hr+':'+min+':'+sec+' '+time_of_day
    return(time_list)

if __name__ == '__main__':
    load_data('minute_dict')
    load_data('num_dict')
    load_data('time_dict')
    load_data('time_div_dict')

    fptr = open('test_lines')
    for s in fptr:
        orginal_line = s.strip('\n')
        s = s.strip('\n').replace(',',' ')
        s = s.replace('  ',' ')
        if s.startswith('#') or s == '':
            pass
        else:

            print('input_string:',s)
            lang = 'hindi'

            t = time_extractor(s,lang)
            print('time:',t)
