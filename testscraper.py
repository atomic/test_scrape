from urllib.request import urlopen
from bs4 import BeautifulSoup

# link = "http://pythonscraping.com/pages/page1.html";

link = "http://asdfsadf";

try:
    html = urlopen(link);
except Exception as e:
    print (e)
else:
    soup = BeautifulSoup(html.read(), "html.parser")
    # print(soup.h1)
    print(soup.prettify())
