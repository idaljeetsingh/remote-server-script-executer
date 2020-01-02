"""
    Author      :   Daljeet Singh Chhabra
    Language    :   Python
    File Name   :   main.py
    Date Created    :   28-12-2019
    Last Modified   :   01-01-2020
"""
from PyQt5 import uic, QtWidgets, QtGui
from paramiko import SSHClient, AutoAddPolicy
from os.path import basename
import sys


class Executer(QtWidgets.QMainWindow):
    def __init__(self):
        super(Executer, self).__init__()
        uic.loadUi('Executer.ui', self)
        # self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.execute_button.clicked.connect(self.execute_button_clicked)
        self.script_entry.returnPressed.connect(self.get_script_file)
        self.clear_button.clicked.connect(self.clear_button_clicked)

    def get_script_file(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file')
        if file[0]:
            # print(file[0])
            # print(basename(file[0]))
            self.script_entry.setText(file[0])
        else:
            print('No File Selected')

    def execute_button_clicked(self):
        host = self.host_entry.text()
        port = self.port_entry.text()
        script_path = self.script_entry.text()
        usr = self.username_entry.text()
        pwd = self.password_entry.text()
        as_sudo = self.as_sudo.isChecked()
        self.execute_script(host, port, usr, pwd, script_path, as_sudo)

    def clear_button_clicked(self):
        self.host_entry.setText('')
        self.port_entry.setText('')
        self.script_entry.setText('')
        self.username_entry.setText('')
        self.password_entry.setText('')
        self.server_response.setReadOnly(False)
        self.server_response.setText('')
        self.server_response.setReadOnly(True)
        self.as_sudo.setChecked(False)

    def execute_script(self, host, port, usr, pwd, script_path, as_sudo):
        try:
            # Connect to remote host                                            192.168.195.130
            client = SSHClient()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(host, port=int(port), username=usr, password=pwd)
            try:
                # Setup sftp connection and transmit this script
                sftp = client.open_sftp()
                sftp.put(script_path, f'/tmp/{basename(script_path)}')
                sftp.close()
                path_to_script_on_server = '/tmp/' + basename(script_path)
                if as_sudo:  # Script will be executed as sudo
                    try:
                        stdin, stdout, stderr = client.exec_command('sudo chmod +x ' + path_to_script_on_server)
                        stdin.write(pwd + '\n')
                        stdin.flush()

                        stdin, stdout, stderr = client.exec_command('sudo ' + path_to_script_on_server, get_pty=True)
                        stdin.write(pwd + '\n')
                        stdin.flush()

                        output = stdout.read().splitlines()
                        self.server_response.setReadOnly(False)
                        for line in range(1, len(output)):
                            # Process each line in the remote output
                            # print(str(output[line], 'utf-8'))
                            self.server_response.append(str(output[line], 'utf-8'))
                        stdout.flush()
                        self.server_response.setReadOnly(True)
                        client.close()
                    except:
                        print('Error executing the script as SUDO')
                else:  # Script will be executed without root
                    try:
                        stdout = client.exec_command('chmod +x ' + path_to_script_on_server)
                        stdout = client.exec_command(path_to_script_on_server)[1]
                        self.server_response.setReadOnly(False)
                        for line in stdout:
                            # Process each line in the remote output
                            # print(line)
                            self.server_response.append(str(line))
                        client.close()
                        self.server_response.setReadOnly(True)
                    except:
                        print('Error executing the script.')
            except:
                print('Error making SFTP connection')
        except:
            print('Connection to SSH server failed')


app = QtWidgets.QApplication(sys.argv)
window = Executer()
window.show()
sys.exit(app.exec_())
