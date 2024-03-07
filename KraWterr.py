import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from colorama import Fore, Back, Style

def check_sql_injection(url, params):
    try:
        response = requests.get(url, params=params)
        if "SQL syntax" in response.text:
            return True
    except requests.RequestException as err:
        print(f"{Fore.RED}HTTP isteği başarısız oldu. Hata: {err}")
    return False

def crawl_and_check_sql_injection(url, depth=3, params=None):
    visited = set()
    to_visit = [(url, 0)]
    sql_vulnerable_urls = []

    print(f"{Fore.YELLOW}SQL taraması başlatılıyor...")

    while to_visit:
        current_url, current_depth = to_visit.pop(0)
        print(f"{Fore.CYAN}Taranan URL: {current_url}")

        if current_url in visited:
            print(f"{Fore.YELLOW}[Ziyaret Edildi]")
            continue

        visited.add(current_url)

        try:
            response = requests.get(current_url)
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
                            print(f"{Fore.GREEN}[✓] Potansiyel SQL açığı bulundu.")
                            break

                if current_depth < depth:
                    links = soup.find_all("a", href=True)
                    for link in links:
                        absolute_link = urljoin(current_url, link["href"])
                        to_visit.append((absolute_link, current_depth + 1))

            else:
                print(f"{Fore.RED}[Başarısız]")
        except requests.RequestException as err:
            print(f"{Fore.RED}[Başarısız]")
            print(f"{Fore.RED}HTTP isteği başarısız oldu. Hata: {err}")

    return sql_vulnerable_urls

def save_results(sql_vulnerable_urls):
    if not sql_vulnerable_urls:
        return

    with open("sql_vulnerabilities.txt", "w") as file:
        file.write("Potansiyel SQL Enjeksiyonu Bulunan URL'ler:\n")
        for url in sql_vulnerable_urls:
            file.write(f"{url}\n")

def center_text(text, width=80):
    padding = (width - len(text)) // 2
    return " " * padding + text

def show_menu():
    print("\nSeçenekler:")
    print("1. Yeni URL girmek")
    print("2. Çıkış")
    choice = input("Lütfen seçiminizi yapın: ")
    return choice

def print_welcome():
    welcome_art = """
      *******               ***     
    *       ***              ***    
   *         **               **    
   **        *                **    
    ***             ****      **    
   ** ***          * ***  *   **    
    *** ***       *   ****    **    
      *** ***    **    **     **    
        *** ***  **    **     **    
          ** *** **    **     **    
           ** ** **    **     **    
            * *  **    **     **    
  ***        *    *******     **    
 *  *********      ******     *** * 
*     *****            **      ***  
*                      **           
 **                    **           
                        **          
                                    
                                    """
    print(Fore.BLUE + welcome_art + Style.RESET_ALL)
    print(f"\n{Fore.MAGENTA}Hata, soru, öneri için: [https://t.me/weertyyyy]\n")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print_welcome()

    start_url = input(f"{Fore.YELLOW}Lütfen başlangıç URL'sini girin: ")
    sql_vulnerable_urls = crawl_and_check_sql_injection(start_url)
    if sql_vulnerable_urls:
        print(f"{Fore.GREEN}Potansiyel SQL enjeksiyonu bulunan URL'ler:")
        for url in sql_vulnerable_urls:
            print(f"{Fore.GREEN}  - [ {url} ]")
        save_results(sql_vulnerable_urls)
        print(f"{Fore.YELLOW}Sonuçlar 'sql_vulnerabilities.txt' dosyasına kaydedildi.")
    else:
        print(f"{Fore.RED}Şansız bir URL...")

    while True:
        choice = show_menu()
        if choice == "1":
            os.system('cls' if os.name == 'nt' else 'clear')
            print_welcome()
            start_url = input(f"{Fore.YELLOW}Lütfen başlangıç URL'sini girin: ")
            sql_vulnerable_urls = crawl_and_check_sql_injection(start_url)
            if sql_vulnerable_urls:
                print(f"{Fore.GREEN}Potansiyel SQL enjeksiyonu bulunan URL'ler:")
                for url in sql_vulnerable_urls:
                    print(f"{Fore.GREEN}  - [ {url} ]")
                save_results(sql_vulnerable_urls)
                print(f"{Fore.YELLOW}Sonuçlar 'sql_vulnerabilities.txt' dosyasına kaydedildi.")
            else:
                print(f"{Fore.RED}Şansız bir URL...")
            continue
        elif choice == "2":
            print("Programdan çıkılıyor...")
            break
        else:
            print("Geçersiz seçim. Lütfen tekrar deneyin.")
