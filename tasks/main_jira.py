import jira

z = jira.jira(
    jira_user='mark.lopez',
    jira_password='regulated2015',
    rdb_host='rethinkdb',
    rdb_db='zohotojira',
    rdb_table='jira'
)
z.get_tickets()
