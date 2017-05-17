# ML-PANDAS-Project

##### This is a project I am doing for the fun of it to practice PANDAS dataframe aggregation, generating csv data, Tidy data Guidelines, and creating Machine Learning Models from Data and More

##### I created the database myself by generating CSV files; The data is generated randomly, some with a guassian distribution and priority of selection.

##### You can see how the data was generated in the pdf 'DBsummary'

##### The classification I am trying to determine is whether a customer is a good lead or not. The customer 'GOOD_LEAD' label will be determine by Data afte Exploratory Data Analysis. I catered the generation of it to make a working ML model by
	* Assigning 'TEXT' data from a conversation to have only postive or negitive words with stopwords
	* Making the 'CONVO_COUNT' higher for platform 'A', then 'B'', then 'C'
	* Setting the convo 'LENGTH_MINS' to be generated with a guassion distribution; Mean=5, std=5
	* Setting half the are code from the phone numbers to be American
	* More

##### The goal of this project is to get more comfortable with PANDAS dataframe manipulation/transformation, EDA analysis, make a ML accurate model form 'real' data, and to have some coding fun =).

##### Database Schema
 ![](https://github.com/WolfCoder22/ML-PANDAS-Project/blob/master/DBschema.png "Logo Title Text 1")

## File Organization

#### Cleaning the Data
	- tidyCSVtables.py

#### Exploratory Data Analysis
    - analyzeCustomerData.py
    - EDA Graphs/

##### Code to make the CSV Database and unique keys
	- makeDataFunctions/

#### fullCSVtables
	- Single CSV files for each table
	-Have test data and will have full data once read to make full model

#### storedData
	- Where unique/primary key Data is stored


