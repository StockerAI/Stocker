import pandas as pd
from sklearn.linear_model import LinearRegression

def base_linear_regression(initial_dataframe, prediction_column_name, prediction_dataframe):
    '''
    Function for base `Linear Regression` execution.
    Arguments:
        `initial_dataframe`: The Initial DataFrame to train the machine.
        `prediction_column_name`: The Name of the Column that needs to be predicted.
        `prediction_dataframe`: The Prediction DataFrame for the machine to predict.
    '''
    x_train = initial_dataframe.drop(columns=[prediction_column_name])
    y_train = pd.Series(initial_dataframe[prediction_column_name])
    lr = LinearRegression()
    lr.fit(X=x_train, y=y_train)
    prediction = lr.predict(prediction_dataframe)
    return prediction
