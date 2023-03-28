from html_telegraph_poster import TelegraphPoster
from requests import post

# Lettura file HTML
with open("resources/html/index.html", "r") as file:
    html = file.read()
    
# Conversione HTML in formato Telegraph
poster = TelegraphPoster()
poster.post(html)
content = poster.get_content()

# Settaggio parametri pagina telegraph
data = {
    'access_token' : 'ad4b2376ed950b71893b62b59abed411a889810844d96c4be2bf8894249d',
    'title': 'Command List',
    'author_name': '@D3enny04',
    'content': content,
    'return_content':True
}

# Invio richiesta POST
response = post('https://api.telegra.ph/WITBCommand', data=data)
#
print(response.json())

# Verifica esito della richiesta
#if response.status_code == 200:
#    page_url = "https://telegra.ph/{}".format(response.json()["path"])
#    print(page_url)
#else:
#    print("Errore durante l'invio della richiesta: {}".format(response.status_code))
