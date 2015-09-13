import falcon
import json

import zoho
import jira

api = falcon.API()
zoho = zoho.Zoho()
jira = jira.Jira()

api.add_route('/zoho/tasks', zoho)
api.add_route('/jira/tasks', jira)
