import os
import sys
import time
import requests
from colorama import *
from datetime import datetime
from urllib.parse import unquote

merah = Fore.LIGHTRED_EX
kuning = Fore.LIGHTYELLOW_EX
hijau = Fore.LIGHTGREEN_EX
hitam = Fore.LIGHTBLACK_EX
biru = Fore.LIGHTBLUE_EX
putih = Fore.LIGHTWHITE_EX
reset = Style.RESET_ALL


class PocketfiTod:
    def __init__(self):
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Host": "rubot.pocketfi.org",
            "Origin": "https://pocketfi.app",
            "Referer": "https://pocketfi.app/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
            "sec-ch-ua": '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
        }
        self.line = putih + "~" * 50

    def next_claim_is(self, last_claim):
        next_claim = last_claim + 3600
        now = datetime.now().timestamp()
        tetod = round(next_claim - now)
        return tetod
    
    def http(self,url,headers,data=None):
        while True:
            try:
                if data is None:
                    res = requests.get(url,headers=headers)
                    open("http.log","a",encoding="utf-8").write(f"{res.text}\n")
                    return res
                
                if data == "":
                    res = requests.post(url,headers=headers)
                    open("http.log","a",encoding="utf-8").write(f"{res.text}\n")
                    return res
                
                res = requests.post(url,headers=headers,data=data)
                open("http.log","a",encoding="utf-8").write(f"{res.text}\n")
                return res
            
            except (requests.exceptions.Timeout,requests.exceptions.ConnectionError):
                self.log(f'{merah}connection error / connection timeout !')
                time.sleep(1)
                continue

    def countdown(self, t):
        while t:
            menit, detik = divmod(t, 60)
            jam, menit = divmod(menit, 60)
            jam = str(jam).zfill(2)
            menit = str(menit).zfill(2)
            detik = str(detik).zfill(2)
            print(f"{putih}waiting until {jam}:{menit}:{detik} ", flush=True, end="\r")
            t -= 1
            time.sleep(1)
        print("                          ", flush=True, end="\r")

    def log(self,msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f'{hitam}[{now}] {reset}{msg}')

    def get_user_mining(self,tg_data):
        url = 'https://rubot.pocketfi.org/mining/getUserMining'
        url_claim = 'https://rubot.pocketfi.org/mining/claimMining'
        headers = self.headers.copy()
        headers['telegramRawData'] = tg_data
        res = self.http(url,headers)
        if len(res.text) <= 0:
            self.log(f'{merah}failed get resopnse, 0 length response !')
            return 60
        balance = res.json()['userMining']['gotAmount']
        last_claim = res.json()['userMining']['dttmLastClaim'] / 1000
        self.log(f'{hijau}balance : {putih}{balance}')
        can_claim = self.next_claim_is(last_claim)
        if can_claim >= 0:
            self.log(f'{kuning}not time to claim !')
            return can_claim
        
        res = self.http(url_claim,headers,'')
        if len(res.text) <= 0:
            self.log(f'{merah}failed get response, 0 length response !')
            return 60
        new_balance = res.json()['userMining']['gotAmount']
        self.log(f'{hijau}balance after claim : {putih}{new_balance}')
        return 3600
    
    def main(self):
        banner = f"""
    {hijau}Auto Claim {putih}Pocketfi Bot {hijau}Telegram Every 1 Hour
    
    {putih}By : {hijau}t.me/AkasakaID
    {putih}Github : {hijau}@AkasakaID
    
        """
        arg = sys.argv
        if "marinkitagawa" not in arg:
            os.system("cls" if os.name == "nt" else "clear")
        print(banner)
        datas = open("data.txt","r").read().splitlines()
        if len(datas) <= 0:
            self.log(f"{merah}add data account in data.txt first !")
            sys.exit()
        self.log(f'{hijau}account detected : {putih}{len(datas)}')
        print(self.line)
        while True:
            list_countdown = []
            _start = int(time.time())
            for no,data in enumerate(datas):
                self.log(f"{hijau}account number : {putih}{no + 1}/{len(datas)}")
                res = self.get_user_mining(data)
                print(self.line)
                list_countdown.append(res)
                self.countdown(5)
            _end = int(time.time())
            _tot = _end - _start
            _min = min(list_countdown)
            
            if (_min - _tot) <= 0:
                continue
            
            self.countdown(_min - _tot)
            

if __name__ == "__main__":
    try:
        PocketfiTod().main()
    except KeyboardInterrupt:
        sys.exit()