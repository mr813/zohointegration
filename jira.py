import sys
import json
import math
import requests
from requests.auth import HTTPBasicAuth

import logging
logging.basicConfig( \
        format='[%(levelname)8s] [%(asctime)s] [%(name)s] %(message)s', \
        level=logging.INFO \
)
logger = logging.getLogger(__name__)

class jira:

    def __init__(self, **kwargs):
        self.init_jira(kwargs)
        pass


    def init_jira(self, kwargs):
        """Constructor for Jira"""

        self.jira_url = "https://icucsolutions.atlassian.net/rest/api/2/"

        # Copy kwargs to self
        # Available variables: jira_user, jira_password, jira_project, jira_project_key, jira_dict
        self.__dict__.update(kwargs)

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

                url = self.jira_url+url+"?jql=project="+self.jira_project_key
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
            'fields': 'id,summary'
        }

        return self.send("search", params)


    def get_all_tickets(self):
        """Get all jira tickets"""

        logger.info("Get all jira tickets...")

        collected_issues = []

        params = {
            'fields': 'id,summary'
        }

        result = self.send("search", params).json()

        # Pagination
        if result['total'] > result['maxResults']:
            logger.info("Pagination detected...")

            collected_issues.extend(result['issues'])       # Append first page to collection
            pages = result['total'] / result['maxResults']  # Get total page number
            pages = int(math.ceil(pages))                   # Rounding to upper number

            for i in range(1, pages):                       # Iterate through pages
                logger.info("Getting page "+str(i+1))
                params['startAt'] = (result['maxResults']*1)+1   # Start from 51th record, then 101
                collected_issues.extend( \
                    self.send('search', params).json()['issues']
                )
            return collected_issues

        return result['issues']


    def create_ticket(self, jira_dict):
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
        return self.send('issue', jira_dict, 'post')

