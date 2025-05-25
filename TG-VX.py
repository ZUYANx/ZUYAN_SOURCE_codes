import os, sys, time, urllib, threading
from os import system as execute
from threading import active_count

# Optional system open disabled
# execute('xdg-open https://t.me/DARKTEAM_HSNX9')

# Simple introduction
print("TELEGRAM POST VIEW BOT BY MR ZUYAN")
print("This script sends views to your Telegram post using proxies.\n")

try:
    import requests
except:
    os.system('pip install requests')
    import requests

max_threads = 400
task_threads = []

post_link = input(f'\x1b[38;5;46m𝐄𝐍𝐓𝐀𝐑 𝐘𝐎𝐔𝐑 𝐓𝐆 𝐏𝐎𝐒𝐓 𝐋𝐈𝐍𝐊 : ')

def execute_view(proxy):
    channel_name = post_link.split('/')[3]
    message_id = post_link.split('/')[4]
    send_view_request(channel_name, message_id, proxy)

def send_view_request(channel_name, message_id, proxy):
    session = requests.Session()
    proxy_settings = {
        'http': proxy,
        'https': proxy,
    }
    try:
        response = session.get("https://t.me/" + channel_name + "/" + message_id, timeout=10, proxies=proxy_settings)
        session_cookie = response.headers['set-cookie'].split(';')[0]
    except:
        return False

    headers_one = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "5",
        "Content-type": "application/x-www-form-urlencoded",
        "Cookie": session_cookie,
        "Host": "t.me",
        "Origin": "https://t.me",
        "Referer": "https://t.me/" + channel_name + "/" + message_id + "?embed=1",
        "User-Agent": "Chrome"
    }

    data_one = {"_rl": "1"}
    try:
        post_response = session.post('https://t.me/' + channel_name + '/' + message_id + '?embed=1', json=data_one, headers=headers_one, proxies=proxy_settings)
        view_key = post_response.text.split('data-view="')[1].split('"')[0]
        current_view = post_response.text.split('<span class="tgme_widget_message_views">')[1].split('</span>')[0]
        if "K" in current_view:
            current_view = current_view.replace("K", "00").replace(".", "")
    except:
        return False

    headers_two = {
        "Accept": "*/*",
        "Cookie": session_cookie,
        "Referer": "https://t.me/" + channel_name + "/" + message_id + "?embed=1",
        "User-Agent": "Chrome",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        validation_response = session.get('https://t.me/v/?views=' + view_key, timeout=10, headers=headers_two, proxies=proxy_settings)
        if validation_response.text == "true":
            print(f'[+] VIEW SENT: {current_view}')
    except:
        return False

    headers_three = {
        "Accept": "text/html",
        "Cookie": session_cookie,
        "User-Agent": "Chrome"
    }
    try:
        session.get("https://t.me/" + channel_name + "/" + message_id, headers=headers_three, timeout=10, proxies=proxy_settings)
    except:
        return False

def fetch_proxies():
    try:
        https_proxies = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=https&timeout=0", proxies=urllib.request.getproxies(), timeout=5).text
        http_proxies = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=0", proxies=urllib.request.getproxies(), timeout=5).text
        zuyan_proxies = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4&timeout=0", proxies=urllib.request.getproxies(), timeout=5).text
    except Exception as error:
        print("Error fetching proxies:", error)
        return False
    with open("/sdcard/proxies.txt", "w") as proxy_file:
        proxy_file.write(https_proxies + "\n" + http_proxies)
    with open("/sdcard/zuyan.txt", "w") as zuyan_file:
        zuyan_file.write(zuyan_proxies)

def verify_proxy(proxy):
    proxy_settings = {'http': proxy, 'https': proxy}
    try:
        execute_view(proxy)
    except:
        return False

def initiate():
    if fetch_proxies() == False:
        return
    with open('/sdcard/proxies.txt', 'r') as proxy_list:
        proxies = proxy_list.readlines()
    for proxy in proxies:
        proxy = proxy.strip()
        if not proxy:
            continue
        while active_count() > max_threads:
            pass
        thread = threading.Thread(target=verify_proxy, args=(proxy,))
        task_threads.append(thread)
        thread.start()

    with open('/sdcard/zuyan.txt', 'r') as zuyan_list:
        proxies = zuyan_list.readlines()
    for proxy in proxies:
        proxy = proxy.strip()
        if not proxy:
            continue
        while active_count() > max_threads:
            pass
        thread = threading.Thread(target=verify_proxy, args=(proxy,))
        task_threads.append(thread)
        thread.start()

def execute_process(loop: bool = False):
    if loop:
        while True:
            initiate()
    else:
        initiate()

execute_process(True)