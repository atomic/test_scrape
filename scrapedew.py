import requests
from lxml import etree
import sys

# probably gonna do this im run.py later
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# move to run.py later, and import

class MainDownloader(object):
    '''
    Class to download main page
    '''

    def __init__(self, url):
        self.url = url
        # dictionary to cache downloaded contents
        self.contents = {}

    '''
    Get the contents of the downloaded url
    '''

    def download(self, path=''):
        # content to be filled with result of reading the url/path
        content = ''
        try:
            # if its in the dictionary, no need to fetch again
            c = self.contents[path]
            logger.info('Cache found for : %s' % (url + path))
            return c
        except:
            try:
                browser = requests.get(self.url + path)
                response = browser.status_code
            except Exception as e:
                logger.error('Connection error: ' + e)
                sys.exit(1)

            if response == 200:
                content = browser.text
            else:
                logger.error('Bad header response')
                sys.exit(1)

            self.contents[path] = content
            return content

    def getVillagersName(self):
        from tabulate import tabulate
        # get list of villagers from http://stardewvalleywiki.com/List_of_All_Gifts
        page = self.download('List_of_All_Gifts')
        # debug
        f = open('page_result.html', 'w')
        soup = BeautifulSoup(page, "html.parser")
        # print(soup.prettify(), end="", file=f)
        # print(soup.contents)
        all_tr = soup.find_all('tr')
        print(all_tr[1].a)
        # print(tabulate(all_tr.contents), end="", file=f)

        villagers = []
        for tr in soup.find_all('tr'):
            first_column = tr.find('td')
            if first_column:
                villagers.append(first_column.find('a')['title'])
        return  villagers

if __name__ == '__main__':
    from bs4 import BeautifulSoup

    # url = "http://xkcd.com/"
    url = "http://stardewvalleywiki.com/"
    # url = "http://stardewvalleywiki.com/Demetrius"

    downloader = MainDownloader(url)
    # main_content = downloader.download('17')

    # soup = BeautifulSoup(main_content, "html.parser")
    # print(soup.prettify())
    # f = open('page_result.html', 'w')
    # print(soup.prettify(), end="", file=f)
    # print(main_content, end="", file=f)

    npc = downloader.getVillagersName()
    print(npc)

'''

//a[@title="Alex"]/text()


'''
