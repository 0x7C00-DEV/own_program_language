from tkinter import *
from tkinter import ttk
import Lexer
from tkinter import filedialog, messagebox
import Parser

class Window(Tk):
    def __init__(self):
        super().__init__()
        self.title('View')
        self.geometry('1000x600')
        # self.resizable(False, False)

        self.current_file = None
        self.tokens = []
        self.asts = []

        self.menu = Menu(self)

        self.file = Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(menu = self.file, label = '文件')
        self.file.add_command(label = '打开', command = self.open_file)
        self.file.add_command(label = '转Token', command = self.convert_token)
        self.file.add_command(label = '转AST', command = self.convert_ast)

        self.notepad = ttk.Notebook(self)
        self.notepad.pack(fill = BOTH, expand = TRUE)

        self.text = Frame(self.notepad)
        self.txt = Text(self.text, font='consolas 10')
        self.txt.pack(fill = BOTH, expand = TRUE)

        self.tokens = Frame(self.notepad)
        self.lis = ttk.Treeview(self.tokens)
        self.lis['columns'] = ('value')
        self.lis.heading('#0', text='类型')
        self.lis.heading('value', text = '值')
        self.lis.pack(fill = BOTH, expand = TRUE)

        self.ast = Frame(self.notepad)
        self.tv = ttk.Treeview(self.ast)
        self.tv.pack(fill = BOTH, expand = TRUE)

        self.notepad.add(self.text, text = 'Text')
        self.notepad.add(self.tokens, text='Token')
        self.notepad.add(self.ast, text = 'AST')

        self.config(menu = self.menu)

    def convert_token(self):
        lexer = Lexer.Lexer(self.txt.get(1.0, END))
        for i in lexer.tokens:
            self.lis.insert('', 'end', text=i.data, values=(i.type))

    def convert_ast(self):
        pass 

    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="选择文件",
            filetypes=[ ("所有文件", "*.*") ]
        )  
        self.current_file = open(file_path, 'r', encoding='UTF-8')
        self.txt.insert(END, self.current_file.read())

def main():
    root = Window()
    root.mainloop()

if __name__ == '__main__':
    main()