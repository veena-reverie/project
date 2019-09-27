#only take ddmmyy or ddmmyyyy format
from dateutil.parser import parse
import re
def extract_normal_date(string):
    date_list=[]
    final_date_list=[]

    try:
        pattern='\d{1,2}\s?[\.\/-]\s?\d{1,2}\s?[\.\/-]\s?\d{2,4}'
        date_list = re.findall(pattern, string)
        new_string=string
        for date_item in date_list:
            new_string=new_string.replace(date_item,'D@te')
        rem_string=new_string.split('D@te')
        # print(rem_string)


        if date_list:
            for item in date_list:
                date_val=parse(item,fuzzy=True)
                final_date_list.append(date_val.strftime('%d/%m/%Y'))
            # print (date_val.strftime('%d/%m/%Y'))
            return(final_date_list,rem_string)
        else:
            return(None)
    except:
        return(None)

# extract_normal_date('cancel the ticket on 31.12.2019 and 21/1/2019')