import urllib.request
from random import randint

from bs4 import BeautifulSoup


def get_gif_url(message, log):
    keyword = get_keyword(message, log)
    if keyword == 'err':
        return "Did you forget to give me a keyword to search for?"

    url = "http://imgur.com/search/score/?q_type=gif&q_all={}&qs=thumbs".format(keyword)
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent}

    urlbase = "https://imgur.com"

    request = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(request)
    data = response.read()
    soup = BeautifulSoup(data, 'lxml')

    posts = soup.find('div', class_='cards')

    links = []
    try:
        for a in posts.find_all('a', href=True):
            links.append("{}{}".format(urlbase, a['href']))
    except:
        return "I could not find an image matching your keyword: {} :slight_frown:".format(keyword)

    return links[randint(0, len(links) - 1)]


def get_keyword(message, log):
    try:
        space_loc = message.index(" ")
    except ValueError as verr:
        log.error("Error: ValueError [{}]".format(verr))
        return 'err'
    return message[space_loc + 1:]
