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

    # make a box plot
    fig= plt.figure()
    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
    fig.suptitle('Customer Conversation Count Statistics', fontsize=16)

    ax = fig.add_subplot(111)
    colNames = list(custDf.columns.values)
    ax.boxplot(custDf[['A', 'B', 'C', 'ABC Sum']].values, showmeans=True, labels=colNames)

    #get the mean and median for each value
    ax.set_xlabel('Platform')
    ax.set_ylabel('Number of Conversations')

    plt.savefig('EDA Graphs/customerConvoCount.png', bbox_inches='tight')
    plt.show()

visualizeConvoCount()