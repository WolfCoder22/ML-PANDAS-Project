import pandas as pd
from random import randint, gauss, random, choice, randrange
import string
from itertools import cycle
from math import inf

from makeDataFunctions.makeUniqueIds import getIds

"""
Functions to Makes CSV files for PANDAS
"""

personIDfile= "../storedData/personIds.csv"
conversationIDfile= "../storedData/conversationIds.csv"
textIdFile= "../storedData/textIds.csv"

customerFile= '../fullCSVtables/testData/Customer.csv'
CustRepFile= '../fullCSVtables/testData/CustomerRep.csv'
personFile= '../fullCSVtables/testData/Person.csv'
textFile= '../fullCSVtables/testData/Text.csv'
conversationFile= '../fullCSVtables/testData/Conversation.csv'

stopwordsFile= "../storedData/words/stopWords.csv"
posWordsFile= "../storedData/words/positiveWords.csv"
negWordsFile= "../storedData/words/negativeWords.csv"

# get the stop, positive, and negwords
stopwords = getIds(stopwordsFile, False)
posWords = getIds(posWordsFile, False)
negWords = getIds(negWordsFile, False)

def makePersonCSV(numPeople):

    if numPeople>20000:
        print("Error: Can only make 20000 people Maximum")
        return

    phonesDf = pd.read_csv('../storedData/uniquePhoneNums.csv')

    # initiate csv files
    PersonOut = open(personFile, 'w')
    RepOut = open(CustRepFile, 'w')
    CustomerOut = open(customerFile, 'w')

    #write header columns
    personHeader = getCsvHeader('Person')
    customerHeader = getCsvHeader('Customer')
    RepHeader = getCsvHeader('CustomerRep')

    PersonOut.write(personHeader)
    RepOut.write(RepHeader)
    CustomerOut.write(customerHeader)

    #make 1/10 of ppl reps
    numReps= round(numPeople/10)
    for i in range(numReps):

        personId= str(getUniquePersonId(i))
        repData = makeRepData(personId, i, numPeople)

        if i == numReps-1:
            repData=repData[:len(repData)-1]

        RepOut.write(repData)

        #make the personData for the rep too
        personData = makePersonData(phonesDf, i, numPeople, personId)
        PersonOut.write(personData)


    #make 9/10 of people customers
    for i in range(numReps, numPeople):

        # write customer Rep CSV
        personId = str(getUniquePersonId(i))
        customerData = personId

        if i != numPeople-1:
            customerData=customerData+'\n'

        CustomerOut.write(customerData)

        # make the personData for the rep too
        personData= makePersonData(phonesDf, i, numPeople, personId)
        PersonOut.write(personData)

    RepOut.close()
    CustomerOut.close()
    PersonOut.close()


def makeConversationandTextTable(numReps):

    if numReps > 2000:
        print("Error: Can only make Rep Conversations Maximum")
        return

    # get convoIds, and textIds
    convoIds = getIds(conversationIDfile)
    textIds = getIds(textIdFile)

    # initiate csv files
    ConvoOut = open(conversationFile, 'w')
    TextOut = open(textFile, 'w')

    # write header columns
    ConvoHeader = getCsvHeader('Conversation')
    TextHeader = getCsvHeader('Text')

    ConvoOut.write(ConvoHeader)
    TextOut.write(TextHeader)

    #get pIds of customer and reps
    custDf = pd.read_csv(customerFile)
    repDf = pd.read_csv(CustRepFile)
    personDf = pd.read_csv(personFile)

    # get df for convocount customer and rep
    fullCustDf = custDf.merge(right=personDf, how='left')
    fullRepDf = repDf.merge(right=personDf, how='left', on='idPerson')

    customerIdsdf = fullCustDf.idPerson
    repIdsdf = fullRepDf.idPerson

    numReps = repIdsdf.shape[0]
    numCustomers= customerIdsdf.shape[0]

    # make 10 convos for each rep
    k=0
    repIndex=0
    textIdCIndex = 0
    isLastRep = False
    for i in range(numReps):
        repPid = repIdsdf.iloc[repIndex]
        repIndex+=1

        if i == (numReps - 1):
            isLastRep = True

        # make a conversation for 100 random customers
        isLastConvo=False

        # make a conversation for 100 random customers
        for j in range(100):

            if j == 99:
                isLastConvo = True
            idConvo= convoIds[k]
            k+=1

            callLength = getGuassianPosNum(5, 5, 1)  # mean 5, std 5, min 1

            #make it a call half the time and twice as long on average
            isCall= False
            isText=False
            if random()>.5:
                isCall=True
                callLength= int(round(callLength*2))
            else:
                isText=True

            #make it platform more 'A', then 'B', then 'C'
            platforms= ['A', 'B', 'C']
            if random()<.75:
                platformIndex=0
            elif random()<.9:
                platformIndex=1
            else:
                platformIndex=2
            platform= platforms[platformIndex]

            #assign a random customer to the convo
            customerIndex= randint(0, numCustomers-1)
            customerPid= customerIdsdf.loc[customerIndex]

            pIdCycle = cycle([repPid, customerPid])

            #make random amount of texts for each convo with guassian distribution
            numTextsInConvo= getGuassianPosNum(10, 7, 3) #mean 10, std 7, min
            for r in range(numTextsInConvo):

                #cycle between rep then customer
                pId=next(pIdCycle)
                textData= makeTextEntry(textIds[textIdCIndex], idConvo, pId, r, numTextsInConvo, isLastRep, isLastConvo)
                TextOut.write(textData)

                textIdCIndex+=1

            #write conversation data
            convoData=makeConvoData(idConvo, callLength, isCall, isText, platform, repPid, customerPid, j, isLastRep)
            ConvoOut.write(convoData)

            #fix convo counts for rep and customer
            countcolName= 'PLATFORM_'+platform+'_CONVO_COUNT'

            customerData=(personDf.idPerson==customerPid)
            repData= (personDf.idPerson==repPid)

            customerIndex= personDf[personDf.idPerson==customerPid].index.tolist()[0]
            repIndexT = personDf[personDf.idPerson == repPid].index.tolist()[0]

            #Get desired person Rows
            customerConvoCount= personDf.loc[customerData][countcolName].values[0]
            repConvoCount = personDf.loc[repData][countcolName].values[0]

            #add 1 to the counts
            customerConvoCount+=1
            repConvoCount+=1

            #add one to specified platform count
            personDf.set_value(customerIndex, countcolName, customerConvoCount)
            personDf.set_value(repIndexT, countcolName, repConvoCount)

    #store the new Person Dataframe with counts to CSV
    personDf.to_csv(personFile, index=False)



def makeConvoData(idConvo, callLength, isCall, isText, platform, repPid, customerPid, j, isLastRep):

    convoData=str(idConvo)+','+str(callLength)+','+str(isCall)+','+str(isText)+","+platform+','+str(repPid)+','+str(customerPid)+'\n'

    #don't add new line for last entry
    if isLastRep and j==99:
        convoData= convoData[:len(convoData)-1]

    return convoData


def makeTextEntry(idtext, idConvo, pId, k, numTextsInConvo, isLastRep, isLastConvo):

    text=''

    #generate text with random stop words and random Pos or Neg Words
    isPositive= False
    if random()>.5:
        isPositive=True

    #make words in text be random 3 to 66 total
    numWordsInText= randrange(3, 66)
    for i in range(int(numWordsInText/3)):

        #add two random stop words
        numStopWords= len(stopwords)
        stopword1= stopwords[randint(0, numStopWords-1)]
        stopword2 = stopwords[randint(0, numStopWords - 1)]

        text=text+' '+stopword1
        text = text + ' ' + stopword2

        #get a random postive or negative word with guassian indexing
        if isPositive:
            length= len(posWords)
            posWordIndx = getGuassianPosNum(0,length/2, max=length-1)
            decionword = posWords[posWordIndx]

        else:
            length = len(negWords)
            negWordIndx = getGuassianPosNum(0, length / 2, max=length-1)
            decionword = negWords[negWordIndx]


        text=text+' '+decionword

    #make Text data to write to csv
    textData= str(idtext)+','+str(idConvo)+','+str(pId)+','+text+'\n'

    #don't ad new line for last entry
    if isLastRep and isLastConvo and k==numTextsInConvo-1:
        textData=textData[:len(textData)-1]

    return textData



def makePersonData(phonesDf, i, numPeople, pId):

    firstName, lastName = getRandName()
    middleInitial = choice(string.ascii_letters)
    timezone = getRandTimeZone()

    email = firstName + '.' + middleInitial + '.' + lastName + "@gmail.com"
    phone = phonesDf.iloc[i].values[0]

    # iset counts initially to zero
    platformAcount = 0
    platformBcount = 0
    platformCcount = 0

    personDatap1 = pId + ',' + firstName + ',' + middleInitial + ',' + lastName + ',' + timezone
    personDatap2 = ',' + email + ',' + phone + ',' + str(platformAcount) + ',' + str(platformBcount) + ',' + str(
        platformCcount)
    personData = personDatap1 + personDatap2

    if i != numPeople - 1:
        personData = personData + '\n'

    return personData


#get Random Company
def makeRepData(personId, i, numPeople):

    #assign rep to a random company
    comps = ['Google', 'Microsoft', 'Facebook', 'Amazon']
    i = randint(0, 3)
    company= comps[i]
    data= personId+','+company

    if i != numPeople - 1:
        data = data + '\n'

    return data

def makeNewLine(out):
        out.write("\n")

"""table Param: 'Person', 'Customer', 'CustomerRep', 'Conversation', or 'Text'  """
def getCsvHeader(table):
    tables=['Person', 'Customer', 'CustomerRep', 'Conversation', 'Text']

    if table not in tables:
        print("Error: No Table with Name: "+table)
        print("     Use: 'Person', 'Customer', 'CustomerRep', 'Conversation', or 'Text'")
        return

    if table=='Person':
        csvHeader= "idPerson,FIRST_NAME,MIDDLE INITIAL,LAST_NAME,UTC_TIMEZONE,EMAIL,PHONE NUMBER,PLATFORM_A_CONVO_COUNT,PLATFORM_B_CONVO_COUNT,PLATFORM_C_CONVO_COUNT\n"

    elif table=='Customer':
        csvHeader="idPerson\n"

    elif table=='CustomerRep':
        csvHeader = "idPerson,COMPANY\n"

    elif table== 'Conversation':
        csvHeader= 'idConversation,LENGTH_MINS,IS_CALL,IS_TEXT_CHAT,PLATFORM,CUSTOMER_REP_idPerson,CUSTOMER_idPerson\n'
    else:
        csvHeader= "idText,idConversation,personId,TEXT\n"

    return csvHeader


def getUniquePersonId(index):
    pIds= pd.read_csv("../storedData/personIds.csv")
    return pIds.loc[index].values[0]


def getRandName():

    firstNames= pd.read_csv("otherData/firstNamesList.csv")
    lastNames= pd.read_csv("otherData/lastNamesList.csv")

    numFnames= firstNames.shape[0]
    numLnames= lastNames.shape[0]

    #get random name
    i= randint(0, numFnames-1)
    j = randint(0, numLnames-1)

    fName= firstNames.loc[i].values[0]
    lname= lastNames.loc[j].values[0]

    return fName, lname


def getRandTimeZone():

    zone= randint(-12, 12)
    return "UTC "+str(zone)


"""Make data more suited for ML by making a Normal Distibution"""
def getGuassianPosNum(mean, std, min=0, max=inf):
    convoCount= gauss(mean, std)

    #make sure above to min limit
    if convoCount<=min:
        return getGuassianPosNum(mean, std, min, max)

    #make sure not over max if given as a param
    num= int(round(convoCount))
    if num>max:
        return getGuassianPosNum(mean, std, min, max)

    return num

def makeAllCSVData(numPeople):

    #makePersonCSV(numPeople)
    makeConversationandTextTable(round(numPeople/10))

makeAllCSVData(10)
