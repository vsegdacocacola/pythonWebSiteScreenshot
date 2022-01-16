from flask import Flask,request,send_file
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
from ipaddress import ip_address, ip_network
from tempfile import NamedTemporaryFile
from time import sleep
import re

app=Flask(__name__)
@app.route('/api/makeScreenshot',methods=['POST'])
def makeScreenshot():
    if request.method=='POST':
        if not request.is_json:
            return {"error" : "invalid request"}
        url = request.json.get("url")
        device = request.json.get("device")

        url_struct = urlparse(url)
        if ( not url_struct.scheme in ["http", "https"] ):
            return {"error" : "invalid url scheme"}
        if ( re.match(r"[^A-Za-z0-9\.\-]+", url_struct.netloc) ):
            return  { "error" : "invalid url" }
        if ( re.match(r"[0-9\.\:]+", url_struct.netloc) ):
            ip = re.sub(r"([0-9\.]+)[\:0-9]*",r"\1", url_struct.netloc)
            try:
                ip = ip_address(ip)
                if(ip in ip_network("192.168.0.0/16") or ip in ip_network("172.16.0.0/12") or ip in ip_network("10.0.0.0/8") or ip in ip_network("127.0.0.0/8")):
                    return { "error" : "invalid host"}
            except Exception as e:
                return { "error" : "invalid host"}
        if( re.match(r"[^A-Za-z0-9\.\/\%\-\+\#]+", url_struct.path )):
            return { "error" : "invalid path" }
        if( re.match(r"[^A-Za-z0-9\.\/\%\-\+\#\&\?]+", url_struct.query )):
            return { "error" : "invalid url query" }

        if not device in ["mobile", "desktop"]:
            device = "desktop"

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        if (device == "mobile"):
            mobile_emulation = { "deviceName": "iPhone X" }
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        else:
            chrome_options.add_argument('--window-size=1920,1080')
        chrome = webdriver.Chrome(chrome_options=chrome_options)
        chrome.get('https://abnamro.nl')
        s = chrome.get_window_size()
        w = chrome.execute_script('return document.body.parentNode.scrollWidth')
        h = chrome.execute_script('return document.body.parentNode.scrollHeight')
        print("Screenshot dimensions: {}x{}".format(w,h))
        chrome.set_window_size(w, h)
        f = NamedTemporaryFile()
        print(f.name)
        chrome.save_screenshot(f.name)
        chrome.quit()
        return send_file(f.name, attachment_filename='screenshot.png')
    return {"error": "invalid request"}

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)
