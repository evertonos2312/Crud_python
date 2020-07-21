from tkinter import ttk
from tkinter import *
import sqlite3


class Product(object):
    db_name = 'database.db'

    def __init__(self, window):
        self.wind = window
        self.wind.geometry("409x412+0+0")
        self.wind.title('Ruanzin Lanches')
        self.wind.resizable(0, 0)
        self.wind.iconbitmap('structure/lanche.ico')

        frame = LabelFrame(self.wind, text='Novo Produto: ')
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        Label(frame, text='Nome: ').grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.grid(row=1, column=1)

        Label(frame, text='Preço: ').grid(row=2, column=0)
        self.price = Entry(frame)
        self.price.grid(row=2, column=1)

        ttk.Button(frame, text='Cadastrar Produto', command=self.adding).grid(row=3, columnspan=2, sticky=W + E)
        self.message = Label(text='', fg='red')
        self.message.grid(row=3, column=0)

        self.tree = ttk.Treeview(height=10, column=3)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#0', text='Produto', anchor=CENTER)
        self.tree.heading('#1', text='Preço', anchor=CENTER)
        
        ttk.Button(text='Deletar', command=self.delete).grid(row=5, column=1)
        ttk.Button(text='Editar', command=self.edit).grid(row=5, column=0)
        self.viewing_records()

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
            return query_result

    def viewing_records(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=row[2])

    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def adding(self):
        if self.validation():
            query = 'INSERT INTO product VALUES (NULL, ?, ?)'
            parameters = (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.message['text'] = f'Cadastro efetuado com sucesso'
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
            self.message['text'] = 'FAVOR PREENCHER OS CAMPOS OBRIGATÓRIOS'
        self.viewing_records()

    def delete(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            self.message['text'] = 'Favor selecionar um item cadastrado'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name,))
        self.message['text'] = f'Produto {name} deletado'
        self.viewing_records()

    def edit(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Favor selecionar um item cadastrado'
            return

        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]

        self.edit_wind = Toplevel()
        self.edit_wind.title(f'Editar produto: {name}')

        screen_width = self.edit_wind.winfo_screenwidth()
        screen_height = self.edit_wind.winfo_screenheight()

        width = 220
        height = 110

        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)

        self.edit_wind.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.edit_wind.resizable(0, 0)
        self.edit_wind.configure(bg='snow3')

        Label(self.edit_wind, text='Nome anterior: ', bg='snow3').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=name),
              state='readonly').grid(row=0, column=2)

        Label(self.edit_wind, text='Novo nome:', bg='snow3').grid(row=1, column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1, column=2)

        Label(self.edit_wind, text='Preço anterior: ', bg='snow3').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable=DoubleVar(self.edit_wind, value=old_price),
              state='readonly').grid(row=2, column=2)
        Label(self.edit_wind, text='Novo preço: ', bg='snow3').grid(row=3, column=1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row=3, column=2)

        button = Button(self.edit_wind, bd=2, text='Editar produto',
                        command=lambda: self.edit_records(new_name.get(), name,
                                                          new_price.get(), old_price)).grid(row=4, column=2, sticky=W)
        self.edit_wind.mainloop()

    def edit_records(self, new_name, name, new_price, old_price):
        query = 'UPDATE product SET name=?,price=? WHERE name=? AND price =?'
        parameters = (new_name, new_price, name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = f'Produto {name} editado com sucesso.'
        self.viewing_records()


if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()
