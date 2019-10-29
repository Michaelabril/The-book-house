from tkinter import *
from tkinter import ttk

from tkinter import messagebox as MessageBox

import sqlite3

class Boosk:

    db_name = 'database.db'

    def __init__(self, window):
        # Initializations 
        self.wind = window
        self.wind.title('The Home Books')
        window.config(bg ="SkyBlue1")



        # Creating a frame container
        frame = LabelFrame(self.wind, text = 'Register a new Book')
        frame.grid(row =0, column = 0, columnspan = 3, pady = 20)


        Label(frame, text = 'Name Book: ').grid(row =1, column = 0)
        self.name  = Entry(frame)
        self.name.focus()
        self.name.grid(row =1, column = 1)

        Label(frame, text = 'Author: ').grid(row =2, column = 0)
        self.autor  = Entry(frame)
        self.autor.grid(row =2, column = 1)
        


        Label(frame, text = 'Editorial: ').grid(row =3, column = 0)
        self.edit  = Entry(frame)
        self.edit.grid(row =3, column = 1)
        
        Label(frame, text = 'year of publication: ').grid(row =4, column = 0)
        self.year  = Entry(frame)
        self.year.grid(row =4, column = 1)

        ttk.Button(frame, text = 'Register Book', command = self.add_book ).grid(row = 5, columnspan = 2, sticky = W + E)

        self.message = Label( text = '', fg = 'red', bg= 'black', font = ("Verdana",15),pady=10, )
        self.message.grid(row = 6, column = 0, columnspan = 4, sticky = W + E)   

        self.tree = ttk.Treeview(height =  10, column = 5)
        self.tree.grid ( row = 7, column = 0, columnspan = 4, pady = 20, padx=20)
        self.tree.heading ('#0', text = 'Name Book', anchor = CENTER)
        self.tree.heading ('#1', text = 'Autor', anchor = CENTER)
        self.tree.heading ('#2', text = 'Name', anchor = CENTER)

        #Delete an edit Buttons
        ttk.Button(text = 'Delete', command = self.delete_book).grid(row = 12, column = 0, pady=20)
        ttk.Button(text = 'Update', command =self.edit_book).grid(row = 12, column = 1,pady=20)
        ttk.Button(text = 'Search').grid(row = 12, column = 2,pady=20)


        self.get_products()
 
    def run_query(self,query,parameters = ()):
        with sqlite3.connect(self.db_name) as connection:
          cursor = connection.cursor() 
          result = cursor.execute(query, parameters)
          connection.commit()
        return  result  
    
    def  get_products(self):

        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        query = 'SELECT * FROM  Books ORDER BY name DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], value = row[2])

    def validation(self):
        return len(self.name.get()) != 0 and len(self.autor.get()) != 0
    
    def add_book(self):
        if self.validation():
            query = 'INSERT INTO Books VALUES(NULL, ?, ?)'
            parameters =  (self.name.get(), self.autor.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Book {} added Successfully'.format(self.name.get())
            self.name.delete(0, END)
            self.autor.delete(0, END)
            self.edit.delete(0, END)
            self.year.delete(0, END)
        else:
            MessageBox.showinfo("Alert" , "Book name and Author is Required")
        self.get_products()

    def delete_book(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]

        except IndexError as e:
            MessageBox.showinfo("Alert_Info" , "Please select a record")
            return
        self.message['text'] = ''
        name =self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM Books WHERE name = ?'
        self.run_query(query,  (name, ))
        self.message['text'] = 'The Record {} delete succesfully'. format(name)
        self.get_products()

    def edit_book(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]

        except IndexError as e:
            self.message['text'] = 'Please select a Record '
            return
       
        name = self.tree.item(self.tree.selection())['text']
        autor = self.tree.item(self.tree.selection())['values'][0]

        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit Book'

        # Old Name of Book
        Label(self.edit_wind, text = 'Old Name:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2)
        # New Name
        Label(self.edit_wind, text = 'New Name:').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)

        # Old AUTOR 
        Label(self.edit_wind, text = 'Old Autor:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = autor), state = 'readonly').grid(row = 2, column = 2)
        # New AUTOR
        Label(self.edit_wind, text = 'New Autor:').grid(row = 3, column = 1)
        new_autor= Entry(self.edit_wind)
        new_autor.grid(row = 3, column = 2)

        Button(self.edit_wind, text = 'Update', command = lambda: self.edit_Book(new_name.get(), name, new_autor.get(), autor)).grid(row = 4, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def edit_Book(self, new_name, name, new_autor, autor):
        query = 'UPDATE Books SET name = ?, autor = ? WHERE name = ? AND autor = ?'
        parameters = (new_name, new_autor, name , autor)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} updated successfylly'.format(name)
        self.get_products()
       
if __name__ == '__main__':
    window = Tk()
    application = Boosk(window)
    window.mainloop()

