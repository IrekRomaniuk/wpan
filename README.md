
# Work in progress (Under Development)

### Format of config file

```
--- # Workspot credentials
- ApiClientId : "" #Workspot Control API Client ID
- ApiClientSecret : "" #Workspot Control API Client Secret
- WsControlUser : "" #Workspot Control Administrator user email address
- WsControlPass : "" #Workspot Control Administrator user password
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
admin@PA-200> show user ip-user-mapping all
(container-tag: user container-tag: ip-user-mapping container-tag: all pop-tag: pop-tag: pop-tag:)
((eol-matched: . #t) (context-inserted-at-end-p: . #f))


<request cmd="op" cookie="6777592993635321" uid="500"><operations><show><user><ip-user-mapping><all/></ip-user-mapping></user></show></operations></request>


2019-07-14 23:40:52
<response status="success"><result>IP                                            Vsys   From    User                             IdleTimeout(s) MaxTimeout(s)
--------------------------------------------- ------ ------- -------------------------------- -------------- -------------
1.1.1.1                                       vsys1  XMLAPI  user1                            1802           1802
3.3.3.3                                       vsys1  XMLAPI  user3                            Never          Never
Total: 2 users
</result></response>
IP                                            Vsys   From    User                             IdleTimeout(s) MaxTimeout(s)
--------------------------------------------- ------ ------- -------------------------------- -------------- -------------
1.1.1.1                                       vsys1  XMLAPI  user1                            1802           1802
3.3.3.3                                       vsys1  XMLAPI  user3                            Never          Never
Total: 2 users
```
