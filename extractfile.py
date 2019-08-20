import pandas as pd
import os
import time
from datetime import datetime

path  = os.getenv("HOME") + "/Downloads/intraQuarter"
print (path)
ROOT_DIR = os.path.abspath(os.curdir)

def Key_Stats (gather="Total Debt/Equity (mrq)"):
    statspath = path + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]
    #print (stock_list)
    #print ("hie")
    df = pd.DataFrame (columns = ['Date', 'Unix','Ticker', 'DE Ratio','Price','SP500'])
    sp500_df = pd.read_csv(ROOT_DIR + "/data/YAHOO-INDEX-GSPC.csv")


    for each_dir in stock_list[1:]:
        each_file = os.listdir(each_dir)
        ticker = each_dir.split("\\")[0]
        #print (each_file)

        if len(each_file)>0:
            for file in each_file:
                #print (file)
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                #print (date_stamp, unix_time)
                full_file_path = each_dir + '/' + file
                #print (full_file_path)
                source = open (full_file_path,'r', encoding="utf-8").read()
                #print (source)

                try :
                    value = float (source.split (gather + ':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])

                    try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        row = sp500_df[sp500_df["Date"] == sp500_date]
                        sp500_value = float(row["Adj Close"])

                    except:
                        sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
                        row = sp500_df[sp500_df["Date"] == sp500_date]
                        sp500_value = float(row["Adj Close"])

                    stock_price = float (source.split('</small><big><b>')[1].split('</b></big>')[0])
                    #print ("stock price : " + stock_price, "ticker:" + ticker)

                    df=df.append({'Date':date_stamp, 'Unix':unix_time,'Ticker':ticker,'DE Ratio':value,'Price':stock_price, 'SP500':sp500_value},ignore_index=True)
                    #print (ticker + ":" , value)
                    #time.sleep(15)

                except IndexError :
                    print ("out of range for :" + ticker)

                except Exception as e:
                    print (e)
                    pass

    save = gather.replace(' ','').replace(')','').replace('(','').replace('/','') + ('.csv')
    print (save)
    df.to_csv(save)

    print (df)
Key_Stats()