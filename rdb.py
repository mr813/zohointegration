import rethinkdb as r
import sys

import logging
logging.basicConfig( \
        format='[%(levelname)8s] [%(asctime)s] [%(name)s] %(message)s', \
        level=logging.INFO \
)
logger = logging.getLogger(__name__)

class rdb:

    def __init__(self, **kwargs):
        self.r_host = kwargs['r_host']
        self.r_port = kwargs.get('r_port', 28015)
        self.r_db = kwargs.get('r_db', 'jira')
        self.r_tables = kwargs['r_tables']

        self.init_connection(kwargs)
        self.create_database(self.r_db)
        self.create_tables(self.r_tables)

        pass


    def init_connection(self, kwargs):

        try: # Quit if couldn't connect to db
            logger.info('Connecting to rethinkdb...')
            r.connect(self.r_host, self.r_port).repl()
        except Exception as e:
            logger.error('Connecting to rethinkdb failed! '+str(e))
            sys.exit(1)

    def create_database(self, db):

        try: # If db or table created, ignore it.
            logger.info('Creating database...')
            r.db_create(db).run()
        except:
            logger.warning('Database already created')

        pass

    def create_tables(self, tables):
        for table in tables:
            try:
                logger.info('Creating table '+table)
                r.db(self.r_db).table_create(table).run()
            except:
                logger.warning('Table '+table+' already created!')


