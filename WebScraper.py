import bs4
import requests
from LogHandler import LogHandlerClass

class WebScraperClass:

    def __init__(self, url, *args, **kwargs):
        self.url = url
        self.subpage = kwargs

    def __str__(self):
        return self.url + self.subpage

    def add_subpage(self, **kwargs):
        self.subpage = kwargs

    def make_html_beautiful(self, html):
        self.bs4_text = bs4.BeautifulSoup(html.text, "lxml")

    def web_request(self, url):
        return requests.get(url)

    def get_bs4_data(self):
        pass

    def get_raw_data(self, data_id):
        # print(type(bs))
        if type(self.bs4_text) is bs4.BeautifulSoup:
            # print(self.bs4_text.select(data))
            return self.bs4_text.select(data_id)
        else:
            return -1

    def get_value(self, variable, tag = [], num = 0):
        """

        :param tag: text
        :type variable: beautifulsoup list
        """
        # print(type(variable))#, len(variable))

        if variable and not tag:
            numth_value = variable[num]
            return numth_value.text.strip()
        if variable and tag:
            numth_value = variable[num][tag]
            return numth_value.strip()
        elif not variable:
            return 0
        else:
            return -1

    def get_last_page(self, url):
        pass

    def get_first_page(self, url):
        pass

    def is_next_page(self):
        self.format_page(self.subpage['actual_page'])
        next_page_raw = self.get_raw_data(".pagination-next a")
        if next_page_raw:
            # print('There is next page.')
            return True
        elif not next_page_raw:
            # print('No more pages')
            return False
        return

    def get_next_page(self):
        next_page_raw = self.get_raw_data(".pagination-next a")
        if next_page_raw:
            next_page = self.get_value(next_page_raw, 'href')
            # print(f'The next page is {next_page}')
            return next_page
        elif not next_page_raw:
            # print('There is no next site to return...')
            return False

        return

    def format_page(self, url):
        try:
            plain_html = requests.get(url)
        except requests.ConnectionError:
            print(f'ERROR: Site is not reachable!!!\n'
                  f'URL is {url}\nMessage is: {plain_html}')
        except:
            print("Something is wrong!!!")
        else:
            print("OK")
        self.make_html_beautiful(plain_html)

    # It can be run just after format_page function
    def get_info(self, html_tag, tag=[], num=0):
        data = self.get_raw_data(html_tag)
        return self.get_value(data, tag, num)
