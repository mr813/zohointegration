import falcon
import json
import rethinkdb as rdb
import requests

import config

class Zoho:

    def _send(self, request_params=None):
        """Request crafting method"""

        params = {}
        params.update(config.zoho_params)

        if(request_params):
            params.update(request_params)

        r = requests.get(config.zoho_url+"requests/getrecords", params=params)
        return r.text


    def _get_tasks(self):
        """Get all available tasks"""
        return self._send()


    def on_get(self, req, resp):

        resp.body = self._get_tasks()
        resp.status = falcon.HTTP_200

        """
        try:
            rdb.connect(config.rethinkdb_host, config.rethinkdb_port).repl()
            data = { 'info': 'success'}
        except Exception as e:
            data = { 'error': str(e) }
        """

        #resp.body = json.dumps(data)



