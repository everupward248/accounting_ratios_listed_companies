from src.helper_modules.logger_setup import get_logger, shared_logger
from src.helper_modules import accounting_ratios as ar
from src.helper_modules import data_requests as dr
from tabulate import tabulate
import pandas as pd
import datetime as dt
import sys

logger = get_logger(__name__)

# functions for financial statements
def main():
    valuation("AAPL", 5)

# .tolist() used, as if the dataframe is passed directly to tabulate() the type checker will raise a warning though the function still executes without issue
def get_balance_sheet(ticker: str) -> None:
    """
    retrieves the balance sheet data for a company when specified in the cli
    
    """
    limit = dr.get_period()
    if (df := dr.get_bs(ticker, limit)) is not None and not df.empty:
        df_transposed = df.transpose()
        print(tabulate(df_transposed.reset_index().values.tolist(), tablefmt="grid"))
        logger.info(f"The balance sheet data for the requested company has been successfully returned to the user: {df["symbol"][0]}")
        shared_logger.info(f"The balance sheet data for the requested company has been successfully returned to the user: {df["symbol"][0]}")
    else:
        print("There was an issue rendering your request. Please try again.")
        logger.warning(f"Function returned: {df}")
        shared_logger.warning(f"Function returned: {df}")

# .tolist() used, as if the dataframe is passed directly to tabulate() the type checker will raise a warning though the function still executes without issue
def get_income_statement(ticker: str) -> None:
    """
    retrieves the income statement data for a company when specified in the cli
    
    """
    limit = dr.get_period()
    if (df := dr.get_is(ticker, limit)) is not None and not df.empty: 
        df_transposed = df.transpose()
        print(tabulate(df_transposed.reset_index().values.tolist(), tablefmt="grid"))
        logger.info(f"The income statement data for the requested company has been successfully returned to the user: {df["symbol"][0]}")
        shared_logger.info(f"The income statement data for the requested company has been successfully returned to the user: {df["symbol"][0]}")
    else:
        print("There was an issue rendering your request. Please try again.")
        logger.warning(f"Function returned: {df}")
        shared_logger.warning(f"Function returned: {df}")

# .tolist() used, as if the dataframe is passed directly to tabulate() the type checker will raise a warning though the function still executes without issue
def get_cash_flows(ticker: str) -> None:
    """
    retrieves the cash flows data for a company when specified in the cli
    
    """
    limit = dr.get_period()
    if (df := dr.get_cf(ticker, limit)) is not None and not df.empty: 
        df_transposed = df.transpose()
        print(tabulate(df_transposed.reset_index().values.tolist(), tablefmt="grid"))
        logger.info(f"The cash flows data for the requested company has been successfully returned to the user: {df["symbol"][0]}")
        shared_logger.info(f"The cash flows data for the requested company has been successfully returned to the user: {df["symbol"][0]}")
    else:
        print("There was an issue rendering your request. Please try again.")
        logger.warning(f"Function returned: {df}")
        shared_logger.warning(f"Function returned: {df}")

# functions for ratios
def liquidity(ticker: str, limit: int) -> pd.DataFrame:
    """
    obtains the liquidity ratios for a listed company
    
    """
    if (bs := dr.get_bs(ticker, limit)) is not None:
        # create a copy of the balance sheet dataframe otherwise .apply() will give a warning
        ratio_data = bs.copy(deep=True)
        
        # apply the liquidity ratios to the balance sheet data
        ratio_data["current_ratio"] = ratio_data.apply(
            lambda x: round(ar.current_ratio(x["totalCurrentAssets"], x["totalCurrentLiabilities"]), 3), axis=1
            )
        ratio_data["quick_ratio"] = ratio_data.apply(
            lambda x: round(ar.quick_ratio(x["totalCurrentAssets"], x["inventory"], x["totalCurrentLiabilities"]), 3), axis=1
            )
        ratio_data["cash_ratio"] = ratio_data.apply(
            lambda x: round(ar.cash_ratio(x["cashAndCashEquivalents"], x["totalCurrentLiabilities"]), 3), axis=1
            )
        
        # create a list of the ratio columns and to pass as headers to tabulate
        cols = ["fiscalYear", "date", "current_ratio", "quick_ratio", "cash_ratio"]
        liquidity_ratios = ratio_data[cols]
        liquidity_ratios_list = liquidity_ratios.values.tolist()

        print(tabulate(liquidity_ratios_list, headers=cols, tablefmt="grid"))
        logger.info(f"The liquidity ratios have been provided for {ratio_data["symbol"][0]}")
        shared_logger.info(f"The liquidity ratios have been provided for {ratio_data["symbol"][0]}")
        return liquidity_ratios
    else:
        logger.warning(f"The liquidity ratios failed, ensure valid ticker")
        shared_logger.warning(f"The liquidity ratios failed, ensure valid ticker")
        sys.exit("WARNING(NO DATA RETURNED): Ensure that company ticker provided is a valid ticker of a listed company.")

def profitability(ticker: str, limit: int) -> pd.DataFrame:
    """
    obtains the profitability ratios for a listed company
    
    """
    # obtain the data across all financial statements to compute the ratios
    if (inc_s := dr.get_is(ticker, limit)) is not None and (bs := dr.get_bs(ticker, limit)) is not None and (cf := dr.get_cf(ticker, limit)) is not None:
        # create a copy of the balance sheet dataframe otherwise .apply() will give a warning
        is_data = inc_s.copy(deep=True)
        bs_data = bs.copy(deep=True)
        cf_data = cf.copy(deep=True)
        # merge the financial statements on fiscal year
        # starting with the is and bs, then the cf
        merged_df = pd.merge(is_data, bs_data, on="fiscalYear", how="inner", suffixes=("", "_df2"))
        merged_df = pd.merge(merged_df, cf_data, on="fiscalYear", how="inner", suffixes=("", "_df2"))

        # apply the profitability ratios to the income statement data
        merged_df["gross_profit_margin"] = merged_df.apply(lambda x: round(ar.gross_profit_margin(x["grossProfit"], x["revenue"]), 3), axis=1)
        merged_df["operating_profit_margin"] = merged_df.apply(lambda x: round(ar.operating_profit_margin(x["operatingIncome"], x["revenue"]), 3), axis=1)
        merged_df["net_profit_margin"] = merged_df.apply(lambda x: round(ar.operating_profit_margin(x["netIncome"], x["revenue"]), 3), axis=1)
        
        # user provides an option for the calculation of capital employed to be passed to the roce computation
        while True:
            try:
                capital_employed_type = int(input("select 1 for total assets less current liabilities or select 2 for equity plus non-current liabilities as measure of capital employed? ").strip())

                if capital_employed_type == 1:
                    merged_df["capital_employed"] = merged_df.apply(lambda x: round(ar.capital_employed(x["totalAssets"], x["totalCurrentLiabilities"], 1), 3), axis=1)
                    break
                elif capital_employed_type == 2:
                    merged_df["capital_employed"] = merged_df.apply(lambda x: round(ar.capital_employed(x["totalStockholdersEquity"], x["longTermDebt"] + x["capitalLeaseObligations"], 2), 3), axis=1)
                    break
                else:
                    print("must select a number 1 or 2")
                    continue
            except EOFError:
                sys.exit("program quit...")
            except Exception as e:
                print(e)
                continue

        merged_df["return_on_capital_employed"] = merged_df.apply(lambda x: round(ar.roce(x["operatingIncome"], x["capital_employed"]), 3), axis=1)
        merged_df["operating_cash_flow_margin"] = merged_df.apply(lambda x: round(ar.operating_cash_flow_margin(x["operatingCashFlow"], x["revenue"]), 3), axis=1)
        merged_df["free_cash_flow_margin"] = merged_df.apply(lambda x: round(ar.free_cash_flow_margin(x["freeCashFlow"], x["revenue"]), 3), axis=1)
        merged_df["return_on_equity"] = merged_df.apply(lambda x: round(ar.return_on_equity(x["netIncome"], x["totalStockholdersEquity"]), 3), axis=1)
        merged_df["return_on_assets"] = merged_df.apply(lambda x: round(ar.return_on_assets(x["netIncome"], x["totalAssets"]), 3), axis=1)
        
        
        # create a list of the ratio columns and to pass as headers to tabulate
        cols = ["fiscalYear", "date", "gross_profit_margin", "operating_profit_margin", "net_profit_margin", "return_on_capital_employed", "operating_cash_flow_margin", "free_cash_flow_margin", "return_on_equity", "return_on_assets"]
        profitability_ratios = merged_df[cols]
        profitability_ratios_list = profitability_ratios.values.tolist()

        print(tabulate(profitability_ratios_list, headers=cols, tablefmt="grid"))
        logger.info(f"The profitability ratios have been provided for {merged_df["symbol"][0]}")
        shared_logger.info(f"The profitability ratios have been provided for {merged_df["symbol"][0]}")
        return profitability_ratios
    else:
        logger.warning(f"The profitability ratios failed, ensure valid ticker")
        shared_logger.warning(f"The profitability ratios failed, ensure valid ticker")
        sys.exit("WARNING(NO DATA RETURNED): Ensure that company ticker provided is a valid ticker of a listed company.")

def gearing(ticker: str, limit: int) -> pd.DataFrame:
    """
    obtains the gearing ratios for a listed company
    
    """
    # obtain the data across all financial statements to compute the ratios
    if (inc_s := dr.get_is(ticker, limit)) is not None and (bs := dr.get_bs(ticker, limit)) is not None:
        # create a copy of the balance sheet dataframe otherwise .apply() will give a warning
        is_data = inc_s.copy(deep=True)
        bs_data = bs.copy(deep=True)
        merged_df = pd.merge(is_data, bs_data, on="fiscalYear", how="inner", suffixes=("", "_df2"))

        merged_df["debt_to_equity"] = merged_df.apply(lambda x: round(ar.debt_equity_ratio(x["totalLiabilities"], x["totalStockholdersEquity"]), 3), axis=1)
        merged_df["interest_cover"] = merged_df.apply(lambda x: round(ar.interest_cover(x["ebit"], x["interestExpense"]), 3), axis=1)
        merged_df["equity_ratio"] = merged_df.apply(lambda x: round(ar.equity_ratio(x["totalEquity"], x["totalAssets"]), 3), axis=1)
        merged_df["debt_ratio"] = merged_df.apply(lambda x: round(ar.debt_ratio(x["totalDebt"], x["totalAssets"]), 3), axis=1)


        # create a list of the ratio columns and to pass as headers to tabulate
        cols = ["fiscalYear", "date", "debt_to_equity", "interest_cover", "equity_ratio", "debt_ratio"]
        gearing_ratios = merged_df[cols]
        gearing_ratios_list = gearing_ratios.values.tolist()

        print(tabulate(gearing_ratios_list, headers=cols, tablefmt="grid"))
        logger.info(f"The gearing ratios have been provided for {merged_df["symbol"][0]}")
        shared_logger.info(f"The gearing ratios have been provided for {merged_df["symbol"][0]}")
        return gearing_ratios
    else:
        logger.warning(f"The profitability ratios failed, ensure valid ticker")
        shared_logger.warning(f"The profitability ratios failed, ensure valid ticker")
        sys.exit("WARNING(NO DATA RETURNED): Ensure that company ticker provided is a valid ticker of a listed company.")

def valuation(ticker: str, limit: int) -> pd.DataFrame:
    """
    obtain the valuation ratios for a listed company
    
    """
    if (inc_s := dr.get_is(ticker, limit)) is not None:
        is_data = inc_s.copy(deep=True)
        
        # convert the dates for the search into a list and slice the earliest and lates periods to pass as query parameters into the stock price search
        dates = list(is_data["date"])
        from_date = dates[-1]
        to_date = dates[0]

        # obtain the rows of the stock prices for only the financial statement year end dates
        if (stock_prices := dr.stock_prices(ticker, from_date, to_date)) is not None:
            # initialize an empty dataframe with the stock price columns to extract only the ye dates, 
            df = pd.DataFrame(columns=stock_prices.columns)

            # append only the year date prices
            for i in range(len(stock_prices)):
                if stock_prices.loc[i]["date"] in dates:
                    df.loc[i] = stock_prices.loc[i]
            
            # there could potentially be misses if the year end date on the financials was not an actively trading day
            # create a separate list for the misses then try decrementing dates until a valid date is found and then append to the df
            date_miss = []

            try:
                for date in dates:
                    if date not in df.date.to_string(index=False):
                        date_miss.append(date)
            except Exception as e:
                print(e)
            
            # convert the date misses into datetimes and then decrement and retry appending from the stock list dates
            # decrement for a range of a 3 days to ensure a hit
            # use datetime.strptime to parse the date string according to its format and then convert to datetime, use timedelta to decrement the days

            if len(date_miss) > 0:
                logger.warning(f"the following dates were not obtained for the stock price: {date_miss}")
                shared_logger.warning(f"the following dates were not obtained for the stock price: {date_miss}")

                date_format_string = "%Y-%m-%d"

                try:
                    # create a list of lists to store the date misses with their decrements
                    converted_date_misses = []

                    for date in date_miss:
                        converted_date = dt.datetime.strptime(date, date_format_string)
                        
                        decremented_dates = []

                        for i in range(3):
                            decremented_date = converted_date - dt.timedelta(days=i+1)
                            # convert the datetime objects into dates before converting to strings
                            decremented_dates.append(str(decremented_date.date()))
                        
                        converted_date_misses.append(decremented_dates)
                
                    logger.info("missing dates have been successuflly decremented and converted into date strings")
                    shared_logger.info("missing dates have been successuflly decremented and converted into date strings")
                except Exception as e:
                    print(e)
                    logger.warning(f"{e}")
                    shared_logger.warning(f"{e}")
            
                # iterate throught the converted date misses until a stock price is found
                for date in converted_date_misses:
                    # append only the year date prices
                    hit = False

                    for i in range(len(stock_prices)):
                        if hit == True:
                            break
                        elif stock_prices.loc[i]["date"] in date:
                            df.loc[i] = stock_prices.loc[i]
                            hit = True
                        else:
                            continue
                
                # sort the df by the date column
                df = df.sort_values(by=["date"], ascending=False)
                # extract only the year to match on the fiscal year
                df["fiscalYear"] = df["date"].str.split("-").str[0]

            else:
                pass

            stock_price_data = df.copy(deep=True)
            # merge the data sets
            merged_df = pd.merge(is_data, stock_price_data, on="fiscalYear", how="inner", suffixes=("", "_df2"))

            merged_df["p/e_ratio"] = merged_df.apply(lambda x: round(ar.pe_ratio(x["close"], x["eps"]), 3), axis=1)
            merged_df["p/e_ratio_diluted"] = merged_df.apply(lambda x: round(ar.pe_ratio(x["close"], x["epsDiluted"]), 3), axis=1)

            # create a list of the ratio columns and to pass as headers to tabulate
            cols = ["fiscalYear", "date", "eps", "epsDiluted", "p/e_ratio", "p/e_ratio_diluted", "close"]
            valuation_ratios = merged_df[cols]
            valuation_ratios_list = valuation_ratios.values.tolist()

            print(tabulate(valuation_ratios_list, headers=cols, tablefmt="grid"))
            logger.info(f"The valuation ratios have been provided for {merged_df["symbol"][0]}")
            shared_logger.info(f"The valuation ratios have been provided for {merged_df["symbol"][0]}")
            return valuation_ratios
        else:
            logger.warning(f"The valuation ratios failed, ensure valid ticker")
            shared_logger.warning(f"The valuation ratios failed, ensure valid ticker")
            sys.exit("WARNING(NO DATA RETURNED): Ensure that company ticker provided is a valid ticker of a listed company.")
                    
    else:
        logger.warning(f"The valuation ratios failed, ensure valid ticker")
        shared_logger.warning(f"The valuation ratios failed, ensure valid ticker")
        sys.exit("WARNING(NO DATA RETURNED): Ensure that company ticker provided is a valid ticker of a listed company.")

def all_ratios(ticker: str, limit: int) -> None:
    """
    returns all ratios of a listed company
    
    """
    print("\n")
    print("Liquidity Ratios")
    liquidity_df = liquidity(ticker, limit)
    print("\n")
    print("Profitability Ratios")
    profitability_df = profitability(ticker, limit)
    print("\n")
    print("Gearing Ratios")
    gearing_df = gearing(ticker, limit)
    print("\n")
    print("Valuation Ratios")
    valuation_df = valuation(ticker, limit)
 


if __name__ == "__main__":
    main()