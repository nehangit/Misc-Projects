# Crack SHA (Secure Hashing Algorithm) Hashes
# Author: Nehan Tarefder

import itertools
from sys import exit
import argparse
import hashlib

parser = argparse.ArgumentParser(description='Crack a SHA hash (will add support for MD5 and SHA3 hashes in the future)...')
parser.add_argument('hash', type=str, help='Specify the SHA1/SHA2 hash to crack. SUPPORTED TYPES: SHA256, SHA384, SHA224, SHA512, SHA1')
parser.add_argument('-w', '--wordlist', type=str, help='Specify a wordlist (or path to wordlist)')
parser.add_argument('-l', '--maxlength', type=int, default=10, help='Max password length for bruteforcing.')
parser.add_argument('-m', '--minlength', type=int, default=1, help='Min password length for bruteforcing.')
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
  bruteforce(inphash, args.minlength, args.maxlength)

def bruteforce(inphash, minl, maxl):
  # Can add other symbols to alphabet if needed
  alphabet = '!@#$0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
  if(minl < 1 or maxl < 1):
    print("Min/max bruteforce length cannot be less than 1.\nExiting...")
    exit(0)
  elif(maxl < minl):    
    print("Max bruteforce length must be greater than or equal to min bruteforce length. (Max length = {0}, Min length = {1})\nExiting...".format(maxl, minl))
    exit(0)
  print('Bruteforcing passwords from length {0} to {1}...'.format(minl, maxl))
  # For every possible combination from alphabet...
  for i in range(minl, maxl+1):    # change these values to change the min/max password lengths to bruteforce
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
  bruteforce(thehash, args.minlength, args.maxlength)
else:
  dictionary(thehash, args.wordlist)
# If no password was found by the end..
print('Password not found.')
