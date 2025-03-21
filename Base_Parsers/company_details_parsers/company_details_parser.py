import io
import sys
import yfinance
import yahooquery
import pandas
import logging

# Create a string buffer to capture standard error
err_buffer = io.StringIO()

# Save the original stderr stream
original_stderr = sys.stderr

def company_details_parser(ticker):
    try:
        # Redirect stderr to the buffer
        sys.stderr = err_buffer

        yfinance_info = yfinance.Ticker(ticker[2]).info
        yfinance_history_metadata = yfinance.Ticker(ticker[2]).history_metadata
        
        # Reset stderr to its original value
        sys.stderr = original_stderr
        
        info = {**yfinance_info,
                **yfinance_history_metadata}
        # yahooquery_info = {**yahooquery.Ticker(ticker[2]).summary_detail[ticker[2]],
        #                    **yahooquery.Ticker(ticker[2]).summary_profile[ticker[2]],
        #                    **yahooquery.Ticker(ticker[2]).key_stats[ticker[2]]}
        # info = {**yfinance_info,
        #         **yahooquery_info}
        company_details_dict = {
            'tickerId': ticker[0],
            'sector': info.get('sector'),
            'industry': info.get('industry'),
            'fullTimeEmployees': info.get('fullTimeEmployees'),
            'longBusinessSummary': info.get('longBusinessSummary'),
            'city': info.get('city'),
            'state': info.get('state'),
            'country': info.get('country'),
            'website': info.get('website'),
            'ebitdaMargins': info.get('ebitdaMargins'),
            'profitMargins': info.get('profitMargins'),
            'grossMargins': info.get('grossMargins'),
            'operatingCashflow': info.get('operatingCashflow'),
            'revenueGrowth': info.get('revenueGrowth'),
            'operatingMargins': info.get('operatingMargins'),
            'ebitda': info.get('ebitda'),
            'targetLowPrice': info.get('targetLowPrice'),
            'grossProfits': info.get('grossProfits'),
            'freeCashflow': info.get('freeCashflow'),
            'targetMedianPrice': info.get('targetMedianPrice'),
            'currentPrice': info.get('currentPrice'),
            'earningsGrowth': info.get('earningsGrowth'),
            'currentRatio': info.get('currentRatio'),
            'returnOnAssets': info.get('returnOnAssets'),
            'numberOfAnalystOpinions': info.get('numberOfAnalystOpinions'),
            'targetMeanPrice': info.get('targetMeanPrice'),
            'debtToEquity': info.get('debtToEquity'),
            'returnOnEquity': info.get('returnOnEquity'),
            'targetHighPrice': info.get('targetHighPrice'),
            'totalCash': info.get('totalCash'),
            'totalDebt': info.get('totalDebt'),
            'totalRevenue': info.get('totalRevenue'),
            'totalCashPerShare': info.get('totalCashPerShare'),
            'financialCurrency': info.get('financialCurrency'),
            'revenuePerShare': info.get('revenuePerShare'),
            'quickRatio': info.get('quickRatio'),
            'recommendationMean': info.get('recommendationMean'),
            'exchange': info.get('exchange'),
            'shortName': info.get('shortName'),
            'longName': info.get('longName'),
            'exchangeTimezoneName': info.get('exchangeTimezoneName'),
            'exchangeTimezoneShortName': info.get('exchangeTimezoneShortName'),
            'quoteType': info.get('quoteType'),
            'symbol': ticker[2],
            'messageBoardId': info.get('messageBoardId'),
            'market': info.get('market'),
            'annualHoldingsTurnover': info.get('annualHoldingsTurnover'),
            'enterpriseToRevenue': info.get('enterpriseToRevenue'),
            'enterpriseToEbitda': info.get('enterpriseToEbitda'),
            '_52WeekChange': info.get('52WeekChange'),
            'forwardEps': info.get('forwardEps'),
            'revenueQuarterlyGrowth': info.get('revenueQuarterlyGrowth'),
            'sharesOutstanding': info.get('sharesOutstanding'),
            'annualReportExpenseRatio': info.get('annualReportExpenseRatio'),
            'totalAssets': info.get('totalAssets'),
            'bookValue': info.get('bookValue'),
            'sharesShort': info.get('sharesShort'),
            'sharesPercentSharesOut': info.get('sharesPercentSharesOut'),
            'lastFiscalYearEnd': pandas.to_datetime(info.get('lastFiscalYearEnd'), errors='coerce'),
            'heldPercentInstitutions': info.get('heldPercentInstitutions'),
            'netIncomeToCommon': info.get('netIncomeToCommon'),
            'trailingEps': info.get('trailingEps'),
            'lastDividendValue': info.get('lastDividendValue'),
            'SandP52WeekChange': info.get('SandP52WeekChange'),
            'priceToBook': info.get('priceToBook'),
            'heldPercentInsiders': info.get('heldPercentInsiders'),
            'nextFiscalYearEnd': pandas.to_datetime(info.get('nextFiscalYearEnd'), errors='coerce'),
            'mostRecentQuarter': pandas.to_datetime(info.get('mostRecentQuarter'), errors='coerce'),
            'shortRatio': info.get('shortRatio'),
            'sharesShortPreviousMonthDate': pandas.to_datetime(info.get('sharesShortPreviousMonthDate'), errors='coerce'),
            'floatShares': info.get('floatShares'),
            'beta': info.get('beta'),
            'enterpriseValue': info.get('enterpriseValue'),
            'priceHint': info.get('priceHint'),
            'lastSplitDate': pandas.to_datetime(info.get('lastSplitDate'), errors='coerce'),
            'lastSplitFactor': info.get('lastSplitFactor'),
            'lastDividendDate': pandas.to_datetime(info.get('lastDividendDate'), errors='coerce'),
            'earningsQuarterlyGrowth': info.get('earningsQuarterlyGrowth'),
            'priceToSalesTrailing12Months': info.get('priceToSalesTrailing12Months'),
            'dateShortInterest': pandas.to_datetime(info.get('dateShortInterest'), errors='coerce'),
            'pegRatio': info.get('pegRatio'),
            'forwardPE': info.get('forwardPE'),
            'shortPercentOfFloat': info.get('shortPercentOfFloat'),
            'sharesShortPriorMonth': info.get('sharesShortPriorMonth'),
            'impliedSharesOutstanding': info.get('impliedSharesOutstanding'),
            'category': info.get('category'),
            'previousClose': info.get('previousClose'),
            'regularMarketOpen': info.get('regularMarketOpen'),
            'twoHundredDayAverage': info.get('twoHundredDayAverage'),
            'trailingAnnualDividendYield': info.get('trailingAnnualDividendYield'),
            'payoutRatio': info.get('payoutRatio'),
            'regularMarketDayHigh': info.get('regularMarketDayHigh'),
            'averageDailyVolume10Day': info.get('averageDailyVolume10Day'),
            'regularMarketPreviousClose': info.get('regularMarketPreviousClose'),
            'fiftyDayAverage': info.get('fiftyDayAverage'),
            'trailingAnnualDividendRate': info.get('trailingAnnualDividendRate'),
            'open': info.get('open'),
            'averageVolume10days': info.get('averageVolume10days'),
            'dividendRate': info.get('dividendRate'),
            'exDividendDate': pandas.to_datetime(info.get('exDividendDate'), errors='coerce'),
            'regularMarketDayLow': info.get('regularMarketDayLow'),
            'currency': info.get('currency'),
            'trailingPE': info.get('trailingPE'),
            'regularMarketVolume': info.get('regularMarketVolume'),
            'marketCap': info.get('marketCap'),
            'averageVolume': info.get('averageVolume'),
            'dayLow': info.get('dayLow'),
            'ask': info.get('ask'),
            'askSize': info.get('askSize'),
            'volume': info.get('volume'),
            'fiftyTwoWeekHigh': info.get('fiftyTwoWeekHigh'),
            'fiveYearAvgDividendYield': info.get('fiveYearAvgDividendYield'),
            'fiftyTwoWeekLow': info.get('fiftyTwoWeekLow'),
            'tradeable': info.get('tradeable'),
            'dividendYield': info.get('dividendYield'),
            'bidSize': info.get('bidSize'),
            'dayHigh': info.get('dayHigh'),
            'regularMarketPrice': info.get('regularMarketPrice'),
            'instrumentType': info.get('instrumentType'),
        }
        return company_details_dict
    except Exception as e:
        logger = logging.getLogger('Logger')
        logger.info(f'Something went wrong with details parser: {e}')