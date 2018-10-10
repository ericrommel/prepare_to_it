import Tkinter as tk
import ttk

import Tkconstants, tkFileDialog
from os import path, environ
from string import ascii_letters as alphabet

class MainScreen:

    def __init__(self, master):
        self.username = environ['USERNAME']

        self.Q = '\\europe.prestagroup.com\D1\\04_project_documents'  # Q drive
        ifile = 'Q:\\INT_Gen_EPAS_R10\\11_Measurement\\03_EcuSw\\PolySpace\\PolySpace_4.18.33.0_2018_09_26-13_50_27.zip'
        ifolder = 'Q:\\INT_Gen_EPAS_R10\\11_Measurement\\03_EcuSw\\PolySpace\\'
        # self.master = master
        self.master = master  # tk.Frame(self.master)
        self.master.title('Polyspace Work Environment Preparation tool')
        self.master.geometry('930x200')

        self.lbl_tar_file = tk.Label(self.master, text='TAR.GZ or ZIP file: ')
        self.lbl_tar_file.grid(column=0, row=0)

        self.lbl_work_destination_folder = tk.Label(self.master, text='Work destination folder: ')
        self.lbl_work_destination_folder.grid(column=0, row=1)

        # Combobox with all components #
        # ['<Write down here or press CTRL+CLICK to select more then one>']
        self.lbl_components = tk.Label(self.master, text='Select components: ')
        self.lbl_components.grid(column=0, row=2)

        self.lbox_component = tk.Listbox(self.master, width=90, height=5, selectmode='multiple')
        for i in self.fill_combo():
            self.lbox_component.insert(tk.END, i)

        self.lbox_component.grid(column=1, row=2)

        self.content_txt_targz = tk.StringVar()
        self.content_txt_destination = tk.StringVar()

        self.txt_targz_file = tk.Entry(self.master, textvariable=self.content_txt_targz, width=90)
        self.initial_file = ifile
        self.txt_targz_file.insert(0, self.initial_file)
        self.txt_targz_file.grid(column=1, row=0)

        self.txt_logs_dir = tk.Entry(self.master, textvariable=self.content_txt_destination, width=90)
        self.initial_folder = ifolder
        self.txt_logs_dir.insert(0, self.initial_folder)
        self.txt_logs_dir.grid(column=1, row=1)

        self.txt_targz_file.focus()

        self.btn_choose_trs = tk.Button(
            self.master,
            text=' ... ',
            command=self.open_file_dialog_targz
        ).grid(column=2, row=0)

        self.btn_choose_logs = tk.Button(
            self.master,
            text=' ... ',
            command=self.open_folder_dialog_logs
        ).grid(column=2, row=1)

    def open_file_dialog_targz(self):
        self.master.filename = tkFileDialog.askopenfilename(
            initialdir=path.dirname(self.txt_targz_file.get()),
            title='Select file',
            filetypes=(('tar gz zip files', '*.gz *.zip *.tar'), ('all files', '*.*'))
        )

        if self.master.filename == '' or self.master.filename is None:
            self.master.filename = self.initial_file

        self.content_txt_targz.set(self.master.filename)
        self.txt_targz_file.focus()

    def open_folder_dialog_logs(self):
        self.master.directory = tkFileDialog.askdirectory(
            initialdir=path.dirname(self.txt_logs_dir.get())
        )

        if self.master.directory == '' or self.master.directory is None:
            self.master.directory = self.initial_folder

        self.content_txt_destination.set(self.master.directory)
        self.txt_logs_dir.focus()

    def fill_combo(self):
        comp_list = []
        with open('components.txt') as f:
            for i in f.readlines():
                comp_list.append(i)
        return comp_list

    def find_in_cbox(self, event):
        keypress = event.char.upper()

        components = self.fill_combo()
        if keypress in alphabet:
            for index, comp_name in components:
                if comp_name[0] >= keypress:
                    self.lbox_component.current(index)
                    break

    def callback_combo(event):
        print("method is called")



class Demo2:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text='Quit', width=25, command=self.close_windows)
        self.quitButton.pack()
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()


def main():
    root = tk.Tk()
    app = MainScreen(root)
    root.mainloop()

if __name__ == '__main__':
    main()
