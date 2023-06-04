# Crack SHA (Secure Hashing Algorithm) Hashes
# Author: Nehan Tarefder

import itertools
from sys import exit
import argparse
import hashlib

parser = argparse.ArgumentParser(description='Crack a SHA hash (will add support for MD5 and SHA3 hashes in the future)...')
parser.add_argument('hash', type=str, help='Specify the SHA1/SHA2 hash to crack. SUPPORTED TYPES: SHA256, SHA384, SHA224, SHA512, SHA1')
parser.add_argument('-w', '--wordlist', type=str, help='Specify a wordlist (or path to wordlist)')
args = parser.parse_args()

thehash = args.hash
# checking hash type
if(len(thehash) == 64):
  typ = 256
elif(len(thehash) == 96):
  typ = 384
elif(len(thehash) == 56):
  typ = 224
elif(len(thehash) == 128):
  typ = 512
elif(len(thehash) == 40):
  typ = 1
else:
  print("Input hash is not of supported type... Exiting.")
  exit(0)

def dictionary(inphash, wordlist):
  with open(wordlist,'r') as file:  
    for line in file:
      for wrd in line.split():
        com = hasher(wrd)        
        res = com.hexdigest()
        if (res == inphash):
          print('*' * 20)
          print('Password found: %s' % wrd)
          exit(0)
  print('Dictionary attack failed..')
  bruteforce(inphash)

def bruteforce(inphash):
  # Can add other symbols to alphabet if needed
  alphabet = '!@#$0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
  print('Bruteforcing passwords...')
  # For every possible combination from alphabet...
  for i in range(1, 11):    # change these values to change the min/max password lengths to bruteforce
    print('Testing passwords of length '+str(i)+'..')
    for c in itertools.product(alphabet, repeat=i):
      password = ''.join(c)
      com = hasher(password)        
      res = com.hexdigest()
      if (res == inphash):
          print('*' * 20)
          print('Password found: %s' % password)
          exit(0)

def hasher(word):
  if(typ==256):
    tester = hashlib.sha256(word.encode())
  elif(typ==384):
    tester = hashlib.sha384(word.encode())
  elif(typ==224):
    tester = hashlib.sha224(word.encode())
  elif(typ==512):
    tester = hashlib.sha512(word.encode())
  elif(typ==1):
    tester = hashlib.sha1(word.encode())
  return tester

if(args.wordlist==None):
  bruteforce(thehash)
else:
  dictionary(thehash, args.wordlist)
# If no password was found by the end..
print('Password not found.')

