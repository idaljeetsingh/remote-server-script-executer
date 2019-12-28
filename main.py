"""
    Author      :   Daljeet Singh Chhabra
    Language    :   Python
    File Name   :   main.py
    Date Created    :   28-12-2019
    Last Modified   :   28-12-2019
"""

from tkinter import Entry, Label, StringVar, Tk, Listbox, Scrollbar, Button, END
import paramiko


def view_command():
    server_response.delete(0, END)
    # Connect to remote host
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host_text.get(), username=uname_text.get(), password=password_text.get())

    # SSHClient.exec_command() returns the tuple (stdin,stdout,stderr)
    try:
        stdout = client.exec_command(script_path_text.get())[1]
        for line in stdout:
            # Process each line in the remote output
            # print(line)
            server_response.insert(END, line)
    except:
        print('Execution failed')
    client.close()
    server_response.insert(END)


window = Tk()
window.title("Server Script Executer")

host = Label(window, text="Host")
host.grid(row=0, column=0)

host_text = StringVar()
host_entry = Entry(window, textvariable=host_text)
host_entry.grid(row=0, column=1)

script_path_label = Label(window, text="Script Path")
script_path_label.grid(row=0, column=3)

script_path_text = StringVar()
script_path_entry = Entry(window, textvariable=script_path_text)
script_path_entry.grid(row=0, column=4)

uname_label = Label(window, text="Username")
uname_label.grid(row=1, column=0)

uname_text = StringVar()
uname_entry = Entry(window, textvariable=uname_text)
uname_entry.grid(row=1, column=1)

password_label = Label(window, text="Password")
password_label.grid(row=1, column=3)

password_text = StringVar()
password_entry = Entry(window, textvariable=password_text)
password_entry.grid(row=1, column=4)

server_response = Listbox(window, height=10, width=40)
server_response.grid(row=3, column=0, rowspan=6, columnspan=3)

s_bar = Scrollbar(window)
s_bar.grid(row=2, column=3, rowspan=6)

server_response.configure(yscrollcommand=s_bar.set)
s_bar.configure(command=server_response.yview)

# server_response.bind('<<ListboxSelect>>', get_selected_row)

execute_button = Button(window, text="Execute", width=12, command=view_command)
execute_button.grid(row=3, column=4)

window.mainloop()
