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
addBeer("Pilsner", "Stella Artois", "Stella Artois")
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

# Helper functions for manipulating the list of beers
def styles():
    return list(set([b["style"] for b in beers]))   # set selects only unique values

def pilsners():
    return [b for b in beers if b["style"] == "Pilsner"]
    
def stouts():
    return [b for b in beers if b["style"] == "Stout"]

def ipas():
    return [b for b in beers if b["style"] == "IPA"]
    
def dipas():
    return [b for b in beers if b["style"] == "Double IPA"]


def brewers():
    return [b["brewer"] for b in beers]
        
# Resource classes for get, post, etc.  
# TODO: wrap the returns in a dict object to enable Kore to handle response
class Pilsners(Resource):
    def get(self):
        return {'pilsners': pilsners()}
        
class Stouts(Resource):
    def get(self):
        return {'stouts': stouts()}
        
class IPAs(Resource):
    def get(self):
        return {'ipas': ipas()}
        
class Dipas(Resource):
    def get(self):
        return {'dipas': dipas()}
       
class Beers(Resource):
    def get(self):        
        return {'beers': beers}
        
class Brewers(Resource):
    def get(self):
        return {'brewers': brewers()}
        
class Styles(Resource):
    def get(self):
        return {'styles': styles()}
    
class Names(Resource):
    def get(self):
        return [b["product"] for b in beers]
        
class Auth(Resource):
    def get(self):
        print "Authentication made"
        return 'Authorized'
        

# Pure rest
api.add_resource(Pilsners, '/pilsners')
api.add_resource(Stouts, '/stouts')
api.add_resource(IPAs, '/ipas')
api.add_resource(Dipas, '/dipas')
api.add_resource(Beers, '/beers')
api.add_resource(Brewers, '/brewers')
api.add_resource(Styles, '/styles')
api.add_resource(Names, '/names')
api.add_resource(Auth, '/')

# Rest, but adhering to format required for API.ai
class Apiai(Resource):
    def post(self):          
        payload = request.get_json()
        
        # some debugging controls
        print 'action: ' + payload['result']['action']        
        print 'parameters: ' + json.dumps(payload['result']['parameters'])
        #print json.dumps(payload, indent=4, separators=(',', ':'))

#TODO: Add some randomized variations on the response speech.
#TODO:  Consider letting API.ai handle response, use parms/data for any customizations
#TODO: Add ability to open a tab
#TODO: Request beers from a particular brewer
#TODO: Recommend a particular beer in a style

        #
        # Beer.List 
        #   User requested a list of beers served
        #
        if payload['result']['action'] == 'Beer.List':
            # Check to see if a particular style was requested
            if 'style' in payload['result']['parameters']:
                style = payload['result']['parameters']['style']
                blist = [b for b in beers if b['style'] == style]
                speech = 'For ' + style + 's I have '
            else:
                style = ''
                speech = 'On tap I have '
                blist = beers
           
            for beer in blist[:-1]:
                if beer['brewer'] == beer['product']:
                    speech += beer['brewer'] + ', '
                else:
                    speech += beer['brewer'] + ' ' + beer['product'] + ', '
            speech += 'and ' + blist[-1]['brewer'] + ' ' + blist[-1]['product'] + '. '   # pretty up the last one
            speech += 'Now, what can I get you?'                            # Webhook m/provide all text
            
            return {
                "speech": speech,
                "displayText": speech,
                # "data": data,
                # "contextOut": [],
                "source": "bartender service"
            }

        #
        # Beer.StylesQuery
        #   User requested styles
        #
        if payload['result']['action'] == 'Beer.StylesQuery':
            speech = 'Today I am serving: '
            stylelist = styles()
            
            for style in stylelist[:-1]:
                speech += style + 's, '
            speech += 'and ' + stylelist[-1] + 's. '   # pretty up the last one
            
            return {
                "speech": speech,
                "displayText": speech,
                # "data": data,
                # "contextOut": [],
                "source": "bartender service"
            }
        
        #
        # Beer.Query
        #   Specific beer or brewer queried for availability
        #
        if payload['result']['action'] == 'Beer.Query':
            outContext = {'name': 'beer_available', 'lifespan': 1}
            print payload['result']['parameters']
            # check to see which keys are present...
            brewer = ''
            product = ''
            if 'brewer' in payload['result']['parameters']['beer']:
                brewer = payload['result']['parameters']['beer']['brewer']
            if 'product' in payload['result']['parameters']['beer']:
                product = payload['result']['parameters']['beer']['product']

            # If both brewer and product are empty, then we don't know about this beer
            if brewer == '' and product == '':
                speech = 'No, we do not have ' + payload['result']['parameters']['beer'] + '. Would you like to see the beer list?'
                outContext = {'name': 'See_Beer_List', 'lifespan': 1}

                return {
                    "speech": speech,
                    "displayText": speech,
                    # "data": data,
                    "contextOut": [outContext],
                    "source": "bartender service"
                }
                
            # If we have both brewer and product, search the list
            if brewer != '' and product != '':
                blist = [b for b in beers if b["brewer"] == brewer and b['product'] == product]
                if len(blist) != 0:
                    speech = 'Yes, I do have that beer! Would you like one?'
                    outContext['parameters'] = {'brewer': brewer, 'product': product}
                else:
                    speech = 'Not on tap, but I do have one in the cellar, shall I get it for you?'
                    outContext['parameters'] = {'brewer': brewer, 'product': product}
            else:    
                # If we have only the brewer, search the list like we do for Beer.Order
                if brewer != '':                
                    # Check to see if the requested brewer has more than one product on tap
                    blist = [b for b in beers if b["brewer"] == brewer]
                    if len(blist) > 1:
                        speech = 'That brewer makes ' 
                        for b in blist[:-1]:
                            speech += b['product'] + ', '
                        speech += 'and ' + blist[-1]['product'] + '. Which do you want?'
                        outContext = {'name': 'ambiguous_product', 'lifespan': 1}
                        outContext['parameters'] = {'brewer': brewer}
                    else:
                        speech = 'Yes, I have the ' + blist[0]['product'] + ' on tap. Would you like me to pour one?'
                        outContext['parameters'] = {'brewer': brewer, 'product': blist[0]['product']}
                else:    # brewer not specified so look for product
                    # Are there more than one products with that same name?
                    blist = [b for b in beers if b["product"] == product]
                    if len(blist) > 1:
                        speech = 'Several brewers make a beer with that name, including: '
                        for b in blist[:-1]:
                            speech += b['brewer'] + ', '
                        speech += 'and ' + blist[-1]['brewer'] + '. Which do you want?'
                        outContext = {'name': 'ambiguous_brewer', 'lifespan': 1}
                        outContext['parameters'] = {'product': product}
                    else:                 
                        speech = 'Yes, I have one from ' + blist[0]['brewer'] + ' on tap. Would you like me to pour one?'
                        outContext['parameters'] = {'brewer': blist[0]['brewer'], 'product': product}
            

            return {
                "speech": speech,
                "displayText": speech,
                # "data": data,
                "contextOut": [outContext],
                "source": "bartender service"
            }


        #
        # Beer.Order
        #   Specific beer or brewer requested
        #
        if payload['result']['action'] == 'Beer.Order':
            outContext = {'name': 'beer_served', 'lifespan': 1}
            # check to see which keys are present...
            brewer = ''
            product = ''
            if 'brewer' in payload['result']['parameters']['beer']:
                brewer = payload['result']['parameters']['beer']['brewer']
            if 'product' in payload['result']['parameters']['beer']:
                product = payload['result']['parameters']['beer']['product']

            # If both brewer and product are empty, then we don't know about this beer
            if brewer == '' and product == '':
                speech = 'No, we do not have ' + payload['result']['parameters']['beer'] + '. Would you like to see the beer list?'
                outContext = {'name': 'See_Beer_List', 'lifespan': 1}

                return {
                    "speech": speech,
                    "displayText": speech,
                    # "data": data,
                    "contextOut": [outContext],
                    "source": "bartender service"
                }
                                
            # if both brewer and product provided, we are done
            if brewer != '' and product != '':
                speech = 'Now serving your ' + brewer + ' ' + product + '.'
                outContext['parameters'] = {'brewer': brewer, 'product': product}
            else:    
                if brewer != '':                
                    # Check to see if the requested brewer has more than one product on tap
                    blist = [b for b in beers if b["brewer"] == brewer]
                    if len(blist) > 1:
                        speech = 'That brewer makes ' 
                        for b in blist[:-1]:
                            speech += b['product'] + ', '
                        speech += 'and ' + blist[-1]['product'] + '. Which do you want?'
                        outContext = {'name': 'ambiguous_product', 'lifespan': 1}
                        outContext['parameters'] = {'brewer': brewer}
                    else:
                        speech = 'Here is your ' + brewer + '.'
                        outContext['parameters'] = {'brewer': brewer, 'product': blist[0]['product']}
                else:    # brewer not specified so look for product
                    # Are there more than one products with that same name?
                    blist = [b for b in beers if b["product"] == product]
                    if len(blist) > 1:
                        speech = 'Several brewers make a beer with that name, including: '
                        for b in blist[:-1]:
                            speech += b['brewer'] + ', '
                        speech += 'and ' + blist[-1]['brewer'] + '. Which do you want?'
                        outContext = {'name': 'ambiguous_brewer', 'lifespan': 1}
                        outContext['parameters'] = {'product': product}
                    else:                 
                        speech = 'Here is your ' + product + '.'
                        outContext['parameters'] = {'brewer': blist[0]['brewer'], 'product': product}
            
            return {
                "speech": speech,
                "displayText": speech,
                # "data": data,
                "contextOut": [outContext],
                "source": "bartender service"
            }


api.add_resource(Apiai, '/apiai')
        
if __name__ == '__main__':
    app.run(debug=True)