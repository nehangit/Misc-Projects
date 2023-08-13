# Password generator
# Author: Nehan Tarefder
import requests
import secrets
from sys import exit
import argparse

parser = argparse.ArgumentParser(description='Generate secure passwords.')
parser.add_argument('-l', '--length', type=int, default=8, help='Specify the length of the password')
parser.add_argument('-c', '--complexity', type=int, default=2, help='Specify the complexity of the password: 1 = Low, 2 = Medium, 3 = High')
args = parser.parse_args()

alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$&*%~^"

# Main
if(args.length < 3):
  print("Length too short.")
  exit()
elif(args.length < 6):
  print("Longer password recommended.") #add check ehre

if(args.complexity < 1 or args.complexity > 3):
  print("Invalid complexity input, run python pwg.py -h for help message.")

secureRand = secrets.SystemRandom()
if(args.complexity == 1):
  response = requests.get("https://random-word-api.herokuapp.com/word?length="+str(args.length))
  pw = response.json()[0]
  for k in range(int(len(pw)/2)):
    ind = secureRand.randint(0, len(pw)-1)
    pw = pw[:ind] + pw[ind].upper() + pw[ind+1:]
  print("Generated password of length {0} with low complexity: ".format(args.length) + pw)

if(args.complexity == 2):
  cf = secureRand.randint(2, args.length-1)
  response = requests.get("https://random-word-api.herokuapp.com/word?length="+str(cf))
  pw = response.json()[0]
  password = pw + ''.join(secureRand.choice(alphabet) for i in range(args.length - cf))      # can swap the order here, add random capitalization, etc.
  print("Generated password of length {0} with medium complexity: ".format(args.length) + password)   

if(args.complexity==3):
    password = ''.join(secureRand.choice(alphabet) for i in range(args.length))
    print("Generated password of length {0} with high complexity: ".format(args.length) + password)
