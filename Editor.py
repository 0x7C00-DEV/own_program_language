from tkinter import *
import tkinter.ttk as tk
import tkinter.font as tf
import os

class TerminalWidget(Text):
    def __init__(self, master, *a, **b):
        super().__init__(master, *a, **b)
        self.buffer = ''

class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title(f'{os.getcwd()}')
        self.geometry('1000x600')
        self.main_pw = tk.PanedWindow(self, orient='horizontal')
        self.left_frame = tk.Frame(self.main_pw)
        self.left_struct = tk.PanedWindow(self, orient='vertical')
        self.file_view = tk.Treeview(self.left_frame)
        self.file_text = tk.Notebook(self.left_struct)
        self.terminal_s = tk.Notebook(self.left_struct)
        # setup menu
        self.menu = Menu(self)
        self.file = Menu(self.menu, tearoff=0)
        self.edit = Menu(self.menu, tearoff=0)
        self.run  = Menu(self.menu, tearoff=0)
        self.setup_ui()

    def setup_ui(self):
        self.main_pw.pack(fill = BOTH, expand=True)
        self.file_view.pack(fill='both', expand=True)
        self.main_pw.add(self.left_frame, weight=1)
        self.main_pw.add(self.left_struct, weight=4)
        self.left_struct.add(self.file_text, weight=7)
        self.left_struct.add(self.terminal_s, weight=3)
        self.menu.add_cascade(label='文件', menu=self.file)
        self.menu.add_cascade(label='编辑', menu=self.edit)
        self.menu.add_cascade(label='运行', menu=self.run)

        self.file.add_command(label='打开', command=self.open_file)
        self.file.add_command(label='保存', command=self.save_current_file)
        self.file.add_command(label='保存所有', command=self.save_all_file)

        self.edit.add_command(label='设置', command=self.open_config_window)
        self.edit.add_command(label='新建终端', command=self.new_terminal)

        self.run.add_command(label='在终端中运行', command=self.run_in_terminal)
        self.run.add_command(label='在外部终端中运行', command=self.run_in_extern_console)

        self.config(menu = self.menu)
        # self.add_test_widgets()

    def add_test_widgets(self):
        for i in range(1, 6):
            self.file_view.insert('', 'end', text=f'文件{i}.py')
        self.file_text.add(tk.Frame(self.file_text), text='main.py')
        self.file_text.add(tk.Frame(self.file_text), text='utils.py')
        self.terminal_s.add(tk.Frame(self.terminal_s), text='终端')
        self.terminal_s.add(tk.Frame(self.terminal_s), text='输出')

    def open_file(self):
        pass

    def save_current_file(self):
        pass

    def save_all_file(self):
        pass

    def open_config_window(self):
        pass

    def new_terminal(self):
        pass

    def run_in_terminal(self):
        pass

    def run_in_extern_console(self):
        pass

if __name__ == '__main__':
    m = MainWindow()
    m.mainloop()