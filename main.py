from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
import pyperclip
import pyfiglet
import time
import random
import os


# ==========================================
# KELAS INTI BOT (BACKEND SELENIUM)
# Scalable: Kalau mau ganti browser/logika, cukup ubah di class ini
# ==========================================
class WhatsAppBot:
    def __init__(self, console: Console):
        self.console = console
        self.driver: WebDriver | None = None
        self.wait: WebDriverWait | None = None

    def initialize_driver(self):
        with self.console.status(
            "[bold cyan]init --browser[/]  [dim]# launching automation...[/]", spinner="dots"
        ):
            options = webdriver.ChromeOptions()
            options.add_argument(
                f"--user-data-dir={os.path.join(os.getcwd(), 'chrome_profile')}"
            )

            self.driver = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, 90)
            self.driver.get("https://web.whatsapp.com")

    def wait_for_login(self):
        assert self.wait is not None, "Driver belum diinisialisasi"
        with self.console.status(
            "[bold yellow]awaiting --qr-scan[/]  [dim]# session pending...[/]", spinner="dots"
        ):
            # Menunggu panel obrolan muncul (tanda login berhasil)
            self.wait.until(EC.presence_of_element_located((By.ID, "pane-side")))
        self.console.print("[bold green]✔✔  auth --success[/]  [dim]# whatsapp session active[/]")

    def send_messages(self, target_number: str, message: str, total_spam: int):
        assert self.driver is not None, "Driver belum diinisialisasi"
        target_url = f"https://web.whatsapp.com/send?phone={target_number}"

        with self.console.status(
            f"[bold cyan]Menembak URL ruang obrolan {target_number}...",
            spinner="aesthetic",
        ):
            self.driver.get(target_url)
            wait_chat = WebDriverWait(self.driver, 60)
            # Menunggu kotak ketik pesan muncul
            msg_box = wait_chat.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@contenteditable='true'][@data-tab='10']")
                )
            )

        self.console.print(f"[bold green]✔ Target {target_number} terkunci![/]\n")

        # ==========================================
        # Copy ke Clipboard OS
        # ==========================================
        pyperclip.copy(message)
        self.console.print(
            "[dim cyan]Meyalin teks kompleks ke dalam memori clipboard...[/]"
        )

        count = 0
        while True:
            # Gunakan Ctrl+V untuk Paste, lalu tekan Enter
            msg_box.send_keys(Keys.CONTROL, "v")
            time.sleep(0.5)  # Beri nafas sedikit agar sistem WA memproses paste-nya
            msg_box.send_keys(Keys.ENTER)

            count += 1
            self.console.print(f"[green] ➔ Pesan ke-{count} berhasil terkirim![/]")

            # Cek batasan
            if total_spam != 0 and count >= total_spam:
                break

            # Algoritma delay manusiawi (1.5 - 3.5 detik)
            jeda = random.uniform(1.5, 3.5)
            time.sleep(jeda)

    def send_from_file(self, target_number: str, file_path: str, total_spam: int):
        # Baca isi file txt
        with open(file_path, "r", encoding="utf-8") as f:
            message = f.read()

        self.console.print(
            f"[bold cyan]📄 Pesan dari file dimuat ({len(message)} karakter)[/]\n"
        )
        self.send_messages(target_number, message, total_spam)

    def send_interactive(self, target_number: str, total_spam: int):
        assert self.driver is not None, "Driver belum diinisialisasi"
        target_url = f"https://web.whatsapp.com/send?phone={target_number}"

        with self.console.status(
            f"[bold cyan]Menembak URL ruang obrolan {target_number}...",
            spinner="aesthetic",
        ):
            self.driver.get(target_url)
            wait_chat = WebDriverWait(self.driver, 60)
            msg_box = wait_chat.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@contenteditable='true'][@data-tab='10']")
                )
            )

        self.console.print(f"[bold green]✔ Target {target_number} terkunci![/]\n")

        # Instruksi untuk User
        self.console.print(
            "[bold yellow]👉 SILAKAN KETIK PESAN BEBASMU DI BROWSER WHATSAPP SEKARANG.[/]"
        )
        self.console.print(
            "[bold red]⚠️ JANGAN DITEKAN ENTER/KIRIM DULU DI WHATSAPP-NYA![/]"
        )

        # Menahan program sampai user menekan Enter di terminal
        Prompt.ask(
            "\n[bold white]➤ Kalau sudah selesai ngetik di WA, tekan ENTER di terminal ini untuk mulai ngirim[/]"
        )

        self.console.print("[bold cyan]Memproses dan menggandakan teks...[/]")

        # Trik Copy-Paste (Blok semua teks yang diketik user lalu Copy)
        msg_box.send_keys(Keys.CONTROL, "a")
        time.sleep(0.5)
        msg_box.send_keys(Keys.CONTROL, "c")
        time.sleep(0.5)

        count = 0
        while True:
            # Paste teks yang sudah di-copy dan tekan Enter
            msg_box.send_keys(Keys.CONTROL, "v")
            time.sleep(0.1)  # Jeda rendering UI WhatsApp
            msg_box.send_keys(Keys.ENTER)

            count += 1
            self.console.print(f"[green] ➔ Pesan ke-{count} berhasil terkirim![/]")

            if total_spam != 0 and count >= total_spam:
                break

            time.sleep(random.uniform(1.5, 3.5))

    def close(self):
        if self.driver:
            self.driver.quit()
            self.console.print("[bold red]✖  exit --graceful[/]  [dim]# session terminated[/]")


# ==========================================
# KELAS ANTARMUKA PENGGUNA (CLI FRONTEND)
# Scalable: Logika UI terpisah dari logika bot
# ==========================================
class BotCLI:
    def __init__(self):
        self.console = Console()
        self.bot = WhatsAppBot(self.console)

    def show_banner(self):
        # Membersihkan layar terminal (Windows/Linux/Mac)
        os.system("cls" if os.name == "nt" else "clear")

        # ASCII Art Generator
        ascii_banner = pyfiglet.figlet_format("WaveSend", font="slant")

        # Desain Panel Credit
        credit_text = Text()
        credit_text.append("Developer : ", style="bold white")
        credit_text.append("nez.\n", style="bold cyan")
        credit_text.append("GitHub    : ", style="bold white")
        credit_text.append("https://github.com/nezmajesty-dev\n", style="bold magenta")
        credit_text.append("Version   : 2.0", style="dim white")

        # Menggabungkan Banner dan Credit di dalam Panel kotak
        panel = Panel.fit(
            f"[bold green]{ascii_banner}[/]\n{credit_text}",
            title="[bold yellow]Automated Messaging System[/]",
            border_style="cyan",
        )
        self.console.print(panel)
        self.console.print()

    def get_user_inputs(self) -> tuple:
        self.console.print("[bold yellow]❖ Konfigurasi Target[/]")
        target = Prompt.ask(
            "[bold white]   ➤ Masukkan nomor target (contoh: 628123...)[/]"
        )
        msg = Prompt.ask("[bold white]   ➤ Masukkan teks pesan[/]")
        count = IntPrompt.ask(
            "[bold white]   ➤ Berapa kali kirim pesan?[/] [dim](Ketik 0 untuk unlimited)[/]",
            default=1,
        )
        self.console.print()
        return target, msg, count

    def show_menu(self):
        self.console.print()
        self.console.print("[dim]  ────────────────────────────────────────[/]")
        self.console.print("  [bold yellow]Menu[/]")
        self.console.print("[dim]  ────────────────────────────────────────[/]")
        self.console.print()
        self.console.print("  [bold cyan]1[/]  [dim]›[/]  [white]send --manual[/]         [dim]input terminal[/]")
        self.console.print("  [bold cyan]2[/]  [dim]›[/]  [white]send --file[/]   [dim]import .txt[/]")
        self.console.print("  [bold cyan]3[/]  [dim]›[/]  [white]send --interactive[/]      [dim]ketik di WA[/]")
        self.console.print("  [bold magenta]4[/]  [dim]›[/]  [magenta]Keluar[/]")
        self.console.print()
        self.console.print("[dim]  ────────────────────────────────────────[/]")
        self.console.print()
        return Prompt.ask("  [green]root@wavesend[/][dim]:[/][cyan]~[/][dim]$[/]", choices=["1", "2", "3", "4"])

    def run(self):
        self.show_banner()
        self.bot.initialize_driver()
        self.bot.wait_for_login()

        while True:
            pilihan = self.show_menu()

            if pilihan == "1":
                target_number, message, total_spam = self.get_user_inputs()
                try:
                    self.bot.send_messages(target_number, message, total_spam)
                    self.console.print("\n[bold green]✅ SELESAI![/]\n")
                except Exception as e:
                    self.console.print(f"\n[bold red]✖ ERROR: {e}[/]")

            elif pilihan == "2":
                target = Prompt.ask(
                    "[bold white]   ➤ Nomor target (contoh: 628123...)[/]"
                )
                file_name = Prompt.ask(
                    "[bold white]   ➤ Nama file TXT (contoh: pesan.txt)[/]"
                )
                file_path = os.path.join(os.getcwd(), file_name)
                count = IntPrompt.ask(
                    "[bold white]   ➤ Berapa kali kirim?[/] [dim](0 = unlimited)[/]",
                    default=1,
                )

                try:
                    self.bot.send_from_file(target, file_path, count)
                    self.console.print("\n[bold green]✅ SELESAI![/]\n")
                except FileNotFoundError:
                    self.console.print(
                        f"\n[bold red]✖ File '{file_name}' tidak ditemukan di folder project![/]"
                    )
                except Exception as e:
                    self.console.print(f"\n[bold red]✖ ERROR: {e}[/]")

            elif pilihan == "3":
                target = Prompt.ask(
                    "[bold white]   ➤ Nomor target (contoh: 628123...)[/]"
                )
                count = IntPrompt.ask(
                    "[bold white]   ➤ Berapa kali kirim?[/] [dim](0 = unlimited)[/]",
                    default=1,
                )

                try:
                    self.bot.send_interactive(target, count)
                    self.console.print("\n[bold green]✅ SELESAI![/]\n")
                except Exception as e:
                    self.console.print(f"\n[bold red]✖ ERROR: {e}[/]")

            elif pilihan == "4":
                self.bot.close()
                break


# ==========================================
# EKSEKUSI PROGRAM UTAMA
# ==========================================
if __name__ == "__main__":
    app = BotCLI()
    app.run()
