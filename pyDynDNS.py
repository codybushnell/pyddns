from ddnsHelper import *
import json

settings = ReadSettings('settings.json')

current_ip = GetComcastIP(settings["router"]["routerIP"],
                          settings["router"]["user"],
                          settings["router"]["password"])

dns_ip = GetHomeARecord(settings["hosting"]["apikey"], settings["hosting"]["home_url"])

if dns_ip != current_ip:
    # delete old record
    delete_result = DeleteHomeARecord(settings["hosting"]["apikey"], settings["hosting"]["home_url"], dns_ip)
    # add new record
    add_result = AddHomeARecord(settings["hosting"]["apikey"], settings["hosting"]["home_url"], current_ip)