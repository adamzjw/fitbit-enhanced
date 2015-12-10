__author__ = 'adamzjw'

import urllib2
import json

# make requests
class DataFetcher:
    def __init__(self, token):
        self.token = token

    def _fecth(self, data_url):
        headers = { 'Authorization': 'Bearer %s' % self.token.access_token}
        request = urllib2.Request(data_url, headers=headers)

        try:
            response = urllib2.urlopen(request)
            data = response.read()
            return json.loads(data)
        except urllib2.URLError, e:
            print e.code
            print e.read()

    def fetch_heartrate_intraday(self, date, detail_level, end_date=None, start_time=None, end_time=None):
        # to-do: date\time check

        if end_date is None:
            # when end_date isn't provided, return 1-day data
            end_date = '1d'

        detail_level_choices = ["1sec", "1min"]
        if detail_level not in detail_level_choices:
            raise ValueError("Choices for detail_level: %s" % ",".join(detail_level_choices))

        if start_time is not None and end_time is not None:
            # query specifit time
            data_url = 'https://api.fitbit.com/1/user/%s/activities/heart/date/%s/%s/%s/time/%s/%s.json' \
                       % (self.token.user_id, date, end_date, detail_level, start_time, end_time)

        else:
            # query specifit time
            data_url = 'https://api.fitbit.com/1/user/%s/activities/heart/date/%s/%s/%s.json' \
                       % (self.token.user_id, date, end_date, detail_level)

        return self._fecth(data_url)