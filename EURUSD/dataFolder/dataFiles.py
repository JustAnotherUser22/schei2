

#############
#i dati si possono scaricare da qua
#http://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/eurusd/2022
#############




#BASE_PATH = "daUSB/schei/EURUSD/"
BASE_PATH = "schei2/EURUSD/dataFolder/"
PATH_LOG = "log.txt"


PATH_LAST_PARAMETERS = "schei2/EURUSD/log/last_parameters_macd.txt"


#dati giornalieri da 2010 a 2023
ALL_DATA = 'EUR_USD Dati Storici.csv'

#dati giornalieri del 2022
ALL_DAYLY_DATA = 'EUR_USD Dati Storici 2022.csv'

#dati del 2022 con intervallo 1 minuto
FILE_2022_1M = 'DAT_ASCII_EURUSD_M1_2022.csv'

#dati del 2022 con intervallo 1 minuto su cui è stata calcolata 
#una classe basandosi sui 100 valori futuri
FILE_2022_1M_WITH_WINDOW = 'DAT_ASCII_EURUSD_M1_2022_window_100.csv'

#dati di gennaio 2022 con intervallo 1 minuto
FILE_2022_1M_GENUARY = 'DAT_ASCII_EURUSD_M1_2022_gennaio.csv'

#dati di gennaio 2022 con intervallo 1 minuto su cui è stata calcolata 
#una classe basandosi sui 100 valori futuri
FILE_2022_1M_WITH_CLASS = 'DAT_ASCII_EURUSD_M1_2022_gennaio_class.csv'

#stesso file di 'DAT_ASCII_EURUSD_M1_2022_gennaio_class.csv', ma con le classi inserite da me a mano
FILE_2022_1M_MANUAL_CLASS = 'DAT_ASCII_EURUSD_M1_2022_gennaio_class.csv'

#file formattato; è equivalente a "DAT_ASCII_EURUSD_M1_2022.csv" ma il separatore è ',' invece di ';'
FILE_2022_1M_FORMATTED = 'DAT_ASCII_EURUSD_M1_2022_formatted.csv'

FILE_FULL_PATH = BASE_PATH + FILE_2022_1M_FORMATTED





