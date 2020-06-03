from datetime import date


class Book:
    def __init__(self, name, user_position, gr_id, book_info):
        self.name = name
        self.user_position = float(user_position)
        self.rating = float(book_info.average_rating.text)
        self.gr_id = gr_id
        self.author = book_info.author.find('name').text
        self.main_series = False
        self.publication_date = None
        self.published = False

        self._book_info = book_info
        self._is_main()
        self._pub_date()

    def __repr__(self):
        return f'<Book: {self.name} ({self.gr_id})>'

    def _is_main(self):
        try:
            if self.user_position.is_integer():
                self.main_series = True
        except AttributeError:
            pass

    def _pub_date(self):
        if self._book_info.original_publication_year.text:
            year = int(self._book_info.original_publication_year.text)
            try:
                month = int(self._book_info.original_publication_month.text)
                day = int(self._book_info.original_publication_day.text)
            except ValueError:
                if locals().get('month'):
                    day = 1
                else:
                    month = 1
                    day = 1
            pub_date = date(year, month, day)
            self.publication_date = pub_date
            if pub_date < date.today():
                self.published = True
