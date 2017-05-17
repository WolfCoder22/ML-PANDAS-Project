from random import randint, random
import os.path

"""
Functions to Read and store IDs for the DB in the text file to make sure there are no duplicates
"""

# testIDfile= "storedData/testIds.txt"
personIDfile= "storedData/personIds.csv"
conversationIDfile= "storedData/conversationIds.csv"
textIdFile= "storedData/textIds.csv"
phoneNumFile= "storedData/uniquePhoneNums.csv"


#recurively find a new unique ID
def genrateUniqueId(idLength, idList):

    newId = randint(0, 10**idLength)

    #make sure unique id
    if newId in idList:
        newId = genrateUniqueId(idLength, idList)
    return newId


#return a list of all pIDs
def getIds(fileName, isint=True):

    fileExists= os.path.exists(fileName)
    if fileExists:
        with open(fileName) as file:
            Ids = file.readlines()

        #get rid of headerLine
        Ids= Ids[1:]

        #get last id
        last= Ids[len(Ids)-1]

        if isint:
            #strip whitespace and convert to int
            Ids = [int(x.strip()) for x in Ids]

        #getrid of newline char
        else:
                newIds=[]
                for id in Ids:
                    if id!=last:
                        id= id[:len(id)-1]
                    newIds.append(id)
                Ids=newIds
        return Ids

    else:
        return []

def makeHeader(fileName, out):

    header=''
    if fileName== personIDfile:
        header= 'Person Id'
    elif fileName== conversationIDfile:
        header= 'Conversation ID'
    elif fileName== textIdFile:
        header= 'Text Id'
    else:
        header= 'Unique Phones'

    out.write(header+'\n')

#add a new uniue 8 digit personID
def writeNewIds(fileName, numNewIds, idLength, incremental=False):

    #get current Ids
    currIds= getIds(fileName)
    out = open(fileName, 'w')

    makeHeader(fileName, out)

    for i in range(numNewIds):

        #make all ids in incrental order
        if incremental:
            newId= i
            currIds.append(i)
        #make
        else:
            newId= genrateUniqueId(idLength, currIds)
            currIds.append(newId)

        #don't add new line if making new list
        newLine=''
        if len(currIds)!=1:
            newLine="\n"

        out.write(newLine+str(newId))

    out.close()

"""Testing ID Generator"""
# writeNewIds(testIDfile, 2000, 4)
# ids= getIds(testIDfile)
# print(any(ids.count(x) > 1 for x in ids))

"""Generate Unique Ids for Text, Person, Conversation, and Phone Numbers"""
# writeNewIds(personIDfile, 20000, 6)
#writeNewIds(conversationIDfile, 2000000, 7, incremental=True) #avg 10 conversations per customer
#writeNewIds(textIdFile, 49000000, 8, incremental=True)  #each convo has 10 text avg
#writeNewIds(textIdFile, 4900000, 8, incremental=True)  #each convo has 10 text avg
#writeNewIds(phoneNumFile, 20000, 10)


def makePhoneNumbersRealistic():

    unChangedNums= getIds(phoneNumFile)
    numberOfPhones= len(unChangedNums)
    newNums=[]

    for num in unChangedNums:
        num=str(num)
        addDashes=False
        parenAreaCode=False

        #add dashes half the time
        if random()>.5:
            num= num[0:3]+'-'+num[3:6]+'-'+num[6:10]
            addDashes=True

        # put area code in parenthesis half of time
        if random() > .5:
            aCode=num[0:3]
            num= '('+aCode+')'+num[3:]
            parenAreaCode= True

        #add county code 1/3 of time
        if random()>(2/3):

            # most of the time add American
            if random() > (3 / 5):
                cCode = '+1'
            else:
                cCode = '+'+str(randint(2, 99))

            if addDashes and parenAreaCode:
                cCode='('+cCode+')'

            num= cCode+num
        newNums.append(num)

    #write new Nums to the file
    out= open(phoneNumFile, 'w')

    #make header again
    makeHeader(phoneNumFile, out)

    for i in range(numberOfPhones):

        #don't add new line for last phone
        if i==(numberOfPhones-1):
            out.write(newNums[i])
        else:
            out.write(newNums[i] + "\n")
        i+=1


"""Make the phone numbers realistic"""
#makePhoneNumbersRealistic()



