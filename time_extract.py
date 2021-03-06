import re
from pathlib import Path
from dateutil.relativedelta import relativedelta
from datetime import datetime
from enums import Language
from collections import defaultdict


def nested_dict():
    return defaultdict(nested_dict)


languages = [Language.Hindi, Language.English, Language.Malayalam]
lang_dict = {"english":Language.English,'hindi':Language.Hindi,'malayalam':Language.Malayalam}

time_dict_new=nested_dict()
num_dict_new=nested_dict()
minute_dict=nested_dict()
data_path = Path(Path(__file__).parent).parent / 'project'/'data'
relative_time_dict={'before':-1,'ago':-1,'after':+1,'bAda':+1,'pahalE':-1}

def get_key(string, lang):
    string = string.strip()
    if lang == Language.English:
        string = string.lower()
    return (string)

def load_time():
    global time_dict_new
    f = data_path / 'time_dict'
    with open(f,encoding='utf-8') as fp:
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

            time_dict_new[lang][parts[lang.value]] = value
def load_minute():
    global minute_dict
    f = data_path / 'minute_dict'
    with open(f,encoding='utf-8') as fp:
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

            minute_dict[lang][parts[lang.value]] = value

def load_num():
    global num_dict_new
    f = data_path / 'num_dict'
    with open(f,encoding='utf-8') as fp:
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

            num_dict_new[lang][parts[lang.value]] = value


def time_extractor(s,lang):
    load_time()
    load_num()
    load_minute()
    time_list=[]
    rel_flag=0
    rel_ind=0
    hr=00
    min=00
    sec=00
    final_time=''
    lang_dic = lang_dict[lang]

    if lang == 'english':
        s = s.lower().strip('\n')
        tl = re.finditer(r'([1-9][1 2]?\s?pm|[1-9][1 2]?\s?am)', s)
        for item in tl:
            time_list.append(item.group())
        s = s.split()
        num=''
        for ind, ele in enumerate(s):
            if ele in time_dict_new[lang_dic].keys():
                prev_word = s[ind - 1]
                if prev_word.isalpha():
                    num = num_dict_new[lang_dic][prev_word]
                elif ele == 'o\'clock':
                    if int(prev_word) in list(range(13)):
                        time_list.append(prev_word+ ' ' + ele)
                else:
                    return (time_list)

                if int(num) in list(range(13)):
                    time_list.append(str(num) + ' ' + ele)
                else:
                    return (time_list)

            elif ele == 'at':
                next_word = s[ind + 1]
                if re.match('1[0-2]|0?[1-9]:([0-5][0-9])?', next_word):
                    time_list.append(next_word)
            elif ele == 'hour' or ele == 'hr' or ele == 'hours':
                prev_word=s[ind-1]
                if prev_word.isdigit():
                    hr=prev_word
                elif prev_word.isalpha():
                    if prev_word == 'an' and s[ind-2]!='half':
                        hr = '1'
                    else:
                        hr=num_dict_new[lang_dic][prev_word]

            elif ele =='minute' or ele == 'min' or ele=='minutes':
                prev_word=s[ind-1]
                if prev_word.isdigit():
                    min=prev_word
                elif prev_word.isalpha():
                    min=num_dict_new[lang_dic][prev_word]

            elif ele =='seconds' or ele == 'sec' or ele=='seconds':
                prev_word=s[ind-1]
                if prev_word.isdigit():
                    sec=prev_word
                elif prev_word.isalpha():
                    sec=num_dict_new[lang_dic][prev_word]
            elif ele in relative_time_dict.keys():
                rel_ind=ind
                rel_flag=1
        if hr or min and rel_flag:
            operator=relative_time_dict[s[rel_ind]]
            current_time = datetime.now()
            change = relativedelta(hours=operator*int(hr),minutes=operator*int(min),seconds=operator*int(sec))
            final_time=(current_time+change).time().strftime('%I:%M:%S %p')
            time_list.append(final_time)
    else:
        lang_dic=lang_dict[lang]
        s = s.strip('\n').split()
        time_of_day=""
        num='00'
        min='00'
        for ind,item in enumerate(s):
            if item in time_dict_new[lang_dic].keys():
                time_of_day=time_dict_new[lang_dic][item]

            elif item in minute_dict[lang_dic].keys():
                min = minute_dict[lang_dic][item]
                try:
                    next_word=s[ind+1]
                    if next_word in num_dict_new[lang_dic].keys():
                        num = num_dict_new[lang_dic][next_word]
                        if item == 'pYOnE':
                            if num == '1':
                                num = '12'
                            else:
                                num = str(int(num)-1)
                        else:
                            num = num
                except:
                    return ''

            elif item == 'bajE' and num == '00' and lang == 'hindi':
                prev_word = s[ind-1]
                if prev_word in num_dict_new[lang_dic].keys():
                    num = num_dict_new[lang_dic][prev_word]

            elif item == 'bajakara' and lang=='hindi':
                prev_word = s[ind - 1]
                num = num_dict_new[lang_dic][prev_word]

            elif item == 'GxTA' and lang == 'hindi':
                prev_word = s[ind - 1]
                hr = num_dict_new[lang_dic][prev_word]

            elif item == 'minaTa' and lang == 'hindi':
                prev_word = s[ind-1]
                min = num_dict_new[lang_dic][prev_word]
            elif item in relative_time_dict.keys():
                rel_ind = ind
                rel_flag = 1
        if rel_flag!=0 :
            operator = relative_time_dict[s[rel_ind]]
            current_time = datetime.now()
            change = relativedelta(hours=operator*int(hr),minutes=operator*int(min),seconds=operator*int(sec))
            final_time = (current_time+change).time().strftime('%I:%M:%S %p')
            time_list.append(final_time)


        if min=='':
            min='00'
        if final_time=='':
            full_time_string=num+':'+min+' '+time_of_day
            full_time_string.replace("  "," ")
            time_list.append(full_time_string.strip())
    return(time_list)


if __name__ == '__main__':

    fptr = open('test_lines')
    for s in fptr:
        orginal_line = s.strip('\n')
        s = s.strip('\n').replace(',',' ')
        s = s.replace('  ',' ')
        if s.startswith('#') or s == '':
            pass
        else:

            print('input_string:',s)
            lang = 'english'

            t = time_extractor(s,lang)
            print('time:',t)
