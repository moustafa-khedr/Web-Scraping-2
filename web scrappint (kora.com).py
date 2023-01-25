#moustafa khedr
import csv

import requests
from bs4 import BeautifulSoup
import lxml

date = input("please enter a Date in following format MM/DD/YYY :")
url = requests.get(f"https://www.yallakora.com/match-center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={date}")

def main(url):

    src = url.content
    #print(src)

    soup = BeautifulSoup(src, "lxml")
    #print(soup)
    matches_details = []      #list of dictionar

    championships = soup.findAll("div",{"class":"matchCard"})
    #print(championships)

    def get_match_info(championships):
        championship_title = championships.contents[1].find("h2").text.strip()  #contents[] sarch in tag of (child tag put in list)  ::dicomentation
        #print(championship_title)
        all_matches = championships.contents[3].find_all("li")
        number_of_matches = len(all_matches)   # number of matches in champion in day to loop
        #print(number_of_matches)

        for i in range(number_of_matches):
            # get teams name
            teamA = all_matches[i].find("div",{"class":"teams teamA"}).find("p").text.strip()
            teamB = all_matches[i].find("div",{"class":"teams teamB"}).find("p").text.strip()
            #print(teamA)

            #get teams socre
            matches_result =all_matches[i].find("div",{"class":"MResult"}).find_all("span",{"class":"score"})
            score = f"{matches_result[0].text.strip()} - {matches_result[1].text.strip()}"

            #get time of match
            match_time = all_matches[i].find("div", {"class": "MResult"}).find("span", {"class": "time"}).text.strip()
            #time = f"{match_time[0].text.strip()}"

            # add match info to matches_details
            matches_details.append({"نوع البطولة":championship_title, "الفريق الاول":teamA,"النتيجة":score,
                                    "الفريق الثاني ":teamB, "ميعاد المباراة":match_time})




    for i in range(len(championships)):
        get_match_info(championships[i])   #[0] first champion


    header = matches_details[0].keys()  #dict 1 in list[0] i need a keys to hedar in csv

    with open("yalla kora matches.csv", "w",encoding="utf8") as file:
        dict_writer = csv.DictWriter(file, header)
        dict_writer.writeheader()
        dict_writer.writerows(matches_details)
        print("file saved")




main(url)
