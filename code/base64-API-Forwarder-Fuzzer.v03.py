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
    'Host': 'www.target.com',
    'Accept': 'application/json',
    'Origin': 'https://www.target.com',
    'Authorization': 'Basic',
    'User-Agent': 'divisionzero2025',
    'Content-Type': 'application/json',
    'Referer': 'https://www.target.com/login',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive'
}

print(f"{bcolors.RED}\n USAGE: {bcolors.ENDC}")
print("\nFuzz-API-Forwarder.py payloads.txt\n")
print(f"The string {bcolors.RED}FUZZER{bcolors.ENDC} marks the injection point in the 'uri' field.\n")

# Read payloads from file
try:
    input_payload_file = sys.argv[1]
    with open(input_payload_file, 'r') as file:
        payloads = [line.strip() for line in file.readlines()]
except IndexError:
    print(f"{bcolors.FAIL}Error: Missing input payload file argument!{bcolors.ENDC}")
    sys.exit(1)
except FileNotFoundError:
    print(f"{bcolors.FAIL}Error: File '{sys.argv[1]}' not found!{bcolors.ENDC}")
    sys.exit(1)

# Base JSON template with FUZZER as a placeholder for the injected wordlist

raw_post_data_template = """{"id":"MzI5OTc2ODIvR2V0RmVhdHVyZVN3aXRjaGVz","uri":"/api/FUZZER?Z=X","httpMethod":"get"}"""  


# Loop through each payload
for count, injected_payload in enumerate(payloads, start=1):
    print(f"{bcolors.RED} INJECTING PAYLOAD {count}: FUZZER replaced with {injected_payload}{bcolors.ENDC}")

    # Replace "FUZZER" in the JSON template
    raw_post_data = raw_post_data_template.replace("FUZZER", injected_payload)

    # Print Raw Data
    print(f"{bcolors.OKCYAN}[i] Injected Raw POST Data {bcolors.ENDC}")
    print(raw_post_data, "\n")

    # Encode to Base64
    payload_bytes = raw_post_data.encode('utf-8')
    base64_payload = base64.b64encode(payload_bytes).decode('utf-8')

    print(f"{bcolors.OKGREEN}[i] Base64 Payload {bcolors.ENDC}")
    print(base64_payload, "\n")

    # Update Content-Length dynamically
    headers['Content-Length'] = str(len(base64_payload))

    # Send request via Burp Suite Proxy
    try:
        response = requests.post(
            'https://www.target.com/api/forwarder',
            headers=headers,
            data=base64_payload,
            proxies=listproxies,
            verify=False
        )

        # Output response details
        print(f"{bcolors.OKGREEN}[o] Response Status Code: {response.status_code}{bcolors.ENDC}")
        print(f"{bcolors.OKGREEN}[o] Response Headers: {bcolors.ENDC}")
        print(response.headers, "\n")

        print(f"{bcolors.WARNING}[o] Response JSON: {bcolors.ENDC}")
        try:
            pretty_json = json.dumps(response.json(), indent=4)
            print(pretty_json)
        except ValueError:
            print("Warning: Response is not valid JSON.")

    except requests.RequestException as e:
        print(f"{bcolors.FAIL}Error: HTTP request failed - {e}{bcolors.ENDC}")

    print(f"{bcolors.ENDC}")
    time.sleep(1)  # Pause to prevent rate limiting
