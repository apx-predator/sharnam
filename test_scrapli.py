from nornir import InitNornir

from nornir.core.plugins.inventory import InventoryPluginRegister
from nornir_scrapli.tasks import netconf_get_config




def get_running(task):
    result = netconf_get_config(task, source="running", filter_="<interfaces/>")
    print(f"[{task.host.name}] got {len(result.result)} chars of running config")
    return result


nr = InitNornir(
    runner={"plugin": "threaded", "options": {"num_workers": 1}},
    inventory={
        "plugin": "FlatDataInventory",
        "options": {
            "data": [{
                "name": "sandbox",
                "hostname": "devnetsandboxiosxec9k.cisco.com",
                "platform": "cisco_iosxe",
                "username": "yusufnjenga145",
                "password": "2xuq1-9BU-saM5R",
                "connection_options": {
                    "scrapli_netconf": {
                        "port": 830,
                        "extras": {
                            
                            "ssh_strict_key": False,
                             
                        }
                    }
                },
            }]
        },
    },
)

result = nr.run(task=get_running)

for host, multi in result.items():
    if multi.failed:
        print(f"❌ {host} FAILED: {type(multi.exception).__name__}: {multi.exception}")
    else:
        print(f"✅ {host} OK")