from time import gmtime, strftime

class CryptoCurrency:
    def __init__(self, name):
        self.name = name
        self.bx_price = None
        self.global_price = None
        self.usd_price = None
        self.percent_change_1h = None
        self.percent_change_1d = None
        self.percent_change_7d = None
        self.time = strftime("%Y-%m-%d %H:%M:%S", gmtime(-1))

    def updateBX(self, bx_price):
        self.bx_price = bx_price
        self.time = strftime("%Y-%m-%d %H:%M:%S", gmtime(-1))

    def updateGlobal(self, global_price, usd_price, percent_change_1h, percent_change_1d, percent_change_7d):
        self.global_price = global_price
        self.usd_price = usd_price
        self.percent_change_1h = percent_change_1h
        self.percent_change_1d = percent_change_1d
        self.percent_change_7d = percent_change_7d
        self.time = strftime("%Y-%m-%d %H:%M:%S", gmtime(-1))

    def __str__(self):
        return '%s | %s\n--------------------------------------\nGlobal Price: %s\nBX Price: %s\nUSD Price: %s\nPercent Change 1HR: %s\nPercent Change 1D: %s\nPercent Change 7D: %s\n' % (self.name, self.time, format(float(self.global_price), ".2f"), self.bx_price, self.usd_price, self.percent_change_1h, self.percent_change_1d, self.percent_change_7d)
