from customtkinter import *
from PIL import Image
from online_chat import MainWindow


class RegisterWindow(CTk):
    def __init__(self):
        super().__init__()
        self.title("Register")
        self.geometry("700x400")
        self.resizable(False, False)
        self.configure(fg_color="white")

        self.left_frame = CTkFrame(self)
        self.left_frame.pack(side="left", fill="both")
        img = Image.open("img\\bg.png")
        img_ctk = CTkImage(dark_image=img, size=(450, 400))
        self.img_label = CTkLabel(
            self.left_frame,
            text="WELCOME",
            text_color="#ffffff",
            image=img_ctk,
            font=("Helvetica", 60, "bold"),
        )
        self.img_label.pack()

        self.right_frame = CTkFrame(self, fg_color="#ffffff")
        self.right_frame.pack(side="right", fill="both")

        # todo Додати загаловок
        self.title_label = CTkLabel(
            self.right_frame,
            text_color="#9424da",
            text="LogiTalk",
            font=("Helvetica", 20, "bold"),
        )
        self.title_label.pack(pady=30)

        # todo Додати поля для введення іменні
        self.name_entry = CTkEntry(
            self.right_frame,
            placeholder_text="Ім'я",
            placeholder_text_color="#7819b3",
            border_color="#ffffff",
            height=45,
            text_color="#000000",
            corner_radius=25,
            fg_color="#e8c3ff",
            font=("Helvetica", 20, "bold"),
        )
        self.name_entry.pack(fill="x", padx=10, pady=10)

        self.sett_button = CTkButton(
            self.right_frame,
            text="Налаштування",
            height=45,
            corner_radius=25,
            fg_color="#e8c3ff",
            font=("Helvetica", 20, "bold"),
            text_color="#7819b3",
            image=CTkImage(dark_image=Image.open("img\\setting.png"), size=(30, 30)),
            compound="left",
        )
        self.sett_button.pack(fill="x", padx=10, pady=10)

        # todo Додати кнопку увійти
        self.login_button = CTkButton(
            self.right_frame,
            text="Увійти",
            height=45,
            corner_radius=25,
            fg_color="#ed64ff",
            font=("Helvetica", 20, "bold"),
            text_color="#ffffff",
            compound="left",
            command=self.login #!!!!!!!!!!!!!!!!!!!!!!!!!!!
        )
        self.login_button.pack(fill="x", padx=10, pady=10)

    def login(self):
        username = self.name_entry.get().strip() # "Yulia Menes"
        if username == "":
            return
        self.destroy()
        chat = MainWindow(username)
        chat.mainloop()
