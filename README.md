# stockholm
Encrypts / decrypts all files in folder 'infection' found in user's $HOME directory.
This script will only try to encrypt files with extensions targeted by the ransomware WannaCry.
For the encryption logic, stockholm uses the Fernet cryptography Python library
Have fun!
### usage
´´´
python3 stockholm.py [-h | -s | -v | -r DECRYPT_KEY] 
´´´
