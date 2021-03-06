import os, time

# Set the timezone!!
os.environ['TZ'] = 'America/New_York'

# Zoho

# Zoho portal name
zoho_portal = 'icontrolusa'

# Zoho department name
zoho_department = 'IT'

# Zoho token
zoho_token = '5e32980f1c7513f0f6dcc9247d21f37a'

# Zoho last ticket update seconds ago
zoho_last_time = 10 # 10 minutes
# Zoho domain
zoho_domain = 'https://support.zoho.com'

# Jira

# Jira user
jira_user = 'ZohoTicketMover'

# Jira password
jira_password = 'regulated2015'

# Jira project name
jira_project = 'Engineering-R&D'

# Jira project key name
jira_project_key = 'HRMY'

# Jira dictionary which will be used to create tickets. 
# This dict follow format of jira API documentation. 
# Check jira.py for details.
# Field "summary" and "description" of the keys will
# be added in jira.py because it contains Zoho ticket ID.
jira_dict = {
    "fields" : {
        "project": {
            "key": jira_project_key,
            "name": jira_project
        },
        "issuetype": {
            "name": "Bug"
        },
        "customfield_10401": [ {
            "id": "10406"
        } ],
        "customfield_10300": {
            "id": "10202"
        }
    }
}

# RethinkDB
r_host = 'rethinkdb'
r_db = 'zohotojira'
r_table_zoho = 'zoho_it2hrmy'
r_table_jira ='jira_it2hrmy'
r_tables = [r_table_zoho, r_table_jira]
