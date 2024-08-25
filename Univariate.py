class Univariate():
    def qualQuan(dataset):
        qual=[]
        quan=[]
        for columnName in dataset.columns:
            if (dataset[columnName].dtype=='O'):
                qual.append(columnName)
            else:
                quan.append(columnName)
        return qual,quan

    def univariatee(dataset,quan):
        import pandas as pd
        import numpy as np
        descriptive=pd.DataFrame(index=['Mean','Median','Mode','Q1:25%','Q2:50%','Q3:75%','99%','Q4:100%','IQR','1.5rule','Lesser','Greater','Min','Max'],columns=quan)
        for ColunmName in quan:
            descriptive[ColunmName]['Mean']=dataset[ColunmName].mean()
            descriptive[ColunmName]['Median']=dataset[ColunmName].median()
            descriptive[ColunmName]['Mode']=dataset[ColunmName].mode()[0]
            descriptive[ColunmName]['Q1:25%']=dataset.describe()[ColunmName]['25%']
            descriptive[ColunmName]['Q2:50%']=dataset.describe()[ColunmName]['50%']
            descriptive[ColunmName]['Q3:75%']=dataset.describe()[ColunmName]['75%']
            descriptive[ColunmName]['99%']=np.percentile(dataset[ColunmName],99)
            descriptive[ColunmName]['Q4:100%']=dataset.describe()[ColunmName]['max']
            descriptive[ColunmName]['IQR']=descriptive[ColunmName]['Q3:75%']-descriptive[ColunmName]['Q1:25%']
            descriptive[ColunmName]['1.5rule']=1.5*descriptive[ColunmName]['IQR']
            descriptive[ColunmName]['Lesser']=descriptive[ColunmName]['Q1:25%']-descriptive[ColunmName]['1.5rule']
            descriptive[ColunmName]['Greater']=descriptive[ColunmName]['Q3:75%']+descriptive[ColunmName]['1.5rule']
            descriptive[ColunmName]['Min']=dataset[ColunmName].min()
            descriptive[ColunmName]['Max']=dataset[ColunmName].max()
        return descriptive
    
    def finding_outliers(quan,descriptive):
        Lesser=[]
        Greater=[]
        for ColunmName in quan:
            if descriptive[ColunmName]['Min']<descriptive[ColunmName]['Lesser']:
                Lesser.append(ColunmName)
            if descriptive[ColunmName]['Max']>descriptive[ColunmName]['Greater']:
                Greater.append(ColunmName)
        return Lesser,Greater
 
    def handle_outliers(dataset,descriptive,Lesser,Greater):
        for ColunmName in Lesser:
            dataset.loc[dataset[ColunmName] < descriptive[ColunmName]["Lesser"], ColunmName] = descriptive[ColunmName]["Lesser"]
        for ColunmName in Greater:
            dataset.loc[dataset[ColunmName] > descriptive[ColunmName]["Greater"], ColunmName] = descriptive[ColunmName]["Greater"]
        return dataset

    def freqTable(dataset,columnName):
        import pandas as pd
        freqTable=pd.DataFrame(columns=['unique_value','Frequency','Relative_Freq','cumsum'])
        freqTable['unique_value']=dataset[columnName].value_counts().index
        freqTable['Frequency']=dataset[columnName].value_counts().values
        freqTable['Relative_Freq']=(freqTable['Frequency']/len(freqTable))
        freqTable['cumsum']=freqTable['Relative_Freq'].cumsum()
        return freqTable