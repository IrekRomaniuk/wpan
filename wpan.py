#!/usr/bin/env python3
""" Worskpot PAN User-ID integration """
####################################
# Worskpot PAN User-ID integration #
####################################

import sys, base64, json, logging 
import requests, urllib3, asyncio, pan.xapi
from aiohttp import ClientSession
from aiohttp import TCPConnector

# Variable initialization #
URL = "https://api.workspot.com/v1.0/pools"
timeout = 60 # minutes

# Logging setup #

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger(sys.argv[0])
logging.getLogger("chardet.charsetprober").disabled = True

############################  

async def workspot(url,headers):
    """ Calling Workspot API `url` with authorization `headers`"""
    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
        async with session.get(url,headers=headers) as response:
            if response.status != 200:
                logger.error("--->Got response [%s] for url: %s", response.status, url)
                sys.exit(2)
            response = await response.read()            
            return response

def get_token(ApiClientPair, Username, Password):
    """ Get authorization token from Workspot API """
    EncodedApiCreds = base64.b64encode(ApiClientPair.encode('ascii'))
    HeaderAuthValue = b"Basic " + EncodedApiCreds
    Headers = { 'Authorization': '{}'.format(HeaderAuthValue.decode('ascii'))}
    logger.debug("-->>Authorization [%s]", Headers["Authorization"])
    url = "https://api.workspot.com/oauth/token" #?grant_type=password
    payload = { # "Content-Type": "x-www-form-urlencoded", grant_type": 'password', "grant_type": 'client_credentials'
        'username': Username,
        'password': Password,
        'Content-Type': 'x-www-form-urlencoded',
        'grant_type': 'password'
        }  
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)     
    ApiReturn = requests.post(url, data=payload, headers=Headers, verify=False) #,auth=HTTPBasicAuth(WsControlUser, WsControlPass)
    ApiToken = json.loads(ApiReturn.content)["access_token"]
    logger.info("--->Got token [%s]", ApiToken)
    return { "Authorization": ("Bearer "+ ApiToken), 'Content-Type': 'application/json'}

def get_pools(j):
    """ Parse desktop pools id """
    #logger.info("--->desktopPools:")
    id = []
    for i in j["desktopPools"]:
        logger.info(('--->{0:<20} {1:<3} {2:<20} {3:<30}'.format(i["name"],i["usedCount"],i["description"],i["id"])))
        id.append(i["id"])
    return id 

def get_ugxml(j):
    """ Parse users and groups into xml  """
    logger.debug("--->desktops:")
    ipuser, groups = "", ""
    for i in j["desktops"]:
        if i["email"]:
            logger.debug(('--->{0:<20} {1:<3} {2:<20} {3:<30}'.format(i["name"],i["email"],i["ipAddress"],i["status"])))       
            ipuser+="""<entry name="{}" ip="{}" timeout="{}"/>""".format("ws_" + i["poolName"] + "\\" + i["email"].split('@')[0],i["ipAddress"], timeout)  
            groups+="""<entry name="{}"/>""".format("WS\\" + i["email"].split('@')[0]) 
    groups="""<entry name="{}"><members>{}</members></entry>""".format("ws_"+i["poolName"], groups)                
    return ipuser, groups  

def panuserid(panapi, panhost, xml):
    try:
        xapi = pan.xapi.PanXapi(api_key=panapi, hostname=panhost)
    except pan.xapi.PanXapiError as msg:
        logger.error(f"--->{msg}")
        sys.exit(1)
    xpath = "/api/"
    try:
        xapi.user_id(cmd=xml, vsys=None)
    except pan.xapi.PanXapiError as msg:
        logger.error(f"--->{msg}")
        sys.exit(1)
    logger.info(f"--->userid to {panhost} applied")

def set_user(ipuser, timeout):
    uid_xml = """
    '''<uid-message>
    <type>update</type>
    <payload>
        <login>
        {}
        </login>
    </payload>
    </uid-message>'''
    """.format(ipuser, timeout)
    return uid_xml    
    
def set_group(group):
    uid_xml = """
    '''<uid-message>
  <type>update</type>
  <payload>
    <groups>
      {}
    </groups>
  </payload>
</uid-message>'''
    """.format(group)
    return uid_xml    
    
    
async def main(url, Headers): 
    #res = await asyncio.gather(workspot(url, Headers))  
    res = await asyncio.gather(*(workspot(url, Headers) for url in urls))
    return res 
    
if __name__ == "__main__":
    import time, yaml
    from itertools import chain

    assert sys.version_info >= (3, 7), "Script requires Python 3.7+."
    with open("config.yaml", 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            logger.info(f"--->{config}")
        except yaml.YAMLError as exc:
            logger.error(f"--->{exc}")
    ApiClientPair = config[0]["ApiClientId"] + ':' + config[1]["ApiClientSecret"]
    Username = config[2]["WsControlUser"],
    Password = config[3]["WsControlPass"],

    Headers = get_token(ApiClientPair, Username, Password)
    urls = [URL]
    start = time.perf_counter()
    r = asyncio.run(main(urls, Headers))
    id = list(chain.from_iterable([get_pools(json.loads(j)) for j in r])) # flatten list
    logger.info(f"--->{id}")
    userid = []
    urls.pop(0) 
    [urls.append(URL+'/'+i+'/desktops') for i in id]   
    r = asyncio.run(main(urls, Headers))    
    for j in r:
        user, group = get_ugxml(json.loads(j))
        logger.debug(f"--->{user}\n{group}")
        xml_user = set_user(user, 3600)
        xml_group = set_group(group)
        #logger.debug(f"--->{config[5]["Firewalls"]}")
        for i in config[5]["Firewalls"]:
            panuserid(config[4]["PanApi"],i, xml_user)
            panuserid(config[4]["PanApi"],i, xml_group)
    end = time.perf_counter() - start
    logger.info(f"--->finished in {end:0.2f} seconds.")
    
   
                

