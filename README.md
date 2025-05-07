Run Command Prompt:
cd network-security-evil-twin
python3 main.py


In Powershell:

To test matching fingerprint:
curl.exe -H "User-Agent: test-browser" -H "Accept-Language: en-US" -H "Accept-Encoding: gzip" -H "Referer: http://legit.site" http://127.0.0.1:10000/foo


To test a mismatched fingerprint:
curl.exe -H "User-Agent: evil-browser" -H "Accept-Language: en-US" -H "Accept-Encoding: gzip" -H "Referer: http://legit.site" http://127.0.0.1:10000/foo



To view database:

In Command Prompt:
cd "C:\Program Files\MySQL\MySQL Server 8.0\bin"
mysql -u user -p
password: pass
mysql> USE evil_twin_db;
