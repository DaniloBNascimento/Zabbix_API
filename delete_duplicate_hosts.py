from zabbix_api import ZabbixAPI

# Instance access at API Zabbix
zbx_api = ZabbixAPI(server="http://yourserver/zabbix/")
# User for services
zbx_api.login("youruser", "yourpass")

# Get hosts
hosts = zbx_api.host.get({
    "output": [
        "hostid",
        "host",
    ]
})

# Instance lists for storage hosts
store_hosts_ids = {}
store_hosts = []
store_duplicate = []
store_ids_delete = []

for host in hosts:
    host_str = str(host['host']).lower()
    id_str = str(host['hostid'])
    store_hosts_ids[host_str] = id_str
    store_hosts.append(host_str)


for host in store_hosts_ids:
    if store_hosts.count(host) > 1:
        store_duplicate.append(host)

print("Lista de hosts que serão deletados:\n " + str(store_duplicate))

# Confirmando se os hosts serão deletados
confirm = input("Deseja realmente deletar os hosts supracitados? [y](default), [n](no): ")

if confirm == "y" or confirm == "Y":
    # Show id host in dict
    count_store_duplicate = len(store_duplicate)

    if count_store_duplicate == 0:
        print("Não existem hosts duplicados para deletar!")

    count = 0

    while count_store_duplicate > 0:
        store_ids_delete.append(store_hosts_ids[store_duplicate[count]])
        count = count + 1
        count_store_duplicate = count_store_duplicate - 1

        delete_hosts = zbx_api.host.delete(
            store_ids_delete
        )
    print("Hosts deletados: "+str(store_duplicate))

elif confirm == "n" or confirm == "N":
    print("Nenhum host deletado!")
else:
    print("Nenhuma opção válida foi fornecida!")
