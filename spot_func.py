from datetime import datetime,timedelta,date
import sqlite3


def CalculateCurrentDayPivot(open_list,close_list,high_list,low_list,currency_pair_list):
    calculation_dict={'Standard':[],'Woodie':[],'Camrarilla':[],'Fibonacci':[],'Final':[]} #R1,R2,R3,PP,S1,S2,S3 values in list in order
    for o,c,h,l,pair in zip(open_list,close_list,high_list,low_list,currency_pair_list):
        o=float(o)
        c=float(c)
        h=float(h)
        l=float(l)
        #standard
        pp = (h+l+c)/3
        r1 = (2*pp)-l
        r2 = pp+(h-l)
        r3 = h+ 2*(pp-l)
        s1 = (2*pp) - h
        s2 = pp-(h-l)
        s3 = l-2*(h-pp)
        if pair=='usd/inr' and s3-r3>0.5:
            s3 = (s2+s3)/2
        
        calculation_dict['Standard'].append(r3)
        calculation_dict['Standard'].append(r2)
        calculation_dict['Standard'].append(r1)
        calculation_dict['Standard'].append(pp)
        calculation_dict['Standard'].append(s1)
        calculation_dict['Standard'].append(s2)
        calculation_dict['Standard'].append(s3)

        pp,r1,r2,r3,s1,s2,s3 = 0,0,0,0,0,0,0

        #Woodie 
        pp = (o+o+h+l)/4
        r1 = (2*pp)-l
        r2 = pp+(h-l)
        r3 = h+2*(pp-l)
        s1 = 2*pp-h
        s2 = pp-(h-l)
        s3 = l-2*(h-pp)

        if pair=='usd/inr' and s3-r3>0.5:
            s3 = (s2+s3)/2

        calculation_dict['Woodie'].append(r3)
        calculation_dict['Woodie'].append(r2)
        calculation_dict['Woodie'].append(r1)
        calculation_dict['Woodie'].append(pp)
        calculation_dict['Woodie'].append(s1)
        calculation_dict['Woodie'].append(s2)
        calculation_dict['Woodie'].append(s3)

        pp,r1,r2,r3,s1,s2,s3 = 0,0,0,0,0,0,0

        #Camrarilla

        pp = (h+l+c)/3
        r1 = c+((h-l)*1.0833)
        r2  = c+((h-l)*1.1666)
        r3 = c+((h-l)*1.2500)
        s1 = c-((h-l)*1.0833)
        s2 = c-((h-l)*1.1666)
        s3 = c-((h-l)*1.2500)

        if pair=='usd/inr' and s3-r3>0.5:
            s3 = (s2+s3)/2
        
        calculation_dict['Camrarilla'].append(r3)
        calculation_dict['Camrarilla'].append(r2)
        calculation_dict['Camrarilla'].append(r1)
        calculation_dict['Camrarilla'].append(pp)
        calculation_dict['Camrarilla'].append(s1)
        calculation_dict['Camrarilla'].append(s2)
        calculation_dict['Camrarilla'].append(s3)

        pp,r1,r2,r3,s1,s2,s3 = 0,0,0,0,0,0,0

        #Fibonacci

        pp = (h+l+c)/3
        r1 = pp+(0.382*(h-l))
        r2 = pp+(0.618*(h-l))
        r3 = pp+(1.0*(h-l))
        s1 = pp-(0.382*(h-l))
        s2 = pp-(0.618*(h-l))
        s3 = pp+(1.0*(h-l))

        if pair=='usd/inr' and s3-r3>0.5:
            s3 = (s2+s3)/2

        calculation_dict['Fibonacci'].append(r3)
        calculation_dict['Fibonacci'].append(r2)
        calculation_dict['Fibonacci'].append(r1)
        calculation_dict['Fibonacci'].append(pp)
        calculation_dict['Fibonacci'].append(s1)
        calculation_dict['Fibonacci'].append(s2)
        calculation_dict['Fibonacci'].append(s3)

        pp,r1,r2,r3,s1,s2,s3 = 0,0,0,0,0,0,0

        #calculate final
        loop_counter_stop = 7
        loop_counter_start = 0
        for i in range(loop_counter_start,loop_counter_stop):
            calculation_dict['Final'].append((calculation_dict['Standard'][i]+calculation_dict['Woodie'][i]+calculation_dict['Camrarilla'][i]+calculation_dict['Fibonacci'][i])/4)
        loop_counter_start  = loop_counter_stop
        loop_counter_stop+=7

    return calculation_dict    
         
def CalculateHistoricPivot(pair,from_date,to_date):
    conn = sqlite3.connect('test.db')
    c=conn.cursor()
    today_included=0
    dates_list=[]
    today_date = datetime.today()
    start_date = datetime.strptime(from_date,'%Y/%m/%d')
    end_date = datetime.strptime(to_date,'%Y/%m/%d')
    # print(end_date)
    print(end_date.date())
    print(datetime.today().date())
    if end_date.date() == datetime.today().date(): #check if user wants pivot includiing today's date
        today_included=1
        
    if start_date > end_date or start_date > today_date:
        return "Start date cannot be greater than end date or today's date"
    if end_date > today_date:
        return "End date cannot be greater than today's date"
    
    days_range = (end_date - start_date).days
    
    if days_range <0:
        return "to_date is less than from date"
    print(days_range)

    if today_included == 1:
        days_range = days_range+1
    else:
        days_range = days_range+2    

    for i in range(days_range):
        day = start_date+timedelta(days=i)
        date_,time = str(day).split(' ')
        dates_list.append(date_)
    print(dates_list)    
    print(today_included)
    all_rows = []
    for each_date in dates_list:
        c.execute('select * from test_GBPINR_spot1 where Time_Stamp like ? order by Time_Stamp desc limit 1', ('%'+each_date+'%',))
        rows = c.fetchall()
        # print(rows)
        for row in rows:
            # print(row)
            all_rows.append(row)

    print(all_rows)     
    print(len(all_rows)) 
    calculation_dict={'Standard':[],'Woodie':[],'Camrarilla':[],'Fibonacci':[],'Final':[]} #R1,R2,R3,PP,S1,S2,S3 values in list in order
    if today_included:
        i,j=0,1 #i is starting at zero and j one ahead of i
        while i!=len(all_rows):
            if i == len(all_rows) -1: #when today is included so last date will be today's date and we will use all the fields there
                j=i

            open_ = all_rows[j][2]
            high_ = all_rows[i][3]
            low_ = all_rows[i][4]
            close_ = all_rows[i][5]

            #standard
            pp = (high_+low_+close_)/3
            r1 = (2*pp)-low_
            r2 = pp+(high_-low_)
            r3 = high_+ 2*(pp-low_)
            s1 = (2*pp) - high_
            s2 = pp-(high_-low_)
            s3 = low_-2*(high_-pp)
            if pair=='usd/inr' and s3-r3>0.5:
                s3 = (s2+s3)/2
            
            calculation_dict['Standard'].append(r3)
            calculation_dict['Standard'].append(r2)
            calculation_dict['Standard'].append(r1)
            calculation_dict['Standard'].append(pp)
            calculation_dict['Standard'].append(s1)
            calculation_dict['Standard'].append(s2)
            calculation_dict['Standard'].append(s3)

            pp,r1,r2,r3,s1,s2,s3 = 0,0,0,0,0,0,0

            #Woodie 
            pp = (open_+open_+high_+low_)/4
            r1 = (2*pp)-low_
            r2 = pp+(high_-low_)
            r3 = high_+2*(pp-low_)
            s1 = 2*pp-high_
            s2 = pp-(high_-low_)
            s3 = low_-2*(high_-pp)

            if pair=='usd/inr' and s3-r3>0.5:
                s3 = (s2+s3)/2

            calculation_dict['Woodie'].append(r3)
            calculation_dict['Woodie'].append(r2)
            calculation_dict['Woodie'].append(r1)
            calculation_dict['Woodie'].append(pp)
            calculation_dict['Woodie'].append(s1)
            calculation_dict['Woodie'].append(s2)
            calculation_dict['Woodie'].append(s3)

            pp,r1,r2,r3,s1,s2,s3 = 0,0,0,0,0,0,0

            #Camrarilla

            pp = (high_+low_+close_)/3
            r1 = close_+((high_-low_)*1.0833)
            r2  = close_+((high_-low_)*1.1666)
            r3 = close_+((high_-low_)*1.2500)
            s1 = close_-((high_-low_)*1.0833)
            s2 = close_-((high_-low_)*1.1666)
            s3 = close_-((high_-low_)*1.2500)

            if pair=='usd/inr' and s3-r3>0.5:
                s3 = (s2+s3)/2
            
            calculation_dict['Camrarilla'].append(r3)
            calculation_dict['Camrarilla'].append(r2)
            calculation_dict['Camrarilla'].append(r1)
            calculation_dict['Camrarilla'].append(pp)
            calculation_dict['Camrarilla'].append(s1)
            calculation_dict['Camrarilla'].append(s2)
            calculation_dict['Camrarilla'].append(s3)

            pp,r1,r2,r3,s1,s2,s3 = 0,0,0,0,0,0,0

            #Fibonacci

            pp = (high_+low_+close_)/3
            r1 = pp+(0.382*(high_-low_))
            r2 = pp+(0.618*(high_-low_))
            r3 = pp+(1.0*(high_-low_))
            s1 = pp-(0.382*(high_-low_))
            s2 = pp-(0.618*(high_-low_))
            s3 = pp+(1.0*(high_-low_))

            if pair=='usd/inr' and s3-r3>0.5:
                s3 = (s2+s3)/2

            calculation_dict['Fibonacci'].append(r3)
            calculation_dict['Fibonacci'].append(r2)
            calculation_dict['Fibonacci'].append(r1)
            calculation_dict['Fibonacci'].append(pp)
            calculation_dict['Fibonacci'].append(s1)
            calculation_dict['Fibonacci'].append(s2)
            calculation_dict['Fibonacci'].append(s3)

            pp,r1,r2,r3,s1,s2,s3 = 0,0,0,0,0,0,0

            #calculate final
            loop_counter_stop = 7
            loop_counter_start = 0
            for k in range(loop_counter_start,loop_counter_stop):
                calculation_dict['Final'].append((calculation_dict['Standard'][k]+calculation_dict['Woodie'][k]+calculation_dict['Camrarilla'][k]+calculation_dict['Fibonacci'][k])/4)
            loop_counter_start  = loop_counter_stop
            loop_counter_stop+=7

            i+=1
            j+=1

    else: # when today's date is not included
        i,j=0,1
        while i !=len(all_rows)-1: 
            print(f'i  -> {i}   j  -> {j}')
            open_ = all_rows[j][2]
            high_ = all_rows[i][3]
            low_ = all_rows[i][4]
            close_ = all_rows[i][5] 

            #standard
            pp = (high_+low_+close_)/3
            r1 = (2*pp)-low_
            r2 = pp+(high_-low_)
            r3 = high_+ 2*(pp-low_)
            s1 = (2*pp) - high_
            s2 = pp-(high_-low_)
            s3 = low_-2*(high_-pp)
            if pair=='usd/inr' and s3-r3>0.5:
                s3 = (s2+s3)/2
            
            calculation_dict['Standard'].append(r3)
            calculation_dict['Standard'].append(r2)
            calculation_dict['Standard'].append(r1)
            calculation_dict['Standard'].append(pp)
            calculation_dict['Standard'].append(s1)
            calculation_dict['Standard'].append(s2)
            calculation_dict['Standard'].append(s3)

            pp,r1,r2,r3,s1,s2,s3 = 0,0,0,0,0,0,0

            #Woodie 
            pp = (open_+open_+high_+low_)/4
            r1 = (2*pp)-low_
            r2 = pp+(high_-low_)
            r3 = high_+2*(pp-low_)
            s1 = 2*pp-high_
            s2 = pp-(high_-low_)
            s3 = low_-2*(high_-pp)

            if pair=='usd/inr' and s3-r3>0.5:
                s3 = (s2+s3)/2

            calculation_dict['Woodie'].append(r3)
            calculation_dict['Woodie'].append(r2)
            calculation_dict['Woodie'].append(r1)
            calculation_dict['Woodie'].append(pp)
            calculation_dict['Woodie'].append(s1)
            calculation_dict['Woodie'].append(s2)
            calculation_dict['Woodie'].append(s3)

            pp,r1,r2,r3,s1,s2,s3 = 0,0,0,0,0,0,0

            #Camrarilla

            pp = (high_+low_+close_)/3
            r1 = close_+((high_-low_)*1.0833)
            r2  = close_+((high_-low_)*1.1666)
            r3 = close_+((high_-low_)*1.2500)
            s1 = close_-((high_-low_)*1.0833)
            s2 = close_-((high_-low_)*1.1666)
            s3 = close_-((high_-low_)*1.2500)

            if pair=='usd/inr' and s3-r3>0.5:
                s3 = (s2+s3)/2
            
            calculation_dict['Camrarilla'].append(r3)
            calculation_dict['Camrarilla'].append(r2)
            calculation_dict['Camrarilla'].append(r1)
            calculation_dict['Camrarilla'].append(pp)
            calculation_dict['Camrarilla'].append(s1)
            calculation_dict['Camrarilla'].append(s2)
            calculation_dict['Camrarilla'].append(s3)

            pp,r1,r2,r3,s1,s2,s3 = 0,0,0,0,0,0,0

            #Fibonacci

            pp = (high_+low_+close_)/3
            r1 = pp+(0.382*(high_-low_))
            r2 = pp+(0.618*(high_-low_))
            r3 = pp+(1.0*(high_-low_))
            s1 = pp-(0.382*(high_-low_))
            s2 = pp-(0.618*(high_-low_))
            s3 = pp+(1.0*(high_-low_))

            if pair=='usd/inr' and s3-r3>0.5:
                s3 = (s2+s3)/2

            calculation_dict['Fibonacci'].append(r3)
            calculation_dict['Fibonacci'].append(r2)
            calculation_dict['Fibonacci'].append(r1)
            calculation_dict['Fibonacci'].append(pp)
            calculation_dict['Fibonacci'].append(s1)
            calculation_dict['Fibonacci'].append(s2)
            calculation_dict['Fibonacci'].append(s3)

            pp,r1,r2,r3,s1,s2,s3 = 0,0,0,0,0,0,0

            #calculate final
            loop_counter_stop = 7
            loop_counter_start = 0
            for k in range(loop_counter_start,loop_counter_stop):
                calculation_dict['Final'].append((calculation_dict['Standard'][k]+calculation_dict['Woodie'][k]+calculation_dict['Camrarilla'][k]+calculation_dict['Fibonacci'][k])/4)
            loop_counter_start  = loop_counter_stop
            loop_counter_stop+=7

            i+=1
            j+=1

    return calculation_dict



open_list=[]
close_list=[]
high_list=[]
low_list=[]
currency_pair_list = []

# open_price = input('put open price ')
# close_price = input('put close price ')
# high_price = input('put high price ')
# low_price = input('put low price ')
currency_pair = input('put currency pair ')
from_date = input('put starting date')
to_date = input('put ending date')

# open_list = open_price.split(' ')
# close_list=close_price.split(' ')
# high_list=high_price.split(' ')
# low_list=low_price.split(' ')
currency_pair_list = currency_pair.split(' ') 

# cal = CalculateCurrentDayPivot(open_list,close_list,high_list,low_list,currency_pair_list)
# print(cal)

response = CalculateHistoricPivot(currency_pair_list,from_date,to_date)
print(response)