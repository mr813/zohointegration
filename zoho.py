import rethinkdb as r
import json
import requests
import sys
import datetime

import logging
logging.basicConfig( \
        format='[%(levelname)8s] [%(asctime)s] [%(name)s] %(message)s', \
        level=logging.INFO \
)
logger = logging.getLogger(__name__)

class zoho_collect_tickets:

    def __init__(self, **kwargs):

        # Copy kwargs to self
        # Available variables: zoho_portal, zoho_department, zoho_token, last_time
        self.__dict__.update(kwargs)

        self.init_zoho(kwargs)


    def init_zoho(self, kwargs):
        """Constructor for zoho"""
        self.zoho_url = "https://support.zoho.com/api/json/"
        self.last_time = datetime.datetime.now() - \
                datetime.timedelta( \
                    minutes=kwargs.get('zoho_last_time', 5000) \
                )
        self.last_time = self.last_time.strftime("%Y-%m-%d %H:%M:%S")


    def send(self, url, request_params=None):
        """Crafting request and send it"""

        params = {}
        params.update({
            # NEVER SPECIFY PARAMS IN CAMELCASE! IT DOESN'T WORK!
            'portal'    : self.zoho_portal,
            'department': self.zoho_department,
            'authtoken' : self.zoho_token,
            'scope'     : 'crmapi',
            'newformat' : 2,
        })

        if(request_params):
            params.update(request_params)

        try:
            return requests.get(self.zoho_url+url, params=params)
        except Exception as e:
            logger.error("Can't connect to Zoho: "+str(e))
            sys.exit(1)


    def get_all_tickets(self):
        """Get all Zoho tickets"""
        return self.send('cases/getrecords')


    def get_recent_tickets(self):
        """Get recently updated tickets"""
        return self.send('cases/getrecords', \
                {'lastmodifiedtime': self.last_time})

    def change_ticket_status(self, id, status):
        pass


