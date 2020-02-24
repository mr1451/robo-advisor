# app/robo_advisor.py

import csv
import json
import os
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from dotenv import load_dotenv

load_dotenv()

# utility function to convert float or integer to usd-formatted string
def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

# INFO INPUTS  

while True:
    SYMBOL = input("Please input a stock symbol:")
    if SYMBOL == "MIKE":
        print("Hi, Professor Rossetti! Python rules! :)")
    elif SYMBOL.isalpha() and len(SYMBOL) > 2 and len(SYMBOL) < 6 :
        break
    else:
        print("Please enter a stock symbol that is 3 to 5 characters, only letters A-Z.")

SEND_ADDRESS = input("Please input your email:")

print("REQUESTING SOME DATA FROM THE INTERNET...")
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default = "OOPS")

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&apikey={API_KEY}"

response = requests.get(request_url)

parsed_response = json.loads(response.text)

#if error message occurs

if "Error Message" in response.text:
    print("Oops, couldn't find that symbol. Please run the program again!")
    exit()

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

# INFO OUTPUTS

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above
    for date in dates:
         daily_prices = tsd[date]
         writer.writerow({
             "timestamp": date,
             "open": daily_prices["1. open"],
             "high": daily_prices["2. high"],
             "low": daily_prices["3. low"],
             "close": daily_prices["4. close"], 
             "volume": daily_prices["5. volume"]
         })

import datetime
now = datetime.datetime.now()

print("-------------------------")
print(f"SELECTED SYMBOL: {SYMBOL}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT:")
print(now.strftime("%Y-%m-%d %H:%M:%S"))
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")

latest_close_var = float(latest_close)
recent_high_var = float(recent_high)
recent_low_var = float (recent_low)
determinant = recent_low_var*1.2 

if latest_close_var <= determinant: 
    print("RECOMMENDATION: BUY!")
    print("REASON: THE STOCK HAS SUFFICIENT GROWTH POTENTIAL TO SUGGEST INVESTING.")
else:
    print("RECOMMENDATION: DON'T BUY!")
    print("REASON: THE STOCK DOES NOT HAVE SUFFICIENT GROWTH POTENTIAL TO SUGGEST INVESTING.")

print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

#---------------------------------------------------------------------------------------------------------

if recent_high_var >= latest_close_var * 1.10:
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "OOPS, please set env var called 'SENDGRID_API_KEY'")
    MY_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", "OOPS, please set env var called 'MY_EMAIL_ADDRESS'")
    client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
    print("CLIENT:", type(client))
    subject = f"PRICE MOVEMENT ALERT: {SYMBOL} UP MORE THAN 5%"
    html_content = f"Hey there! We are sending this message to inform you that {SYMBOL}, the stock you are tracking, has recently surpassed its latest closing price by more than 10%. This is a stock to watch -- happy investing!"
    print("HTML:", html_content)
    message = Mail(from_email=MY_ADDRESS, to_emails=SEND_ADDRESS, subject=subject, html_content=html_content)
    try:
        response = client.send(message)

        print("RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
        print(response.status_code) #> 202 indicates SUCCESS
        print(response.body)
        print(response.headers)
    except Exception as e:
        print("OOPS", e.message)
else:
    exit()