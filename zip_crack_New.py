# (Zip legacy encryption must be enabled on the zip archive for this script to work)
# Author: Nehan Tarefder

import zipfile
import itertools
from sys import exit
import argparse

parser = argparse.ArgumentParser(description='Crack a zip file...')
parser.add_argument('zipfile', type=str, help='Specify the zipfile to crack (or path to zipfile)')
parser.add_argument('-w', '--wordlist', type=str, help='Specify a wordlist (or path to wordlist)')
parser.add_argument('-l', '--maxlength', type=int, default=10, help='Max length of password for bruteforcing.')
parser.add_argument('-m', '--minlength', type=int, default=1, help='Min length of password for bruteforcing.')
args = parser.parse_args()

# Main functions start here...
def dictionary(zipfilename, wordlist, minl, maxl):
  zip_file = zipfile.ZipFile(zipfilename)
  with open(wordlist,'r') as file:  
    for line in file:
      for word in line.split():
        if extractFile(zip_file, word):
          print('*' * 20)
          print('Password found: %s' % word)
          print('Files extracted...')
          exit(0)
  print('Dictionary attack failed..')
  bruteforce(zipfilename, minl, maxl)

def bruteforce(zipfilename, minl, maxl):
  # Can add other symbols to alphabet
  alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
  zip_file = zipfile.ZipFile(zipfilename)
  if(minl < 1 or maxl < 1):
    print("Min/max bruteforce length cannot be less than 1.")
    exit(0)
  elif(maxl < minl):
    print("Max bruteforce length must be greater than min bruteforce length.")
    exit(0)
  print('Bruteforcing passwords from length {0} to {1}...'.format(str(minl), str(maxl)))
  # For every possible combination from alphabet...
  for i in range(minl, maxl+1):
    for c in itertools.product(alphabet, repeat=i):
      password = ''.join(c)
      # print(password)
      if extractFile(zip_file, password):
        print('*' * 20)
        print('Password found: %s' % password)
        print('Files extracted...')
        exit(0)

# Function for extracting zip files to test a password
def extractFile(zip_file, password):
  try:
    zip_file.extractall(pwd=password.encode())
    return True
  except KeyboardInterrupt:
    exit(0)
  except Exception as e:
    # print(e)
    pass

# execution
if(args.wordlist==None):
  bruteforce(args.zipfile, args.minlength, args.maxlength)
else:
  dictionary(args.zipfile, args.wordlist, args.minlength, args.maxlength)
# If no password was found by the end..
print('Password not found.')
