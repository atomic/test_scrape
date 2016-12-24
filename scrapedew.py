import requests
from bs4 import BeautifulSoup
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
        return villagers

    @staticmethod
    def getSeasonalSchedule(soupObject, season_name):
        """
        (NOT WORKING)
        Static Helper function to get schedule dictionary for a season
        soupObject :  result of BeautifulSoup(page_content)
        season_name:  Spring,Summer,Fall,Winter, etc?
        """
        # get spring
        header = soupObject.find("a", {"title": season_name})
        table = header.parent.parent.parent.parent.next_sibling.next_sibling.td
        # print(spring_table.td)
        # A lot of DOM traversal, gotta look at the page
        # bug, why previous sibling is twice?
        schedule = {}
        for wkday in table.findAll("table"):
            day = wkday.previous_sibling.previous_sibling.get_text()
            day = day.rstrip('\r\n')
            schedule[day] = wkday
        return schedule

    def getVillagerSchedule(self, name):
        """
        Given a villager return a dictionary of schedule based on season
        {
            "Spring" : {
            "Monday" : schedule table
            "Tuesday" : schedule table,
            ...
            }

            "Summer" : { ... }
            ...
        }
        """
        page = self.download(name)
        soup = BeautifulSoup(page, "html.parser")
        # Check if there is a schedule section
        exist_schedule = soup.find("span", {"id": "Schedule"})
        if not exist_schedule:
            return '<p>No schedule found.</p>'

        # get all tr that contains <big> tag, unique to the season table it seems
        all_tr = soup.findAll("table", {"class": "mw-collapsible"})
        tr_season = []
        for tr in all_tr:
            if tr.select("big > span > a[href]"):
                # have to be specific, there are other NPC page that uses <big>
                tr_season.append(tr)
        logger.info('season length found : ' + str(len(tr_season)))  # debug

        schedule = {}
        for tr in tr_season:
            season_name = tr.select('a[title]')[0]['title']
            schedule[season_name] = tr.contents[3]

        return schedule


if __name__ == '__main__':
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

    # Testing get all NPC names
    # npc = downloader.getVillagersName()
    # print(npc)

    # Testing get NPC schedule(Elliot)
    # note: many exceptions in the site
    elliot_sched = downloader.getVillagerSchedule('Elliott')
    # elliot_sched = downloader.getVillagerSchedule('Emily')
    # print(elliot_sched)

'''
//a[@title="Alex"]/text()

'''
