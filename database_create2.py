import sqlite3

conn = sqlite3.connect('test.db')

conn.execute('''CREATE TABLE Sales
            (date TEXT NOT NULL,
            gross_sales REAL NOT NULL,
            net_sales  REAL NOT NULL,
            adjustments REAL NOT NULL,
            day TEXT NOT NULL,
            week NUMERIC NOT NULL,
            location TEXT NOT NULL
            ;''')
