import falcon
import json

import zoho

api = falcon.API()
sugar = zoho.Zoho()
api.add_route('/', zoho)
