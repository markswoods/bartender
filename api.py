from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_basicauth import BasicAuth
import json

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'mwoods'
app.config['BASIC_AUTH_PASSWORD'] = 'hp92275a'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)

api = Api(app)

beers = []

def addBeer(style, brewer, product):
    beers.append({"brewer": brewer, "product": product, "style": style})
    
addBeer("Pilsner", "Pilsner Urquell", "Pilsner Urquell")
addBeer("Pilsner", "AB Inbev", "Stella Artois")
addBeer("Pilsner", "Stiegl", "Pils")
addBeer("Pilsner", "Trummer", "Pils")
addBeer("Pilsner", "Two Roads", "Ol' Factory Pils")

addBeer("Stout", "Victory", "Donnybrook Stout")
addBeer("Stout", "Deschutes", "Obsidian Stout")
addBeer("Stout", "Brooklyn", "Black Chocolate Stout")
addBeer("Stout", "4 Hands", "Chocolate Milk Stout")

addBeer("IPA", "Founders", "All Day IPA")
addBeer("IPA", "Two Roads", "Lil Heaven")
addBeer("IPA", "Bells", "Two Hearted")
addBeer("IPA", "Temperance", "Gatecrasher")

addBeer("Double IPA", "Two Roads", "Road 2 Ruin")
addBeer("Double IPA", "The Alchemist", "Heady Topper")
addBeer("Double IPA", "Russian River", "Pliny the Elder")
addBeer("Double IPA", "Lagunitas", "Hop Stoopid")

class Pilsners(Resource):
    def get(self):
        return [b for b in beers if b["style"] == "Pilsner"]
        
class Stouts(Resource):
    def get(self):
        return [b for b in beers if b["style"] == "Stout"]
        
class IPAs(Resource):
    def get(self):
        return [b for b in beers if b["style"] == "IPA"]
        
class Dipas(Resource):
    def get(self):
        return [b for b in beers if b["style"] == "Double IPA"]
        
class Beers(Resource):
    def get(self):        
        return beers
        
class Brewers(Resource):
    def get(self):
        return [b["brewer"] for b in beers]
        
class Styles(Resource):
    def get(self):
        return list(set([b["style"] for b in beers]))   # set selects only unique values
    
class Names(Resource):
    def get(self):
        return [b["product"] for b in beers]
        

# Pure rest
api.add_resource(Pilsners, '/pilsners')
api.add_resource(Stouts, '/stouts')
api.add_resource(IPAs, '/ipas')
api.add_resource(Dipas, '/dipas')
api.add_resource(Beers, '/beers')
api.add_resource(Brewers, '/brewers')
api.add_resource(Styles, '/styles')
api.add_resource(Names, '/names')

# Rest, but adhering to format required for API.ai
class Apiai(Resource):
    def post(self):          
        payload = request.get_json()
        print 'action: ' + payload['result']['action']

        json.loads(payload)
        print json.dumps(resp, indent=4, separators=(',', ':'))

        if payload['result']['action'] == 'Beer.List':
            speech = 'On tap I have '
            for beer in beers[:-1]:
                speech += beer['brewer'] + ' ' + beer['product'] + ', '
            speech += 'and ' + beer['brewer'] + ' ' + beer['product'] + '. '   # pretty up the last one
            speech += 'Now, what can I get you?'                            # Webhook m/provide all text
            
            return {
                "speech": speech,
                "displayText": speech,
                # "data": data,
                # "contextOut": [],
                "source": "bartender service"
            }

        if payload['result']['action'] == 'Beer.Order':
            print payload['result']['parameters']
            beer = payload['result']['parameters']['brewer']
            if beer == '':
                beer = payload['result']['parameters']['beer']['product']
                 

            speech = 'One ' + beer + ' coming up!'
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