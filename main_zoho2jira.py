import rethinkdb as r
import json, sys, re

import logging
logging.basicConfig( \
        format='[%(levelname)8s] [%(asctime)s] [%(name)s] %(message)s', \
        level=logging.INFO \
)
logger = logging.getLogger(__name__)

try:
    import config
except ImportError:
    loggger.error("You need to execute run.sh first!")

import rdb
import zoho
import jira

logger.info('Starting zoho2jira...')

class zoho_to_jira:

    def __init__(self, **kwargs):
        # Some debug info
        logger.info('Jira project: ' + kwargs['jira_project'])
        logger.info('Zoho portal: ' + kwargs['zoho_portal'])

        # Copy kwargs to self
        # Available variables:  r_host, r_db, r_table_jira, r_table_zoho
        #                       zoho_portal, zoho_department, zoho_token, last_time, zoho_domain
        self.__dict__.update(kwargs)

        self.zoho = zoho.zoho_collect_tickets(**kwargs)
        self.jira = jira.jira(**kwargs)

    def jira_ticket_to_db(self):
        """Dump all jira tickets (or single one) to DB"""

        data = self.jira.get_all_tickets()
        output = r.db(self.r_db).table(self.r_table_jira) \
                .insert(data, conflict="replace") \
                .run()
        logger.info("RethinkDB output: " + str(output))


    def jira_check_duplicate(self, zoho_ticket_id):
        """Check if tickets been created earlier"""
        logger.info("Ticket ID ["+zoho_ticket_id+"]: Checking ticket #" + zoho_ticket_id + " for duplicate")
        output = r.db(self.r_db).table(self.r_table_jira) \
                .filter( lambda row: row['fields']['summary'].match("\[ZOHO\#" + zoho_ticket_id + "\]")) \
                .run()
        if len(output.items):
            return True

        return False


    def save_tickets(self, data):
        """Save Zoho tickets to DB, replace if needed"""

        logger_info = "Ticket ID [" + data['Ticket Id'] + "]: "
        logger.info(logger_info + "Saving ticket to database...")
        data = [data]  # required for the loop

        for key, val in enumerate(data):               # Rename 'no' field to 'id' for nosql db
            data[key]['id'] = data[key]['Ticket Id']   # so it would be overriden/updated when

        try:
            output = r.db(self.r_db).table(self.r_table_zoho)    \
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


    def jira_create_ticket(self, data):
        """Call Jira client to create ticket

        That how zoho proper dict looks like:

        {
            'CONTACTID': '91932000000561155',
            'Ticket Id': '625',
            'Due Date': '2015-09-23 22:00:00',
            'Email': 'null',
            'Subject': 'qwewewewe',
            'URI': '/support/icontrolusa/ShowHomePage.do#Cases/dv/42488da48da23d8e137ba6c977c6cdddf3148ec5bcd90913',
            'Department': 'SBT-Client Services',
            'DEP_ID': '91932000000284673',
            'Request Id': '625',
            'CASEID': '91932000000561157',
            'Contact Name': 'mak lopez'
        }

        """

        logger_info = "Ticket ID [" + data['Ticket Id'] + "]: "
        logger.info(logger_info + "Creating ticket in Jira...")

        # Prepare subject for jira ticket subject
        data['Subject'] = self.zoho_ticket_subject_clear(data['Subject'])
        data['Subject'] = self.zoho_ticket_subject_truncate(data['Subject'])

        # Append summary and description fields to jira_dict
        self.jira_dict['fields']['summary'] = data['Subject'] + " [ZOHO#" + data['Ticket Id'] + "]"
        self.jira_dict['fields']['description'] =  "Zoho TicketID: " + data['Ticket Id'] + \
                                                 "\nZoho TicketURL: " + self.zoho_domain + data['URI']

        result = self.jira.create_ticket(self.jira_dict)

        if int(result.status_code) is not int(201):
            logger.error("Creating ticket failed!!! \n\nResponse status code: "+str(result.status_code) +\
                    "\n\n" + "Response url: \n\n" + str(result.url) + \
                    "\n\n" + "Response request method: " + str(result.request.method) + \
                    "\n\n" + "Response request headers: \n\n" + str(result.request.headers) + \
                    "\n\n" + "Response headers: \n\n" + str(result.headers) + \
                    "\n\n" + "Response text: \n\n" + str(result.text)
            )
            sys.exit(1)
        else:
            logger.info(logger_info + "Ticket created!")
            return result.json()

    def zoho_ticket_subject_clear(self, subject):
        """Find a previous jira tag and remove it."""

        try:
            subj_match = re.findall(r'\[JIRA.*\]', subject)[0]
            subject = subject.replace(subj_match, '').rstrip()
        except:
            pass

        return subject

    def zoho_ticket_subject_truncate(self, subject):
        """Truncate subject if it's more than 240 chars, rest will be used for ticket id's."""
        return subject[:230] + (subject[230:] and '..')

    def zoho_ticket_subject_update(self, caseid, jiraid, subject):
        """Update zoho ticket subject after jira ticket is created"""
        logger.info("Updating zoho ticket...")

        subject = self.zoho_ticket_subject_clear(subject)
        subject = self.zoho_ticket_subject_truncate(subject)

        self.zoho.update_ticket_subject(caseid, jiraid, subject)

    def zoho_bug_fix(self, data):
        """ This is zoho bug fix, when only one ticket returned they give it as single dictionary """

        if type(data) is dict:
            data = [data]

        return data

    def sync_jira(self, data, first_time_sync=False):
        """Sync data to Jira

           first_time_sync - parameters which specified that it's first time synhronization
                             no ticket will be checked on jira, you must start from fresh project!
        """
        logger.info("Syncing data to Jira...")

        # Let's check do we have any zoho tickets added, if so, skip them for now
        data = self.zoho_data_strip(data)
        data = self.zoho_bug_fix(data)

        if not first_time_sync:

            for key, val in enumerate(data):
                data[key] = self.zoho_proper_dict(data[key])
                logger_info = "Ticket ID [" + data[key]['Ticket Id'] + "]: "
                logger.info(logger_info + "Checking if exists in DB...")

                result = r.db(self.r_db).table(self.r_table_zoho).filter({
                    "id" : str(data[key]['Ticket Id']) #<--- MUST BE STRING!
                }).run()


                if not len(list(result)): # If ticket not found...
                    logger.info(logger_info + "Not found! Creating ticket in Jira...")

                    if self.jira_check_duplicate(data[key]['Ticket Id']):
                        logger.warning('Duplicate found! Skipping...')
                        continue

                    jira_ticket = self.jira_create_ticket(data[key])
                    self.zoho_ticket_subject_update( data[key]['CASEID'], jira_ticket, data[key]['Subject']  )
                    self.save_tickets(data[key])

                else:
                    # TODO: Update ticket in Jira
                    logger.info("Ticket ID ["+data[key]['Ticket Id']+"]: Found! Skipping...")
                    pass

        else: # First time sync

            logger.info("Dumping all jira tickets to DB")
            self.jira_ticket_to_db() # Dump all jira tickets to DB, required for checking duplicates

            for ticket in data:
                ticket = self.zoho_proper_dict(ticket)
                if self.jira_check_duplicate(ticket['Ticket Id']):
                    logger.warning('Duplicate found! Skipping...')
                    continue
                jira_ticket = self.jira_create_ticket(ticket)
                self.zoho_ticket_subject_update(ticket['CASEID'], jira_ticket, ticket['Subject'])
                self.save_tickets(ticket)


    def run(self):
        """Main workflow method"""

        # If rethinkdb is empty, we need to fetch tickets first!
        # Ignoring exception in here, as it's the only way to check
        # if table is empty without count() which is terribly slow!
        try:
            r.db(self.r_db).table(self.r_table_zoho).nth(0).run()
            result = 1
        except:
            result = None

        if result is not None:

            logger.info('Getting recent zoho tickets...')
            data = self.zoho.get_recent_tickets()

            try:
                if data.json()['response']['error']['code'] == 4832:
                    logger.info('Nothing to sync :}')
                    sys.exit()

            except KeyError:
                logger.info('There new data to sync :}')
                self.sync_jira(data)

        else:
            logger.info('Seems to be table is empty, fetching all zoho tickets...')
            data = self.zoho.get_all_tickets()

            try:
                if data.json()['response']['error']['code'] == 4832:
                    logger.error("Zoho project doesn't have any tickets")
                    sys.exit()
            except KeyError:
                pass

            self.sync_jira(data, True)



db = rdb.rdb(
    r_host=config.r_host,
    r_db=config.r_db,
    r_tables = config.r_tables
)


ztoj = zoho_to_jira(
    r_host=config.r_host,
    r_db=config.r_db,
    r_table_zoho=config.r_table_zoho,
    r_table_jira=config.r_table_jira,

    jira_user = config.jira_user,
    jira_password = config.jira_password,
    jira_project = config.jira_project,
    jira_project_key = config.jira_project_key,
    jira_dict = config.jira_dict,

    zoho_portal = config.zoho_portal,
    zoho_department = config.zoho_department,
    zoho_token = config.zoho_token,
    zoho_last_time =  config.zoho_last_time,
    zoho_domain = config.zoho_domain
)
ztoj.run()
