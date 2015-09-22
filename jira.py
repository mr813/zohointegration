import sys
import json
import requests
from requests.auth import HTTPBasicAuth

class jira:

    def __init__(self, **kwargs):
        self.init_jira(kwargs)
        pass


    def init_jira(self, kwargs):
        """Constructor for Jira"""

        self.jira_url = "https://icucsolutions.atlassian.net/rest/api/2/"
        self.jira_user =  kwargs['jira_user']
        self.jira_password = kwargs['jira_password']
        self.jira_project = kwargs['jira_project']
        self.jira_project_key = kwargs['jira_project_key']

    def send(self, url, request_params=None, method='get'):
        """Crafting request and send it"""


        # Construct URL - hardcoding project name, because it's invalid GET parameter
        auth=HTTPBasicAuth(self.jira_user, self.jira_password)

        # Send request
        try:

            if method=='get':

                params = {}

                # Append provided parameters to default param dict
                if(request_params):
                    params.update(request_params)

                url = self.jira_url+url+"?jql=project="+self.jira_project
                return requests.get(url, params=params, auth=auth)

            if method=='post':

                # Jira wants json plain text body
                url = self.jira_url+url
                headers = {'Content-type': 'application/json'}
                return requests.post(url, data=json.dumps(request_params), auth=auth, headers=headers)

            print('Wtf method is that?')
            sys.exit()

        except Exception as e:
            print("Can't connect to Jira: "+str(e))
            sys.exit()

    def search_tickets(self):
        """Search for tickets only with summary field"""

        params = {
            'fields': 'summary'
        }

        return self.send("search", params)

    def create_ticket(self, **kwargs):
        """Create jira ticket

        https://developer.atlassian.com/jiradev/jira-apis/jira-rest-apis/jira-rest-api-tutorials/jira-rest-api-example-create-issue

        {
            "fields": {
               "project":
               {
                  "key": "TEST"
               },
               "summary": "REST ye merry gentlemen.",
               "description": "Creating of an issue using project keys and issue type names using the REST API",
               "issuetype": {
                  "name": "Bug"
               }
           }
        }
        """

        data = {
            "fields" : {
                "project": {
                    "key": self.jira_project_key,
                    "name": self.jira_project
                },
                "summary": kwargs['summary'],
                "description": kwargs['description'],
                "issuetype": {
                    "name": kwargs['issuetype'],
                }
            }
        }

        return self.send('issue', data, 'post')


