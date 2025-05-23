import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import random

CONFIG_FILE = "config.fgc"
save_directory = os.getcwd()
default_resolution = "880x640"
default_theme = "dark"

def parse_config_line(line):
    if "=" in line:
        key, value = line.strip().split("=", 1)
        return key.strip(), value.strip()
    return None, None

def load_config():
    global save_directory, default_resolution
    if not os.path.exists(CONFIG_FILE):
        return
    try:
        with open(CONFIG_FILE, "r") as f:
            for line in f:
                key, value = parse_config_line(line)
                if key == "saveDirectory":
                    if os.path.exists(value):
                        save_directory = value
                elif key == "theme":
                    ctk.set_appearance_mode(value)
                elif key == "windowResolution":
                    default_resolution = value.replace("px", "")
    except Exception as e:
        messagebox.showerror("Ошибка загрузки настроек", str(e))

def save_config():
    try:
        with open(CONFIG_FILE, "w") as f:
            f.write(f"saveDirectory = {save_directory}\n")
            f.write(f"theme = {ctk.get_appearance_mode()}\n")
            f.write(f"windowResolution = {app.winfo_width()}x{app.winfo_height()}px\n")
    except Exception as e:
        messagebox.showerror("Ошибка сохранения настроек", str(e))

def choose_directory():
    global save_directory
    selected_dir = filedialog.askdirectory()
    if selected_dir:
        save_directory = selected_dir
        dir_label.configure(text=f"📂 Сохранять в: {save_directory}")
        save_config()

def create_file(name, ext):
    if not name or not ext:
        messagebox.showerror("Ошибка", "Имя и расширение не могут быть пустыми.")
        return
    filename = os.path.join(save_directory, f"{name}.{ext.lstrip('.')}")
    try:
        with open(filename, 'w') as f:
            f.write("")
        messagebox.showinfo("Успех", f"✅ Файл '{filename}' создан.")
        save_config()
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def create_corrupted_file(name, ext, size_value, size_unit):
    if not name or not ext:
        messagebox.showerror("Ошибка", "Имя и расширение не могут быть пустыми.")
        return
    try:
        size = int(size_value)
        if size <= 0:
            raise ValueError
        if size_unit == "КБ":
            size *= 1024
        elif size_unit == "МБ":
            size *= 1024 * 1024
    except ValueError:
        messagebox.showerror("Ошибка", "Размер файла должен быть положительным числом.")
        return

    filename = os.path.join(save_directory, f"{name}.{ext.lstrip('.')}")
    try:
        with open(filename, 'wb') as f:
            f.write(os.urandom(size))
        messagebox.showinfo("Успех", f"💾 Битый файл '{filename}' размером {size_value} {size_unit} создан.")
        save_config()
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

# Загрузка конфигурации до создания окна
load_config()

# Главное окно
app = ctk.CTk()
app.title("Генератор файлов")
app.geometry(default_resolution)
app.minsize(700, 500)

# Шапка
header = ctk.CTkLabel(app, text="🛠 Генератор файлов", font=ctk.CTkFont(size=24, weight="bold"))
header.pack(pady=10)

# Блок выбора папки
dir_frame = ctk.CTkFrame(app, corner_radius=12)
dir_frame.pack(pady=10, padx=20, fill="x")

choose_btn = ctk.CTkButton(dir_frame, text="📁 Выбрать папку", width=150, command=choose_directory)
choose_btn.pack(side="left", padx=20, pady=10)

dir_label = ctk.CTkLabel(dir_frame, text=f"📂 Сохранять в: {save_directory}", anchor="w")
dir_label.pack(side="left", padx=10, pady=10)

# Переключение темы
def change_theme(theme):
    ctk.set_appearance_mode(theme)
    save_config()

theme_menu = ctk.CTkOptionMenu(app, values=["light", "dark", "system"], command=change_theme)
theme_menu.set(ctk.get_appearance_mode())
theme_menu.pack(pady=5)

# Вкладки
tabs = ctk.CTkTabview(app, segmented_button_selected_color="#5ba160")
tabs.pack(padx=20, pady=20, fill="both", expand=True)

file_tab = tabs.add("📄 Обычные файлы")
corrupt_tab = tabs.add("🧨 Битые файлы")

def add_inputs(tab, is_corrupt=False):
    frame = ctk.CTkFrame(tab, corner_radius=12)
    frame.pack(pady=30, padx=30, fill="x")

    title = "Создание обычного файла" if not is_corrupt else "Создание битого файла"
    ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(10, 15))

    name_entry = ctk.CTkEntry(frame, placeholder_text="Имя файла")
    name_entry.pack(pady=10, padx=20, fill="x")

    ext_entry = ctk.CTkEntry(frame, placeholder_text="Расширение (например, txt)")
    ext_entry.pack(pady=10, padx=20, fill="x")

    if is_corrupt:
        size_entry = ctk.CTkEntry(frame, placeholder_text="Размер (число)")
        size_entry.pack(pady=10, padx=20, fill="x")

        size_unit = ctk.CTkComboBox(frame, values=["Б", "КБ", "МБ"], width=100)
        size_unit.set("КБ")
        size_unit.pack(pady=10)

        btn = ctk.CTkButton(frame, text="💣 Создать битый файл", height=40, fg_color="#d9534f", hover_color="#c9302c",
                            command=lambda: create_corrupted_file(
                                name_entry.get(), ext_entry.get(), size_entry.get(), size_unit.get()))
        btn.pack(pady=20)
    else:
        btn = ctk.CTkButton(frame, text="📝 Создать файл", height=40, fg_color="#5cb85c", hover_color="#4cae4c",
                            command=lambda: create_file(name_entry.get(), ext_entry.get()))
        btn.pack(pady=20)

add_inputs(file_tab, is_corrupt=False)
add_inputs(corrupt_tab, is_corrupt=True)

app.mainloop()
