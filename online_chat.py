from customtkinter import *
from socket import *
import threading


# ! Декілька вікооон

class MainWindow(CTk):
    # Зміна з фото: додано параметр username в __init__
    def __init__(self, username):
        super().__init__()

        self.geometry("400x300")
        self.title("Online Chat")

        self.is_show_menu = False
        self.speed_animate_menu = -5

        # Заздалегідь оголошуємо, щоб не було AttributeError
        # при першому виклику show_menu()
        self.change_name_entry = None
        self.change_theme_option = None
        self.change_name_btn = None

        self.menu_frame = CTkFrame(
            self,
            width=30,
            height=300,
        )
        self.menu_frame.propagate(False)
        self.menu_frame.place(x=0, y=0)

        self.open_menu_btn = CTkButton(
            self,
            text=">",
            width=30,
            font=("Arial", 15, "bold"),
            command=self.toggle_show_menu
        )
        self.open_menu_btn.place(x=0, y=0)

        self.chat_field = CTkTextbox(
            self,
            font=("Arial", 20, "bold"),
            state="disabled"
        )
        self.chat_field.place(x=0, y=0)

        self.message_entry = CTkEntry(
            self,
            placeholder_text="Type your message ...",
            height=50
        )
        self.message_entry.bind("<Return>", self.send_message)
        self.message_entry.place(x=0, y=0)

        self.send_button = CTkButton(
            self,
            text=">",
            font=("Arial", 15, "bold"),
            width=60,
            height=50,
            command=self.send_message
        )
        self.send_button.place(x=0, y=0)

        # Зміна з фото: динамічне присвоєння нікнейму з параметра
        self.username = username

        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect(("7.tcp.eu.ngrok.io", 20602))

            hello = f"TEXT@{self.username}@[SYSTEM] {self.username} приєднався до чату\n"

            self.sock.send(hello.encode())

            threading.Thread(target=self.recv_message, daemon=True).start()

        except Exception as e:
            self.add_message(f"Не вдалось підключитись до сервера: {e}")

        self.adaptive_ui()

    def add_message(self, text):
        self.chat_field.configure(state="normal")
        self.chat_field.insert(END, text + "\n")
        self.chat_field.configure(state="disabled")

    def send_message(self, event=None):
        message = self.message_entry.get().strip()
        if message:
            self.add_message(f"{self.username}: {message}")
            data = f"TEXT@{self.username}@{message}\n"
            try:
                self.sock.sendall(data.encode())
            except:
                pass
        self.message_entry.delete(0, END)

    def recv_message(self):
        buffer = ""
        while 1:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                buffer += chunk.decode()
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    self.handle_line(line.strip())
            except:
                break
        self.sock.close()

    def handle_line(self, line):
        if not line:
            return

        parts = line.split("@", 3)

        msg_type = parts[0]

        if msg_type == "TEXT":
            if len(parts) >= 3:
                author = parts[1]
                message = parts[2]
                self.add_message(f"{author}: {message}")
            else:
                self.add_message(f"Це повідомлення не підримується вашою версію :)")
        else:
            self.add_message(f"Це повідомлення не підримується вашою версію :)")

    def adaptive_ui(self):
        self.menu_frame.configure(height=self.winfo_height())

        self.chat_field.place(x=self.menu_frame.winfo_width())
        self.chat_field.configure(width=self.winfo_width() - self.menu_frame.winfo_width(),
                                  height=self.winfo_height() - 50)

        self.send_button.place(x=self.winfo_width() - 50, y=self.winfo_height() - 50)

        self.message_entry.place(x=self.menu_frame.winfo_width(), y=self.send_button.winfo_y())
        self.message_entry.configure(width=self.winfo_width() - self.menu_frame.winfo_width()
                                           - self.send_button.winfo_width())

        self.after(50, self.adaptive_ui)

    def toggle_show_menu(self):
        if self.is_show_menu:
            self.is_show_menu = False
            self.speed_animate_menu *= -1
            self.open_menu_btn.configure(text=">")
            self.show_menu()
        else:
            self.is_show_menu = True
            self.speed_animate_menu *= -1
            self.open_menu_btn.configure(text="<")
            self.show_menu()

            self.change_name_entry = CTkEntry(self.menu_frame,
                                              placeholder_text="Enter your name",
                                              width=150,
                                              height=50,
                                              font=("Arial", 15, "bold"))
            self.change_name_entry.bind("<Return>", self.change_username)
            self.change_name_entry.pack(pady=(50, 0))

            # Кнопка для зміни нікнейму
            self.change_name_btn = CTkButton(self.menu_frame,
                                             text="Змінити нік",
                                             width=150,
                                             command=self.change_username)
            self.change_name_btn.pack(pady=(10, 0))

            self.change_theme_option = CTkOptionMenu(self.menu_frame,
                                                     values=["Темна", "Світла"],
                                                     command=self.change_theme)
            self.change_theme_option.pack(pady=(20, 0))

    def change_username(self, event=None):
        new_name = self.change_name_entry.get().strip()
        if not new_name or new_name == self.username:
            return

        old_name = self.username
        self.username = new_name
        self.change_name_entry.delete(0, END)
        self.change_name_entry.configure(placeholder_text=f"Поточний нік: {self.username}")

        self.add_message(f"[SYSTEM] Ви змінили нік з {old_name} на {self.username}")

        # Повідомляємо сервер/інших учасників про зміну нікнейму
        data = f"TEXT@{old_name}@[SYSTEM] {old_name} змінив нік на {self.username}\n"
        try:
            self.sock.sendall(data.encode())
        except:
            pass

    def show_menu(self):
        self.menu_frame.configure(width=self.menu_frame.winfo_width() + self.speed_animate_menu)
        if not self.menu_frame.winfo_width() >= 200 and self.is_show_menu:
            self.after(10, self.show_menu)
        elif self.menu_frame.winfo_width() >= 40 and not self.is_show_menu:
            self.after(10, self.show_menu)
            if self.change_name_entry and self.change_theme_option:
                self.change_name_entry.destroy()
                self.change_theme_option.destroy()
                if self.change_name_btn:
                    self.change_name_btn.destroy()

    def change_theme(self, value):
        if value == "Темна":
            set_appearance_mode("dark")
        else:
            set_appearance_mode("light")


if __name__ == "__main__":
    app = MainWindow("Biba")
    app.mainloop()




