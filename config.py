import os

# Zoho

# Zoho portal name
zoho_portal = os.getenv('ZOHO_PORTAL', 'icontrolusa')

# Zoho department name
zoho_department = os.getenv('ZOHO_DEPARTMENT', 'SBT-Client Services')

# Zoho token
zoho_token = os.getenv('ZOHO_TOKEN', '5e32980f1c7513f0f6dcc9247d21f37a')

# Zoho last ticket update seconds ago
zoho_last_time = int(os.getenv('ZOHO_LAST_TIME', 12000)) # 20 minutes

# Jira

# Jira user
jira_user = os.getenv('JIRA_USER', 'mark.lopez')

# Jira password
jira_password = os.getenv('JIRA_PASSWORD', 'regulated2015')

# Jira project name
jira_project = os.getenv('JIRA_PROJECT', 'ISD')

# Jira project key name
jira_project_key = os.getenv('JIRA_PROJECT_KEY', 'ISD')

# RethinkDB
r_host = os.getenv('R_HOST', 'rethinkdb')
r_db = os.getenv('R_DB', 'zohotojira')
r_table_zoho = 'zoho'
r_table_jira ='jira'
r_tables = ['zoho', 'jira']
