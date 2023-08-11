from flask import Flask, request
from flask_restful import Api, Resource

from simulatorNode import SimulatorNode

app = Flask(__name__)
api = Api(app)
port_number = 5000

class Simulator(Resource):
    node = SimulatorNode()
    def get(self):
        return "Hi There"

    def post(self):
        return self.node.OnStep(request)


api.add_resource(Simulator, '/')

if __name__ == '__main__':
       app.run(port=port_number)