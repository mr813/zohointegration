import falcon
import json
import rethinkdb as rdb

class Zoho:

    def on_get(self, req, resp):
        try:
            rdb.connect("rethinkdb", 28015).repl()
            data = { 'info': 'success'}
        except Exception as e:
            data = { 'error': str(e) }

        resp.body = json.dumps(data)
        resp.status = falcon.HTTP_200



