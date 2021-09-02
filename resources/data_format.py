def formatDF(dataframe):
    dataframe.dropna(inplace=True, how='all')
    dataframe.dropna(inplace=True, axis='columns')

    new_header = dataframe.iloc[0]
    dataframe = dataframe[1:] 
    dataframe.columns = new_header
    
    return dataframe

def getPDL(summoner, formatedDf):
    try:
        return int(formatedDf.loc[formatedDf['Invocador'] == summoner]['PDL'].iloc[:,0])
    except TypeError:
        return -1

def aaa():
    return('aaa')