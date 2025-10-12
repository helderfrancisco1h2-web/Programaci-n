import tkinter as tk
from tkinter import ttk

agenda = []

def add():
    name = input_name.get().strip()
    phone = input_phone.get().strip()
    if name and phone:
        id = len(agenda) + 1
        agenda.append([id, name, phone])
        update()
        input_name.delete(0, tk.END)
        input_phone.delete(0, tk.END)

def update():
    for elem in tree_agenda.get_children():
        tree_agenda.delete(elem)
    for contact in agenda:
        tree_agenda.insert("", "end", values=(contact[0], contact[1], contact[2]))

def remove_selected():
    selected = tree_agenda.selection()
    if selected:
        contact = tree_agenda.item(selected, "values")
        contact_id = int(contact[0])
        for c in agenda:
            if c[0] == contact_id:
                agenda.remove(c)
                break
        tree_agenda.delete(selected)

def update_selected():
    selected = tree_agenda.selection()
    if selected:
        name = input_name.get().strip()
        phone = input_phone.get().strip()
        contact = tree_agenda.item(selected, "values")
        contact_id = int(contact[0])
        for i, c in enumerate(agenda):
            if c[0] == contact_id:
                agenda[i] = [contact_id, name or c[1], phone or c[2]]
                break
        update()


win = tk.Tk()
win.geometry("600x400")
win.configure(bg="#04ddfa")
win.title("Agenda de prueba")


style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
                background="#f0ffff",
                foreground="black",
                rowheight=25,
                fieldbackground="#f0ffff")
style.map("Treeview", background=[('selected', "#00e1ff")])


label_name = tk.Label(win, text="Nombre:", bg="#00eeff", fg="red")
label_name.pack()
input_name = tk.Entry(win)
input_name.pack(pady=(0, 10))

label_phone = tk.Label(win, text="Teléfono:", bg="#0bdcf7", fg="red")
label_phone.pack()
input_phone = tk.Entry(win)
input_phone.pack(pady=(0, 10))

frame_buttons = tk.Frame(win, bg="#04ddfa")
frame_buttons.pack(pady=10)

btn_add = tk.Button(frame_buttons, text="Añadir", command=add)
btn_add.grid(row=0, column=0, padx=5)

btn_update = tk.Button(frame_buttons, text="Actualizar", command=update_selected)
btn_update.grid(row=0, column=1, padx=5)

btn_remove = tk.Button(frame_buttons, text="Borrar", command=remove_selected)
btn_remove.grid(row=0, column=2, padx=5)


tree_agenda = ttk.Treeview(win, columns=("id", "name", "phone"), show="headings")
tree_agenda.pack(pady=20, fill="x")

tree_agenda.heading("id", text="ID")
tree_agenda.heading("name", text="Nombre")
tree_agenda.heading("phone", text="Teléfono")

tree_agenda.column("id", anchor="center", width=50)
tree_agenda.column("name", anchor="center", width=200)
tree_agenda.column("phone", anchor="center", width=150)

win.mainloop()
