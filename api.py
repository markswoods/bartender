from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

pilsners = []
stouts = []
ipas = []
dipas = []

def addBeer(style, brewer, product):
    style.append({"brewer": brewer, "product": product})
    
addBeer(pilsners, "Pilsner Urquell", "Pilsner Urquell")
addBeer(pilsners, "AB Inbev", "Stella Artois")
addBeer(pilsners, "Stiegl", "Pils")
addBeer(pilsners, "Trummer", "Pils")

addBeer(stouts, "Victory", "Donnybrook Stout")
addBeer(stouts, "Deschuts", "Obsidian Stout")
addBeer(stouts, "Deschutes", "Obsidian Stout")
addBeer(stouts, "Brooklyn", "Black Chocolate Stout")

addBeer(ipas, "Founders", "All Day IPA")
addBeer(ipas, "Bells", "Two Hearted")
addBeer(ipas, "Temperance", "Gatecrasher")

addBeer(dipas, "Two Roads", "Road 2 Ruin")
addBeer(dipas, "The Alchemist", "Heady Topper")
addBeer(dipas, "Russian River", "Pliny the Elder")
addBeer(dipas, "Lagunitas", "Hop Stoopid")

class Pilsners(Resource):
    def get(self):
        return pilsners
        
class Stouts(Resource):
    def get(self):
        return stouts
        
class IPAs(Resource):
    def get(self):
        return ipas
        
class Dipas(Resource):
    def get(self):
        return dipas
        


api.add_resource(Pilsners, '/pilsners')
api.add_resource(Stouts, '/stouts')
api.add_resource(IPAs, '/ipas')
api.add_resource(Dipas, '/dipas')

if __name__ == '__main__':
    app.run(debug=True)