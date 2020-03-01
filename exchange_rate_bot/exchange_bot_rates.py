import json
from urllib.request import urlopen
from exchange_bot_db import exchange_rates_DB
from config import url_all_currencies, polling_interval, url_graph, graph_period
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import io
import collections

class exchange_rates:
    db = exchange_rates_DB()

    def list_all(self, cur_base):
        rates = self.checkAndUpdateRates()
        return rates

    def exchange(self, amount, cur_from, cur_to):
        rates = self.checkAndUpdateRates()
        ret = 0
        try:
            ret = amount * rates[cur_to] / rates[cur_from]
        except Exception as e:
            print(f"Error converting from {cur_from} to {cur_to}")
        return ret

    def hist(self, cur_base, cur_sym):
        now = datetime.now()
        end_date = now.strftime("%Y-%m-%d")
        start_date = (now - timedelta(days=graph_period)).strftime("%Y-%m-%d")
        data = {}
        url = url_graph % (start_date, end_date, cur_base, cur_sym)
        try:
            json_url = urlopen(url)
            data = json.loads(json_url.read())
        except Exception as e:
            print(f"Error downloading data from {url}")

        if len(data['rates']) == 0:
            return None

        x = []
        y = []
        data = collections.OrderedDict(sorted(data['rates'].items()))
        for k in data:
            x.append(k)
            y.append(data[k][cur_sym])

        plt.ioff()
        fig, ax = plt.subplots()
        ax.plot(x,y)

        ax.set(xlabel="Days", ylabel=cur_sym,
               title=f'{cur_sym} for 1 {cur_base} for last {graph_period} days')
        ax.grid()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return buf

    def getAllData(self):
        data = None
        try:
            json_url = urlopen(url_all_currencies)
            data = json.loads(json_url.read())
        except Exception as e:
            print(f"Error downloading data from {url_all_currencies}")
        return data

    def checkAndUpdateRates(self):
        now = datetime.now()
        rates = {}
        if self.db.getLastUpdateTime() < now - timedelta(minutes=polling_interval):
            data = self.getAllData()
            if (data):
                try:
                    rates = data['rates']
                    self.db.insertNewRates(rates, now)
                except Exception as e:
                    print(f"Downloaded data from {url_all_currencies} has unknown format")
        else:
            rates = self.db.getLastRates()
        return rates