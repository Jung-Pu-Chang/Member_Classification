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

### 0. Def Contents
| def  | purpose |
|:------:|:-------:|
| init | Transform format | 
| LRFM | Caculate LRFM in python    | 
| NES  | Caculate NES  in python    |
| CAI  | Caculate CAI  in python    |

### 1. def__init__ : 
|  Parameter | Discription | Type |
|:----------:|:------------:|:------------:|
|  **data**  |  **raw data**  | **data.frame**  |
|  **memberID**  |  **col name of customerID**  | **str**  |
|  **date**  |  **col name of date**  | **str**  |
|  **quantity**  |  **col name of consuming times**  | **str**  |
|  **spend**  |  **col name of consuming amount**  | **str**  |

### 2. def LRFM :  
> * L : L_raw_days = first_consuming_date - last_consuming_date, L_raw_days ≥ mean(L_raw_days) = 1, oterwise = 0, every member contact days  
> * R : R_raw_days = current_date - last_consuming_date, R_raw_days < mean(R_raw_days) = 1, oterwise = 0, how long every member days  
> * F : count(quantity) ≥ mean(count(quantity)) = 1, oterwise = 0, every member consumes frequency per day (eg : Member A consumes five times(five envoices) in 2023/8/24, his F = 1)
> * M : sum(spend) ≥ mean(sum(spend)) = 1, oterwise = 0, Sum of every member amount of consuming 
> * LRFM_score_sum ∈ [0,4] = L + R + F + M

|  Parameter | Discription | Type |
|:----------:|:------------:|:------------:|
|  **cur_year**  |  **current year**  | **int**  |
|  **cur_month**  |  **current month**  | **int**  |
|  **cur_day**  |  **current day**  | **int**  |

### 3. def NES : 
> * NES : N = new customer = R_raw_days < new_def，E = freq_ratio ≤ 2，2 < S1 ≤ 2.5，2.5 < S2 ≤ 3，3 < S3
> * count
> * freq
> * freq_ratio
> * R_raw_days = current_date - last_consuming_date

|  Parameter | Discription | Type |
|:----------:|:------------:|:------------:|
|  **cur_year**  |  **current year**  | **int**  |
|  **cur_month**  |  **current month**  | **int**  |
|  **cur_day**  |  **current day**  | **int**  |
|  **period_days**  |  **raw data period days**  | **int**  |
|  **new_def**  |  **new customer definition : current_date - last_consuming_date**  | **int**  |

### 4. def CAI : 
> * CAI : < 0 = 0 > 0
> * weight : R_raw_days = current_date - last_consuming_date, R_raw_days < mean(R_raw_days) = 1, oterwise = 0, how long every member days  
> * avg_freq : count(quantity) ≥ mean(count(quantity)) = 1, oterwise = 0, every member consumes frequency per day (eg : Member A consumes five times(five envoices) in 2023/8/24, his F = 1)
> * w_avg_freq : sum(spend) ≥ mean(sum(spend)) = 1, oterwise = 0, Sum of every member amount of consuming 

## Refference
> Chinese Refference 
>> [LRFM](https://tpl.ncl.edu.tw/NclService/pdfdownload?filePath=lV8OirTfsslWcCxIpLbUfqNJzW0J_5fY1AiPKrbU3_wbb2K0Ts9M4JxzFjBu1X1A&imgType=Bn5sH4BGpJw=&key=aAlnA0ah-t7Oq36Cwm4PtTrdg8Lw2BhvkLlDtTfcMr8eVVU9OyINO4qBZJhLTxWd&xmlId=0006815221)  
>> [NES](https://vocus.cc/article/5dce1d50fd8978000159e446)  
>> [CAI](https://ezorderly.com/blog/2020/08/31/CAI/)
