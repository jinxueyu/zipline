import pandas as pd
import json as js

class RealtimeBarData(object):
    def __init__(self,minute_bar):
        super().__init__()
        self.minute_bar_json = js.loads(minute_bar)

    # def add_latest_minute_bar(self, minute_bar):
    #     self.latest_minute_bar = minute_bar
    #     self.latest_json = js.loads(self.latest_minute_bar)
    #     print(minute_bar)

    def get_data(self):
        return self.minute_bar_json

    def get_symbol(self):
        return self.minute_bar_json.get('symbol')

    def current(self, assets, fields):
        return pd.Series(data=self.minute_bar_json, index=fields)