import tkinter as tk
from tkinter import messagebox
import json
import os

FILE_NAME = "tasks.json"

# ---------- DATA HANDLING ----------
def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as file:
        return json.load(file)

def save_tasks():
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)

# ---------- APP LOGIC ----------
def add_task():
    title = task_entry.get().strip()
    if not title:
        return

    tasks.append({"title": title, "completed": False})
    task_entry.delete(0, tk.END)
    refresh_tasks()
    save_tasks()

def delete_task():
    selected = task_list.curselection()
    if not selected:
        return
    tasks.pop(selected[0])
    refresh_tasks()
    save_tasks()

def toggle_complete(event):
    selected = task_list.curselection()
    if not selected:
        return
    index = selected[0]
    tasks[index]["completed"] = not tasks[index]["completed"]
    refresh_tasks()
    save_tasks()

def refresh_tasks():
    task_list.delete(0, tk.END)
    for task in tasks:
        status = "✔ " if task["completed"] else "◻ "
        task_list.insert(tk.END, status + task["title"])

# ---------- UI ----------
root = tk.Tk()
root.title("To-Do App")
root.geometry("420x520")
root.configure(bg="#1e1e2f")
root.resizable(False, False)

# Title
tk.Label(
    root,
    text="My Tasks",
    font=("Segoe UI", 20, "bold"),
    bg="#1e1e2f",
    fg="white"
).pack(pady=10)

# Entry Frame
entry_frame = tk.Frame(root, bg="#1e1e2f")
entry_frame.pack(pady=10)

task_entry = tk.Entry(
    entry_frame,
    font=("Segoe UI", 12),
    width=25
)
task_entry.pack(side=tk.LEFT, padx=5)

add_btn = tk.Button(
    entry_frame,
    text="Add",
    font=("Segoe UI", 11),
    bg="#6c63ff",
    fg="white",
    command=add_task
)
add_btn.pack(side=tk.LEFT)

# Listbox Frame
list_frame = tk.Frame(root)
list_frame.pack(pady=10)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

task_list = tk.Listbox(
    list_frame,
    font=("Segoe UI", 12),
    width=35,
    height=15,
    yscrollcommand=scrollbar.set,
    selectbackground="#6c63ff"
)
task_list.pack()

scrollbar.config(command=task_list.yview)

task_list.bind("<Double-Button-1>", toggle_complete)

# Delete Button
delete_btn = tk.Button(
    root,
    text="Delete Selected",
    font=("Segoe UI", 11),
    bg="#ff4d4d",
    fg="white",
    command=delete_task
)
delete_btn.pack(pady=10)

# ---------- LOAD DATA ----------
tasks = load_tasks()
refresh_tasks()

root.mainloop()
