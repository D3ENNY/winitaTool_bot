from requests import get
import json, re

base_url = "http://bestemmie.org/api/{}"
bestemmie_list = []

def allBestemmie():
    global bestemmie_list
    global base_url
    url = base_url.format("bestemmie")
    while url is not None:
        response = get(url)
        response.raise_for_status()
        bestemmie_list.append(response.json()['results'])
        url = response.json()['next'] or None
    return bestemmie_list

with open("test.json", 'r') as file:    #TODO IL FILE JSON È SOLO DI DEBUG, POI VERRANNO ESTRAPOLATE DIRETTAMENTE DALLA FUNZIONE PRECENDERE
    jFile = json.load(file)
cnt = 0
print("inizio")
for i in jFile["prova"]:
    for j in i:
        flag = True
        
        if(len(str(j['bestemmia']).split(' ')) < 3 and 
           len(str(j['bestemmia']).split(' ')) > 1 and 
           len(str(j['bestemmia'])) <= 25) and not re.search(r'([a-zA-Z_])\1{2,}' , str(j['bestemmia'])):
                
            for x in j['bestemmia']:
                if(re.search(r'[^A-Za-z0-9\'\" ]', x)): 
                    flag = False
            if flag:
                print(j['bestemmia'])
                cnt+=1
print('fine '+str(cnt)) 

print(json.dumps(allBestemmie(), sort_keys=True, indent=4))
