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

    for ind, ele in enumerate(s):
        if ele in time_dict_new[lang_dic].keys():
            if lang == 'english':
                time_of_day = time_dict_new[lang_dic][ele]
                prev_word = s[ind - 1]
                if prev_word.isdigit() and int(prev_word) in list(range(13)):
                    num=num
                elif prev_word.isalpha():
                    num = num_dict_new[lang_dic][prev_word]
                    if int(num) in list(range(13)):
                        num=num
                if num and time_of_day:
                    time_list.append(num+' '+time_of_day)
            else:
                time_of_day = time_dict_new[lang_dic][ele]
        elif ele == 'at':
            next_word = s[ind + 1]
            if re.match('1[0-2]|0?[1-9]:([0-5][0-9])?', next_word):
                time_list.append(next_word)

        elif ele in minute_dict[lang_dic].keys():
            min = minute_dict[lang_dic][ele]
            try:
                next_word = s[ind + 1]
                if next_word in num_dict_new[lang_dic].keys():
                    num = num_dict_new[lang_dic][next_word]
                    if ele == 'pYOnE':
                        if num == '1':
                            num = '12'
                        else:
                            num = str(int(num) - 1)
                    else:
                        num = num
            except:
                return ''


        elif ele == 'bajakara' and lang == 'hindi':
            prev_word = s[ind - 1]
            num = num_dict_new[lang_dic][prev_word]

        elif ele == 'hour' or ele == 'hr' or ele == 'hours' or ele == 'GxTA' or ele == 'bajE':
            prev_word = s[ind - 1]
            if prev_word.isdigit():
                hr = prev_word
            elif prev_word.isalpha():
                if prev_word == 'an' and s[ind - 2] != 'half':
                    hr = '1'
                else:
                    hr = num_dict_new[lang_dic][prev_word]

        elif ele == 'minute' or ele == 'min' or ele == 'minutes' or ele == 'minaTa':
            prev_word = s[ind - 1]
            if prev_word.isdigit():
                min = prev_word
            elif prev_word.isalpha():
                min = num_dict_new[lang_dic][prev_word]

        elif ele == 'second' or ele == 'sec' or ele == 'seconds' or ele == 'sEkxD‌sa':
            prev_word = s[ind - 1]
            if prev_word.isdigit():
                sec = prev_word
            elif prev_word.isalpha():
                sec = num_dict_new[lang_dic][prev_word]


        elif ele in relative_time_dict.keys():
            rel_ind = ind
            rel_flag = 1

    if hr or min and rel_flag:
        operator = relative_time_dict[s[rel_ind]]
        current_time = datetime.now()
        change = relativedelta(hours=operator * int(hr), minutes=operator * int(min), seconds=operator * int(sec))
        final_time = (current_time + change).time().strftime('%I:%M:%S %p')
        time_list.append(final_time)
    if min == '':
        min = '00'
    if final_time == '':
        full_time_string = str(num) + ':' + str(min) + ' ' + time_of_day
        full_time_string.replace("  ", " ")
        time_list.append(full_time_string.strip())

    return(time_list)


if __name__ == '__main__':
    load_time()
    load_num()
    load_minute()

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
