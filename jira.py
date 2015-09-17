import rethinkdb as rdb
from requests.auth import HTTPBasicAuth
import requests
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


    def send(self, request_params=None):
        """Crafting request and send it"""

        params = {}

        try:
            return requests.get(self.jira_url+"search", params=params,  auth=HTTPBasicAuth(self.jira_user, self.jira_password))
        except Exception as e:
            print("Can't connect to Jira: "+str(e))


