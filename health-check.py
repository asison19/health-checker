import signal
import sys
import time

import requests
import yaml

# Gracefully handle SIGTERM and SIGINT.
def gracefully_exit(sig, frame):
    print ("Exiting...")
    sys.exit(0)
signal.signal(signal.SIGTERM, gracefully_exit)
signal.signal(signal.SIGINT, gracefully_exit)

# Configurable sleep amount in seconds between test cycles.
# TODO check for negatives.
try:
    sleep_amount = int(sys.argv[2])
except IndexError: 
    sleep_amount = 15

# Get the input yaml file.
try:
    input = open(sys.argv[1])
except IndexError:
    print("No input file given. Now exiting...")
    sys.exit(0)

# Normalize the input yaml.
try:
    data = yaml.safe_load(input)
except yaml.YAMLError as e:
    print("Invalid input file\n", e)
    sys.exit(1)

# Make the success count a hashmap where,
#     key: url, if the URL is the same it shouldn't have to be pinged multiple times.
#     value: list, where the first element is the number of successful checks, and the second is unsuccessful checks.
# TODO rolling window
success_count = {}
for item in data:
    success_count[item["url"]] = [0,0]

# Health endpoint test Cycling
# TODO breakdown into functions.
while True:
    output_strings = []
    for item in data:
        # If http method is not given, assume GET
        if "method" in item:
            m = item["method"]
        else:
            m = "GET"

        url = None
        if "url" in item:
            url = item["url"]
        else:
            break

        headers = None
        body = None
        if "headers" in item:
            headers = item["headers"]
        if "body" in item:
            body = item["body"]
        
        # Check the URLs
        response = None
        if m == "GET":
            response = requests.get(url=url, headers=headers)
        elif m == "POST":
            response = requests.post(url=url, headers=headers, data=body)
        elif m == "HEAD":
            response = requests.head(url=url, headers=headers, data=body)

        # Determine if successful response or not.
        is_up = None
        latency_ms = round(response.elapsed.total_seconds() * float(1000))
        if response.status_code >= 200 and response.status_code < 300 and latency_ms < 500:
            is_up = True
            success_count[url][0] += 1
        else:
            is_up = False
            success_count[url][1] += 1

        name = item["name"]
        print(f"Endpoint with name {name} has HTTP response code {response.status_code} and response latency {latency_ms}ms. => {'UP' if is_up else 'DOWN (response latency is not less than 500 ms)'}")
        
        successful = success_count[url][0]
        unsuccessful = success_count[url][1]
        total = successful + unsuccessful
        percent_success = round(successful / total) * 100
        output_strings.append(f"{url} has {percent_success}% availability percentage")

    for str in output_strings:
        print(str)
    print()

    time.sleep(sleep_amount)
