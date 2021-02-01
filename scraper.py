""" 
PyJaC Submission

Prompt - "Build a Web Scraper"

Web Scraper for anime from MAL [myanimelist]. Given some string input,
searches it on the [myanimelist] website and returns details 
regarding the closest matching anime
"""

import requests
from bs4 import BeautifulSoup
from typing import List


class MAL: 
    """ 
    A MAL object that keeps track of it's anime's details
    that are scraped off of [myanimelist.net]
    """
    link: str
    title: str
    desc: str
    imageUrl: str
    score: str
    rank: str
    popular: str
    
    def __init__(self, details: List[str]) -> None:
        """ Initalize a MAL object """
        self.link = details[0]
        self.title = details[1]
        self.desc = details[2][:-27]
        self.imageUrl = details[3]
        self.score = details[4]
        self.rank = details[5]
        self.popular = details[6]
           
    
def details(soup: BeautifulSoup) -> List[str]:
    """ Given <soup> figure out different properties of
    anime and return them in a list"""
    
    title = soup.find('h1', class_='title-name h1_bold_none').getText()
    description = soup.find('p', {'itemprop': 'description'}).getText()
    imageUrl = soup.find('img', alt=title)['data-src']
    score = soup.find('div', class_='score-label').getText()
    rank = soup.find('span', class_='numbers ranked').getText()
    popularity = soup.find('span', class_='numbers popularity').getText()
    
    return [title, description, imageUrl, score, rank, popularity]


def search(anime_name: str) -> MAL:
    """ Given <anime_name> searches it on my anime list
    and returns the details about the closest matching
    anime """

    search_url = ("https://myanimelist.net/search/all?q=" + anime_name +"&cat=anime")
    source_code = requests.get(search_url)
    content = source_code.content
    
    soup = BeautifulSoup(content,features="html.parser")
    link = soup.find('a', class_='hoverinfo_trigger fw-b fl-l')['href']

    actualPage = requests.get(link)
    actualContent = actualPage.content
    goodSoup = BeautifulSoup(actualContent,features="html.parser")

    return MAL([link] + details(goodSoup)) 


if __name__ == "__main__":
    print(search("naruto"))
