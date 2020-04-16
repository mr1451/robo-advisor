# app/robo_advisor.py

# import my packages
import csv
import datetime as dt
import json
import os
import requests

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default="OOPS")

## DEFINE FUNCTIONS

def to_usd(amount):
    """
    Formats value as currency in US dollars.

    Params:
        n (numeric, like int or float), the number to be formatted in USD
    
    Examples:
        to_usd(412.281)
        to_usd(0.9842)
    """
    return "${0:,.2f}".format(amount)

def compile_url(symbol):
    """
    Takes user inputted symbol and compiles into request url along with API key for AlphaVantage.

    Params:
        SYMBOL (string, 3-4 letters), the user input to be located in AlphaVantage database
    
    Examples:
        compile_url (AMZN)
        compile_url (MSFT)
    """
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(request_url)
    #if symbol or API key is wrong
    if "Error Message" in response.text:
        print("We're sorry, but the stock ticker symbol you input does not exist per our records. Please try a different one!")
        exit()
    parsed_response = json.loads(response.text)
    return parsed_response

def transform_response(parsed_response):
    """
    XYZ

    Params:
        XYZ
    
    Examples:
        XYZ
    """
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
    """
    XYZ

    Params:
        XYZ
    
    Examples:
        XYZ
    """
    csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
    with open(csv_filepath, "w", newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader() # uses fieldnames set above
        for row in rows:
            writer.writerow(row)
    return True

def recommendation(latest_close, recent_low):
    """
    XYZ

    Params:
        XYZ
    
    Examples:
        XYZ
    """
    calculation = (float(latest_close) - float(recent_low))/float(recent_low)
    return calculation

def human_friendly_timestamp(request_time):
    """
    Reformats checkout date and time in a more human-friendly way (i.e. rounds to nearest minute, includes AM or PM at end of timestamp).
    Params:
        checkout_start_at (a datetime object), the checkout date and time to be returned as a string.
    Examples:
        human_friendly_timestamp(2020-02-02 20:20:20.202020)
        human_friendly_timestamp(1998-05-28 20:30:30.123456)
    """
    return request_time.strftime("%Y-%m-%d %I:%M %p")

## PROGRAM (INFO CAPTURE AND OUTPUT)

if __name__ == "__main__":

    request_time = dt.datetime.now()

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

    #function implement
    parsed_response = compile_url(SYMBOL)

    #most recent info - request
    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

    #function implement
    rows = transform_response(parsed_response)

    latest_close = rows[0]["close"]
    high_prices = [row["high"] for row in rows] # list comprehension for mapping purposes!
    low_prices = [row["low"] for row in rows] # list comprehension for mapping purposes!

    SEND_ADDRESS = input("Please input your email. We will send you an email update if your stock shows notable growth potential:")

    #identify daily high/low
    recent_high = max(high_prices)
    recent_low = min(low_prices)

    #CSV file path -- define

    csv_filepath = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
    write_to_csv(rows, csv_filepath)

    #INFO OUTPUT
    print("-------------------------")
    print("SELECTED SYMBOL: " + SYMBOL)
    print("-------------------------")
    print("REQUESTING STOCK MARKET DATA...")
    print("REQUEST AT: " + human_friendly_timestamp(request_time))
    #continue to print the information from the parsed response
    print("-------------------------")
    print(f"LATEST DAY: {last_refreshed}")
    print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
    print(f"RECENT HIGH: {to_usd(float(recent_high))}")
    print(f"RECENT LOW: {to_usd(float(recent_low))}")
    print("-------------------------")

    #PRODUCE RECOMMENDATION
    benchmark = .10
    email_trigger = 0.20

    if(recommendation(latest_close, recent_low) < benchmark):
        print("RECOMMENDATION: BUY!")
        print("REASON: THE STOCK HAS SUFFICIENT GROWTH POTENTIAL TO SUGGEST INVESTING.")
        print("THIS STOCK'S LATEST CLOSING PRICE IS 10% BELOW ITS RECENT LOW.")
    else:
        print("RECOMMENDATION: DO NOT BUY!")
        print("REASON: THE STOCK DOES NOT HAVE SUFFICIENT GROWTH POTENTIAL TO SUGGEST INVESTING.")
        print("THIS STOCK'S LATEST CLOSING PRICE IS 10% ABOVE OF ITS RECENT LOW.")
    print("-------------------------")
    print(f"WRITING DATA TO CSV: {csv_filepath}")
    print("-------------------------")
    print("HAPPY INVESTING!")
    print("-------------------------")

    #EMAIL SEND

    if (recommendation(latest_close, recent_low) < email_trigger):
        SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "OOPS, please set env var called 'SENDGRID_API_KEY'")
        MY_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", "OOPS, please set env var called 'MY_EMAIL_ADDRESS'")
        client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
        print("CLIENT:", type(client))
        subject = f"PRICE MOVEMENT ALERT: {SYMBOL} LATEST CLOSE 20% BELOW ITS RECENT LOW%"
        html_content = f"Hey there! We are sending this message to inform you that {SYMBOL}, the stock you are tracking, is 20% its recent low. This is a stock to watch -- happy investing!"
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