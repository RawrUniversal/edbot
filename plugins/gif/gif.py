import urllib.request
from random import randint
from datetime import datetime

from bs4 import BeautifulSoup


# main method to get a url directly to an imgur image matching the keyword found
def get_gif_url(message, log, author):
    # create a timestamp for the datetime in UTC format
    time = datetime.utcnow()
    log.info("ATTEMPTING TO SEND ED.GIF COMMAND FROM {} @ {}...".format(
        author, time
    ))

    # set the gif keyword to anything after the first space in the message content
    keyword = get_keyword(message, log)
    log.info("KEYWORD OBTAINED: {}".format(keyword))

    # if get_keyword method returns 'err'
    if keyword == 'err':
        log.error("KEYWORD IS EMPTY...")
        return "Did you forget to give me a keyword to search for?"

    # begin web scrape process to get raw html for imgur search using keyword
    url = "http://imgur.com/search/score/?q_type=gif&q_all={}&qs=thumbs".format(keyword)
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent}

    # set a urlbase that will be appended before the href links in html
    urlbase = "https://imgur.com"

    request = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(request)
    data = response.read()
    soup = BeautifulSoup(data, 'lxml')

    # set posts variable to contain all div elements with the class cards
    posts = soup.find('div', class_='cards')

    # init empty links list that will randomly choose a url to return to Client
    links = []
    try:
        for a in posts.find_all('a', href=True):
            links.append("{}{}".format(urlbase, a['href']))
    except Exception as e:
        log.error("NO IMAGE FOUND MATCHING KEYWORD: {}".format(keyword))
        log.error(str(e))
        return "I could not find an image matching your keyword: {} :slight_frown:".format(keyword)

    random_img = links[randint(0, len(links) - 1)]
    log.info("RANDOM IMAGE URL SUCCESSFUL: {}".format(random_img))
    return random_img


# method used to key a keyword from the message sent from the author in Discord
def get_keyword(message, log):
    # attempt to find the index location of the first space in message.content
    # will look like "ed.gif cats" -> the space will be located right before the cats keyword
    try:
        space_loc = message.index(" ")
    # if a value error is raised, log it and return 'err' back to original method for recognition
    except ValueError as verr:
        log.error("Error: ValueError [{}]".format(verr))
        return 'err'

    return message[space_loc + 1:]
