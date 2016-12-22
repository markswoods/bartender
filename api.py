from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_basicauth import BasicAuth

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'mwoods'
app.config['BASIC_AUTH_PASSWORD'] = 'hp92275a'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)

api = Api(app)

pilsners = []
stouts = []
ipas = []
dipas = []
beers = []

def addBeer(style, brewer, product):
    style.append({"brewer": brewer, "product": product})
    beers.append({"brewer": brewer, "product": product})
    
addBeer(pilsners, "Pilsner Urquell", "Pilsner Urquell")
addBeer(pilsners, "AB Inbev", "Stella Artois")
addBeer(pilsners, "Stiegl", "Pils")
addBeer(pilsners, "Trummer", "Pils")

addBeer(stouts, "Victory", "Donnybrook Stout")
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
        
class Beers(Resource):
    def get(self):        
        return beers

# Pure rest
api.add_resource(Pilsners, '/pilsners')
api.add_resource(Stouts, '/stouts')
api.add_resource(IPAs, '/ipas')
api.add_resource(Dipas, '/dipas')
api.add_resource(Beers, '/beers')

# Rest, but adhering to format required for API.ai
class Apiai(Resource):
    def post(self):  
        
        parser = reqparse.RequestParser()
        parser.add_argument('action', location='json')
        args = parser.parse_args() 
        #print 'Requested action: ' + args['action']  
        print flask.Request.json

        speech = 'On tap I have '
        for beer in beers:
            speech += beer['brewer'] + ' ' + beer['product'] + ', '
            
        # remove the trailing comma
        speech = speech[:-2]
        return {
            "speech": speech,
            "displayText": speech,
            # "data": data,
            # "contextOut": [],
            "source": "bartender service"
        }


api.add_resource(Apiai, '/apiai')

if __name__ == '__main__':
    app.run(debug=True)