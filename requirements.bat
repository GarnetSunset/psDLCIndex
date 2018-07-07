powershell -Command "(New-Object Net.WebClient).DownloadFile('https://chromedriver.storage.googleapis.com/2.40/chromedriver_win32.zip', 'chromedriver_win32.zip')"
powershell -Command "(New-Object Net.WebClient).DownloadFile('http://stahlworks.com/dev/unzip.exe', 'unzip.exe')"
unzip chromedriver_win32.zip
del chromedriver_win32.zip
del unzip.exe
C:\Python27\Scripts\pip.exe install -q -r requirements.txt