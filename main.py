from datetime import datetime, timedelta
from time import sleep
import requests
from newsapi import NewsApiClient


class NewsAggregator:

    def __init__(self):
        self.api_key = None
        self.client = None

    def getApiKey(self):
        try:
            file = open("api_key.txt", "r")
            self.api_key = file.readline()
            self.client = NewsApiClient(self.api_key)

        except FileNotFoundError as fileNotFoundError:
            self.api_key = input("Enter API key:\t")

    def storeApiKey(self):
        authentication_url = "https://newsapi.org/v2/everything?q=keyword&apiKey={}".format(self.api_key)
        status = requests.get(authentication_url)

        if status.status_code == 200:
            file = open("api_key.txt", "w")
            file.write(self.api_key)
            print("Authentication Success!")

        else:
            print("Invalid API Key")

    def getTopHeadline(self):
        top_headlines_url = "https://newsapi.org/v2/top-headlines?country=in&apiKey={}".format(self.api_key)
        top_headlines = requests.get(top_headlines_url).json()

        print("Total Results:  ", top_headlines["totalResults"])

        number_of_articles_to_print = int(input("Enter number of articles to print:\t"))

        for i in range(number_of_articles_to_print):
            print("{} --> Title: {}\t\n\tDescription: {}\n".format(i + 1,
                                                                 top_headlines["articles"][i]["title"],
                                                                 top_headlines["articles"][i]["description"]))
            sleep(2.5)

    def getTopHeadlinesByCategory(self):
        category = ["business", "entertainment", "general", "health", "science", "sports", "technology"]

        for i in range(7):
            print("{}. {}".format(i + 1, category[i].capitalize()))

        select_category = int(input("Enter option:\t"))

        try:
            categorized_headline_url = "https://newsapi.org/v2/top-headlines?country=in&apiKey={}&category={}".format(
                self.api_key, category[select_category - 1])
            top_headlines = requests.get(categorized_headline_url).json()

            print("Total Results:  ", top_headlines["totalResults"])

            number_of_articles_to_print = int(input("Enter number of articles to print:\t"))

            for i in range(number_of_articles_to_print):
                print("{} --> Title: {}\t\n\tDescription: {}\n".format(i + 1,
                                                                     top_headlines["articles"][i]["title"],
                                                                     top_headlines["articles"][i]["description"]))
                sleep(2.5)

        except IndexError as indexError:
            print("Invalid Option !")

        except requests.exceptions.ConnectionError as connectionError:
            print("Check Internet Connection! Try Again Later")

    def getNewsByQuery(self):
        try:
            from_date = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")
            to_date = datetime.now().strftime("%Y-%m-%d")
            query = input("Enter a query:\t")

            url = "https://newsapi.org/v2/everything?q={}&apiKey={}&from={}&to={}&sortBy={}".format(query, self.api_key,
                                                                                            from_date, to_date,
                                                                                              "popularity")
            news = requests.get(url).json()

            print("Total Results: ", news["totalResults"])
            number_of_articles_to_print = int(input("Enter number of articles to print:\t"))

            for i in range(number_of_articles_to_print):
                print("{} --> Title: {}\n\t Description: {}\n".format(i + 1,
                                                                    news["articles"][i]["title"],
                                                                    news["articles"][i]["description"]))
                sleep(2.5)

        except requests.exceptions.ConnectionError as connectionError:
            print("Check Internet Connection! Try Again Later")

        except Exception as e:
            print(e)


if __name__ == "__main__":
    
    try:
        obj = NewsAggregator()
        obj.getApiKey()
        obj.storeApiKey()

        print("1. Get Top News")
        print("2. Get Categorized News")
        print("3. Search News By Query")
        print("4. Quit")

        while True:

            option = int(input("Enter your choice:\t"))

            if option == 1:
                obj.getTopHeadline()

            elif option == 2:
                obj.getTopHeadlinesByCategory()

            elif option == 3:
                obj.getNewsByQuery()

            elif option == 4:
                print("Exiting !")
                break

    except ValueError as valueError:
        print("Invalid Input!")