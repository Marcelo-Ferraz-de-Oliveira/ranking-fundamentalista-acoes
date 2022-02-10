from flask import Flask, request
from analise import obter_lista_acoes

app = Flask(__name__)

def template (content):
    return '<!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0">   <title>Bootstrap Site</title>   <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha1/css/bootstrap.min.css" integrity="sha384-r4NyP46KrjDleawBgD5tp8Y7UzmLA05oM1iAEQ17CSuDqnUK2+k9luXQOfXJCJ4I" crossorigin="anonymous">   <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script> <script src="https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha1/js/bootstrap.min.js" integrity="sha384-oesi62hOLfzrys4LxRF63OJCXdXDipiYWBnvTl9Y9/TRlw5xlKIEHpNyvvDShgf/" crossorigin="anonymous"></script></head><body>' + content + ' </body> </html>' 

@app.route('/acoes')
def get_acoes():

<<<<<<< HEAD
    return template(obter_lista_acoes().to_html())
=======
    return template(obter_lista_acoes().to_html()

)

if __name__ == "__main__":
    app.run()
>>>>>>> 4e49cd8d2e852c7e5079a3a1b3709bf8fd32ce23
