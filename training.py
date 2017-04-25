
import configparser
import requests, logging, json, sys
from akamai.edgegrid import EdgeGridAuth
import urllib
import json
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-groups", help="Understand groups", action="store_true")
parser.add_argument("-propertyList", help="Understand property list", action="store_true")
parser.add_argument("-individualProperty", help="Understand property list", action="store_true")
parser.add_argument("-propname", help="property Name")

args = parser.parse_args()



try:
    print('Establishing Connection')
    config = configparser.ConfigParser()
    config.read('config_MSCI.txt')
    client_token = config['CREDENTIALS']['client_token']
    client_secret = config['CREDENTIALS']['client_secret']
    access_token = config['CREDENTIALS']['access_token']
    access_hostname = config['CREDENTIALS']['access_hostname']
    session = requests.Session()
    response = session.auth = EdgeGridAuth(
    			client_token = client_token,
    			client_secret = client_secret,
    			access_token = access_token
                )
    print('Connection Established')
except (NameError,AttributeError):
    print("\nUse -h to know the options to run program\n")
    exit()

if args.groups:
    groupUrl = 'https://' + access_hostname + '/papi/v0/groups/'
    groupResponse = session.get(groupUrl)
    if groupResponse.status_code == 200:
        #print(dir(groupResponse))
        #print(groupResponse.status_code)
        print(groupResponse.text)
        #print(json.dumps(groupResponse.json(), indent = 4))
    else:
        print(dir(groupResponse))

if args.propertyList:
    groupUrl = 'https://' + access_hostname + '/papi/v0/groups/'
    groupResponse = session.get(groupUrl)
    if groupResponse.status_code == 200:
        for eachDataGroup in groupResponse.json()['groups']['items']:
            try:
                contractIdList = eachDataGroup['contractIds']
                for contractId in contractIdList:
                    groupId = eachDataGroup['groupId']
                    url = 'https://' + access_hostname + '/papi/v0/properties/?contractId=' + contractId +'&groupId=' + groupId
                    print('-----------------------------------------\n\n\n\n\n')
                    propertiesResponse = session.get(url)
                    if propertiesResponse.status_code == 200:
                        print(json.dumps(propertiesResponse.json(), indent = 4))
            except KeyError:
                pass
    else:
        print(dir(groupResponse))

if args.individualProperty:
    groupUrl = 'https://' + access_hostname + '/papi/v0/groups/'
    groupResponse = session.get(groupUrl)
    if groupResponse.status_code == 200:
        for eachDataGroup in groupResponse.json()['groups']['items']:
            try:
                contractIdList = eachDataGroup['contractIds']
                for contractId in contractIdList:
                    groupId = eachDataGroup['groupId']
                    url = 'https://' + access_hostname + '/papi/v0/properties/?contractId=' + contractId +'&groupId=' + groupId
                    propertiesResponse = session.get(url)
                    if propertiesResponse.status_code == 200:
                        propertiesResponseJson = propertiesResponse.json()
                        propertiesList = propertiesResponseJson['properties']['items']
                        for propertyInfo in propertiesList:
                            propertyName = propertyInfo['propertyName']
                            propertyId = propertyInfo['propertyId']
                            propertyContractId = propertyInfo['contractId']
                            propertyGroupId = propertyInfo['groupId']
                            property_name = args.propname
                            if propertyName == property_name or propertyName == property_name + ".xml":
                                #Update the self attributes with correct values
                                print('Property Name: ' + propertyName)
                                print('Property ID: ' + propertyId)
                                print('Contract ID: ' + propertyContractId)
                                print('Group ID: ' + propertyGroupId)
                                #HARDCODING the version for now
                                rulesUrl = 'https://' + access_hostname  + '/papi/v0/properties/' + propertyId +'/versions/'+str(1)+'/rules/?contractId='+ propertyContractId +'&groupId='+ propertyGroupId
                                rulesResponse = session.get(rulesUrl)
                                if rulesResponse.status_code == 200:
                                    print(json.dumps(rulesResponse.json()))
                                    break
                                else:
                                    print('Failure')
            except KeyError:
                pass
    else:
        print(dir(groupResponse))
