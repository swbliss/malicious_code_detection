import requests
import json

API_KEY = 'AIzaSyDMDbGHtlbv2O1vpQwpd7cx3SRgVnokxPk'
headers = { 'content-type': 'application/json' }
data = {
  "client": {
    "clientId":      "yourcompanyname",
    "clientVersion": "1.5.2"
  },
  "threatInfo": {
    "threatTypes":      ["MALWARE", "SOCIAL_ENGINEERING"],
    "platformTypes":    ["WINDOWS"],
    "threatEntryTypes": ["URL"],
    "threatEntries": [
    ]
  }
}
request_url = 'https://safebrowsing.googleapis.com/v4/threatMatches:find?key='\
                 + API_KEY


def request_helper(benign_checker, data, url_batch, f):
  r = requests.post(request_url, headers=headers, data=json.dumps(data))
  r_json = r.json() 
  if 'matches' in r_json:
    for match in r_json['matches']:
      threat_url = match['threat']['url']
      if benign_checker:
        if threat_url in url_batch:
          url_batch.remove(threat_url)
      else:
        url_batch.append(threat_url)
  for url in url_batch:
    f.write(url)


'''
In order to improve the quality of benign/malicious samples, this function
checks whether the urls from original dataset are really benign or malicious.

Args
benign_checker: True for checking benign, False for malicious URL datset.
'''
def check_dataset(benign_checker):
  f = None
  f_qualified = None
  
  if benign_checker:
    f = open('data/alexatop_1m')
    f_qualified = open('data/alexatop_1m_qualified', 'w')
  else:
    f = open('data/hosts')
    f_qualified = open('data/hosts_qualified', 'w')
  url_batch = []    # For benign checker, this is filled with urls first and 
                    # not qualified urls are deleted from the result of request.
                    # Otherwise, for malicious checker, it remains empty and 
                    # will be fiiled with result of request.
  batch_count = 0   # safebrowsing allow 500 url entries at most.

  while True:
    url = f.readline()
    if not url: break
    batch_count += 1
    if benign_checker: url_batch.append(url)
    data['threatInfo']['threatEntries'].append({'url': url}) 
    if batch_count%500 == 0:
      request_helper(benign_checker, data, url_batch, f_qualified)
      print('.', end='', flush=True)
      batch_count = 0
      url_batch = []         
      data['threatInfo']['threatEntries'] = []

  if batch_count != 0:
    request_helper(benign_checker, data, url_batch, f_qualified)

  f.close()
  f_qualified.close()


if __name__=='__main__':
  check_dataset(True)
  check_dataset(False)

