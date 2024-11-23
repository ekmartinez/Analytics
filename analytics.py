import re
import sys
import csv
import pandas as pd
from PyQt6.QtWidgets import QApplication, QFileDialog


class Reports:
    def __init__(self, location):
        self.location = location    

    def file_open(self):
        app = QApplication(sys.argv) 
        
        file, check = QFileDialog.getOpenFileName(None, 
        "Select file", "", "CSV files (*.csv);;Excel files (*.xlsx)")

        return file
 
    def _data_reader(self):
        f = self.file_open()
    
        matches = list()

        with open(f) as csv_file:
            reader = csv.reader(csv_file)

            for row in reader:

                if len(row) > 0: 

                    date_pattern = re.compile(r'[A-Za-z]{3}\s\d+')
                    
                    if re.search(date_pattern, row[0]):
                        matches.append(row[0])

                    if re.search(r'Gross Sales', row[0]):
                        matches.append(row)

                    if re.search(r'Net Sales', row[0]):
                        matches.append(row)

            return matches

    def _data_organize(self):
        
        data = self._data_reader()

        sales_data = {'Date': None, 
                    'Gross Sales': None, 
                    'Net Sales': None}

        date_range = data[0].split('-')
        date_range = pd.date_range(start=date_range[0], end=date_range[1])

        sales_data['Date'] = date_range
        sales_data['Gross Sales'] = data[5][1:-1]
        sales_data['Net Sales'] = data[6][1:-1] 

        for k,v in enumerate(sales_data['Gross Sales']):
            sales_data['Gross Sales'][k] = sales_data['Gross Sales'][k].replace('$', '').replace(',', '')
            sales_data['Net Sales'][k] = sales_data['Net Sales'][k].replace('$', '').replace(',', '')
        
        return sales_data

    def sales_report(self):

        data = self._data_organize()
        data = pd.DataFrame(data)
        data['Gross Sales'] = data['Gross Sales'].astype('float')
        data['Net Sales'] = data['Net Sales'].astype('float')
        data['Adjustments'] = data['Gross Sales'] - data['Net Sales']
        data['Week #'] = data['Date'].dt.isocalendar().week
        data['Week Day'] = data['Date'].dt.day_name()
        data['Location'] = self.location 
        data.to_clipboard(header=None, index=False) 

        return data

    def purchase_report(self):
      
        file_open = self.file_open()
        df = pd.read_excel(file_open, skiprows=4)
        df.rename(columns={'Unnamed: 0' : 'Category'}, inplace=True)
        df['Category'].ffill(inplace=True)
        df1 = df.drop(['Memo/Description'], axis=1)
        df1.dropna(inplace=True)
        df1['Location'] = self.location
        df1.to_clipboard(index=False)
        
        return df1

    def payroll_report(self):    

        file_open = self.file_open()
        pay_report = pd.read_csv(file_open, encoding='ISO-8859-1')
        
        pay_report = pay_report[['Company Code', 'Pay Period Start Date', 
                'Pay Period End Date', 'Check Date', 'Earning Amount']]

        total_payroll = pay_report['Earning Amount'].sum()
        
        start = pay_report.iloc[0, 1]
        end = pay_report.iloc[0, 2]
        date_range = pd.date_range(start=start, end=end)
        payroll_data = pd.DataFrame(date_range, columns=['Date'])
        payroll_data['Week #'] = payroll_data['Date'].dt.isocalendar().week
        payroll_data['Week Day'] = payroll_data['Date'].dt.day_name()
        payroll_data['Avg Daily Payroll'] = round(total_payroll / len(date_range), 2)
        payroll_data['Location'] = self.location
        payroll_data.to_clipboard(index=False, header=None)

        return payroll_data

class analytics:
    def __init__(self, date_range, location):
        self.date_range = date_range
        self.location = location

    def daily_report(self):
        pass

    def weekly_report(self):
        pass

    def monthly_report(self):
        pass
