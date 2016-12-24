import re
import sys
from urllib.request import urlopen

from lxml import etree


class Downloader():
    '''
  Class to retreive HTML code
  and binary files from a
  specific website
  '''

    def __init__(self, url):
        self.url = url

    def download(self, image_name='', is_image=False):
        try:
            browser = urlopen(self.url)
            response = browser.getcode()
        except Exception as e:
            print('Bad connection: ' + e)
            sys.exit()

        if response == 200:
            contents = browser.read()
        else:
            print('Bad header response')
            sys.exit()

        if is_image:
            self.save_image(contents, image_name)

        return contents

    def save_image(self, contents, image_name):
        image_file = open(image_name, 'wb')
        image_file.write(contents)
        image_file.close()


class xkcdParser(Downloader):
    '''
  Class for parsing xkcd.com
  '''

    def __init__(self, url):
        self.url = url
        self.last_comic_nr = None
        self.contents = self.download(self.url)
        self.title = ''
        self.caption = ''

    def set_last_comic_nr(self):
        downloader = Downloader(self.url)
        self.contents = downloader.download()
        self.last_comic_nr = re.search(r"http://xkcd.com/(\d+)", self.contents).group(1)
        self.last_comic_nr = int(self.last_comic_nr)

    def get_title(self):
        if self.contents:
            tree = etree.HTML(self.contents)
            self.title = tree.xpath("string(//div[@id='ctitle'])")
            print('title: '+ self.title)

    def get_caption(self):
        if self.contents:
            tree = etree.HTML(self.contents)
            self.caption = tree.xpath("string(//div[@id='comic']/img/@title)")

    def get_comic(self):
        if self.contents:
            tree = etree.HTML(self.contents)
            url = tree.xpath("string(//div[@id='comic']/img/@src)")

            downloader = Downloader(url)
            downloader.download(self.title, True)

    def get_last_comic_nr(self):
        try:
            nr_regex = re.compile(r"http://xkcd.com/(\d+)")
            all_nr = nr_regex.findall(str(self.contents))
            return int(all_nr[0])
        except Exception as e:
            print('No regex found: ' + str(e))
            self.last_comic_nr = None

    def get_current_comic(self):
        return self.get_last_comic_nr()


if __name__ == '__main__':
    url = "http://xkcd.com/"
    # url = "http://google.com/"
    xkcd_parser = xkcdParser(url)
    # print(xkcd_parser.get_current_comic())
    xkcd_parser.get_title()
    print(xkcd_parser.title)
    print(str(xkcd_parser.title))
    print(type(xkcd_parser.title))
    print(type(str(xkcd_parser.title)))
