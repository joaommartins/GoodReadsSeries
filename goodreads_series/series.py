from goodreads_series.book import Book
from goodreads_series.connector import GoodreadsConnector
from bs4 import BeautifulSoup as Soup


class BookSeries:
    def __init__(self, api_key, name, gr_id):
        self.connector = GoodreadsConnector(api_key)
        self.name = name
        self.gr_id = gr_id
        self.full_series = []
        self.main_series = []
        self.plan_series = []
        self.stats = {}

        self._fetch_books()
        self._calc_stats()

    def __repr__(self):
        return f'<Series {self.name} ({self.gr_id})>'

    def __getitem__(self, val_index):
        return self.full_series[val_index]

    def _add_book(self, name, user_position, gr_id, book_info):
        new_book = Book(name, user_position, gr_id, book_info)
        if new_book.published:
            self.full_series.append(new_book)
            self._check_main_series(new_book)
        else:
            self.plan_series.append(new_book)

    def _check_main_series(self, book_obj):
        try:
            if book_obj.user_position.is_integer():
                self.main_series.append(book_obj)
        except AttributeError:
            pass

    def _check_numeric_index(self, work):
        # Let's skip "part X formats"
        try:
            float(work.user_position.text)
        except ValueError:
            return False
        return True

    def _fetch_books(self):
        series_return = self.connector.get_series(self.gr_id)
        series_content = Soup(series_return.content, "xml")

        for work in series_content.find_all('series_work'):
            if not self._check_numeric_index(work):
                continue
            fetched_book = self.connector.get_book(work.work.title)
            # should be smarter, check mora than the first if ids dont match
            book_info = Soup(fetched_book.content, 'lxml').find_all('work')[0]

            print(work.user_position.text, work.work.id.text, work.work.title.text, book_info.average_rating.text)

            self._add_book(
                work.work.title.text,
                work.user_position.text,
                work.work.id.text,
                book_info
            )

    def _calc_stats(self):
        # Main series average
        main_series_average = sum(book.rating for book in self.main_series if book.published is True) / len(
            self.main_series)
        self.stats.update({'main_series_average': main_series_average})
        # Full series average
        full_series_average = sum(book.rating for book in self.full_series if book.published is True) / len(
            self.full_series)
        self.stats.update({'full_series_average': full_series_average})




