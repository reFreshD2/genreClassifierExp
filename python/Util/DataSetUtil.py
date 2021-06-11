import mysql.connector
import numpy as np
import pandas as pd
import json
from pandas import DataFrame
from sklearn.model_selection import train_test_split


class DataSetUtil:
    __config = {
        'user': 'genre',
        'password': 'genre',
        'host': '157.230.106.225',
        'database': 'genre',
        'port': '3306',
    }
    __con = None
    __map = {}

    def __getTargetMap(self):
        selectQuery = "SELECT DISTINCT genre FROM music_metrics"
        result = {}
        with self.__con.cursor() as cursor:
            cursor.execute(selectQuery)
            rows = cursor.fetchall()
            for i in range(0, len(rows)):
                result[rows[i][0]] = i
        return result

    def __prepareDataFrame(self, dataFrame):
        dataFrame.drop(['audio_file_id', 'id'], axis=1, inplace=True)
        dataFrame = pd.get_dummies(dataFrame, prefix=['rhythm'], columns=['rhythm'])
        dataFrame = pd.get_dummies(dataFrame, prefix=['rate'], columns=['rate'])
        dataFrame.loc[:, 'Гул'] = 0
        dataFrame.loc[:, 'Низ'] = 0
        dataFrame.loc[:, 'Полнота'] = 0
        dataFrame.loc[:, 'Теплота'] = 0
        dataFrame.loc[:, 'Ясность'] = 0
        dataFrame.loc[:, 'Мутность'] = 0
        dataFrame.loc[:, 'Резкость'] = 0
        dataFrame.loc[:, 'Шиперние'] = 0
        dataFrame.loc[:, 'Звонкость'] = 0
        dataFrame.loc[:, 'Плотность'] = 0
        dataFrame.loc[:, 'Присутствие'] = 0
        for index, row in dataFrame.iterrows():
            musicInstrumentsSoundCharacter = json.loads(row['instruments_sounds_character'])
            dataFrame.loc[index, 'Гул'] = musicInstrumentsSoundCharacter.get('Гул')
            dataFrame.loc[index, 'Низ'] = musicInstrumentsSoundCharacter.get('Низ')
            dataFrame.loc[index, 'Полнота'] = musicInstrumentsSoundCharacter.get('Полнота')
            dataFrame.loc[index, 'Теплота'] = musicInstrumentsSoundCharacter.get('Теплота')
            dataFrame.loc[index, 'Ясность'] = musicInstrumentsSoundCharacter.get('Ясность')
            dataFrame.loc[index, 'Мутность'] = musicInstrumentsSoundCharacter.get('Мутность')
            dataFrame.loc[index, 'Резкость'] = musicInstrumentsSoundCharacter.get('Резкость')
            dataFrame.loc[index, 'Шиперние'] = musicInstrumentsSoundCharacter.get('Шиперние')
            dataFrame.loc[index, 'Звонкость'] = musicInstrumentsSoundCharacter.get('Звонкость')
            dataFrame.loc[index, 'Плотность'] = musicInstrumentsSoundCharacter.get('Плотность')
            dataFrame.loc[index, 'Присутствие'] = musicInstrumentsSoundCharacter.get('Присутствие')
            dataFrame.loc[index, 'music_form'] = len(row['music_form'])
            # dataFrame.loc[index, 'genre'] = self.__map.get(row['genre'])
        dataFrame.drop(['instruments_sounds_character'], axis=1, inplace=True)
        return dataFrame

    def __getTrainTestSplit(self, X, Y, testSize):
        countOfClassInTest = round(testSize / len(self.__map))
        trainX = pd.DataFrame(columns=X.columns)
        testX = pd.DataFrame(columns=X.columns)
        trainY = pd.DataFrame(columns=Y.columns)
        testY = pd.DataFrame(columns=Y.columns)
        currentClass = Y.iloc[0]['genre']
        currentCountOfTest = 0
        for index, row in Y.iterrows():
            if row['genre'] == currentClass:
                if currentCountOfTest < countOfClassInTest:
                    testY.loc[index] = row['genre']
                    testX.loc[index] = X.iloc[index]
                    currentCountOfTest += 1
                else:
                    trainY.loc[index] = row
                    trainX.loc[index] = X.iloc[index]
            else:
                currentClass = row['genre']
                currentCountOfTest = 1
                testY.loc[index] = row
                testX.loc[index] = X.iloc[index]
        return trainX, testX, trainY, testY

    def __init__(self):
        if self.__con is None:
            self.__con = mysql.connector.connect(**self.__config)
        self.__map = self.__getTargetMap()

    def getTrainTestSplit(self, count, type):
        selectQuery = "SELECT * FROM music_metrics"
        with self.__con.cursor() as cursor:
            cursor.execute(selectQuery)
            df = DataFrame(cursor.fetchall())
            df.columns = cursor.column_names
        df = self.__prepareDataFrame(df)
        feature = df.columns.values
        feature = np.delete(feature, 10)
        X = df[feature]
        Y = df[['genre']]
        size = len(df) - round(len(df) * (int(count) / 100))
        if type == 'random':
            return train_test_split(X, Y, test_size=size, random_state=0)
        elif type == 'equable':
            return self.__getTrainTestSplit(X, Y, size)

    def getTargetName(self, id):
        invertMap = {v: k for k, v in self.__map.items()}
        return invertMap.get(id)
