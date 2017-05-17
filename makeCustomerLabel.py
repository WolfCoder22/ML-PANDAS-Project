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
    fullCustomerDF.info()

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
    fullCustomerDF.drop('CUSTOMER_REP_idPerson', axis=1)

    #pivot the plotform count
    fullCustomerDFPivot = fullCustomerDF[['customerId', 'PLATFORM', 'CONVO_COUNT']].pivot_table(index='customerId' , columns='PLATFORM',values='CONVO_COUNT')



    # fullCustomerDF = fullCustomerDF.pivot_table(columns='KEYWORD',values='WORD_COUNT', index=['COMPANY', 'idConversation', 'customerId', 'AREA_CODE'
    #                                           ,'LENGTH_MINS', 'IS_CALL'])

    fullCustomerDFPivot.info()
    print(fullCustomerDFPivot.head())
    print(list(fullCustomerDFPivot.columns.values))
    print(list(fullCustomerDFPivot.index.values))


def addPivotTablesToOrgDF(orgDf, pivotedDF, pivotColName, valueColName, newColNames, orgIndexColname):

    newColNames= pivotedDF.columns.values
    orgIndexColname=

    #add new pivot column names to the orgDF
    newColNamesOrg=[]
    for colName in newColNames:
        newColNamesOrg= pivotColName+"_"+colName+'_'+valeColName
        newColNamesOrg.append(newColNamesOrg)

    for newColName in newColNamesOrg:
        orgDf[newColName]= nan

    #go through each id of orginal
    for id in indexVals:

        #get rows with that index
        specficIndx= orgDf[orgDf[]]

makeFullCustomerDf()

