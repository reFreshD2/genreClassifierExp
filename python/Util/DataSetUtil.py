import mysql.connector


class DataSetUtil:
    __config = {
        'user': 'root',
        'password': '',
        'host': 'mysql',
        'database': 'genre'
    }
    __con = None

    def __init__(self):
        if self.__con is None:
            self.__con = mysql.connector.connect(**self.__config)
