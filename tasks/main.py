import rethinkdb as r
import json
import sys

import logging
logging.basicConfig( \
        format='[%(levelname)8s] [%(asctime)s] [%(name)s] %(message)s', \
        level=logging.INFO \
)
logger = logging.getLogger(__name__)

import zoho

class zoho_to_jira:

    def __init__(self, **kwargs):

        self.init_r(kwargs)
        self.init_zoho(kwargs)

    def init_zoho(self, kwargs):
        self.zoho = zoho.zoho_collect_tickets(
            zoho_portal='icontrolusa',
            zoho_department='SBT-Client Services',
            zoho_token='5e32980f1c7513f0f6dcc9247d21f37a',
            zoho_last_time=300
        )

    def init_r(self, kwargs):
        """Constructor for rethinkdb"""

        self.r_host = kwargs['r_host']
        self.r_port = kwargs.get('r_port', 28015)
        self.r_db = kwargs['r_db']
        self.r_table = kwargs['r_table']

        try: # Quit if couldn't connect to db
            logger.info('Connecting to rethinkdb...')
            r.connect(self.r_host, self.r_port).repl()
        except Exception as e:
            logger.error('Connecting to rethinkdb failed! '+str(e))
            sys.exit(1)

        try: # If db or table created, ignore it.
            logger.info('Creating database...')
            r.db_create(self.r_db).run()

            logger.info('Creating table...')
            r.db(self.r_db).table_create(self.r_table).run()
        except Exception as e:
            logger.warning('Already created')


    def save_all_tickets(self, data):
        """Save all Zoho ticket to DB, replace if needed"""

        data = data.json()['response']['result']['Cases']['row']

        for key, val in enumerate(data):        # Rename 'no' field to 'id' for nosql db
            data[key]['id'] = data[key]['no']   # so it would be overriden/updated when
            data[key].pop('no', None)           # inserting same dictionary

        try:
            logger.info('Saving all zoho tickets to db...')
            output = r.db(self.r_db).table(self.r_table)    \
                    .insert(data, conflict="replace")   \
                    .run()
            logger.info('RethinkDB output: '+str(output))
        except Exception as e:
            logger.error('Failed to save all tickets to database! '+str(e))

    def run(self):
        """Sync data between zoho and jira"""

        # If rethinkdb is empty, we need to fetch tickets first!
        # Ignoring exception in here, as it's the only way to check
        # if table is empty without count() which is terribly slow!
        try:
            r.db(self.r_db).table(self.r_table).nth(0).run()
            result = 1
        except:
            result = None

        if result is not None:
            logger.info('Getting recent zoho tickets...')
            data = self.zoho.get_recent_tickets()
            try:
                if data.json()['response']['error']['code'] == 4832:
                    logger.info('Nothing to sync :}')
            except:
                logger.info('There new data to sync :}')
                self.save_all_tickets(data)


        else:
            logger.info('Seems to be table is empty, fetching all zoho tickets...')
            data = self.zoho.get_all_tickets()
            self.save_all_tickets(data)

ztoj = zoho_to_jira(
    r_host='rethinkdb',
    r_db='zohotojira',
    r_table='zoho'
)
ztoj.run()
