import wikipedia as wiki
import re
import pandas as pd

data = pd.read_csv("names.csv", names=['num','name'])
names = list(data['name']) 

yils = []
for n in names:
    try:
        p = wiki.page(wiki.search('nba '+n)[0])
        print('-',end='')
        sum = p.summary
        print('-',end='')
        draft_year = int(re.findall(r'([0-9]+)+ (NBA)? draft', sum)[0][0])
        print('- ',end='')
        yil = 2015 - draft_year
        print("{} - {} - {:2}".format(n, draft_year, yil))
        yils.append(yil)
    except:
        print("Fail at {}".format(n))
        yils.append(-1)

data['yil'] = yils
data.to_csv(r'./temp.csv')
