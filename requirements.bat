powershell -Command "(New-Object Net.WebClient).DownloadFile('https://gist.githubusercontent.com/TheRadziu/b7321fdf2672197d14b87eeb2a5bd919/raw/b0d534d203e61a9ef63e596d4243abd45c64a66f/ez_fake_dlc.py', 'ez_dlc.py')"
pip install -q -r requirements.txt
Py -3 -m pip install beautifulsoup4 lxml selenium requests