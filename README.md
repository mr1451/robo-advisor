### Robo Advisor Project

Solution for: https://github.com/prof-rossetti/georgetown-opim-243-201901/blob/master/projects/robo-advisor.md

### Installation

Clone or download [this repository] (https://github.com/mr1451/robo-advisor) onto your computer. Then navigate there from the command line:

```sh
cd Desktop/robo-advisor
```

### Environment Setup

Create and activate a new Anaconda virtual environment:

```sh
conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env
```

From within the virtual environment, install the required packages specified in the "requirements.txt" file you created:

```sh
pip install -r requirements.txt
```

### AlphaVantage API Setup

Claim your free API key at the following link: https://www.alphavantage.co/support/#api-key. From there, create a .env file in Desktop/robo-advisor and copy and paste ALPHAVANTAGE_API_KEY = "Z768MPA4BB9AO8XH" into it.

### SendGrid API Setup

Sign up for a free SendGrid account at https://signup.sendgrid.com/. Then, create an API key with "full access permissions" at https://app.sendgrid.com/settings/api_keys. Store the API Key value in the .env file in Desktop/robo-advisor called SENDGRID_API_KEY. Also set an environment variable called MY_EMAIL_ADDRESS to be the email address you just associated with your SendGrid account (e.g. "mr1451@georgetown.edu").

### Usage

From within the virtual environment, demonstrate your ability to run the Python script from the command-line:

```sh
python app/robo_advisor.py