import pandas as pd
from math import nan

customerFile= 'fullCSVtables/testData/Customer.csv'
CustRepFile= 'fullCSVtables/testData/CustomerRep.csv'
personFile= 'tidyTables/Person.csv'
textFile= 'tidyTables/Text.csv'
conversationFile= 'tidyTables/Conversation.csv'

def makeFullCustomerDf():

    #get Dataframes with only the important data
    personDf= pd.read_csv(personFile)[['idPerson', 'AREA_CODE', 'PLATFORM', 'CONVO_COUNT']]
    repDf = pd.read_csv(CustRepFile).rename(columns={'idPerson':'repId'})
    customerDf = pd.read_csv(customerFile)
    textDf = pd.read_csv(textFile)
    convoDf = pd.read_csv(conversationFile)

    #add person data that are customers to the df
    fullCustomerDF= customerDf.merge(right=personDf, how='left')

    #sum the convoOut fo

    #merge convo Data to customers
    #drop CUSTOMER_idPerson since redundant
    fullCustomerDF= fullCustomerDF.merge(right=convoDf, how='left', left_on=['idPerson', 'PLATFORM']
                                         , right_on= ['CUSTOMER_idPerson', 'PLATFORM']).drop('CUSTOMER_idPerson', axis=1)

    #add text data that a customer wrote/said
    fullCustomerDF= textDf.merge(right=fullCustomerDF, how='right', left_on=['personId', 'idConversation'], right_on=['idPerson', 'idConversation']).drop('personId', axis=1)

    #add relevent CustomRep data
    fullCustomerDF = repDf.merge(right=fullCustomerDF, how='right', right_on='CUSTOMER_REP_idPerson', left_on='repId').drop('repId', axis=1)

    #rename the pId and drop TextId
    fullCustomerDF=fullCustomerDF.rename(columns={'idPerson':'customerId'}).drop('idText', axis=1)

    #drop customerRepId
    fullCustomerDF=fullCustomerDF.drop('CUSTOMER_REP_idPerson', axis=1)

    fullCustomerDF.to_csv('tidyTables/fullCustomerData.csv', index=False)
    return fullCustomerDF

# # pivot the plotform count
# pivotColName='PLATFORM'
# valueColName='CONVO_COUNT'
# customerDFPivot = fullCustomerDF[['customerId', pivotColName, valueColName]].pivot_table(index='customerId' , columns=pivotColName,values=valueColName)
# fullCustomerDF= addPivotTablesToOrgDF(fullCustomerDF, customerDFPivot, pivotColName, valueColName)
#
#
# fullCustomerDF = fullCustomerDF.pivot_table(columns='KEYWORD',values='WORD_COUNT', index=['COMPANY', 'idConversation', 'customerId', 'AREA_CODE'
#                                           ,'LENGTH_MINS', 'IS_CALL'])
#
# fullCustomerDFPivot.info()
# print(fullCustomerDFPivot.head())
# print(list(fullCustomerDFPivot.columns.values))
# print(list(fullCustomerDFPivot.index.values))


def addPivotTablesToOrgDF(orgDf, pivotedDF, pivotColName, valueColName, orgIndexColname='idCustomer'):

    pivotColNames= pivotedDF.columns.values
    indexVals=pivotedDF.index.values

    #add new pivot column names to the orgDF
    newColNames=[]
    for colName in pivotColNames:
        newColNamesOrg= pivotColName+"_"+colName+'_'+valueColName
        newColNamesOrg.append(newColNamesOrg)

    for newColName in newColNames:
        orgDf[newColName]= nan

    #go through each id of original
    for id in indexVals:

        #get rows with that index
        specficIndex= orgDf[orgDf[orgIndexColname==id]]

def changeDataInCustomer():
    custDf= pd.read_csv('tidyTables/fullCustomerData.csv')
    custDf.info()

    #change Certain Data to Categorical