import os

# Zoho

# Zoho portal name
zoho_portal = 'icontrolusa'

# Zoho department name
zoho_department = 'Desktop Support'

# Zoho token
zoho_token = '5e32980f1c7513f0f6dcc9247d21f37a'

# Zoho last ticket update seconds ago
zoho_last_time = int(60*2) # 1 minutes
# Zoho domain
zoho_domain = 'https://support.zoho.com'

# Jira

# Jira user
jira_user = 'mark.lopez'

# Jira password
jira_password = 'regulated2015'

# Jira project name
jira_project = 'IT Desktop & Infrastructure Support'

# Jira project key name
jira_project_key = 'IDIS'

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
            "name": "New Feature"
        },
    }
}

# RethinkDB
r_host = 'rethinkdb'
r_db = 'zohotojira'
r_table_zoho = 'zoho_ds2idis'
r_table_jira ='jira_ds2idis'
r_tables = [r_table_zoho, r_table_jira]
