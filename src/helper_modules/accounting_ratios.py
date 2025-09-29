import logging
from src.helper_modules.logger_setup import get_logger, shared_logger

logger = get_logger(__name__)

# liquidity 
def current_ratio(current_assets: float, current_liabilities: float) -> float:
    """
    measures the company's ability to pay of its current liabilities with its total current assets

    """
    return current_assets / current_liabilities

def quick_ratio(current_assets: float, inventory: float, current_liabilities: float) -> float:
    """
    measures the company's ability to pay of its current liabilities with its total current assets but also accounts for the company's level of inventory as this is less liquid

    """
    return (current_assets - inventory) / current_liabilities

def cash_ratio(cash: float, current_liabilities: float) -> float:
    """
    measures the company's ability to pay of its current liabilities using only its cash and cash equivalents

    """
    return cash / current_liabilities

# profitability
def gross_profit_margin():
    ...

def operating_profit_margin():
    ...

def net_profit_margin():
    ...

def roce():
    """
    return on capital employed - 

    """

def cash_flow_margin():
    ...

def return_on_equity():
    ...

def return_on_assets():
    ...

# gearing
def debt_equity_ratio():
    ...

def interest_cover():
    ...

def equity_ratio():
    ...

def debt_ratio():
    ...

# valuation
def eps():
    ...
    
def p_e():
    ...