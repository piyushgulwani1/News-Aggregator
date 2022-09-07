from datetime import datetime, timedelta
from time import sleep
from newsapi import NewsApiClient
import requests
import pycountry

class NewsAggregator:

    def __init__(self):
        self.api_key = None
        self.client = None
        self.country = "in" #Default

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

    def setCountry(self):
        try:
            country = input("Enter your country: ")
            two_digit_iso_code = pycountry.countries.search_fuzzy(country)
            two_digit_iso_code = str(two_digit_iso_code[0])
            two_digit_iso_code = two_digit_iso_code[17:19].lower()
            self.country = two_digit_iso_code
            print(f"Country Changed to {country}. ISO Code: {self.country}")

        except LookupError as lookupError:
            print("Please enter a valid country!")
        
    def getTopHeadline(self):

        try:
            url = f"https://newsapi.org/v2/top-headlines?country={self.country}&apiKey={self.api_key}&pageSize=100"
            headlines = requests.get(url).json()

            total_number_of_news = headlines["totalResults"]
            
            print("Total Results: ", total_number_of_news)
            number_of_news_to_print = int(input("How many number of news you want: "))

            if (number_of_news_to_print > total_number_of_news):
                print("Please enter a valid number!\n")

            else :
                for i in range(number_of_news_to_print):
                    print(f"""{i + 1} --> Title: {headlines["articles"][i]["title"]}\n\tDescription: {headlines["articles"][i]["description"]}\n\tSource: {headlines["articles"][i]["source"]["name"]}\n\tLink: {headlines["articles"][i]["url"]}\n""")
                    sleep(5)
        
        except requests.exceptions.ConnectionError as connectionError:
            print("Please check your Internet Connection!\n")


    def getCategorizedHeadlines(self):

        try:
            categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]
            for i in range(7):
                print(f"{i + 1}. {categories[i].capitalize()}")

            categorySelected = int(input("Enter your choice: "))

            url = f"https://newsapi.org/v2/top-headlines?country={self.country}&apiKey={self.api_key}&pageSize=100&category={categories[categorySelected - 1]}"

            categorizedHeadline = requests.get(url).json()
            total_number_of_news = categorizedHeadline["totalResults"]

            print(f"Total Results: {total_number_of_news}\n")

            number_of_news_to_print = int(input("How many news do you want: "))

            if (number_of_news_to_print > total_number_of_news):
                print("Please enter a valid number!\n")
            
            else:
                for i in range(number_of_news_to_print):
                    print(f"""{i + 1} --> Title: {categorizedHeadline["articles"][i]["title"]}\n\tDescription: {categorizedHeadline["articles"][i]["description"]}\n\tSource: {categorizedHeadline["articles"][i]["source"]["name"]}\n\tLink: {categorizedHeadline["articles"][i]["url"]}\n""")

        except requests.exceptions.ConnectionError as connectionError:
            print("Please check your Internet Connection!\n")

if __name__ == "__main__":

    try:
        news_object = NewsAggregator()
        news_object.getApiKey()
        news_object.storeApiKey()

        print("1. Get Top Headlines")
        print("2. Get Categorized Headlines")
        print("3. Search by query")
        print("4. Change Country")
        print("5. Quit\n")

        while True:
            option = int(input("Enter your option: "))

            if option == 1:
                news_object.getTopHeadline()

            elif option == 2:
                news_object.getCategorizedHeadlines()

            elif option == 4:
                news_object.setCountry()

            elif option == 5:
                print("Exiting!")
                exit()

    except KeyboardInterrupt as keyboardInterrupt:
        print("\nQuit!")
    
    except ValueError as valueError:
        print("Invalid Option!")