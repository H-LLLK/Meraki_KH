import requests
import datetime
import time
import csv
from datetime import date

today = datetime.datetime.now()
a = today + datetime.timedelta(hours=1)
yesterday = a - datetime.timedelta(days=1)
t = time.mktime((a.timetuple()))
y = time.mktime((yesterday.timetuple()))
orgid = ""
api_key = ""


def getnwlist():
    # returns a list of all networks in an organization
    # on failure returns a single record with 'null' name and id
    url = "https://api.meraki.com/api/v0/organizations/%s/networks" % (orgid)
    response = requests.get(url=url, headers={'X-Cisco-Meraki-API-Key': api_key, 'Content-Type': 'application/json'})
    return response



def getdata(id):
    url = "https://api.meraki.com/api/v0/networks/{}/connectionStats?t0={}&t1={}".format(id, y, t)
    response = requests.get(url=url, headers={'X-Cisco-Meraki-API-Key': api_key, 'Content-Type': 'application/json'})
    return response.json()



def main():
    response = getnwlist()
    networks = response.json()

    with open(str(date.today()) + '.csv', 'w', newline='') as f:
        fieldnames = ['Site', 'Association', 'Authentication', 'DHCP', 'DNS', 'Total Failed Connections', 'Success', 'Failed(%)']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for get_id in networks:
            id = get_id['id']
            Data = getdata(id)
            site = get_id['name']

            if Data == None:
                pass
            elif 'assoc' in Data:
                str(site)
                print(Data)
                Total = Data['assoc'] + Data['auth'] + Data['dhcp'] + Data['dns'] + Data['success']
                failed = Data['assoc'] + Data['auth'] + Data['dhcp'] + Data['dns']
                PC = failed/Total * 100
                f.write('%s,%s,%s,%s,%s,%s,%s,%s\n' % (site, Data['assoc'], Data['auth'], Data['dhcp'], Data['dns'], failed, Data['success'], PC))


    print('Complted  ' + str(date.today()))

main()
