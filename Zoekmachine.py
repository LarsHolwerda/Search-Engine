import pandas as pd
import math
import numpy as np
import regex as re

# Maakt een matrix waarin de term frequencies staan
def calctermfrequentie():
    documenten = ['artikel1.txt', 'artikel2.txt', 'artikel3.txt', 'artikel4.txt', 'artikel5.txt', 'artikel6.txt', 'artikel7.txt', 'artikel8.txt', 'artikel9.txt', 'artikel10.txt']
    stopwoorden = open('stopwoordennl.txt').read()
    bestandfrequentie = {}
    for bestand in documenten:
        doc = open(bestand, "r", encoding = 'mbcs')
        woorden = doc.read().replace('\n', '',).split(' ')
        woordfrequenties = {}
        for woord in woorden:
            woord = woord.replace(u'\xa0', u' ')
            if not woord in stopwoorden:
                woord = woord.lower()
                if woord in woordfrequenties:
                    woordfrequenties[woord] += 1
                else:
                    woordfrequenties[woord] = 1
        bestandfrequentie[bestand] = woordfrequenties   
    return bestandfrequentie


# Maakt een lijst met alle unieke woorden in de artikelen
def uniekewoordenlijst():
    bestandfrequentie = calctermfrequentie()
    lijst = []
    for keys, values in bestandfrequentie.items():
        for key, value in values.items():
            if key not in lijst:
                lijst.append(key)
    return lijst

# Maakt een termweight matrix aan
def termweightmatrix():
    bestandfrequentie = calctermfrequentie()
    documenten = calctermfrequentie()
    lijst = uniekewoordenlijst()
    column = []
    for bestand in documenten:
        column.append(bestand)
    termweights = []
    for woord in lijst:
        termweight = []        
        for doc, value in bestandfrequentie.items():
            if woord in value:
                termweight.append(value[woord])
            else:
                termweight.append(0)
        termweights.append(termweight) 
    return column, lijst, termweights

# Maakt een idf matrix aan
def createidfmatrix(termweightmatrix):
    documenten = calctermfrequentie()
    N = len(documenten)
    m = []
    for i in termweightmatrix:
        n = 0
        for j in i:
            if j != 0:
                n += 1
        m.append(n) 
    for index, row in enumerate(termweightmatrix):
        idf = math.log(N/m[index], 2)
        for i, j in enumerate(row):
            termweightmatrix[index][i] = idf * j
    return termweightmatrix
            
def creatematrix():
    column, lijst, termweights = termweightmatrix()
    df = pd.DataFrame(data = termweights, index = lijst, columns = column)
    return df

query = ['jeff']


#Berekent de lengtevectoren van de documenten
def calculatedistance(df):
    lengtevectoren = {}
    columns = list(df.columns)
    for column in columns:
        if column != '':
            vector = df[column]
            vector = vector**2
            vector = math.sqrt(vector.sum())
            lengtevectoren[column] = vector
    return lengtevectoren

# Maakt een numpy array aan die aangeeft hoeveel een woord in de query voorkomt in een tekst
def createqueryvector(matrix):
    documentwoorden = np.array(matrix.index)
    queryvector = np.zeros(documentwoorden.size)
    for querywoord in query:
        for index, woord in enumerate(documentwoorden):
            if woord == querywoord:
                queryvector[index] += 1
    return queryvector

def createkeyword():
    keyword = ''
    lijst = uniekewoordenlijst()
    global query
    for woord in lijst:
        if woord == sorted(query, key = len)[-1]:
            keyword = keyword + woord
    return keyword

def createpreview(similarity):
    keyword = createkeyword()
    for key, value in similarity.items():
        with open(key, "r") as a:
            a = a.read()
            woorden = re.findall(r"\w+|\W+",a)
            for index in range(len(woorden)):
                woorden[index] = woorden[index].lower()
                woorden[index] = woorden[index].replace(u'\xa0', u' ')
            try:
                vindkeywoord = woorden.index(keyword)
                preview = woorden[vindkeywoord-80:vindkeywoord] + woorden[vindkeywoord:vindkeywoord+80]
                preview1 = ""
                for woord in preview:
                    preview1 = preview1 + woord
            except:
                preview = woorden[:80]
                preview1 = ""
                for woord in preview:
                    preview1 = preview1 + woord
            similarity[key] = [value, preview1]
    return similarity

#Berekent het inwendig product
def calcinnerproduct(matrix):
    innerproducts = []
    queryvector = createqueryvector(matrix)
    for column in matrix:
        innerproduct = np.dot(queryvector, matrix[column])
        innerproducts.append(innerproduct)
    return innerproducts

#Berekent het product van de vectoren van de query en de documenten
def calcunderproduct(matrix):
    queryvector = createqueryvector(matrix)
    lengtevectoren = calculatedistance(matrix)
    queryvector = math.sqrt(queryvector.sum())
    documentvector = lengtevectoren
    underproducts = []
    for x in documentvector:
        underproduct = documentvector[x] * queryvector
        underproducts.append(underproduct)
    return underproducts

#Berekent de cosine similarity a.d.h.v. inwendig product en vectoren
def similarity(zoekopdracht):
    df = creatematrix()
    global query
    query = zoekopdracht
    innerproducts = calcinnerproduct(df)
    underproductlijst = calcunderproduct(df)
    similarity = [i / j for i, j in zip(innerproducts, underproductlijst)]
    similarity = zip(list(df.columns),similarity)
    similarity = dict(sorted(similarity, key=lambda item: item[1], reverse=True))
    similarity = createpreview(similarity)
    print(similarity)
    return similarity
print(similarity(['jeff']))