import requests
import re
import json
import uuid

def GetComcastIP(routerIP, username, password):
	router_url = "http://" + routerIP

	# login to router
	router_login = requests.post(router_url + "/home_loggedout.php", 
							 data={	
									"username": username, 
									"password": password, 
									"idseed": re.search('name="idseed" value="(.+?)">', 
												requests.get(router_url + "/home_loggedout.php",params={"out": 1}).text, 
												re.DOTALL|re.MULTILINE
												).group(1)
									}
							 )

	# return the ip address in the xfinity network screen
	return re.search('WAN IP Address\(IPv4\):</span>.+?<span class="value">(.+?)</span>', 
				requests.get(router_url + "/comcast_network.php").text, 
				re.DOTALL|re.MULTILINE
				).group(1);

def GetHomeARecord(apikey, url):
    current_dns = json.loads(requests.get("https://api.dreamhost.com", 
                                          params={"key":apikey,
                                                    "cmd":"dns-list_records",
                                                    "unique_id":uuid.uuid1(),
                                                    "format":"json"}).text)['data']

    return [d for d in current_dns if d['record'] == url][0]['value'];

def DeleteHomeARecord(apikey, url, dns_ip):
    return requests.get("https://api.dreamhost.com", 
                                params={"key":apikey,
                                        "cmd":"dns-remove_record",
                                        "unique_id":uuid.uuid1(),
                                        "record":url,
                                        "type":"A",
                                        "value":dns_ip}).text;

def AddHomeARecord(apikey, url, dns_ip):
    return requests.get("https://api.dreamhost.com", 
                                params={"key":apikey,
                                        "cmd":"dns-add_record",
                                        "unique_id":uuid.uuid1(),
                                        "record":url,
                                        "type":"A",
                                        "value":dns_ip}).text;

def ReadSettings(settingsfile):
    with open(settingsfile,'r') as settingsfile:
        return json.loads(settingsfile.read());