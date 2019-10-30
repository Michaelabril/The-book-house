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
        window.config(bg ="light slate gray")
        
        # Creating a frame container
        frame = LabelFrame(self.wind, text = 'Register a new Book')
        frame.grid(row =0, column = 0, columnspan = 3, pady = 20)

        Label(frame, text = 'Author: ').grid(row =1, column = 0)
        self.autor  = Entry(frame)
        self.autor.focus()
        self.autor.grid(row =1, column = 1)

        Label(frame, text = 'Name Book: ').grid(row =2, column = 0)
        self.name  = Entry(frame)
        self.name.grid(row =2, column = 1)

        Label(frame, text = 'Editorial: ').grid(row =3, column = 0)
        self.edit  = Entry(frame)
        self.edit.grid(row =3, column = 1)
        
        Label(frame, text = 'year of publication: ').grid(row =4, column = 0)
        self.year  = Entry(frame)
        self.year.grid(row =4, column = 1)

        ttk.Button(frame, text = 'Register Book', command = self.add_book ).grid(row = 5, columnspan = 2, sticky = W + E)
        
        self.message = Label( text = '', fg = 'red', bg= 'black', font = ("Verdana",15),pady=10, )
        self.message.grid(row = 6, column = 0, columnspan = 4, sticky = W + E)   

        self.tree = ttk.Treeview(height =  10, column = ("#0", "#1", "#2", "#3"))
        self.tree.grid ( row = 7, column = 0, columnspan = 4, pady = 20, padx=20)
        self.tree.heading ('#0', text = 'ID', anchor = CENTER)
        self.tree.heading ('#1', text = 'Author Name', anchor = CENTER)
        self.tree.heading ('#2', text = 'Book Name', anchor = CENTER)
        self.tree.heading ('#3', text = 'Editorial', anchor = CENTER)
        self.tree.heading ('#4', text = 'Year of publication', anchor = CENTER)

        #Delete an edit Buttons
        ttk.Button(text = 'Delete', command = self.delete_book).grid(row = 12, column = 1, pady=20, padx =5, sticky = W + E)
        ttk.Button(text = 'Update', command =self.edit_book).grid(row = 12, column = 2,pady=20, padx =5, sticky = W + E)
        ttk.Button(text = 'View', command = self.get_products).grid(row = 13, column = 1, pady= 20, padx =5, sticky = W + E)
        ttk.Button(text = 'Search', command = self.search_book).grid(row = 13, column = 2, pady= 20, padx =5, sticky = W + E)
        self.buscar  = Entry(window)
        self.buscar.grid(row =13, column = 3 , sticky = W + E, padx = 5)


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
            self.tree.insert('', "end", text =  row[0], values = (row[1] , row[2] , row[3], row[4] ))

    def validation(self):
        return len(self.name.get()) != 0 and len(self.autor.get()) != 0
    
    def add_book(self):
        if self.validation():
            query = 'INSERT INTO Books VALUES(NULL, ?, ?, ?, ?)'
            parameters =  (self.autor.get(), self.name.get(), self.edit.get(), self.year.get())
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
            self.tree.item(self.tree.selection())['values'][0]

        except IndexError as e:
            MessageBox.showinfo("Alert_Info" , "Please select a record")
            return
        self.message['text'] = ''
        name =self.tree.item(self.tree.selection())['values'][0]
    
        query = 'DELETE FROM Books WHERE name = ?'
        self.run_query(query,  (name, ))
        self.message['text'] = 'The Record {} delete succesfully'. format(name)
        self.get_products()

    def edit_book(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]

        except IndexError as e:
            MessageBox.showinfo("Alert_Info" , "Please select a record")
            return
       
        name = self.tree.item(self.tree.selection())['values'][0]
        autor = self.tree.item(self.tree.selection())['values'][1]
        editorial = self.tree.item(self.tree.selection())['values'][2]
        year = self.tree.item(self.tree.selection())['values'][3]

        self.edit_wind = Toplevel()
        self.edit_wind.geometry("400x350")
        self.edit_wind.title = ("Edit Book")

        # Old AUTOR 
        Label(self.edit_wind, text = 'Autor:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2, pady = 10 )
        # New AUTOR
        Label(self.edit_wind, text = 'New Autor:').grid(row = 1, column = 1)
        new_autor= Entry(self.edit_wind)
        new_autor.grid(row = 1, column = 2)
    
        # Old Name of Book
        Label(self.edit_wind, text = 'Book Name:').grid(row = 3, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = autor), state = 'readonly').grid(row = 3, column = 2, pady = 10,  )
        # New Name
        Label(self.edit_wind, text = 'New Name:').grid(row = 4, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 4, column = 2)

        #old Editorial
        Label(self.edit_wind, text= 'Editorial').grid(row=5, column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = editorial), state = 'readonly').grid(row = 5, column = 2, pady = 10 )
        #newEditorial
        Label(self.edit_wind, text = 'New Editorial:').grid(row = 6, column = 1)
        new_editorial = Entry(self.edit_wind)
        new_editorial.grid(row = 6, column = 2)

        #old Year 
        Label(self.edit_wind, text= 'Year of Publication ').grid(row=7, column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = year), state = 'readonly').grid(row = 7, column = 2, pady = 10)
        #NewYear
        Label(self.edit_wind, text = 'New Year of Publication:').grid(row = 8, column = 1, padx = 20)
        new_year = Entry(self.edit_wind)
        new_year.grid(row = 8, column = 2 )

        Button(self.edit_wind, text = 'Update', command = lambda: self.edit_Book(new_name.get(), name, new_autor.get(), autor, new_editorial.get(), editorial, new_year.get(), year)).grid(row = 9, column = 2, pady = 20 , sticky = W)
        self.edit_wind.mainloop()

    def edit_Book(self, new_name, name, new_autor, autor, new_editorial, editorial, new_year, year):
        
        query = 'UPDATE Books SET name = ?, autor = ?, editorial = ?, year_pub = ? WHERE name = ? AND autor = ? AND editorial = ? AND  year_pub = ?'
        parameters = (new_name, new_autor, new_editorial, new_year, name , autor, editorial, year)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} updated successfylly'.format(name)
        self.get_products()

    def search_book(self):
        self.message['text'] = ''
        search = self.buscar.get()
        if search:
            records = self.tree.get_children()
            for element in records:
                self.tree.delete(element)
            query = f'SELECT * FROM Books WHERE autor LIKE "{search}%" OR name LIKE "{search}%" OR editorial LIKE "{search}%" OR year_pub LIKE "{search}%"'
            db_rows = self.run_query(query)
            for row in db_rows:    
                self.tree.insert('', "end", text =  row[0], values = (row[1] , row[2] , row[3], row[4]))
        else: 
            MessageBox.showinfo("Alert_Info" , "Please Insert a record")
        self.buscar.delete(0, END)  
       
if __name__ == '__main__':
    window = Tk()
    application = Boosk(window)
    window.mainloop()

