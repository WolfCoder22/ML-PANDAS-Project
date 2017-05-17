import pandas as pd
import matplotlib.pyplot as plt
from math import nan


def visualizeConvoCount():
    custDf = pd.read_csv('fullCSVtables/testData/Customer.csv')
    personDf= pd.read_csv('tidyTables/Person.csv')

    #get the word counts for customer
    custDf= custDf.merge(right=personDf, how='left', on='idPerson')
    custDf= custDf.drop(['FIRST_NAME', 'MIDDLE INITIAL', 'LAST_NAME', 'UTC_TIMEZONE', 'EMAIL', 'AREA_CODE', 'PHONE NUMBER'], axis=1)
    custDf=custDf.pivot(index='idPerson',columns='PLATFORM', values='CONVO_COUNT')

    #add a sum collumn for each customer
    custDf['ABC Sum']= custDf.sum(axis=1)

    #make a bar chart
    custDf.plot(kind='box', title='Platform Word Count', cmap='Set2')
    plt.show()


visualizeConvoCount()