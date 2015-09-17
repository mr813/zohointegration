import rethinkdb as rdb
from requests.auth import HTTPBasicAuth
import requests
import json

class jira:

    def __init__(self, **kwargs):
        self.init_rdb(kwargs)
        self.init_jira(kwargs)
        pass

    def init_rdb(self, kwargs):
        """ Constructor for rethinkdb"""

        self.rdb_host = kwargs['rdb_host']
        self.rdb_port = kwargs.get('rdb_port', 28015)
        self.rdb_db = kwargs['rdb_db']
        self.rdb_table = kwargs['rdb_table']

        rdb.connect(self.rdb_host, self.rdb_port).repl()

        try: # If db or table created, ignore it.
            rdb.db_create(self.rdb_db).run()
            rdb.db(self.rdb_db).table_create(self.rdb_table).run()
        except Exception as e:
            pass

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


