import socket
import requests
import threading
import ssl
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text
# Removed Align import since we don't need it anymore

# Initialize Rich Console
console = Console()

class RedReconUltimate:
    def __init__(self, target):
        self.target = target
        self.ip = self.get_ip()
        self.subdomains = set()
        self.waf = "None Detected"
        self.server_type = "Unknown"
        self.results = []
        self.start_time = datetime.now()

    def print_banner(self):
        # I removed the extra padding spaces to make it align left perfectly
        banner_art = """
[bold red]
██████╗ ███████╗██████╗     ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
██╔══██╗██╔════╝██╔══██╗    ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██╗
██████╔╝█████╗  ██║  ██║    ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
██╔══██╗██╔══╝  ██║  ██║    ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
██║  ██║███████╗██████╔╝    ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚══════╝╚═════╝     ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
[/bold red]"""
        
        console.print(banner_art)
        # These lines are now Left-Aligned (No Align.center)
        console.print("[bold yellow] POWERED BY TAREQ ABU KHASHABEH [/bold yellow]")
        

    def get_ip(self):
        try:
            clean = self.target.replace("https://", "").replace("http://", "").split('/')[0]
            self.target = clean
            return socket.gethostbyname(self.target)
        except:
            return None

    def fetch_subdomains(self):
        console.print(f"[bold cyan][*] Phase 1: Passive OSINT (Subdomains)...[/bold cyan]")
        try:
            url = f"https://api.hackertarget.com/hostsearch/?q={self.target}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                for line in response.text.split("\n"):
                    if "," in line:
                        self.subdomains.add(line.split(",")[0])
            
            if len(self.subdomains) < 2:
                url2 = f"https://crt.sh/?q=%.{self.target}&output=json"
                r2 = requests.get(url2, timeout=15)
                if r2.status_code == 200:
                    for entry in r2.json():
                        self.subdomains.add(entry['name_value'])
        except:
            console.print("[red][!] OSINT Connection Failed (Check Internet)[/red]")

    def detect_tech(self):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (RedRecon/1.0)'}
            try:
                r = requests.get(f"https://{self.target}", headers=headers, timeout=5, verify=False)
            except:
                r = requests.get(f"http://{self.target}", headers=headers, timeout=5)

            h = r.headers
            self.server_type = h.get('Server', 'Unknown')
            
            if 'CF-RAY' in h: self.waf = "[bold red]Cloudflare (Active Protection)[/bold red]"
            elif 'X-Sucuri-ID' in h: self.waf = "[bold red]Sucuri Firewall[/bold red]"
            elif 'X-AWS-ID' in h: self.waf = "[bold yellow]AWS Web Application Firewall[/bold yellow]"
            elif 'Akamai' in h.get('Server', ''): self.waf = "[bold red]Akamai Edge[/bold red]"
            else: self.waf = "[green]No Standard WAF Detected[/green]"

        except:
            self.waf = "[dim]Connection Failed[/dim]"

    def scan_port(self, port, progress, task_id):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.8)
            result = s.connect_ex((self.ip, port))
            if result == 0:
                banner = "Unknown Service"
                if port in [80, 443, 8080, 8443]:
                    protocol = "https" if port in [443, 8443] else "http"
                    try:
                        r = requests.head(f"{protocol}://{self.target}:{port}", timeout=2, verify=False)
                        banner = f"Web ({r.headers.get('Server', 'Unknown')})"
                    except:
                        banner = "Web Service"
                else:
                    try:
                        s.send(b'HEAD / \r\n')
                        b = s.recv(1024).decode().strip()
                        if b: banner = b[:40]
                    except:
                        pass
                self.results.append((port, banner))
            s.close()
        except:
            pass
        progress.update(task_id, advance=1)

    def show_report(self):
        grid = Table.grid(expand=True)
        grid.add_column()
        grid.add_column(justify="right")
        grid.add_row(f"[bold white]Target:[/bold white] {self.target}", f"[bold white]IP:[/bold white] {self.ip}")
        grid.add_row(f"[bold white]WAF:[/bold white] {self.waf}", f"[bold white]Server:[/bold white] {self.server_type}")
        console.print(Panel(grid, title="[bold cyan]TARGET OVERVIEW[/bold cyan]", border_style="cyan"))

        port_table = Table(title=" OPEN PORTS & SERVICES ", show_header=True, header_style="bold black on white", border_style="green")
        port_table.add_column("PORT", style="bold cyan", width=10)
        port_table.add_column("STATUS", style="bold green", width=10)
        port_table.add_column("SERVICE BANNER / VERSION", style="white")

        if self.results:
            for port, banner in sorted(self.results):
                port_table.add_row(f"{port}/tcp", "OPEN", banner)
        else:
            port_table.add_row("---", "CLOSED", "No open ports found (or filtered)")
        
        console.print(port_table)

        sub_table = Table(title=f" SUBDOMAINS DISCOVERED ({len(self.subdomains)}) ", show_header=True, header_style="bold black on yellow", border_style="yellow")
        sub_table.add_column("Subdomain URL", style="yellow")
        
        sorted_subs = sorted(list(self.subdomains))
        for sub in sorted_subs[:7]:
            sub_table.add_row(sub)
        
        if len(sorted_subs) > 7:
            sub_table.add_row(f"[dim]... and {len(sorted_subs)-7} more hidden subdomains[/dim]")
        
        if len(self.subdomains) == 0:
            sub_table.add_row("[dim]No subdomains found in public records[/dim]")

        console.print(sub_table)
        console.print(f"\n[dim]Scan completed in {datetime.now() - self.start_time}[/dim]")

    def run(self):
        self.print_banner()
        if not self.ip:
            console.print("[bold red][!] Error: Could not resolve domain.[/bold red]")
            return

        self.detect_tech()
        self.fetch_subdomains()
        
        console.print(f"\n[bold cyan][*] Phase 2: Active Recon (Port Scan)...[/bold cyan]")
        ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 1433, 3306, 3389, 5900, 8080, 8443]
        
        with Progress() as progress:
            task = progress.add_task("[green]Scanning Ports...", total=len(ports))
            threads = []
            for port in ports:
                t = threading.Thread(target=self.scan_port, args=(port, progress, task))
                threads.append(t)
                t.start()
            for t in threads: t.join()
        
        console.print("\n")
        self.show_report()

if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    try:
        target_input = console.input("[bold yellow]Enter Target Domain (e.g. www.redx.site) > [/bold yellow]")
        if target_input:
            tool = RedReconUltimate(target_input)
            tool.run()
    except KeyboardInterrupt:
        console.print("\n[red][!] Scan Aborted by User[/red]")
