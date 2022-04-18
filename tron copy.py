#from curses import window
from locale import currency
from matplotlib.figure import Figure
import requests
import time
from datetime import datetime
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from sortedcontainers import SortedDict
import tkinter as tk

style.use('ggplot')
f = Figure(figsize=(5,4), dpi=100)
a = f.add_subplot(111)

class CryptoPlotter:

    def __init__(self): #self, token: str, url: str, preferred_price: str, up_threshold=False, down_threshold=False) -> None:

        self.parameters = {'convert':'USD',}

        self.headers = {'Accepts': 'application/json',
                    'X-CMC_PRO_API_KEY': '#####',} #replace with your CoinCapMarket API Key

        self.temp_database = SortedDict()

        self.main_window = tk.Tk()
        self.main_window.title("Welcome to Cryptocurrency Plotter")

        self.main_window.rowconfigure(0, minsize=800, weight=1)
        self.main_window.columnconfigure(1, minsize=800, weight=1)

        self.tokenlist_frame = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
        self.tokenlist_frame.pack()

        # Get list of all token here save in {Tokens}
        token_button_dict = {}

        resp_1 = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest", headers=self.headers, params=self.parameters)

        tokens_dict = {}

        if resp_1.status_code == 200:
            results = json.loads(resp_1.text)['data']
            for t in results:
                tokens_dict[t['name']] = t['symbol']
        else:
            raise ConnectionError

        # Display list of tokens here
        for index, key in enumerate(tokens_dict):
            def action (x = tokens_dict[key]):
                return self.chooseCurrency(x)
            token_button_dict[key] = tk.Button(self.tokenlist_frame, text=key, command= action).grid(row=index//5, column=index%5, sticky="nsew")

        self.main_window.mainloop()


        # Select Token
        # Select base currency

        #move to new window with graph of cuurent toekn with price

    def chooseCurrency(self, token):
        self.tokenlist_frame.destroy()
        print(token)
        self.choosecurrency_frame = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
        self.choosecurrency_frame.pack()

        currency_button_dict = {}

        CurrencyListURL = 'http://data.fixer.io/api/symbols?access_key=###############' #replace with your CoinCapMarket API Key

        response = requests.get(CurrencyListURL)

        currencies_dict = {}
        if response.status_code == 200:
            response_json = json.loads(response.text)
            pairs = response_json['symbols']

            for key in pairs:
                currencies_dict[key] = pairs[key]
        else:
            raise ConnectionError
        for index, currency in enumerate(currencies_dict):
            def action (x = currency):
                    return self.getCryptoData(token, x)
            currency_button_dict[currency] = tk.Button(master=self.choosecurrency_frame, text=currencies_dict[currency], command=action).grid(row=index//5, column=index%5, sticky="nsew")


    def getCryptoData(self, token, currency):

        crypto_API_URL = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={token}'
        DATA_FIXER_URL = f'http://data.fixer.io/api/latest?access_key=##############&symbols=USD,{currency}&format=1'

        while True:

            response = requests.get(crypto_API_URL, headers=self.headers, params=self.parameters)
            response = json.loads(response.text)

            usd_price = round(float(response['data'][token]['quote']['USD']['price']), 5)
            str_time = response['status']['timestamp']
            dt_time = datetime.strptime(str_time, "%Y-%m-%dT%H:%M:%S.%fZ")

            response = requests.get(DATA_FIXER_URL)
            response = json.loads(response.text)
            rate = float(response['rates'][currency]/response['rates']['USD'])

            p_price =  round(usd_price * rate, 2)
            #info = ({'USD_PRICE':usd_price, f'{currency} price ':p_price, 'RATE': 'NGN' + str(round(rate, 2)) + '/USD' })

            self.temp_database[dt_time] = p_price

            x_axis = [i for i in self.temp_database]
            y_axis = [self.temp_database[i] for i in self.temp_database]

            plt.plot(x_axis, y_axis)
            plt.title(f"Line Graph of {token}")
            plt.xlabel("Time")
            plt.ylabel(currency)
            plt.show()

            print('waiting')
            plt.pause(10)

            print(y_axis)

"""    def plotCrypto (self, token, currency):
        x_axis = [i for i in self.temp_database]
        y_axis = [self.temp_database[i] for i in self.temp_database]

        plt.plot(x_axis, y_axis)
        plt.title(f"Line Graph of {token}")
        plt.xlabel("Time")
        plt.ylabel(currency)
        plt.show()

        print('waiting')
        plt.pause(10)

        print(y_axis) """

if __name__ == '__main__':
    CryptoPlotter()
