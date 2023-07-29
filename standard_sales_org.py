"""Script written as a temporary solution,
    later replaced by main script"""

import re
import sys
import pandas as pd
import xlwings as xw
import tkinter as tk
from tkinter import filedialog

def file_open():
    root = tk.Tk()
    root.withdraw()

    f = filedialog.askopenfile(initialdir='/Users/Erick/Downloads', title='Select file', 
                               filetypes=(('CSV Files', '*.csv'), ))

    return f.name
    
def sales_rep(file):
    '''Takes Sales Report from Clover and returns in analyzable form'''

    wb = xw.Book(file):
    sht = wb.sheets(1)

    #Get Year
    year_data = sht.range('A2').value
    year = re.search('\d{4}', year_data)
    
    #Month to number conversion
    mnt = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
            'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

    #Data Dictionary
    last_col = sht.range('A12').expand('right').last_cell.address.split('$')[1]
    
    data = {
            'date': list(sht.range('B12:'+last_col+'12').value),
            'gross_sales': list(sht.range('B13:'+last_col+'13').value),
            'Discounts':list(sht.range('B14:'+last_col+'14').value),
            'Repayments':list(sht.range('B15:'+last_col+'15').value),
            'Refunds': list(sht.range('B16:'+last_col+'16').value),
            'net_sales':list(sht.range('B17:'+last_col+'17').value),
            'non_revenue':list(sht.range('B18:'+last_col+'18').value),
            'gift_cards': list(sht.range('B19:'+last_col+'19').value),
            'taxes': list(sht.range('B20:'+last_col+'20').value),
            'tips': list(sht.range('B21:'+last_col+'21').value),
            'service_charges': list(sht.range('B22:'+last_col+'22').value),
            'amount_collected': list(sht.range('B23:'+last_col+'23').value),
            }

    for d in data.values():
        d.pop()

    date_lst = []
    reg = re.compile(r'\s[A-Za-z]{3}\s[0-9]+')

    try:
        for x in data['date']:
            sr = re.search(reg, x)
            date_lst.append(str(sr.group().strip()) + ' ' + str(year.group()))
    except TypeError:
        print('\nError: Make sure the data begins at row 12.\n')
        sys.exit()

    for k, v in enumerate(date_lst):
        spl = v.split(' ')
        date_lst[k] = f'{mnt[spl[0]]}-{spl[1]}-{spl[2]}'

    data['date'] = date_lst

    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])

    df['week'] = df['date'].dt.isocalendar().week
    df['week_day'] = df['date'].dt.day_name()
    df.to_clipboard()
    print(df)

    return True

clover_file = file_open()
print(sales_rep(clover_file))
