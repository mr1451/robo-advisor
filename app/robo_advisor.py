# app/robo_advisor.py

# import my packages
import requests
import csv
import json
import os

import datetime

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default="OOPS")

## DEFINE FUNCTIONS

def to_usd(amount):
    return "${0:,.2f}".format(amount)

def compile_url(symbol):
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(request_url)
    #if symbol or API key is wrong
    if "Error Message" in response.text:
        print("We're sorry, but the stock ticker symbol you input does not exist per our records. Please try a different one!")
        exit()
    parsed_response = json.loads(response.text)
    return parsed_response

def transform_response(parsed_response):
    tsd = parsed_response["Time Series (Daily)"]
    rows = []
    for date, daily_prices in tsd.items():
        row = {
            "timestamp": date,
            "open": float(daily_prices["1. open"]),
            "high": float(daily_prices["2. high"]),
            "low": float(daily_prices["3. low"]),
            "close": float(daily_prices["4. close"]),
            "volume": int(daily_prices["5. volume"])
        }
        rows.append(row)
    return rows

def write_to_csv(rows, csv_filepath):
    csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
    with open(csv_filepath, "w", newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader() # uses fieldnames set above
        for row in rows:
            writer.writerow(row)
    return True

def recommendation(latest_close, recent_low):
    calculation = (float(latest_close) - float(recent_low))/float(recent_low)
    return calculation

if __name__ == "__main__":

    #INFO CAPTURE
    SYMBOL = input("Please input a valid stock ticker: ") #the resulting value is a string

    #figure out the length of the input for data validation
    if len(SYMBOL) > 4 or len(SYMBOL) < 3:
        print("Your stock ticker symbol must be between 3-4 characters!")
        exit()

    #figure out if the variable is an integer for error checking
    has_errors = False

    try:
        int_variable = int(SYMBOL)
        has_errors = True
    except:
        pass
    if has_errors == True:
        print("The stock ticker symbol must be all letters. Please try again!")
        exit()

    # I USE A FUNCTION HERE
    parsed_response = compile_url(SYMBOL)

    # how to get latest day, latest close, recent high and low
    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

    # I USE ANOTHER FUNCTION HERE
    rows = transform_response(parsed_response)

    latest_close = rows[0]["close"]
    high_prices = [row["high"] for row in rows] # list comprehension for mapping purposes!
    low_prices = [row["low"] for row in rows] # list comprehension for mapping purposes!


    #get the high and low price from each day using min and max
    recent_high = max(high_prices)
    recent_low = min(low_prices)

    #best way to get a CSV file path

    csv_filepath = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
    write_to_csv(rows, csv_filepath)

    #info output
    print("-------------------------")
    print("SELECTED SYMBOL: " + SYMBOL)
    print("-------------------------")
    print("REQUESTING STOCK MARKET DATA...")
    #datetime function
    today = datetime.datetime.today()
    print("REQUEST AT: " + today.strftime("%Y-%m-%d %I:%M %p"))
    #continue to print the information from the parsed response
    print("-------------------------")
    print(f"LATEST DAY: {last_refreshed}")
    print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
    print(f"RECENT HIGH: {to_usd(float(recent_high))}")
    print(f"RECENT LOW: {to_usd(float(recent_low))}")
    print("-------------------------")

    benchmark = .10
    email_trigger = 0.20

    if(recommendation(latest_close, recent_low) < benchmark):
        print("RECOMMENDATION: BUY!")
        print("REASON: THE STOCK HAS SUFFICIENT GROWTH POTENTIAL TO SUGGEST INVESTING.")
        print("THIS STOCK'S LATEST CLOSING PRICE IS BELOW 10% OF ITS RECENT LOW.")
    else:
        print("RECOMMENDATION: DO NOT BUY!")
        print("REASON: THE STOCK DOES NOT HAVE SUFFICIENT GROWTH POTENTIAL TO SUGGEST INVESTING.")
        print("THIS STOCK'S LATEST CLOSING PRICE IS ABOVE 10% OF ITS RECENT LOW.")
    print("-------------------------")
    print(f"WRITING DATA TO CSV: {csv_filepath}")
    print("-------------------------")
    print("HAPPY INVESTING!")
    print("-------------------------")

#---------------------------------------------------------------------------------------------------------
    
#if recent_high_var >= latest_close_var * 1.10:
#    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "OOPS, please set env var called 'SENDGRID_API_KEY'")
#    MY_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", "OOPS, please set env var called 'MY_EMAIL_ADDRESS'")
#    client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
#    print("CLIENT:", type(client))
#    subject = f"PRICE MOVEMENT ALERT: {SYMBOL} UP MORE THAN 10%"
#    html_content = f"Hey there! We are sending this message to inform you that {SYMBOL}, the stock you are tracking, has recently surpassed its latest closing price by more than 10%. This is a stock to watch -- happy investing!"
#    print("HTML:", html_content)
#    message = Mail(from_email=MY_ADDRESS, to_emails=SEND_ADDRESS, subject=subject, html_content=html_content)
#    try:
#        response = client.send(message)
#
#        print("RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
#        print(response.status_code) #> 202 indicates SUCCESS
#        print(response.body)
#        print(response.headers)
#    except Exception as e:
#        print("OOPS", e.message)
#else:
#    exit()