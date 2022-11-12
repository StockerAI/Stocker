import pandas as pd
from sklearn import svm

def base_svm(initial_dataframe, prediction_column_name, prediction_dataframe):
    '''
    Function for base `SVM` execution.
    
    Arguments:
        `initial_dataframe`: The Initial DataFrame to train the machine.
        `prediction_column_name`: The Name of the Column that needs to be predicted.
        `prediction_dataframe`: The Prediction DataFrame for the machine to predict.
    '''
    x_train = initial_dataframe.drop(columns=[prediction_column_name])
    y_train = pd.Series(initial_dataframe[prediction_column_name])
    _svm = svm.SVC()
    _svm.fit(X=x_train, y=y_train)
    prediction = _svm.predict(prediction_dataframe)
    return prediction
