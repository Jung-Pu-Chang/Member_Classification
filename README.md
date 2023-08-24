# Member_Classification
> Using pandas to caculate LRFM NES CAI in python.  
> Author: [Jung-Pu-Chang](https://www.linkedin.com/in/jungpu-chang-024859264/)、[容噗玩Data](https://www.youtube.com/channel/UCmWCMqDKCR56pqd10qNkv3Q)  
> Date: 2023-08-23  
> [Chinese Explain](https://mastertalks.tw/products/data-scientist-resume?ref=pu2)   

## Directory

```bash
.
├── README.md
├── LICENSE
├── requirements.txt
├── MemberClass.py
└── example.py
```

## Example

```bash
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

```

## Module Description : MemberClass.py  

### Def Contents
| def  | purpose |
|:------:|:-------:|
| init | Transform format | 
| LRFM | Caculate LRFM     | 
| NES  | Caculate NES      |
| CAI  | Caculate CAI      |

### MemberClass.def__init__ : 
|  I (input) | O (output) |
|:----------:|:------------:|
|  **粗體**  |  `**粗體**`  |
|   *斜體*   |   `*斜體*`   |
| ~~刪除線~~ | `~~刪除線~~` |

> Chinese Refference 
>> [LRFM](https://tpl.ncl.edu.tw/NclService/pdfdownload?filePath=lV8OirTfsslWcCxIpLbUfqNJzW0J_5fY1AiPKrbU3_wbb2K0Ts9M4JxzFjBu1X1A&imgType=Bn5sH4BGpJw=&key=aAlnA0ah-t7Oq36Cwm4PtTrdg8Lw2BhvkLlDtTfcMr8eVVU9OyINO4qBZJhLTxWd&xmlId=0006815221)  
>> [NES](https://vocus.cc/article/5dce1d50fd8978000159e446)  
>> [CAI](https://ezorderly.com/blog/2020/08/31/CAI/)
