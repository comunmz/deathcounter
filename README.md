## **DEPENDENCIES**

* **Python**
* `tkinter` (Standard library)
* `keyboard`
* `json` (Standard library)
* `os` (Standard library)

**Install via pip:**

```bash
pip install keyboard

```

---

## **DESCRIPTION**

A **Death Counter** for those who enjoy playing difficult video games. I needed one for myself and, after noticing there weren't many options available, I decided to build my own.

### **Setup & Customization**

* **Visuals:** For a cleaner look, it is recommended to have the **Times New Roman** font installed.
* **Installation:** Place the `.py` file in your preferred folder and run it using:
```bash
python deathcounter.py

```



🛠️ Requirements & Installation
Python 3.x: Make sure you have Python installed on your system.

Dependencies: Install the required library by running:

Bash
pip install keyboard
Fonts: The application uses Times New Roman by default.


📁 Data Persistence
When you run the app for the first time, a file named boss_tries.json will be automatically created in the same folder. This file stores:

Your list of saved bosses and their respective try counts.

The current boss you are tracking.

Your language preference (English/Spanish).

Note: Do not delete this file if you want to keep your stats!

⌨️ Controls
Up Arrow: Add +1 try.

Down Arrow: Subtract -1 try.

End Key: Save progress and close the app.

Left Click: Drag and move the counter anywhere on your screen.

Right Click: Open the management menu (Change boss, delete, language, etc.).


### **Features**

* **Language Support:** Right-click anywhere on the counter to switch between **Spanish** and **English**.
* **Boss Management:** Includes options to add new bosses and a selection menu to switch between them.
* **Auto-Save:** If you close the counter using the **"Close and Save"** button, a `.json` file will be generated. This file stores your boss list and attempt counts so you can pick up right where you left off the next time you play.

Enjoy! :)

```
