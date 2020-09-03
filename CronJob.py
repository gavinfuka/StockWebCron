import schedule
from datetime import datetime
import time

from YFinance import YFinance
from Database.CouchDB import CouchDB
from _config import config

class CronJob():
    def __init__(self):
        self.LastDate = None
        self.CouchDB = CouchDB(config=config["CouchDB"])

    def Start(self):
        self.LastDate = datetime.now()
        self.UpdateJob()
        schedule.every().day.at("18:00").do(self.UpdateJob)
        while True:
            schedule.run_pending()
            time.sleep(60)

    def UpdateJob(self):
        print('[-] Update Job Starts')
        try:
            for i in range(0,9999):
                symbol = self.PadZero(i)
                yahoo_df = YFinance.Fetch1Year(symbol)
                yahoo_df_clone = yahoo_df
                yahoo_df_clone.index = yahoo_df_clone.index.astype(str)
                self.CouchDB.Update(dbName='yfinance', doc=yahoo_df_clone.to_dict(), _id=symbol)
            print ('[x] Update Success!')
        except Exception as e:
            print('[-] Update Job Ends with Error')
            print(e)



    @staticmethod
    def PadZero(List):
        return str(List).zfill(4) + '.HK' 