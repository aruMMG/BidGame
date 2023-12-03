import requests
from bs4 import BeautifulSoup
import csv



def scaper(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    lines = soup.find_all("div", class_="cb-col cb-col-100 cb-scrd-itms")
    batters_scores = {}
    bowlers_wickets = {}
    for line in lines:
        isBatter = None
        isBolwer = None
        isBatter = line.find("div", class_="cb-col cb-col-25")
        isBolwer = line.find("div", class_="cb-col cb-col-38")
        if isBatter:
            name = isBatter.find('a', class_='cb-text-link').text.strip()
            score = line.find("div", class_="cb-col cb-col-8 text-right text-bold").text.strip()
            batters_scores[name] = int(score)

        elif isBolwer:
            name = isBolwer.find('a', class_='cb-text-link').text.strip()
            score = line.find("div", class_="cb-col cb-col-8 text-right text-bold").text.strip()
            bowlers_wickets[name] = int(score)
    return batters_scores, bowlers_wickets

if __name__=="__main__":
    url = "https://www.cricbuzz.com/live-cricket-scorecard/84026/chb-vs-nw-14th-match-t10-league-2023"
    batters_scores, bowlers_wickets = scaper(url)
    print(batters_scores)
    print(bowlers_wickets)