import falcon
import json

import zoho

api = falcon.API()
zoho = zoho.Zoho()
api.add_route('/zoho/tasks', zoho)
