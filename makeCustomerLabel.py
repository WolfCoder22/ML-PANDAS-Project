import pandas as pd

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


    fullCustomerDF.info()
    print(fullCustomerDF.head())

makeFullCustomerDf()

