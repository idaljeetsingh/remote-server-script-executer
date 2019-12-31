"""
    Author      :   Daljeet Singh Chhabra
    Language    :   Python
    File Name   :   main.py
    Date Created    :   28-12-2019
    Last Modified   :   31-12-2019
"""

from tkinter import Entry, Label, StringVar, Tk, Listbox, Scrollbar, Button, END
from paramiko import SSHClient, AutoAddPolicy, sftp
from tkinter.filedialog import askopenfile
from os.path import basename

local_script_path = None


def view_command():
    server_response.delete(0, END)
    # Connect to remote host
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(host_text.get(), username=uname_text.get(), password=password_text.get())

    # SSHClient.exec_command() returns the tuple (stdin,stdout,stderr)
    try:
        global local_script_path

        # Setup sftp connection and transmit this script
        sftp = client.open_sftp()
        sftp.put(local_script_path.name, f'/tmp/{basename(local_script_path.name)}')
        sftp.close()
        path_to_script_on_server = '/tmp/' + basename(local_script_path.name)
        try:
            stdout = client.exec_command('chmod +x ' + path_to_script_on_server)
            stdout = client.exec_command(path_to_script_on_server)[1]
            for line in stdout:
                # Process each line in the remote output
                # print(line)
                server_response.insert(END, line)
        except:
            print('Error executing the script')
    except:
        print('Execution failed')
    client.close()
    server_response.insert(END)


def file_picker():
    global local_script_path
    local_script_path = askopenfile()
    script_path_entry.delete(0, END)
    script_path_entry.insert(END, local_script_path.name)
    # print(local_script_path.name)


def clear():
    host_entry.delete(0, END)
    script_path_entry.delete(0, END)
    uname_entry.delete(0, END)
    password_entry.delete(0, END)
    server_response.delete(0, END)

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

file_picker = Button(window, text="Select", width=5, command=file_picker)
file_picker.grid(row=0, column=6)

uname_label = Label(window, text="Username")
uname_label.grid(row=1, column=0)

uname_text = StringVar()
uname_entry = Entry(window, textvariable=uname_text)
uname_entry.grid(row=1, column=1)

password_label = Label(window, text="Password")
password_label.grid(row=1, column=3)

password_text = StringVar()
password_entry = Entry(window, textvariable=password_text)
password_entry.config(show='*')
password_entry.grid(row=1, column=4)

server_response = Listbox(window, height=10, width=40)
server_response.grid(row=3, column=0, rowspan=6, columnspan=3)

s_bar = Scrollbar(window)
s_bar.grid(row=2, column=3, rowspan=6)

server_response.configure(yscrollcommand=s_bar.set)
s_bar.configure(command=server_response.yview)

# server_response.bind('<<ListboxSelect>>', get_selected_row)

execute_button = Button(window, text="Execute", width=12, command=view_command)
execute_button.grid(row=4, column=4)

clear_button = Button(window, text="Clear", width=5, command=clear)
clear_button.grid(row=5, column=4)

window.mainloop()
