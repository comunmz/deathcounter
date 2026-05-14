import tkinter as tk
from tkinter import simpledialog, messagebox
import keyboard
import json
import os

DATA_FILE = "boss_tries.json"

TEXTS = {
    "es": {
        "tries": "Tries",
        "select": "Seleccionar Jefe Guardado",
        "manager": "Gestor de Jefes (Historial)",
        "reset": "Resetear Tries",
        "close": "Cerrar y Guardar",
        "lang": "Cambiar a Inglés (English)",
        "no_bosses": "No hay jefes guardados",
        "history_title": "Historial de Jefes",
        "add_boss": "Añadir Nuevo Jefe",
        "new_boss_title": "Nuevo Jefe",
        "new_boss_prompt": "Nombre del nuevo jefe:",
        "close_btn": "Cerrar",
        "delete_confirm": "¿Seguro que quieres borrar a {}?",
        "default_boss": "Jefe"
    },
    "en": {
        "tries": "Tries",
        "select": "Select Saved Boss",
        "manager": "Boss Manager (History)",
        "reset": "Reset Tries",
        "close": "Save and Close",
        "lang": "Change to Spanish (Español)",
        "no_bosses": "No saved bosses",
        "history_title": "Boss History",
        "add_boss": "Add New Boss",
        "new_boss_title": "New Boss",
        "new_boss_prompt": "Name of the new boss:",
        "close_btn": "Close",
        "delete_confirm": "Are you sure you want to delete {}?",
        "default_boss": "Boss"
    }
}

class HollowCounter:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True) 
        self.root.attributes("-topmost", True)
        self.root.config(bg="black")
        self.root.geometry("180x60+100+100")

        self.data = self.load_data()
        self.lang = self.data.get("language", "es")
        self.current_boss = self.data.get("current_boss", TEXTS[self.lang]["default_boss"])
        
        
        if "bosses" not in self.data:
            self.data["bosses"] = {}
            
        self.count = self.data["bosses"].get(self.current_boss, 0)
        
        self.font_style = ("Times New Roman", 26, "bold")
        
        self.label = tk.Label(
            root, 
            text=f"{TEXTS[self.lang]['tries']}: {self.count}", 
            font=self.font_style, 
            fg="white", 
            bg="black"
        )
        self.label.pack(expand=True, fill="both")

        keyboard.add_hotkey('up', self.increment)
        keyboard.add_hotkey('down', self.decrement)
        keyboard.add_hotkey('end', self.save_and_close)

        self.label.bind("<ButtonPress-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)
        self.label.bind("<Button-3>", self.show_menu)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        return {"current_boss": "Jefe", "bosses": {}, "language": "es"}

    def save_data(self):
        if "bosses" not in self.data:
            self.data["bosses"] = {}
        self.data["bosses"][self.current_boss] = self.count
        self.data["current_boss"] = self.current_boss
        self.data["language"] = self.lang
        with open(DATA_FILE, "w") as f:
            json.dump(self.data, f, indent=4)

    def increment(self):
        self.count += 1
        self.update_display()
        self.save_data()

    def decrement(self):
        if self.count > 0:
            self.count -= 1
            self.update_display()
            self.save_data()

    def update_display(self):
        self.label.config(text=f"{TEXTS[self.lang]['tries']}: {self.count}")

    def toggle_language(self):
        self.lang = "en" if self.lang == "es" else "es"
        self.update_display()
        self.save_data()

    def show_menu(self, event):
        t = TEXTS[self.lang]
        self.menu = tk.Menu(self.root, tearoff=0, bg="black", fg="white")
        
        
        boss_menu = tk.Menu(self.menu, tearoff=0, bg="black", fg="white")
        bosses_dict = self.data.get("bosses", {})
        
        if bosses_dict:
            for boss in bosses_dict.keys():
                boss_menu.add_command(label=f"{boss} ({bosses_dict[boss]})", 
                                      command=lambda b=boss: self.select_boss(b))
        else:
            boss_menu.add_command(label=t["no_bosses"], state="disabled")

        
        self.menu.add_cascade(label=t["select"], menu=boss_menu)
        self.menu.add_command(label=t["add_boss"], command=self.add_new_boss) # <-- BOTÓN AÑADIDO
        self.menu.add_command(label=t["manager"], command=self.open_boss_manager)
        self.menu.add_separator()
        self.menu.add_command(label=t["lang"], command=self.toggle_language)
        self.menu.add_command(label=t["reset"], command=self.reset_tries)
        self.menu.add_command(label=t["close"], command=self.save_and_close)
        
        self.menu.tk_popup(event.x_root, event.y_root)

    def select_boss(self, boss_name):
        self.current_boss = boss_name
        self.count = self.data["bosses"].get(boss_name, 0)
        self.update_display()
        self.save_data()
            
    def open_boss_manager(self):
        t = TEXTS[self.lang]
        manager = tk.Toplevel(self.root)
        manager.title(t["history_title"])
        manager.geometry("320x450")
        manager.config(bg="black")
        manager.attributes("-topmost", True)
        
        tk.Label(manager, text=t["history_title"], font=(self.font_style[0], 14), bg="black", fg="white").pack(pady=10)
        
        canvas = tk.Canvas(manager, bg="black", highlightthickness=0)
        scrollbar = tk.Scrollbar(manager, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="black")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")
        
        for boss, tries in list(self.data.get("bosses", {}).items()):
            row = tk.Frame(scrollable_frame, bg="black")
            row.pack(fill="x", pady=2)
            
            tk.Button(row, text=" X ", bg="#440000", fg="white", font=("Arial", 8, "bold"),
                      relief="flat", command=lambda b=boss: self.delete_boss(b, manager)).pack(side="left", padx=5)
            
            tk.Label(row, text=boss, bg="black", fg="white", font=("Times New Roman", 10), anchor="w").pack(side="left", expand=True, fill="x")
            tk.Label(row, text=str(tries), bg="black", fg="red", font=("Times New Roman", 10, "bold")).pack(side="right", padx=5)
                
        tk.Button(manager, text=t["add_boss"], bg="#333", fg="white", relief="flat",
                  command=lambda: self.add_new_boss(manager)).pack(pady=5, fill="x", padx=20)
        tk.Button(manager, text=t["close_btn"], bg="#333", fg="white", relief="flat",
                  command=manager.destroy).pack(pady=5, fill="x", padx=20)

    def delete_boss(self, boss_name, window):
        t = TEXTS[self.lang]
        if messagebox.askyesno("Confirm", t["delete_confirm"].format(boss_name)):
            if boss_name in self.data["bosses"]:
                del self.data["bosses"][boss_name]
            
            if self.current_boss == boss_name:
                remaining = list(self.data["bosses"].keys())
                if remaining:
                    self.current_boss = remaining[0]
                    self.count = self.data["bosses"][self.current_boss]
                else:
                    self.current_boss = t["default_boss"]
                    self.count = 0
                self.update_display()
            
            self.save_data()
            window.destroy()
            self.open_boss_manager()

    def add_new_boss(self, window=None):
        t = TEXTS[self.lang]
        
        parent_win = window if window else self.root
        new_boss = simpledialog.askstring(t["new_boss_title"], t["new_boss_prompt"], parent=parent_win)
        
        if new_boss and new_boss.strip() != "":
            name = new_boss.strip()
            
            if name not in self.data["bosses"]:
                self.data["bosses"][name] = 0
            
            self.current_boss = name
            self.count = self.data["bosses"][name]
            self.update_display()
            self.save_data()
            
            
            if window and window != self.root:
                window.destroy()
                self.open_boss_manager()
            
    def reset_tries(self):
        self.count = 0
        self.update_display()
        self.save_data()
        
    def save_and_close(self):
        self.save_data()
        self.root.destroy()

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HollowCounter(root)
    root.mainloop()
