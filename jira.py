import sys
import json

class jira:

    def __init__(self, **kwargs):
        self.init_jira(kwargs)
        pass


    def init_jira(self, kwargs):
        """Constructor for Jira"""

        self.jira_url = "https://icucsolutions.atlassian.net/rest/api/2/"
        self.jira_user =  kwargs['jira_user']
        self.jira_password = kwargs['jira_password']
        self.jira_project = kwargs.get('jira_project', 'test')
        self.jira_project_key = kwargs.get('jira_project_key', 'TEST-1')

    def send(self, url, request_params=None, method='get'):
        """Crafting request and send it"""

        # TODO: Some default params in here if needed
        # TODO: BE CAREFULL WITH POST PARAMS, still not sure how that's gonna work \
        #       Jira seems to be wants full dictionary in their own structure, so be carefull
        params = {}

        # Append provided parameters to default param dict
        if(request_params):
            params.update(request_params)

        # Construct URL - hardcoding project name, because it's invalid GET parameter
        url = self.jira_url+url+"?jql=project="+self.jira_project
        auth=HTTPBasicAuth(self.jira_user, self.jira_password)

        # Send request
        try:

            if method=='get': # Sorry I just don't want to use eval()
                return requests.get(url, params=params, auth=auth)
            if method=='post':
                return requests.post(url, params=params, auth=auth)

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
                    "key": self.jira_project_key
                },
                "summary": kwargs['summary'],
                "description": kwargs['description'],
                "issuetype": {
                    "name": kwargs['issuetype'],
                }
            }
        }

        self.send('issue', data, 'post')

        pass

