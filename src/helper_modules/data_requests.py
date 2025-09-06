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
    print(get_ticker())

def get_ticker():
    """
    returns the ticker for the company name provided
    """
    while True:
        name = input("Please provide a valid company name or ticker: ")

        company_name = name.strip()
        parameters = {
            "query": company_name,
            "apikey": API_KEY
        }
        
        try:
            response = requests.get(f"{BASE_URL}/search-symbol", params=parameters)
            print(response.url)
            print(response.status_code)

            if response.status_code == 200:
                logger.info(f"Request successful for request at url: {response.url}")
                shared_logger.info(f"Request successful for request at url: {response.url}")
                response = response.json()
                
                if not response:
                    print("Please provide a valid company\n")
                    continue
            else:
                response.raise_for_status()

            return response

        except Exception as e:
            logger.warning(f"response request has failed, status code: {response.status_code}")
            shared_logger.warning(f"response request has failed, status code: {response.status_code}")
            print(e)


def get_financials():
    ...


if __name__ == "__main__":
    main()