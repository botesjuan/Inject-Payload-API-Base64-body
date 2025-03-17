from burp import IBurpExtender, IContextMenuFactory, IHttpListener
from javax.swing import JMenuItem
import json
import base64
import random
from java.awt import Toolkit
from java.awt.datatransfer import StringSelection
from java.util import List, ArrayList
from javax.swing import JFrame, JPanel, JButton, JTextArea, JScrollPane, JLabel
from java.awt import BorderLayout
import threading

class BurpExtender(IBurpExtender, IHttpListener, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("API Forwarder Fuzzer")
        callbacks.registerHttpListener(self)
        callbacks.registerContextMenuFactory(self)
        self._stdout = callbacks.getStdout()
        self._stdout.write("\n[+] API Forwarder Fuzzer Extension Loaded!\n")
        
    def createMenuItems(self, invocation):
        menu_list = ArrayList()
        menu_item = JMenuItem("Send to API Forwarder Fuzzer", actionPerformed=lambda x: self.sendToFuzzer(invocation))
        menu_list.add(menu_item)
        return menu_list

    def sendToFuzzer(self, invocation):
        http_request = invocation.getSelectedMessages()[0]
        request_info = self._helpers.analyzeRequest(http_request)
        headers = request_info.getHeaders()
        body_bytes = http_request.getRequest()[request_info.getBodyOffset():]
        body = self._helpers.bytesToString(body_bytes)

        if not body:
            self._stdout.write("\n[-] No body found in request!\n")
            return
        
        decoded_body = base64.b64decode(body).decode('utf-8')
        json_data = json.loads(decoded_body)
        
        # Generate new fuzz payload
        random_number = random.randint(578673107, 984364545)
        new_payload = "FUZZ_TEST"  # Placeholder fuzz string
        ID_STRING = f"{random_number}/{new_payload}"
        ID_B64 = base64.b64encode(ID_STRING.encode()).decode()
        json_data['id'] = ID_B64
        json_data['uri'] = f"/api/{new_payload}?userName=targetuser@emailz.zyx"
        
        modified_body = base64.b64encode(json.dumps(json_data).encode('utf-8')).decode()
        new_request = self._helpers.buildHttpMessage(headers, modified_body)
        http_request.setRequest(new_request)
        
        self._stdout.write("\n[+] Modified API Forwarder Request Sent!\n")
        
    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        if messageIsRequest:
            request_info = self._helpers.analyzeRequest(messageInfo)
            url = request_info.getUrl().toString()
            
            if "/api/forwarder" in url:
                body_bytes = messageInfo.getRequest()[request_info.getBodyOffset():]
                body = self._helpers.bytesToString(body_bytes)
                
                if body:
                    decoded_body = base64.b64decode(body).decode('utf-8')
                    json_data = json.loads(decoded_body)
                    
                    # Generate new fuzz payload
                    random_number = random.randint(578673107, 984364545)
                    new_payload = "BURP_FUZZ"  # Placeholder fuzz string
                    ID_STRING = f"{random_number}/{new_payload}"
                    ID_B64 = base64.b64encode(ID_STRING.encode()).decode()
                    json_data['id'] = ID_B64
                    json_data['uri'] = f"/api/{new_payload}?userName=targetuser@emailz.zyx"
                    
                    modified_body = base64.b64encode(json.dumps(json_data).encode('utf-8')).decode()
                    new_request = self._helpers.buildHttpMessage(request_info.getHeaders(), modified_body)
                    messageInfo.setRequest(new_request)
                    
                    self._stdout.write("\n[+] API Forwarder request modified and sent!\n")
