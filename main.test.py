from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from Model.config import config
from Model import base, tickers, countries, stocks, company_details
from Control.Executioner.silent_executioner import silent_executioner
from Control.Base_Controllers.Inserters.base_inserter import base_inserter
from Control.Base_Controllers.Selectors.base_selector import base_selector
from Control.Base_Controllers.Updaters.base_updater import base_updater
from Control.Base_Controllers.Updaters.base_conditional_updater import base_conditional_updater
from Control.Base_Controllers.Selectors.base_conditional_ordered_limited_selector import base_conditional_ordered_limited_selector
# from Base_Parsers.Tickers_Parser.ticker_parser import ticker_value_list
from Base_Parsers.SQL_Select_To_Data_Parsers.sql_select_to_data_parser import sql_select_to_generator, sql_select_to_list
from Base_Parsers.Stock_Parsers.stock_parser import stock_parser
from Base_Parsers.company_details_parsers.company_details_parser import company_details_parser
from Control.Util_Controllers.modin_utils import init_modin
from tqdm import tqdm
import yfinance
import os


if __name__ == '__main__':
    os.environ["MODIN_ENGINE"] = "ray" # Modin will use Ray
    init_modin()
    engine = create_engine('postgresql+psycopg2://' + config()['user'] + ':' + config()['password'] + '@' + config()['host'] + '/' + config()['database'] + '', echo=False)    
    with engine.connect() as connection:
        with Session(engine).begin():            
            import pandas
            stock_data = pandas.read_sql(
                base_conditional_ordered_limited_selector(
                    table=base.Base.metadata.tables[stocks.Stocks.__tablename__],
                    columnName=base.Base.metadata.tables[stocks.Stocks.__tablename__].c.tickerId,
                    columnValue='1',
                    orderColumn=base.Base.metadata.tables[stocks.Stocks.__tablename__].c.date,
                    limitNumber=-1), connection)
            stock_data.set_index('date', inplace=True)
            stock_data.drop(columns=['stockId', 'tickerId'], inplace=True)
            
            from sklearn.preprocessing import StandardScaler
            standard_scaler = StandardScaler()
            scaled_stock_data = standard_scaler.fit_transform(stock_data)
            
            from sklearn.model_selection import train_test_split
            train_scaled_stock_data, test_scaled_stock_data = train_test_split(scaled_stock_data, test_size=0.2, shuffle=False)
            print(train_scaled_stock_data.shape)
            print(scaled_stock_data)

            from keras.models import Sequential
            model = Sequential()
            from keras.layers import LSTM
            model.add(LSTM(50, activation='relu', input_shape=(train_scaled_stock_data.shape[0], train_scaled_stock_data.shape[1])))
            from keras.layers import Dense
            model.add(Dense(1))
            model.compile(optimizer='adam', loss='mse')
            model.fit(train_scaled_stock_data, test_scaled_stock_data, epochs=200, verbose=0)
