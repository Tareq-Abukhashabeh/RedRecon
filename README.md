# RedRecon 🔴

```
██████╗ ███████╗██████╗     ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
██╔══██╗██╔════╝██╔══██╗    ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
██████╔╝█████╗  ██║  ██║    ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
██╔══██╗██╔══╝  ██║  ██║    ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
██║  ██║███████╗██████╔╝    ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚══════╝╚═════╝     ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
```

> **POWERED BY TAREQ ABU KHASHABEH**

A fast, feature-rich Python reconnaissance tool for security professionals and CTF players. RedRecon combines passive OSINT and active scanning into a single, beautifully formatted terminal report.

---

## Features

- 🔍 **Passive OSINT** — Subdomain enumeration via HackerTarget API and crt.sh certificate transparency logs
- 🔌 **Multi-threaded Port Scanning** — Fast concurrent scanning of common ports with service banner grabbing
- 🛡️ **WAF Detection** — Identifies Cloudflare, Sucuri, AWS WAF, and Akamai protection
- 🖥️ **Server Fingerprinting** — Detects web server type and technology stack
- 📊 **Rich Terminal Output** — Color-coded, structured reports for fast visual triage

---

## Installation

```bash
git clone https://github.com/Tareq-Abukhashabeh/RedRecon.git
cd RedRecon
pip install -r requirements.txt
```

### Requirements

```
requests
rich
```

Or install manually:

```bash
pip install requests rich
```

---

## Usage

```bash
python RedRecon.py
```

Then enter your target domain when prompted:

```
Enter Target Domain (e.g. www.example.com) > target.com
```

### Example Output

```
TARGET OVERVIEW
┌─────────────────────────────────────────────┐
│ Target: target.com        IP: 93.184.216.34 │
│ WAF: Cloudflare           Server: nginx     │
└─────────────────────────────────────────────┘

 OPEN PORTS & SERVICES
 PORT     STATUS   SERVICE BANNER / VERSION
 80/tcp   OPEN     Web (nginx)
 443/tcp  OPEN     Web (nginx)
 22/tcp   OPEN     SSH-2.0-OpenSSH_8.4

 SUBDOMAINS DISCOVERED (5)
 www.target.com
 mail.target.com
 api.target.com
 ...
```

---

## Scanned Ports

| Port | Service |
|------|---------|
| 21   | FTP |
| 22   | SSH |
| 23   | Telnet |
| 25   | SMTP |
| 53   | DNS |
| 80   | HTTP |
| 110  | POP3 |
| 135  | RPC |
| 139  | NetBIOS |
| 443  | HTTPS |
| 445  | SMB |
| 1433 | MSSQL |
| 3306 | MySQL |
| 3389 | RDP |
| 5900 | VNC |
| 8080 | HTTP-Alt |
| 8443 | HTTPS-Alt |

---

## Disclaimer

> This tool is intended for **educational purposes and authorized security testing only**.  
> Do not use RedRecon against systems you do not own or have explicit permission to test.  
> The author is not responsible for any misuse or damage caused by this tool.

---

## Author

**Tareq Abu Khashabeh**  
Cybersecurity Student | Blue Team | SOC | Automation  

- 🌐 [Portfolio](https://tareq-abukhashabeh.github.io/PORTFOLIO/)
- 💼 [LinkedIn](https://www.linkedin.com/in/tareq-abukhashabeh)
- 🐙 [GitHub](https://github.com/Tareq-Abukhashabeh)

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
