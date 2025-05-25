import os
try:
    import requests
except:
    os.system('pip install requests')
import json
import time
import sys
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
#----------------------#
R = "[red]"
O = "[orange]"
Y = "[yellow]"
G = "[green]"
B = "[blue]"
I = "[indigo]"
V = "[violet]"
P = "[purple]"
C = "[cyan]"
M = "[magenta]"
W = "[white]"
#=======bash-colors=====#
r = "\033[0;31m"  
o = "\033[0;33m"  
y = "\033[1;33m"  
g = "\033[0;32m"  
b = "\033[0;34m"  
i = "\033[0;35m"  
v = "\033[1;35m"  
p = "\033[0;35m"  
c = "\033[0;36m"  
m = "\033[1;35m"  
a = "\033[0;37m"  
n = "\033[0m"     
w = "\033[0;37m"
#========settings======#
console = Console()
style='</>'
line=40*f'{W}-'
STORAGE_DIR = "/data/data/com.termux/files/home/storage/shared"
COOKIE_FILE = os.path.join(STORAGE_DIR, ".cookie.txt")
TOKEN_FILE = os.path.join(STORAGE_DIR, ".token.txt")
#=====================#
def show_banner():
    console.print(Panel(f"""
    {style} FACEBOOK : AUTO-BOT
    {style} GITHUB   : ZUYANX
    {style} VERSION  : 1.0
    {style} OWNER    : MR ZUYAN
    """,title="[bold red]FACEBOOK-TOOLS"))
#============================≠=========#
def main():
    os.system('clear')
    show_banner()
    print(f"{style} FB-SHARE-1")
    print(f"{style} FB-RACTION-2")
    print(f"{style} FB-FOLLWER-3")
    print(f"{style} REMOVE-TOKEN-COKI-4")
    print(f"{style} EXIT-00")
    print(line)
    option=input(f"{style} CHOICE : ")
    if option =='1':
        ZUYAN_Share()
    elif option =='2':
        pass
    elif option =='3':
        pass
    elif option =='4':
        remove_data(COOKIE_FILE)
        remove_data(TOKEN_FILE)
        time.sleep(2)
    elif option =='00':
        exit()
    else:
        print(f"{style} {R}WRONG SELECTION !!")
        time.sleep(2)
        main()


def ZUYAN_Login():
    os.system('clear')
    show_banner()
    cookie = input(f"{style} ENTER COOKIES: ").strip()
    print(line)
    token = input(f"{style} ENTER TOKEN: ").strip()
    print(line)
    if not cookie or not token:
        print(f"{style}Cookies and Token are required.")
        time.sleep(2)
        return
    save_data(COOKIE_FILE, cookie)
    save_data(TOKEN_FILE, token)
    print(f"{G}{style} LOGIN SUCCESSFUL")
    print(line)
    time.sleep(2)
    main()
    
def save_data(file_path, data):
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as file:
        file.write(data)

def remove_data(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{style} Removed *_*")
    else:
        print(f"{style} File  does not exist.")
        
        
def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return file.read().strip()
    return None

def parse_cookies(cookie_string):
    cookies = {}
    for part in cookie_string.split(";"):
        if "=" in part:
            key, value = part.strip().split("=", 1)
            cookies[key] = value
    return cookies    
    
def ZUYAN_Share():
    os.system('clear')
    show_banner()
    token = load_data(TOKEN_FILE)
    cookie_string = load_data(COOKIE_FILE)
    if not os.path.exists(COOKIE_FILE) or not os.path.exists(TOKEN_FILE):
        print(f"{R}{style} No token or cookies found. Please login first.")
        time.sleep(2)
        ZUYAN_Login()
    try:
        cookies = parse_cookies(cookie_string)
        user_info = requests.get(f"https://graph.facebook.com/me?fields=name,id&access_token={token}",cookies=cookies).json()
        nama = user_info.get("name")
        user_id = user_info.get("id")
        ip = requests.get("https://api.ipify.org").text
        print(f"{style} YOUR NAME: {nama}")
        print(f"{style} YOUR UID: {user_id}")
        print(f"{style} YOUR IP: {ip}")
        print(line)
        link = input(f"{style} ENTER POST LINK: ").strip()
        print(line)
        limit = int(input(f"{style} ENTER SHARE LIMIT: "))
        print(line)
        header = {
        "authority": "graph.facebook.com",
        "cache-control": "max-age=0",
        "sec-ch-ua-mobile": "?0",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Mobile/15E148 Safari/604.1"}
        for x in range(limit):
            post = requests.post(f"https://graph.facebook.com/v13.0/me/feed?link={link}&published=0&access_token={token}",headers=header,cookies=cookies).json()
            #print(post)
            if "id" in post:
                print(f"{style} Successfully Shared - [{x + 1}]")
            else:
                print(f"(>) Failed To Share! Error: {post.get('error', {}).get('message', 'Unknown error')}")
            print(line)
        print(f"\n{style} Post Share Completed!")
        time.sleep(2)
        main()
    except requests.exceptions.ConnectionError:
        print(f"{style} Internet Connection Error!")
        print(line)
        time.sleep(2)
        main()
    except Exception as e:
        print(f"{style} ERROR: {str(e)}")
        print(f"{style} Something went wrong. Please check your token and try again.")
        print(line)
        time.sleep(2)
        main()

if __name__ == "__main__":
    main()
    
    
