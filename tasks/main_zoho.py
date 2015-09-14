import zoho

z = zoho.zoho_collect_tickets(
    zoho_portal='icontrolusa',
    zoho_department='SBT-Client Services',
    zoho_token='5e32980f1c7513f0f6dcc9247d21f37a',
    rdb_host='rethinkdb',
    rdb_db='zohotojira',
    rdb_table='zoho'
)
z.get_tickets()
