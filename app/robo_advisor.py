# app/robo_advisor.py

import requests
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

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")