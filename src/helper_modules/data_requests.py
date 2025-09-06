from src.helper_modules.logger_setup import get_logger, shared_logger
import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")

logger = get_logger(__name__)

def main():
    print(get_name())

def get_name():
    """
    returns the company name for the ticker name provided

    """
    while True:
        name = input("Please provide a valid company ticker: ")

        company_name = name.strip()
        parameters = {
            "query": company_name,
            "apikey": API_KEY
        }
        
        try:
            response = requests.get(f"{BASE_URL}/search-symbol", params=parameters)

            if response.status_code == 200:
                logger.info(f"Request successful, status code: {response.status_code} for request at url: {response.url}")
                shared_logger.info(f"Request successful for request at url: {response.url}")
                response = response.json()
                
                if not response:
                    print("Invalid ticker provided. Please ensure this is the company's valid ticker.")
                    continue
                # data returned is for all exchanges, obtain the ticker for the US exchange
                for x in response:
                    if x["currency"] == "USD":
                        company_name = str(x["name"])
                    else:
                        pass
            else:
                response.raise_for_status()
            return company_name
        except requests.HTTPError:
            logger.warning(requests.HTTPError)
            shared_logger.warning(requests.HTTPError)
        except Exception as e:
            logger.warning(f"response request has failed, status code: {response.status_code}")
            shared_logger.warning(f"response request has failed, status code: {response.status_code}")
            print(e)

def get_ticker() -> str:
    """
    returns the ticker for the company name provided

    """
    while True:
        ticker = input("Please provide a valid, legally registered company name: ")

        company_ticker = ticker.strip()
        parameters = {
            "query": company_ticker,
            "apikey": API_KEY
        }
        
        try:
            response = requests.get(f"{BASE_URL}/search-name", params=parameters)

            if response.status_code == 200:
                logger.info(f"Request successful, status code: {response.status_code} for request at url: {response.url}")
                shared_logger.info(f"Request successful for request at url: {response.url}")
                response = response.json()
                
                if not response:
                    print("Invalid company name provided. Please ensure that the name provided is the company's legally registered name.")
                    continue

                # data returned is for all exchanges, obtain the ticker for the US exchange
                for x in response:
                    if x["currency"] == "USD":
                        ticker = str(x["symbol"])
                    else:
                        pass
            else:
                response.raise_for_status()
            return ticker
        except requests.HTTPError:
            logger.warning(requests.HTTPError)
            shared_logger.warning(requests.HTTPError)
        except Exception as e:
            logger.warning(f"response request has failed, status code: {response.status_code}")
            shared_logger.warning(f"response request has failed, status code: {response.status_code}")
            print(e)

def get_financials():
    ...


if __name__ == "__main__":
    main()