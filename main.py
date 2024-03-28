from colorama import Style, Fore, init
from requests import get, exceptions
from time import strftime
from random import randint
from threading import Thread

white   = Style.BRIGHT + Fore.WHITE
magenta = Style.BRIGHT + Fore.MAGENTA
red     = Style.BRIGHT + Fore.RED
green   = Style.BRIGHT + Fore.GREEN
blue    = Style.BRIGHT + Fore.BLUE
yellow  = Style.BRIGHT + Fore.YELLOW

links = []

def analyzer(url, filename):
    req = request(url, filename)
    if type(req) != exceptions.ConnectionError:
        if filename in req.text:
            number1 = len(ireq.text) - len(ireq.url.replace(url,""))
            number2 = len(req.text) - len(filename) 

            if number1 != number2 and number2 != 0:
                success(f"{req.url} {magenta}Zafiyetli", str(req.status_code), str(len(req.text)))
                
            else:
                success(req.url, str(req.status_code), str(len(req.text)))
        else:
            if len(req.text) != len(ireq.text) and len(req.text) != 0:
                success(f"{req.url} {magenta}Zafiyetli", str(req.status_code), str(len(req.text)))
            else:
                success(req.url, str(req.status_code), str(len(req.text)))

def request(url, filename):
    try:
        return get(url + filename, headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0"
        }, allow_redirects=False)
    except Exception as e:
        return e

def ask(message):
    print(f"{magenta}[{strftime('%d.%m.%y %X')}] {white}{message}: {magenta}", end="")
    return input()

def success(message, status_code, content_lenght):
    print(f"{green}[{strftime('%d.%m.%y %X')}] {yellow}[SC: {status_code}] [CL: {content_lenght}] {white}{message}")

def error(message):
    print(f"{red}[{strftime('%d.%m.%y %X')}] {white}{message}")

def info(message):
    print(f"{blue}[{strftime('%d.%m.%y %X')}] {white}{message}")

def main():
    url = ask("Yönetim panelinin bulunduğu dizini girin")
    if "http" not in url:
        error("Geçersiz url girildi.")
        return

    if url[-1:] != "/":
       url += "/"

    global ireq
    ireq = request(url, str(randint(1000,5000)) + ".php")
    if type(ireq) == exceptions.ConnectionError:
        error("Girdiğiniz url adresine ulaşılamıyor.")
        return

    info(f"{white}Durum Kodu: {magenta}{str(ireq.status_code)}{white} / İçerik Uzunluğu:{magenta} {str(len(ireq.text))}")    
    
    filename = ask("Sözlük listesini girin")

    try:
        with open(filename, "r") as file:
            dictionary = file.read().splitlines()
    except FileNotFoundError:
        error("Girdiğiniz dosya adresi bulunamadı.")
        return
    
    info("Tarama işlemi başlamıştır.")

    threads = []
    for filename in dictionary:
        thread = Thread(target=analyzer, args=(url, filename,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
        
    info("Tarama işlemi bitmiştir.")
    

if __name__ == "__main__":
    try:
        init()
        main()
    except KeyboardInterrupt:
        exit()
