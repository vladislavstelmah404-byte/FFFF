# FFFF — Онлайн чат 

## Опис
Простий чат на Python. Є вікно реєстрації вікно чату та сервер який пересилає повідомлення між користувачами

## Файли
- **main.py** — запускає програму
- **register.py** — вікно входу
- **online_chat.py** — вікно чату
- **server.py** — сервер, який приймає й розсилає повідомлення
- **bg.png, setting.png** — картинки для інтерфейсу

## Як запустити
1. Встановити customtkinter
   -pip install customtkinter
2. Запустити сервер
   -python server.py
3. Запустити клієнт
   -python main.py
4. Ввести ім'я — відкриється чат

Код запуску
python
from register import RegisterWindow

app = RegisterWindow()
app.mainloop()

Ці рядки запускають вікно реєстрації з якого далі відкривається чат
