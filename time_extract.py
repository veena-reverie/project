import re
from word2number import w2n
num_dict={'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10,'eleven':11,'twelve':12}
time_dict_hin={'subaha':'AM','SAma':'PM','dOpahara':'PM','bajE':'o\'clock'}
num_dict_hin={'Eka':'1','dO':'2','tIna':'3','cAra':'4','pAxca':'5','Caha':'6','sAta':'7','AHTa':'8','nYO':'9','dasa':'10',
              'gyAraha':'11','bAraha':'12','tEraha':'13','cYOdaha':'14','pxdraha':'15', 'sOlaha':'16', 'satraha':'17', 'aHTAraha':'18',
              'uxnIsa':'19', 'bIsa':'20', 'ikIsa':'21', 'bAIsa':'22', 'tEisa':'23', 'cYObIsa':'24', 'paccIsa':'25', 'CabbIsa':'26',
              'satAisa':'27','aTHTAisa':'28','unatIsa':'29','tIsa':'30','ikatIsa':'31','batIsa':'32','tYExtIsa':'33',
              'cYOxtIsa':'34','pYExtIsa':'35','CatIsa':'36','sYExtIsa':'37','aFdatIsa':'38','unatAlIsa':"39",'cAlIsa':'40',
              'ikatAlIsa':'41','bayAlIsa':'42','tYEtAlIsa':'43','cavAlIsa':'44','pYExtAlIsa':'45','CayAlisa':'46',
              'sYExtAlIsa':'47','aFdatAlIsa':'48','unacAsa':'49','pacAsa':'50','ikyAvana':'51','bAvana':'52','tirapana':'53',
              'cYOvana':'54','pacapana':'55','Cappana':'56','satAvana':'57','aHTAvana':'58','unasaHTa':'59','sAHTa':'60'}
def time_extractor(s,lang):
    time_list=[]
    if lang == 'english':
        s = s.lower().strip('\n')
        tl = re.findall(r'([1 2 3 4 5 6 7 8 9 ][1 2]?\s?pm|[1 2 3 4 5 6 7 8 9 ][1 2]?\s?am)', s)
        for item in tl:
            if item.strip() != 'am' and item.strip() != 'pm':
                time_list.append(item)
        s = s.split()
        num=''
        for ind, ele in enumerate(s):
            if ele == 'pm' or ele == 'am' or ele == 'o\'clock':
                prev_word = s[ind - 1]
                if prev_word.isalpha():
                    num = num_dict[prev_word]
                elif ele == 'o\'clock':
                    if int(prev_word) in list(range(13)):
                        time_list.append(prev_word+ ' ' + ele)
                else:
                    return (time_list)
                if num in list(range(13)):
                    time_list.append(str(num) + ' ' + ele)
                else:
                    return (time_list)
            elif ele == 'at':
                next_word = s[ind + 1]
                if re.match('1[0-2]|0?[1-9]:([0-5][0-9])?', next_word):
                    time_list.append(next_word)


    else:
        s = s.strip('\n').split()
        time_of_day=""
        for ind,item in enumerate(s):
            if item in['subaha','SAma','dOpahara']:
                time_of_day=time_dict_hin[item]
            elif item == 'bajE':
                prev_word=s[ind-1]
                if prev_word in num_dict_hin.keys():
                    num=num_dict_hin[prev_word]
            elif item == 'bajakara':
                if s[ind+2] == 'minaTa':
                    prev_word=s[ind-1]
                    prev_word_num=num_dict_hin[prev_word]
                    next_word=s[ind+1]
                    next_word_num=num_dict_hin[next_word]
                    num=prev_word_num+':'+next_word_num


        full_time_string=num+' '+time_of_day
        time_list.append(full_time_string)





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
            lang = 'hindi'
            t = time_extractor(s,lang)
            print('time:',t)
