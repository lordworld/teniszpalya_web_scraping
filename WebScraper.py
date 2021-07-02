import bs4

class WebScraperClass:

    def __init__(self, url, *args, **kwargs):
        self.url = url
        self.subpage = kwargs

    def add_subpage(self, **kwargs):
        self.subpage = kwargs

    def beautiful_html(self, html):
        return bs4.BeautifulSoup(html.text, "lxml")

    def get_raw_data(self, bs, data):
        # print(type(bs))
        if type(bs) is bs4.BeautifulSoup:
            # print(bs.select(data))
            return bs.select(data)
        else:
            return -1

    def get_value(self, variable, tag=[], num=0):
        """

        :param tag: text
        :type variable: beautifulsoup list
        """
        # print(type(variable))#, len(variable))

        if variable and not tag:
            numth_value = variable[num]
            return numth_value.text.strip()
        if variable and tag:
            # print(variable[num][tag])
            numth_value = variable[num][tag]
            return numth_value.strip()
        elif not variable:
            return 0
        else:
            return -1