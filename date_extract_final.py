from datetime import date,datetime
from nltk.util import everygrams
from date_month import extract_date_wd_month
from date_normal import extract_normal_date
from time_extract import time_extractor
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU

temp_exprsn_eng = {'today':[0,'days'],'today\'s':[0,'days'],'tomorrow':[1,'days'],'tomorrow\'s':[1,'days'],'yesterday':[-1,'days'],
                 'yesterday\'s':[-1,'days'],'day after tomorrow':[2,'days'],'next week':[7,'days'],'last week':[-7,'days'],
                 'sunday':[SU,'weeks'],'monday':[MO,'weeks'],'tuesday':[TU,'weeks'],'wednesday':[WE,'weeks'],'thursday':[TH,'weeks'],
                 'friday':[FR,'weeks'],'saturday':[SA,'weeks']}

#lang other than english dictionary is made with revcode

temp_exprsn_hin = {'Aja':[0,'days'],'kala':[1,'days'],'bitA kala':[-1,'days'],'parasOx':[2,'days'],'agalE saptAha':[7,'days'],
                 'piCalE saptAha':[-7,'days'],'ravivAra':[SU,'weeks'],'sOmavAra':[MO,'weeks'],'mxgalavAra':[TU,'weeks'],
                 'buHdavAra':[WE,'weeks'],'gurUvAra':[TH,'weeks'],'SukravAra':[FR,'weeks'],'SanivAra':[SA,'weeks']}

temp_exprsn_tel = {'nEDu':[0,'days'],'I rOju':[0,'days'],'TuDE':[0,'days'],'TuDEs':[0,'days'],'rEpaTi':[1,'days'],'rEpu':[1,'days'],
                 'TumArO':[1,'days'],'ninna':[-1,'days'],'ninnaTi rOju':[-1,'days'],'esTar DE':[-1,'days'],'elluxDi':[2,'days'],
                 'rEpu tarvAta rOju':[2,'days'],'DE APTar TumArO':[2,'days'],'gaDicina vArx':[-7,'days'],'lAsT vIk':[-7,'days'],
                 'vaccE vArx':[7,'days'],'neksT vIk':[7,'days'],'tadupari vArx':[7,'days'],'gata vArx':[-7,'days'],'AdivArx':[SU,'weeks'],
                 'sOmavArx':[MO,'weeks'],'mxgaLavArx':[TU,'weeks'],'buHdavArx':[WE,'weeks'],'guruvArx':[TH,'weeks'],'SukravArx':[FR,'weeks'],
                 'SanivArx':[SA,'weeks'],'AdivArAniki':[SU,'weeks'],'sOmavArAniki':[MO,'weeks'],'mxgaLavArAniki':[TU,'weeks'],
                 'buHdavArAniki':[WE,'weeks'],'guruvArAniki':[TH,'weeks'],'SukravArAniki':[FR,'weeks'],'SanivArAniki':[SA,'weeks'],
                 'sxDE':[SU,'weeks'],'mxDE':[MO,'weeks'],'TyUs DE':[TU,'weeks'],'veDnes DE':[WE,'weeks'],'Htars DE':[TH,'weeks'],
                 'PrYE DE':[FR,'weeks'],'sATar DE':[SA,'weeks']}

#for identifying next and last

weeks_dict = {'english':{'next':+1,'last':-1},'hindi':{'agalE':+1,'piCalE':-1},'telugu':{'tadupari':+1,'gata':-1,'civari':-1,'vaccE':+1,
                                                                                       'lAsT':-1,'neksT':+1}}

lang_dict = {"english":temp_exprsn_eng,'hindi':temp_exprsn_hin,'telugu':temp_exprsn_tel}

def ngram(string):
    ngram_list = []
    for gm in everygrams(string):
        ngram_list.append(" ".join(gm))
    return(ngram_list)

def get_longest(strn_list,ngram_list):
    unique_ngram = []
    pos_list = []
    for i,e in enumerate(ngram_list):
        if len(ngram_list) == 1:
            return(ngram_list)
        else:
            l = len(e.split())
            try:
                ind = strn_list.index(e)
            except:
                prev = ngram_list[i-1]
            if l == 1:
                unique_ngram.append(e)
            else:
                if prev in e:
                    pos_list.append(i-1)
                    unique_ngram.append(e)
                else:
                    unique_ngram.append(e)

            for pos in pos_list:
                unique_ngram.pop(pos)

    return unique_ngram

def change_datetime (flag_value,y = 0,mt = 0,w = 0,d = 0,week_day = None):
    now = datetime.now()
    change = relativedelta(years =+ y, months =+ mt, weeks =+ w, days =+ d,weekday=week_day)
    expected_day = (now + change).date()
    final_date = expected_day.strftime("%d/%m/%Y")
    return final_date


def date_extract(s,lang):
    org_string = s
    output_string = ''
    ngram_list = []
    modified_list = []
    final_date_list = []
    modified_dict = {}
    day = 0
    w_d = None
    week_inc = ""
    flag_value = 0

    dict_name = lang_dict[lang]

    month_date = extract_date_wd_month(s, lang)
    if month_date != None:
        return(month_date)

    else:
        normal_date = extract_normal_date(org_string)
        if normal_date != None:
            return(normal_date)

        else:
            if lang == 'english':
                s = s.lower().strip('\n').split()
            else:
                #otherwise revcode will be changed
                s = s.strip('\n').split()

            ngram_list = ngram(s)
            for token in ngram_list:
                if token in dict_name.keys():
                    modified_list.append(token)
            if modified_list:
                last_token_list = get_longest(s,modified_list)
            else:
                return ()
            for last_token in last_token_list:
                # rem_string = org_string.split(last_token)
                mod_val, mode = dict_name[last_token]

                if mode == 'days':
                    day = mod_val
                #for next monday ,last saturday
                if mode == 'weeks':
                    if len(last_token.split())>1:
                        ind = s.index(last_token.split()[0])
                    else:
                        ind = s.index(last_token)
                    prev_token = weeks_dict[lang]

                    if s[ind-1] in prev_token.keys():
                        week_inc = prev_token[s[ind-1]]
                        flag_value = 1
                        last_token = s[ind-1]+' '+last_token
                        # rem_string=org_string.split(last_token)

                    if week_inc:
                        w_d = mod_val(week_inc)
                    else:
                        w_d = mod_val

                final_date = change_datetime(flag_value,d = day,week_day = w_d)
                if flag_value == 1:
                    todays_date = datetime.today().strftime('%d/%m/%Y')
                    if final_date == todays_date:
                        w_d = mod_val(week_inc+week_inc)
                        final_date = change_datetime(flag_value, d = day, week_day = w_d)
                modified_dict[last_token] = final_date

            # final_date = expected_day.strftime("%d/%m/%Y")
            if modified_dict:
                new_string = org_string
                for k, v in modified_dict.items():
                    final_date_list.append(v)
                    new_string = new_string.replace(k,"D@te")
                rem_string = new_string.split('D@te')
            return(final_date_list,rem_string)


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
            d = date_extract(s,lang)
            t=time_extractor(s,lang)

            if d!=():
                print('Date:',d[0])
            else:
                print('Date:',d)
            if t!=[]:
                print('time:',t)
            else:
                print('Time:','')


