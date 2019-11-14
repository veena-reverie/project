import re
from pathlib import Path
from dateutil.relativedelta import relativedelta
from datetime import datetime
from enums import Language
from collections import defaultdict

data_path = Path(Path(__file__).parent).parent / 'project' / 'data'


def nested_dict():
    return defaultdict(nested_dict)


time_dict_new = nested_dict()
num_dict_new = nested_dict()
minute_dict = nested_dict()
time_div_dict_new = nested_dict()

languages = [Language.Hindi, Language.English, Language.Malayalam]
lang_dict = {"english": Language.English, 'hindi': Language.Hindi, 'malayalam': Language.Malayalam}

relative_time_dict = {'before': -1, 'ago': -1, 'after': +1, 'bAda': +1, 'pahalE': -1}


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
    num='00'
    number='00'
    rel_ind=0
    rel_flag=0
    time_list=[]
    key=''
    prev_word=''
    time_of_day = ''

    lang_dic = lang_dict[lang]

    if lang == 'english':
        s = s.lower().strip('\n')
    else:
        s = s.strip('\n')

    s = s.split()

    for ind, item in enumerate(s):
        if item in time_dict_new[lang_dic].keys():
            time_of_day = time_dict_new[lang_dic][item]
        elif item in time_div_dict_new[lang_dic].keys():
            try:
                prev_word = s[ind-1]
                if prev_word.isdigit():
                    num = prev_word
                elif prev_word.isalpha() and prev_word in num_dict_new[lang_dic].keys():
                    num = num_dict_new[lang_dic][prev_word]
                else:
                    num = ''
                key = time_div_dict_new[lang_dic][item]
                if key in ['AM','PM']:
                    if int(num) in list(range(13)):
                        time_list.append(num+' '+key)
                    else:
                        pass
                if key == 'hour':
                    prev_word = s[ind - 1]
                    if prev_word.isdigit():
                        hr = prev_word
                    elif prev_word.isalpha():
                        hr = num_dict_new[lang_dic][prev_word]

                elif key == 'minute':
                    prev_word = s[ind - 1]
                    if prev_word.isdigit():
                        min = prev_word
                    elif prev_word.isalpha():
                        min = num_dict_new[lang_dic][prev_word]

                elif key == 'seconds':
                    prev_word = s[ind - 1]
                    if prev_word.isdigit():
                        sec = prev_word
                    elif prev_word.isalpha():
                        sec = num_dict_new[lang_dic][prev_word]
                if item in relative_time_dict.keys():
                    rel_ind = ind
                    rel_flag = 1

            if hr or min and rel_flag:
                operator = relative_time_dict[s[rel_ind]]
                current_time = datetime.now()
                change = relativedelta(hours=operator * int(hr), minutes=operator * int(min),seconds=operator * int(sec))
                final_time = (current_time + change).time().strftime('%I:%M:%S %p')
                time_list.append(final_time)












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
