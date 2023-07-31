import random as rnd
import json, re, requests

base_url = "http://bestemmie.org/api/{}"
bestemmie_list = []

def get():
    '''
        ritorna una lista completa con tutte le bestemmie
        @returns list
    '''
    global bestemmie_list
    return bestemmie_list

def filtred():
    '''
        ritorna una lista filtrata di bestemmie
        @returns list
    '''
    global bestemmie_list
    filtred_list = []
    for i in bestemmie_list:
        flag = True
        if(len(i).split(' ')) < 3 and len(str(i).split(' ')) > 1 and len(str(i) <= 15) and not re.search(r'([a-zA-Z_])\1{2,}' , str(i)):
            for j in i:
                if(re.search(r'[^A-Za-z0-9\'\" ]', j)): 
                    flag = False
            if flag:
                print(i)
    return filtred_list

def random():
    '''
        ritorna una bestemmia randomica
        @returns str
    '''
    global  bestemmie_list
    rnd.shuffle(bestemmie_list)
    return bestemmie_list[rnd.randint(0, len(bestemmie_list))]

def filtred_random():
    '''
        ritorna una bestemmia randomica filtrata
        @returns str
    '''
    filtred = filtred()
    rnd.shuffle(filtred)
    return filtred[rnd.randint(0, len(filtred))]

print('---bestemmie.py---')
url = base_url.format("bestemmie")
while url is not None:
    response = requests.get(url)
    response.raise_for_status()
    bestemmie_list.append(response.json()['results'])
    url = response.json()['next'] or None
 
#with open("test.json", 'r') as file:    #TODO IL FILE JSON È SOLO DI DEBUG, POI VERRANNO ESTRAPOLATE DIRETTAMENTE DALLA FUNZIONE PRECENDERE
#    jFile = json.load(file)

#for i in jFile['prova']:
#    for j in i:
#        bestemmie_list.append(j['bestemmia'])