# app/robo_advisor.py

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

#
# INFO INPUTS 
# 

print("REQUESTING SOME DATA FROM THE INTERNET...")
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default = "OOPS")

SYMBOL = "TSLA" #todo: ask for consumer input

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&apikey={API_KEY}"

response = requests.get(request_url)
print(type(response))
print(response.status_code)
print(response.text)

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

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

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print("LATEST CLOSE: $100,000.00")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")