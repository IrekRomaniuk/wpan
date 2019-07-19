
# Worskpot PAN User-ID integration

### Format of config file

```
--- # Workspot credentials
- ApiClientId : "" #Workspot Control API Client ID
- ApiClientSecret : "" #Workspot Control API Client Secret
- WsControlUser : "" #Workspot Control Administrator user email address
- WsControlPass : "" #Workspot Control Administrator user password
- Firewalls: 
  - "192.168.3.1 vsys2" # List of PAN firewall (vsys included, vsys1 is default)
```

### Install and Run

```
$python3.7 -m pip install -r requirements.txt
$python3.7 wpan.py
```

### Workspot

[Using the Workspot Control API](https://workspot.zendesk.com/hc/en-us/articles/360017693611-Using-the-Workspot-Control-API)

### Palo Alto Networks

[pan-python is a multi-tool set for Palo Alto Networks PAN-OS, Panorama, WildFire and AutoFocus](https://github.com/kevinsteves/pan-python/blob/master/doc/pan.xapi.rst)

```
admin@PA-200> show user ip-user-mapping all | match romaniuk
10.33.16.33                                    vsys1  XMLAPI  ws\iromaniuk                     215941         215941
10.33.20.18                                    vsys1  XMLAPI  ws\iromaniuk                     215940         215940
admin@PA-200> show user group name ws_fte | match romaniuk
[6     ] ws\iromaniuk
admin@PA-200> show user group name ws_externaldeveloper | match romaniuk
[3     ] ws\iromaniuk
```

```
admin@PA-200> show user group list xmlapi | match ws_
ws_fte
ws_powervm
ws_workspot
ws_externaldeveloper

admin@PA-200> show user ip-user-mapping all type XMLAPI | match ws_

```

