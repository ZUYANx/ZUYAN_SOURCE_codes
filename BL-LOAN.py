import requests
import string 
import json

URL='http://portal.ncnd.banglalink.com.bd/sp/dataplan?p=01976485461'
headers = {
  "Host": "portal.ncnd.banglalink.com.bd",
  "Connection": "keep-alive",
  "User-Agent": "Mozilla/5.0 (Linux; Android 13; 21061119AG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36",
  "X-Requested-With": "XMLHttpRequest",
  "Accept": "*/*",
  "Referer": "http://portal.ncnd.banglalink.com.bd/nd/?time_stamp=1746163066299&uid=i0DcDpCAFuFsz3BINA%3D%3D",
  "Accept-Encoding": "gzip, deflate",
  "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
  "Cookie": "conn=3g; _viewed_b=29953%2C28451%2C34353%2C33402%2C33404%2C33405%2C33944%2C28449%2C28450%2C29729%2C32384%2C32325%2C26580%2C31540%2C28484%2C28441%2C28456%2C29732%2C29734%2C29733%2C29735"
}
req = requests.get(URL, headers=headers).json()
print(req)



