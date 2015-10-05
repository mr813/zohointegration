import os

# Zoho

# Zoho portal name
zoho_portal = 'icontrolusa'

# Zoho department name
zoho_department = 'Desktop Support'

# Zoho token
zoho_token = '5e32980f1c7513f0f6dcc9247d21f37a'

# Zoho last ticket update seconds ago
zoho_last_time = int(60*5) # 1 minutes
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

# Jira "Issue type" field
jira_issue_type = 'New Feature'

# Jira "Component" field
jira_components = [{'id': '10406', 'name': 'SBT' }]

# Jira "Request Source" field
jira_customfield_10300 = {'id': '10200', 'value': 'Internal' }

# RethinkDB
r_host = 'rethinkdb'
r_db = 'zohotojira'
r_table_zoho = 'zoho'
r_table_jira ='jira'
r_tables = ['zoho', 'jira']
