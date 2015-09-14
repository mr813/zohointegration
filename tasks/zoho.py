import rethinkdb as rdb
import json
import requests
import sys

class zoho_collect_tickets:

    def __init__(self, **kwargs):
        self.init_zoho(kwargs)
        self.init_rdb(kwargs)


    def init_zoho(self, kwargs):
        """Constructor for zoho"""

        self.zoho_url = "https://support.zoho.com/api/json/"
        self.zoho_portal = kwargs['zoho_portal']
        self.zoho_department = kwargs['zoho_department']
        self.zoho_token = kwargs['zoho_token']


    def init_rdb(self, kwargs):
        """Constructor for rethinkdb"""

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

    def send(self, request_params=None):
        """Crafting request and send it"""

        params = {}
        params.update({
            'portal'    : self.zoho_portal,
            'department': self.zoho_department,
            'authtoken' : self.zoho_token,
            'newFormat' : 2,
        })

        if(request_params):
            params.update(request_params)

        try:
            return requests.get(self.zoho_url+"requests/getrecords", params=params)
        except Exception as e:
            print("Can't connect to Zoho: "+str(e))

    def get_tickets(self):
        """Iterate through all zoho tickets"""

        data = self.send()
        import pprint
        pprint.pprint(data.json())
