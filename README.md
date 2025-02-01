# Summary
Simple python script that checks the health of a given set of HTTP endpoints in yaml.

# Setup
Before using the script, make sure the pyyaml and requests packages are installed by doing:
```
pip install pyyaml requests
```
or using the requirments.txt:
```
pip install -r requirements.txt
```

# Usage
To use the script, call it using python, the script name, and then the input file containing the endpoints to check in yaml format.   
Ex: 
```
python .\health-check.py input.yml
```

You can also pass in the test cycle time in seconds by passing in number.  
Ex
```
python .\health-check.py input.yml 1
```

# Example Output
```txt
Endpoint with name Andrew Sison's website has HTTP response code 200 and response latency 142ms. => UP
https://andrewsison.com has 100% availability percentage

Exiting...
```
