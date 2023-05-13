# (Zip legacy encryption must be enabled on the zip archive for this script to work)
# Author: Nehan Tarefder

import zipfile
import itertools
from sys import exit
import argparse

parser = argparse.ArgumentParser(description='Crack a zip file...')
parser.add_argument('zipfile', type=str, help='specify the zipfile to crack (or path to zipfile)') # make positional
parser.add_argument('-w', '--wordlist', type=str, help='specify a wordlist (or path to wordlist)')
parser.add_argument('-l', '--length', type=int, required=True, help='length of password for bruteforcing')
args = parser.parse_args()

# Main functions start here...
def dictionary(zipfilename, wordlist, n):
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
  bruteforce(zipfilename, n)

def bruteforce(zipfilename, n):
  # Can add other symbols to alphabet
  alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
  zip_file = zipfile.ZipFile(zipfilename)

  print('Bruteforcing...')
  # For every possible combination up to n letters from alphabet...
  for i in range(1, n):
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
    zip_file.extractall(pwd=password.encode()) # find error
    return True
  except KeyboardInterrupt:
    exit(0)
  except Exception as e:
    # print(e)
    pass

# execution
if(args.wordlist==None):
  bruteforce(args.zipfile, args.length)
else:
  dictionary(args.zipfile, args.wordlist, args.length)
# If no password was found by the end...
print('Password not found.')