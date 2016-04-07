__author__ = 'adamzjw'

from oath import Client
from DataFetecher import DataFetcher
from TimeSeriesData import HeartrateTimeSeries

clientID = ''
clientSecret = ''
client = Client(clientID, clientSecret)
client.obtainConsent()
client.requestToken()
dataFetecher = DataFetcher(client.get_token())

date = '2015-12-09'
detail_level = '1sec'
rawData = dataFetecher.fetch_heartrate_intraday(date, detail_level)

heartrateTimeSeries = HeartrateTimeSeries(rawData)
heartrateTimeSeries.generate_plot()