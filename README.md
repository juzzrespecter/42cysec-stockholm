# stockholm
Encrypts / decrypts all files in folder  _infection_  found in user's $HOME directory.  
This script will only try to encrypt files with extensions targeted by the ransomware WannaCry ([documented here](https://logrhythm.com/blog/a-technical-analysis-of-wannacry-ransomware/))  
For the encryption logic, stockholm uses the Fernet cryptography Python library.  
  

Have fun!  

## usage
Set up victim environment:
```
./start.sh [up | exec | listen]
```
Ransomware script:
```
python3 stockholm.py [-h | -s | -v | -r DECRYPT_KEY] 
```
