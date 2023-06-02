# WiFi-FTP

### [+] Description :
***WiFi-FTP is a tool to create a simple ftp server in local network. Anyone under same wifi/router can read/write/modify the folder you shared.***
<h2 align="center">Share files under same Wi-Fi!</h2>

### [+] Installation

```apt install python3 python3-pip -y```

```pip3 install pyftpdlib```

```git clone https://github.com/KasRoudra/wififtp```

```cd wififtp```

```python3 ftp.py```

### Or 
#### Download executable file for windows from <a href="https://github.com/KasRoudra/wififtp/releases/download/v1.0_Beta/ftp.exe">releases</a>!
### Or, Use Single Command
```
git clone https://github.com/KasRoudra/wififtp && cd wififtp && python3 ftp.py
```
### [*] Features
 - You can customize both port and shared folder. Without change, default port will be 2121 and default folder will be the folder from which the file is executed!
 - Now WiFi-FTP also support arguments 

### [-] Options
```
usage: ftp.py [-h] [-p PORT] [-d DIRECTORY]

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  WiFi-FTP's server port [Default: 2121]
  -d DIRECTORY, --directory DIRECTORY
                        Directory where server will start [Default: /home/kasroudra/]
```
## [+] Caution:

### You must need "Python" installed in your operating system. If you use firewall you also have to enable python from "Windows Firewall". If you can't enable python from firewall, you may need to disable firewall while using ftp!
### Your sharing link will be like "ftp://192.168.0.105:2121". Make sure you are connected to same router/Wi-Fi to access folder from other device!
## [+] Screenshot:
<img src="https://github.com/KasRoudra/wififtp/blob/main/ss.jpg">

## [~] Find Me on :

- [![Github](https://img.shields.io/badge/Github-KasRoudra-green?style=for-the-badge&logo=github)](https://github.com/KasRoudra)

- [![Gmail](https://img.shields.io/badge/Gmail-KasRoudra-green?style=for-the-badge&logo=gmail)](mailto:kasroudrakrd@gmail.com)

- [![Facebook](https://img.shields.io/badge/Facebook-KasRoudra-green?style=for-the-badge&logo=facebook)](https://facebook.com/KasRoudra)

- [![Messenger](https://img.shields.io/badge/Messenger-KasRoudra-green?style=for-the-badge&logo=messenger)](https://m.me/KasRoudra)

- [![Telegram](https://img.shields.io/badge/Telegram-KasRoudra-indigo?style=for-the-badge&logo=telegram)](https://t.me/KasRoudra)
