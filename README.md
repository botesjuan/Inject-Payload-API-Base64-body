# Inject Payload API Base64 body

>The target front end API only accpets base64 encoded payload in the POST request to `API/FORWARDER`.  
>This python code inject Payload into API POST body that only accept base64 to determine valid endpoints and parameters.  

## API Penetration Testing  

```
The web or mobile application makes POST requests to the API backend in the base64 encoded body. 
This restricts the simple injection and fuzzing of input parameters to the API endpoint.
The following python script enable the injection of payload wordlists in specific positions to test input validation.  
```  

### Execute the script with input file contain list of payload injections sample on each line.  

>The script direct all request to Burp Suite Proxy for inspection to identify valid results, and filter status code `404 Not Found`.  

```bash
wc -l /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt

python3 ww-api-forwarder-fuzzer-2025-03-15.py /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt
```  

![API Forwarder](/images/2025-03-15_10-36.png)

----  
