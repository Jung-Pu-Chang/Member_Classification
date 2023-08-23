import pandas as pd
from MemberClass import MemberClass

data = {'ID': ['666', '666', 123, ''],
        'DATE': ['2016-01-01', '2016-02-01','2016-12-31','2016-08-01'],
        'count': [10,20,0,'3'],
        'cost': [10,10.26,6,'80'],
        }
df = pd.DataFrame(data)

test = MemberClass(data = df, memberID = 'ID', date = 'DATE', quantity = 'count', spend = 'cost') 
LRFM = test.LRFM(2017,1,1)
NES = test.NES(2017,1,1,366,60)
CAI = test.CAI()
