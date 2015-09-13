import falcon
import requests

import config

class Jira:

    def _send(self, request_params=None):
        """Request crafting method"""

        params = {}
        params.update(config.zoho_params)

        if(request_params):
            params.update(request_params)

        r = requests.get(config.zoho_url+"requests/getrecords", params=params)
        return r.text
        """Request crafting method"""

        params = {}
        params.update(config.zoho_params)

        if(request_params):
            params.update(request_params)

        r = requests.get(config.zoho_url+"requests/getrecords", params=params)
        return r.text
