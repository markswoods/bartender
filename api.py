from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

pilsner = ["Stella Artois", "Pilsner Urquell"]
stout = ["Guiness", "Chocolate Stout"]
ipa = ["All Day IPA", "Two Hearted", "Gate Crasher"]
dipa = ["Road 2 Ruin", "Heddy Topper", "Pliny the Elder", "Hop Stupid"]

class Pilsners(Resource):
    def get(self):
        return pilsner
        
class Stouts(Resource):
    def get(self):
        return stout
        
class IPAs(Resource):
    def get(self):
        return ipa
        
class Dipas(Resource):
    def get(self):
        return dipa
        


api.add_resource(Pilsners, '/pilsners')
api.add_resource(Stouts, '/stouts')
api.add_resource(IPAs, '/ipas')
api.add_resource(Dipas, '/dipas')

if __name__ == '__main__':
    app.run(debug=True)