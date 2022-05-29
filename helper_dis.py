import numpy as np
import pandas as pd
import nltk
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from fuzzywuzzy import process

class Diagnosis:

    def __init__(self):

        # Load the data
        # self.data = pd.read_csv("data_med.csv")
        self.data = pd.read_csv("symptom_file.csv")
        self.X=self.data.iloc[:,0]
        self.Y=self.data.iloc[:,1]

        all_symps = [x for x in (','.join(self.X)).split(',')]

        # Lemmatize the data
        self.lemmatizer= WordNetLemmatizer()
        all_symps=[self.lemmatizer.lemmatize(symp) for symp in all_symps]

        self.all_symptoms=[]
        for i in all_symps:
            if i not in self.all_symptoms:
                self.all_symptoms.append(i)

    def prepare_vect(self, n):
        n= [self.lemmatizer.lemmatize(symps) for symps in n] 
        vect=[]
        for i in self.all_symptoms:
            if i in n:vect.append(1)
            else: vect.append(0)
        
        return vect

    def train(self):
        X1=[]
        for i in self.X:
            X1.append(self.prepare_vect(i.split(',')))

        Y1=[i for i in range(0,261)]

        # Train model using multinomial naive bayes
        # self.nb = MultinomialNB()
        # self.nb.fit(X1,Y1)
        self.rf = RandomForestClassifier()
        self.fr.fit(X1,Y1)


    def fuzzy_symptoms(self, message):
        return process.extract(message, self.all_symptoms)[0][0]

    def suggest_symptoms(self, symptom_list):

        X_lemmatized=[]
        for i in self.X:
            i= i.split(",")
            temp= [self.lemmatizer.lemmatize(symps) for symps in i] 
            X_lemmatized.append(temp)

        symptom_list = [self.lemmatizer.lemmatize(symp) for symp in symptom_list]
        test_symp=self.prepare_vect(symptom_list)
        y=self.nb.predict([test_symp])[0]
        temp_X=X_lemmatized[y]
        suggestion_X= list(set(temp_X)-set(symptom_list))  
        #logger statement here
        return suggestion_X

    def predict(self,symptoms):
        test_symp=self.prepare_vect(symptoms)

        predicted_disease = self.Y[self.nb.predict([test_symp])[0]]
        
        return [predicted_disease]