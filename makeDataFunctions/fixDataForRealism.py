import pandas as pd
from math import nan

from makeDataFunctions.makeUniqueIds import getIds

"""
Functions to fix Data in the Full Table Database to make realistic for Machine Learning 
"""

customerFile= '../fullCSVtables/Customer.csv'
CustRepFile= '../fullCSVtables/CustomerRep.csv'
personFile= '../fullCSVtables/Person.csv'

stopwordsFile= '../storedData/words/stopWords.csv'
posWordsFile= '../storedData/words/positiveWords.csv'
negWordsFile= '../storedData/words/negativeWords.csv'

""" Adding counts iteritvely when making DB instead. Not using this"""
# def fixPlatformConvoCount():
#
#     # get pandas df for Customer and Customer Rep
#     custDf = pd.read_csv(customerFile)
#     repDf = pd.read_csv(CustRepFile)
#     personDf= pd.read_csv(personFile)
#
#     #get df for convocount customer and rep
#     fullCustDf = custDf.merge(right=personDf, how='left', on='idPerson')
#     fullRepDf = repDf.merge(right=personDf, how='left', on='idPerson')
#
#     custCountdf= fullCustDf[['idPerson','PLATFORM_A_CONVO_COUNT', 'PLATFORM_B_CONVO_COUNT', 'PLATFORM_C_CONVO_COUNT']]
#     repCountdf = fullRepDf[['idPerson', 'PLATFORM_A_CONVO_COUNT', 'PLATFORM_B_CONVO_COUNT', 'PLATFORM_C_CONVO_COUNT']]
#
#     #get the counts
#     custACount= custCountdf['PLATFORM_A_CONVO_COUNT'].sum()
#     custBCount = custCountdf['PLATFORM_B_CONVO_COUNT'].sum()
#     custCCount = custCountdf['PLATFORM_C_CONVO_COUNT'].sum()
#
#     repACount = fullRepDf['PLATFORM_A_CONVO_COUNT'].sum()
#     repBCount = fullRepDf['PLATFORM_B_CONVO_COUNT'].sum()
#     repCCount = fullRepDf['PLATFORM_C_CONVO_COUNT'].sum()
#
#
#
#     print(repCountdf.head())
#     print(custCountdf.head())
#
# # platoform is 'A', 'B', or 'C'
# def fixConvoCount(personDf, custCountdf, repCountdf, custCount, repCount, platform):
#
#     colName= 'PLATFORM_'+platform+'_CONVO_COUNT'
#     #find how much to add to count
#     toAdd= custCount- repCount
#
#     #find to add to customer or rep
#     if toAdd== 0:
#         return  #stop if equal count
#     elif toAdd>=0:
#         dfToChange = repCountdf[colName]
#     else:
#         dfToChange = custCountdf[colName]
#         toAdd= abs(toAdd)


def checkWordsLineUp():

    stopWordsDf = pd.read_csv(stopwordsFile)
    posDf= pd.read_csv(posWordsFile)
    negDf = pd.read_csv(negWordsFile)

    negWords= getIds(negWordsFile, False)
    posWords= getIds(posWordsFile, False)
    stopWords= getIds(stopwordsFile, False)

    #raise error if psotive or negative words is in the series
    posCheckBools=posDf.isin(stopWords)
    negCheckBools= negDf.isin(stopWords)

    assert (posCheckBools.positiveWords==False).all()
    assert (negCheckBools.negativeWords==False).all()


checkWordsLineUp()