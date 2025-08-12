#!/usr/bin/env python3
import requests
import sys
import time
import os
from colorama import init, Fore, Back, Style
from pyfiglet import Figlet
import argparse
from datetime import datetime

# Initialize colorama
init(autoreset=True)

# Constants
API_BASE_URL = "https:example.com"
API_KEY = "example123"
VERSION = "2.0.1"
DEVELOPMENT_TEAM = "Indian Cyber Crime Division"
LEGAL_DISCLAIMER = """
█▀▀ █▀█ █▀▀ █▀▄ █ █▄░█ █▀▀   █▀▀ █░█ █▄░█ █▀▀ █▀ █▀▀ █▀█
█▄▄ █▀▄ ██▄ █▄▀ █ █░▀█ █▄█   █▀░ █▄█ █░▀█ ██▄ ▄█ █▄▄ █▄█

This tool is property of the Government of India
Unauthorized access punishable under IT Act 2000 (Section 43, 66, 69)
"""

class ForensicAnimator:
    @staticmethod
    def print_scanning():
        frames = [
            "🛰️  Scanning Telecom Databases...",
            "📡 Intercepting Signals...",
            "🔍 Cross-Referencing Records...",
            "📊 Analyzing Transactions..."
        ]
        for frame in frames:
            print(Fore.YELLOW + frame, end='\r')
            time.sleep(0.5)
        print()

    @staticmethod
    def print_decrypting():
        for i in range(3):
            print(Fore.BLUE + f"🔓 Decrypting [{'■'*(i+1)}{'□'*(2-i)}]", end='\r')
            time.sleep(0.3)
        print()

def display_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    f = Figlet(font='doom')
    print(Fore.RED + f.renderText('CYBER  CELL'))
    print(Fore.MAGENTA + "▄"*60)
    print(Fore.BLUE + f"v{VERSION} | {DEVELOPMENT_TEAM}".center(60))
    print(Fore.GREEN + "सत्यमेव जयते".center(60))
    print(Fore.MAGENTA + "▀"*60)

def show_legal_warning():
    print(Fore.RED + "\n⚠ 𝗟𝗘𝗚𝗔𝗟 𝗡𝗢𝗧𝗜𝗖𝗘")
    print(Fore.YELLOW + LEGAL_DISCLAIMER)
    print(Fore.WHITE + Back.RED + "ALL ACTIVITIES ARE LOGGED".center(60))
    
    accept = input("\n" + Fore.RED + "🔐 CONFIRM AUTHORIZATION [y/n]: ").lower()
    if accept != 'y':
        print(Fore.RED + "⛔ ACCESS TERMINATED")
        sys.exit(1)

def query_api(param, value):
    url = f"{API_BASE_URL}?key={API_KEY}&{param}={value}"
    try:
        ForensicAnimator.print_scanning()
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        if response.status_code == 200:
            ForensicAnimator.print_decrypting()
            return response.json()
        else:
            print(Fore.RED + f"💢 API ERROR: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"🌐 CONNECTION FAILED: {str(e)}")
        return None

def clean_result(result):
    cleaned = {}
    for k, v in result.items():
        key = k.upper().replace('_', ' ')
        if isinstance(v, str):
            v = v.strip()
            if key == 'ADDRESS':
                v = v.replace('!', ', ')
        cleaned[key] = v
    return cleaned

def display_results(data, search_param, search_value):
    if not data:
        print(Fore.RED + "🔴 NO DATA RECEIVED")
        return
    
    print(Fore.MAGENTA + "\n" + "🟣"*40)
    print(Fore.CYAN + f"🛡️ RESULTS: {search_param.upper()} » {search_value}")
    print(Fore.CYAN + f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(Fore.MAGENTA + "🟣"*40)
    
    results = []
    if isinstance(data, dict):
        results.append(clean_result(data))
    elif isinstance(data, list):
        results.extend(clean_result(item) for item in data if isinstance(item, dict))
    
    # Remove duplicates with properly closed parenthesis
    unique_results = []
    seen = set()
    for res in results:
        identifier = (res.get('MOBILE', ''), res.get('NAME', '').lower(), res.get('ADDRESS', '').lower())
        if identifier not in seen:
            seen.add(identifier)
            unique_results.append(res)
    
    for i, res in enumerate(unique_results, 1):
        print(Fore.GREEN + f"\n🔰 RESULT #{i}")
        print(Fore.BLUE + f"📱 » {res.get('MOBILE', 'N/A')}")
        print(Fore.BLUE + f"👤 » {res.get('NAME', 'N/A')}")
        print(Fore.BLUE + f"👨‍👦 » {res.get('FNAME', res.get('FATHER/HUSBAND', 'N/A'))}")
        print(Fore.BLUE + f"🏠 » {res.get('ADDRESS', 'N/A')}")
        print(Fore.BLUE + f"📶 » {res.get('CIRCLE', 'N/A')}")
        print(Fore.MAGENTA + "─"*40)
    
    print(Fore.RED + f"\n🔐 SESSION LOGGED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    parser = argparse.ArgumentParser(description='Cyber Forensic Tool')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-m', '--mobile', help='Mobile number search')
    group.add_argument('-a', '--aadhar', help='Aadhar number search')
    
    args = parser.parse_args()
    
    display_banner()
    show_legal_warning()
    
    if args.mobile:
        result = query_api('mobile', args.mobile)
        display_results(result, 'mobile', args.mobile)
    elif args.aadhar:
        result = query_api('aadhar', args.aadhar)
        display_results(result, 'aadhar', args.aadhar)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n🚨 EMERGENCY SHUTDOWN")
        sys.exit(1)