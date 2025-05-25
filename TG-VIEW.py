import os, sys, time, urllib, threading
from os import system as execute
from threading import active_count
from os import system as none
#none('xdg-open https://t.me/DARKTEAM_HSNX9  ')
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
    except Exception as error:
        return False

    headers_one = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,fa;q=0.8,de;q=0.7",
        "Connection": "keep-alive",
        "Content-Length": "5",
        "Content-type": "application/x-www-form-urlencoded",
        "Cookie": session_cookie,
        "Host": "t.me",
        "Origin": "https://t.me",
        "Referer": "https://t.me/" + channel_name + "/" + message_id + "?embed=1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Chrome"
    }
    data_one = {
        "_rl": "1"
    }
    try:
        post_response = session.post('https://t.me/' + channel_name + '/' + message_id + '?embed=1', json=data_one, headers=headers_one, proxies=proxy_settings)
        view_key = post_response.text.split('data-view="')[1].split('"')[0]
        current_view = post_response.text.split('<span class="tgme_widget_message_views">')[1].split('</span>')[0]
        if "K" in current_view:
            current_view = current_view.replace("K", "00").replace(".", "")
    except Exception as error:
        return False

    headers_two = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,fa;q=0.8,de;q=0.7",
        "Connection": "keep-alive",
        "Cookie": session_cookie,
        "Host": "t.me",
        "Referer": "https://t.me/" + channel_name + "/" + message_id + "?embed=1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Chrome",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        validation_response = session.get('https://t.me/v/?views=' + view_key, timeout=10, headers=headers_two, proxies=proxy_settings)
        if validation_response.text == "true":
            print(f'[😎🤟️]\x1b[38;5;46m𝐓𝐆_𝐕𝐈𝐄𝐖_𝐒𝐔𝐂𝐂𝐄𝐒𝐒-𝐅𝐔𝐋𝐋𝐘_𝐒𝐄𝐍𝐃👉: ' + current_view)
    except Exception as error:
        return False

    headers_three = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,fa;q=0.8,de;q=0.7",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": session_cookie,
        "Host": "t.me",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Chrome"
    }
    try:
        session.get("https://t.me/" + channel_name + "/" + message_id, headers=headers_three, timeout=10, proxies=proxy_settings)
    except Exception as error:
        return False

def fetch_proxies():
    try:
        https_proxies = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=https&timeout=0", proxies=urllib.request.getproxies(), timeout=5).text
        http_proxies = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=0", proxies=urllib.request.getproxies(), timeout=5).text
        hsnx9_proxies = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=hsnx95&timeout=0", proxies=urllib.request.getproxies(), timeout=5).text
    except Exception as error:
        print(error)
        return False
    with open("/sdcard/proxies.txt", "w") as proxy_file:
        proxy_file.write(https_proxies + "\n" + http_proxies)
    with open("/sdcard/hsnx9.txt", "w") as hsnx9_file:
        hsnx9_file.write(hsnx9_proxies)

def verify_proxy(proxy):
    proxy_settings = {
        'http': proxy,
        'https': proxy,
    }

    try:
        execute_view(proxy)
    except Exception as error:
        return False

def initiate():
    proxy_result = fetch_proxies()
    if proxy_result == False:
        return
    with open('/sdcard/proxies.txt', 'r') as proxy_list:
        proxies = proxy_list.readlines()
    for proxy in proxies:
        proxy = proxy.strip()
        if not proxy:
            continue
        while active_count() > max_threads:
            pass
        proxy_thread = threading.Thread(target=verify_proxy, args=(proxy,))
        task_threads.append(proxy_thread)
        proxy_thread.start()

    with open('/sdcard/hsnx9.txt', 'r') as hsnx9_list:
        proxies = hsnx9_list.readlines()
    for proxy in proxies:
        proxy = proxy.strip()
        if not proxy:
            continue
        while active_count() > max_threads:
            pass
        hsnx9_proxy = "hsnx9://" + proxy
        proxy_thread = threading.Thread(target=verify_proxy, args=(hsnx9_proxy,))
        task_threads.append(proxy_thread)
        proxy_thread.start()
    return True

def execute_process(keep_running: bool = False):
    if keep_running:
        while True:
            initiate()
    else:
        initiate()

execute_process(True)
