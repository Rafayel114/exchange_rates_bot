import sqlite3
from config import database_path
from datetime import datetime

class exchange_rates_DB:
    def __init__(self):
        try:
            self.conn = sqlite3.connect(database_path, timeout=30, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Error creating DB connection {e.args}")

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def insertNewRate(self, sym: str, value: float, now: datetime):
        insert_statement = f"INSERT INTO rates(sym, rate, date) VALUES (?, ?, ?)"
        self.cursor.execute(insert_statement, (sym, value, now))
        self.conn.commit()

    def insertNewRates(self, rates: dict, now: datetime):
        for sym in rates:
            self.insertNewRate(sym, rates[sym], now)

    def getLastUpdateTime(self):
        ret = datetime(1900, 1, 1, 0, 0, 0)
        select_statement = "SELECT date FROM rates ORDER BY date DESC LIMIT 1"
        self.cursor.execute(select_statement)
        row = self.cursor.fetchone()
        if row:
            ret = datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S.%f')
        return ret

    def getLastRates(self):
        select_statement = """SELECT sym, rate FROM rates WHERE date in
                                (SELECT date FROM rates ORDER BY date DESC LIMIT 1)"""
        self.cursor.execute(select_statement)
        return { row['sym']: row['rate'] for row in self.cursor.fetchall() }

