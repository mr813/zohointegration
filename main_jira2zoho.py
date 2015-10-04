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
import jira
import config
import rdb


class jira_to_zoho:

    def __init__(self, **kwargs):
        # Some debug info
        logger.info('Jira project: ' + self.jira_project)
        logger.info('Zoho portal: ' + self.zoho_portal)

        self.r_host = kwargs['r_host']
        self.r_db = kwargs['r_db']
        self.r_tables = kwargs['r_tables']
        self.r_table_jira = kwargs['r_table_jira']
        self.r_table_jira = kwargs['r_table_zoho']

        self.zoho = zoho.zoho_collect_tickets(**kwargs)
        self.jira = jira.jira(**kwargs)

    def save_tickets(self, data):
        """Save Zoho tickets to DB, replace if needed"""

        if len(data) == 2:
            logger_info = "Ticket ID [" + data['id'] + "]: "
            logger.info(logger_info + "Saving ticket to database...")
        else:
            logger.info('Saving all jira tickets to database...')

        try:
            output = r.db(self.r_db).table(self.r_table_jira)    \
                    .insert(data, conflict="replace")   \
                    .run()
            logger.info('RethinkDB output: '+str(output))
        except Exception as e:
            logger.error('Failed to save ticket/s to database! '+str(e))
            sys.exit(1)


    def zoho_data_strip(self, data):
        """Get rid of trash in JSON result of Zoho"""
        return data.json()['response']['result']['Cases']['row']


    def zoho_proper_dict(self, data):
        """Convert Zoho response to proper dictionary

           data - Zoho stripped data from cycle
        """
        proper_dict = {}
        for row in data['fl']:
            proper_dict[ row['val'] ] = row['content']

        return proper_dict

    def jira_first_time_sync(self, data):
        """First time syncing from jira to DB"""

        for ticket in data:
            # Get ID of Zoho ticket
            output = r.db(self.r_db).table(self.r_table_zoho) \
                    .filter({
            self.zoho.change_ticket_status(ticket)
            self.save_tickets(ticket)


    def sync_zoho(self, data, first_time_sync=False):
        """Sync data to Zoho

           TODO: Currently syncing only if status closed!

           first_time_sync - parameters which specified that it's first time synhronization
                             no ticket will be checked on zoho, you must start from fresh project!
        """
        logger.info("Syncing data to Zoho...")

        if not first_time_sync:

            for key, val in enumerate(data):
                logger_info = "Ticket ID [" + data[key]['no'] + "]: "
                logger.info(logger_info + "Checking if exists in DB...")

                result = r.db(self.r_db).table(self.r_table_zoho).filter({
                    "id" : str(data[key]['no']) #<--- MUST BE STRING!
                }).run()


                if not len(list(result)): # If ticket not found...
                    logger.info(logger_info + "Not found! Creating ticket in Jira...")

                    self.jira_create_ticket(data[key], data[key]['no'])
                    self.save_tickets(data[key])

                else:
                    # TODO: Update ticket in Jira
                    logger.info("Ticket ID ["+data[key]['no']+"]: Found! Skipping...")

        else:
            self.jira_first_time_sync(data)

    def check_zoho_data(self):
        """Check if zoho table empty, if yes exit script"""

        try:
            logger.info("Checking is zoho table empty...")
            r.db(config.r_db).table(config.r_table_zoho).nth(0).run()
            result = 1
        except:
            sys.exit("Zoho table empty, please run zoho2jira first")


    def check_jira_data(self):
        """Check if jira table empty"""

        # If rethinkdb is empty, we need to fetch tickets first!
        # Ignoring exception in here, as it's the only way to check
        # if table is empty without count() which is terribly slow!
        try:
            logger.info("Checking is jira table empty...")
            r.db(config.r_db).table(config.r_table_jira).nth(0).run()
            return 1
        except:
            return None

    def run(self):
        """Main workflow method"""

        self.check_zoho_data()
        result = self.check_jira_data()

        if result is not None:

            logger.info('Getting recent jira tickets...')
            data = self.jira.get_recent_tickets()

            try:
                if data.json()['response']['error']['code'] == 4832:
                    logger.info('Nothing to sync :}')
                    sys.exit()

            except KeyError:
                logger.info('There new data to sync :}')
                self.sync_jira(data)

        else:
            # Currently fetch only with status closed
            logger.info('Seems to be table is empty, fetching all jira tickets...')
            data = self.jira.get_all_tickets()
            self.sync_zoho(data, True)


db = rdb.rdb(
    r_host=config.r_host,
    r_db=config.r_db,
    r_tables = config.r_tables
)

ztoj = jira_to_zoho(

    r_host=config.r_host,
    r_db=config.r_db,
    r_tables = config.r_tables

    jira_user = config.jira_user,
    jira_password = config.jira_password,
    jira_project = config.jira_project,
    jira_project_key = config.jira_project_key,

    zoho_portal = config.zoho_portal,
    zoho_department = config.zoho_department,
    zoho_token = config.zoho_token,
    zoho_last_time =  config.zoho_last_time
)
ztoj.run()
