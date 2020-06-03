import requests
import time


class GoodreadsConnector:
    base_address = 'https://www.goodreads.com'

    def __init__(self, api_key, secret=None):
        self.delay = 1.6
        self.params = {
            'key': api_key,
            'format': 'xml'
        }

    # Good highjacking of getattribute dunder, adds delay if callable
    # from https://stackoverflow.com/a/8618289/521812
    def __getattribute__(self, name):
        attr = object.__getattribute__(self, name)
        if hasattr(attr, '__call__'):
            def proxFct(*args, **kwargs):
                time.sleep(object.__getattribute__(self, "delay"))
                return attr(*args, **kwargs)
            return proxFct
        else:
            return attr

    def get_series(self, series_id):
        req = requests.get(f'{self.base_address}/series/{series_id}', params=self.params)
        return req

    def get_review_stats(self, isbn_list):
        params = self.params.copy()
        params.update({'isbns': ','.join(isbn_list)})
        req = requests.get(f'{self.base_address}/book/review_counts.json', params=params)
        return req

    def get_book(self, book_name):
        params = self.params.copy()
        params.update({'q': book_name,
                       'search': 'title'})
        req = requests.get(f'{self.base_address}/search/index.xml/', params=params)
        return req
