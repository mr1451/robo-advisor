# app/robo_advisor.py

import requests
import csv
import json
import os
from dotenv import load_dotenv

load_dotenv()

# utility function to convert float or integer to usd-formatted string
def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

# INFO INPUTS  

print("REQUESTING SOME DATA FROM THE INTERNET...")
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default = "OOPS")

SYMBOL = "TSLA" #TODO: ask for consumer input

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&apikey={API_KEY}"

response = requests.get(request_url)
#print(type(response))
#print(response.status_code)
#print(response.text)

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys()) #TODO: sort to ensure latest day is first

latest_day = dates[0] #"2020-02-19"

latest_close = tsd[latest_day]["4. close"]

#get high price from each day
high_prices = []
low_prices = []

for date in dates: 
    high_price = tsd[date]["2. high"]
    low_price = tsd[date]["3. low"]
    high_prices.append(float(high_price))
    low_prices.append(float(low_price))

#maximum of all high prices
recent_high = max(high_prices)
recent_low = min(low_prices)

#print("URL:", request_url)
#print(type(response.text)) #> str

#if error message occurs

#if "Error Message" in response.text:
    #print("OOPS, couldn't find that symbol. Please try again!")
    #exit()

#parsed_response = json.loads(response.text)

#print(type(parsed_response)) #> dict

#print(parsed_response)

#tsd = parsed_response["Time Series (Daily)"]

# INFO OUTPUTS

#csv_file_path = "data/prices.csv" # a relative filepath

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=["city", "name"])
    writer.writeheader() # uses fieldnames set above
    writer.writerow({"city": "New York", "name": "Yankees"})
    writer.writerow({"city": "New York", "name": "Mets"})
    writer.writerow({"city": "Boston", "name": "Red Sox"})
    writer.writerow({"city": "New Haven", "name": "Ravens"})

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")