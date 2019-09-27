# for 21st nov 2019,nov 24 2019,november 24th 2019
import re
import numpy as np
import dateparser
from dateutil.parser import parse
months=['january','february','march','april','may','june','july','august','september','october','november','december',
    'jan','feb','mar','apr','may','june','july','aug','sep','oct','nov','dec','janavarI','FParavarI','mArca','aprYEla','maI','jUna','julAI','agasta','sitxbara','akTUbara','navxbara','disxbara','janavari',
'Pibravari','mArci','Epril','mE','jUn','jUlYE','AgasTu','sepTexbar','akTObar','navxbar','Disexbar','AgasT']
months_hin={'janavarI':'january','FParavarI':'february','mArca':'march','aprYEla':'april','maI':'may','jUna':'june','julAI':'july','agasta':'august','sitxbara':'september','akTUbara':'october','navxbara':'november','disxbara':'december'}
months_tel={'janavari':'january','Pibravari':'february','mArci':'march','Epril':'april','mE':'may','jUn':'june','jUlYE':'july','AgasTu':'august','AgasT':'august','sepTexbar':'september','akTObar':'october','navxbar':'november','Disexbar':'december'}
def checkConsecutive(l):
    n = len(l) - 1
    return (sum(np.diff(sorted(l)) == 1) >= n)

def extract_month(s):
    mon=''
    pos=''
    for i,token in enumerate(s):
        if token in months:
            mon=token
            pos=i
            break
        else:
            continue
    if mon!='':
        return mon,pos
    else:
        return None,None

def extract_date_wd_month(s,lang):
    normal_string=s
    if lang=='english':
        s = s.lower().strip('\n').split()
    else:
        s = s.split()
    date_list = []
    mon,pos=extract_month(s)
    if mon!=None:
        if lang=='hindi':
            mon=months_hin[mon]
        elif lang=='telugu':
            mon=months_tel[mon]

        date_list.append((mon,pos))
        for ind,item in enumerate(s):
            if item.isnumeric():
                if ind in range(pos-2,pos+3):
                    date_list.append((item,ind))

            #check for 21st,3rd,2nd,20th
            elif item.isalnum():
                if re.match('^\d{1,2}[st nd rd th]',item) and ind in range(pos-2,pos+3):
                    date_list.append((item,ind))


        date_list.sort(key = lambda x: x[1])
        lst=[]
        value_lst=[]
        for item in date_list:
            lst.append(item[1])
            value_lst.append(item[0])
        bvalue=checkConsecutive(lst)
        if bvalue:
            value=" ".join(value_lst)
            if lang=='english':
                rem_string=normal_string.split(value)
            else:
                value_new=' '.join(s[i] for i in lst)
                rem_string=normal_string.split(value_new)
            try:
                date_value=parse(value)
                return(date_value.strftime('%d/%m/%Y'),rem_string)
            except:
                return('Not valid Date','')
    else:
        return None


# # # s='book for 2nd class show on jan 21st, 2019'
# # # # s='FParavarI 28th 2019 kO Eka TikaTa buka karadiyE '
# lang='telugu'
# # # s=s.replace(',',' ')
# s='dayacEsi Pibravari 27 2019 na sITu aDagxDi'
# # s='plIja 21st janavarI 2019 kE liE Eka PlAiTa TikaTa buka kArDO'
# date=extract_date_wd_month(s,lang)
# print(date)
