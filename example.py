import pandas as pd
from MemberClass import MemberClass

data = {
        'ID': ['666', '666', 123, '666', ''],  # any type can be caculate
         # only date with ('%Y-%m-%d','%Y/%m/%d','%d-%m-%Y','%d/%m/%Y') can be caculate
        'DATE': ['2016-01-01', '2016-02-01','2016-12-31','2016-08-01','2016-07-02'],
        'count': [10,20.1,0,'3','4'], # only str, int, float can be caculate
        'cost': [10,10.26,6,'80','100'], # only str, int, float can be caculate
        }
df = pd.DataFrame(data)

test = MemberClass(data = df, memberID = 'ID', date = 'DATE', quantity = 'count', spend = 'cost') 
LRFM = test.LRFM(cur_year = 2017, cur_month = 1, cur_day = 1)
NES = test.NES(cur_year = 2017, cur_month = 1, cur_day = 1, period_days = 366, new_def = 60)
CAI = test.CAI()
