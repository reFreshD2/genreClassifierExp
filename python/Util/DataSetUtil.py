import mysql.connector
from pandas import DataFrame
from sklearn.model_selection import train_test_split


class DataSetUtil:
    __config = {
        'user': 'root',
        'password': '',
        'host': 'mysql',
        'database': 'genre'
    }
    __con = None

    def __prepareDataFrame(self, dataFrame):
        return dataFrame

    def __getTrainTestSplit(self, X, Y, count):
        return X, Y

    def __init__(self):
        if self.__con is None:
            self.__con = mysql.connector.connect(**self.__config)

    def getDataSet(self, count, type):
        selectQuery = "SELECT * FROM music_metrics LIMIT 5"
        with self.__con.cursor() as cursor:
            cursor.execute(selectQuery)
            df = DataFrame(cursor.fetchall())
            df.columns = cursor.keys()
        df = self.__prepareDataFrame(df)
        feature = []
        X = df[feature]
        Y = df[['genre']]
        if type == 'random':
            return train_test_split(X, Y, test_size=len(df) * (count/100), random_state=0)
        elif type == 'equable':
            return self.__getTrainTestSplit(X, Y, count)
