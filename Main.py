from tkinter import *
from tkinter import ttk
import os
from tkinter import tix
from tkinter import messagebox
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import base64
import pyodbc
from PIL import ImageTk, Image
import time
from tkinter import Tk, font
from mascaraEntry import *

#configs
os.system('cls')
root2 = Tk()

#variaveis de controle
bt_widht = 0.1
bt_height = 0.04
btColor = '#a84b60'
#fonte
fontSize = 15
fontType = 'Ramajara'

class dataBase():
    def connectDB(self):
        self.conn = (
            'Driver={SQL Server};'
            'Server=DESKTOP-C337USR\SQLEXPRESS;'
            'Database=Controle_de_Estoque;'
        )
        
        self.connect = pyodbc.connect(self.conn)
        self.cursor = self.connect.cursor()
        print('Conexão feita com suscesso!')

    def disconnectDB(self):
        self.connect.close()
        print('Desconectado com suscesso!')

class funcs(dataBase):
    def variavelGET(self):
        self.registration = self.input_registration.get()
        self.price = self.input_price.get()
        self.product_name = self.input_product_name.get()
        self.type = self.tipvar.get()
        self.product_size = self.input_product_size.get()
        self.qtd = self.input_qtd.get()
        self.typeSearch = self.tipvar1.get()
    
    def insertTrueview(self, command):
        row = self.cursor.fetchone()
        while row:
            self.trueview.insert("", END, value = str(row[0]) + ' ' + str(row[1]) + ' ' + str(row[2])+ ' ' + str(row[3])+ ' ' + str(row[4]) + ' ' + str(row[5]))
            row = self.cursor.fetchone()

        for i in command:
            self.trueview.insert("", END, values=i) 
        
    def openFV(self):
        self.service = Service(ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=self.service)

        self.browser.maximize_window()
        self.browser.get('https://fv.tupperware.com.br/#!/')
        self.browser.implicitly_wait(100)
        self.browser.find_element('xpath', '//*[@id="input_0"]').send_keys('00000')
        self.browser.find_element('xpath', '//*[@id="input_1"]').send_keys('00000')
        self.browser.find_element('xpath', '//*[@id="login-view"]/div[1]/div[2]/div[2]/div[2]/form/div[2]/div[3]/button').click()
   
    def criptoImage(self):
        self.btSearch_image = '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'

    def onDoubleClickTrueview(self, event=None):
        self.cleanWindow()
        self.trueview.selection()

        for n in self.trueview.selection():
            col1, col2, col3, col4, col5, col6 = self.trueview.item(n, 'values')
            self.input_registration.insert(END, col1)
            self.input_product_name.insert(END, col2)
            self.tipvar.set(str(col3))
            self.input_qtd.insert(END, col4)
            self.input_product_size.insert(END, col5)
            self.input_price.insert(END, col6)

    def cleanWindow(self, event=None):
        self.input_price.delete(0, END)
        self.input_registration.delete(0, END)
        self.input_product_name.delete(0, END)
        self.tipvar.set('')
        self.input_product_size.delete(0, END)
        self.input_qtd.delete(0, END)
        self.input_search.delete(0, END)

    def bindsOfButtons(self):
        self.variavelGET()
        self.root2.bind('<F2>', self.cleanWindow) 
        self.root2.bind('<F9>', self.addProduct)
        self.root2.bind('<>')
        self.root2.bind('<>')
        self.root2.bind('<>')
        self.root2.bind('<>')

    def selectList(self):
        self.trueview.delete(*self.trueview.get_children())
        self.connectDB()
        
        self.command = self.cursor.execute("""
                            SELECT codigo, produto, tipo, quantidade, tamanho, preco FROM Estoque 
                            ORDER BY codigo ASC;
                        """)

        self.insertTrueview(self.command)
        self.disconnectDB()
        self.cleanWindow()

    def change_product(self):
        self.variavelGET()
        self.connectDB()
        self.cursor.execute(
            f""" UPDATE Estoque SET codigo = {self.registration}, preco = {self.price}, produto = '"{self.product_name}"', tipo = '"{self.type}"', quantidade = {self.qtd}, tamanho = {self.product_size}
            WHERE codigo = {self.registration}""")
        self.cursor.commit()
        self.disconnectDB()
        self.selectList()
        self.cleanWindow()
    
    def addProduct(self, event=None):
        self.connectDB()
        self.variavelGET()
        
        if self.registration == '':
            messagebox.showwarning(title='ERROR', message='Campo "Código" se encontra vazio!')
            return 
        elif self.price == '':
            messagebox.showwarning(title='ERROR', message='Campo "Preço" se encontra vazio!')
            return 
        elif self.product_name == '':
            messagebox.showwarning(title='ERROR', message='Campo "Nome" se encontra vazio!')
            return 
        elif self.type == '':
            messagebox.showwarning(title='ERROR', message='Campo "Tipo" se encontra vazio!')
            return 
        elif self.product_size == '':
            messagebox.showwarning(title='ERROR', message='Campo "Tamanho" se encontra vazio!')
            return 
        elif self.qtd == '':
            messagebox.showwarning(title='ERROR', message='Campo "Quantidade" se encontra vazio!')
            return 

        self.cursor.execute(f"""INSERT INTO Estoque(codigo, preco, produto, tipo, quantidade, tamanho)
        VALUES({self.registration}, {self.price}, '"{self.product_name}"', '"{self.type}"', {self.qtd}, {self.product_size})""")

        self.cursor.commit()
        self.selectList()
        self.disconnectDB()
        
        messagebox.showinfo(title='Info', message='Produto adicionado com suscesso!')

    def deleteProduct(self):
        self.variavelGET()
        if self.registration == '':
            messagebox.showwarning('Aviso', 'Preencha o campo Código!')
            return
        self.textBox = messagebox.askyesno('Deletar Produto', f'Você realmente deseja deletar seu produto de Código {self.registration}?')

        if self.textBox == True:
            self.connectDB()
            self.cursor.execute(f"""DELETE FROM Estoque WHERE codigo = '{self.registration}'""")
            self.cursor.commit()
            self.disconnectDB()
            self.cleanWindow()
            self.selectList()
            messagebox.showinfo('Aviso', f'O produto com o código {self.registration} foi removido')

class search(funcs):
    
    def search_product_name(self):
        self.connectDB()
        self.variavelGET()
        self.trueview.delete(*self.trueview.get_children())
        self.input_search.insert(END, '%')
        self.product = self.input_search.get()
        self.command = self.cursor.execute(
            """ SELECT codigo, produto, tipo, quantidade, tamanho, preco FROM Estoque
            WHERE produto LIKE '"%s"' ORDER BY codigo ASC""" % self.product)
        self.insertTrueview(self.command)
        self.cleanWindow()
        self.disconnectDB()
    
    def search_price(self):
        self.connectDB()
        self.variavelGET()
        self.trueview.delete(*self.trueview.get_children())
        self.input_search.insert(END, '%')
        self.product = self.input_search.get()
        self.command = self.cursor.execute(
            """ SELECT codigo, produto, tipo, quantidade, tamanho, preco FROM Estoque
            WHERE preco LIKE '%s' ORDER BY codigo ASC""" % self.product)
        self.insertTrueview(self.command)
        self.cleanWindow()
        self.disconnectDB()

    def search_registration(self):
        self.connectDB()
        self.variavelGET()
        self.trueview.delete(*self.trueview.get_children())
        self.input_search.insert(END, '%')
        self.product = self.input_search.get()
        self.command = self.cursor.execute(
            """ SELECT codigo, produto, tipo, quantidade, tamanho, preco FROM Estoque
            WHERE codigo LIKE '%s' ORDER BY codigo ASC""" % self.product)
        self.insertTrueview(self.command)
        self.cleanWindow()
        self.disconnectDB()
    
    def search_type(self):
        self.connectDB()
        self.variavelGET()
        self.trueview.delete(*self.trueview.get_children())
        self.input_search.insert(END, '%')
        self.product = self.input_search.get()
        self.command = self.cursor.execute(
            """ SELECT codigo, produto, tipo, quantidade, tamanho, preco FROM Estoque
            WHERE tipo LIKE '"%s"' ORDER BY codigo ASC""" % self.product)
        self.insertTrueview(self.command)
        self.cleanWindow()
        self.disconnectDB()
    
    def search_qtd(self):
        self.connectDB()
        self.variavelGET()
        self.trueview.delete(*self.trueview.get_children())
        self.input_search.insert(END, '%')
        self.product = self.input_search.get()
        self.command = self.cursor.execute(
            """ SELECT codigo, produto, tipo, quantidade, tamanho, preco FROM Estoque
            WHERE quantidade LIKE '%s' ORDER BY codigo ASC""" % self.product)
        self.insertTrueview(self.command)
        self.cleanWindow()
        self.disconnectDB()
    
    def search_size(self):
        self.connectDB()
        self.variavelGET()
        self.trueview.delete(*self.trueview.get_children())
        self.input_search.insert(END, '%')
        self.product = self.input_search.get()
        self.command = self.cursor.execute(
            """ SELECT codigo, produto, tipo, quantidade, tamanho, preco FROM Estoque
            WHERE tamanho LIKE '%s' ORDER BY codigo ASC""" % self.product)
        self.insertTrueview(self.command)
        self.cleanWindow()
        self.disconnectDB()
    
    def decisao(self):
        self.variavelGET()
        if self.typeSearch == 'Produto':
            self.search_product_name()

        elif self.typeSearch == 'Preço':
            self.search_price()

        elif self.typeSearch == 'Código':
            self.search_registration()

        elif self.typeSearch == 'Tipo':
            self.search_type()

        elif self.typeSearch == 'Quantidade':
            self.search_qtd()

        elif self.typeSearch == 'Tamanho':
            self.search_size()
            
        else:
            print('Erro')

class application(search):
    def __init__(self):
        self.defaultFont = font.nametofont("TkDefaultFont") 
        self.defaultFont.configure(family=fontType, size=10, weight=font.BOLD)
        self.root2 = root2
        self.criptoImage()
        self.app()
        self.widgets_frame1()
        self.widgets_frame2()
        self.selectList()
        self.bindsOfButtons()
        self.root2.mainloop()
    
    def app(self):
        self.root2.title('Controle de Estoque')
        self.root2.geometry("{0}x{1}+0+0".format(root2.winfo_screenwidth(), root2.winfo_screenheight()))
        self.root2.resizable(True, True)
        self.root2.state('zoomed')
    
    def widgets_frame1(self):
        self.frame1 = Frame(self.root2, bd=0, bg='#3d4561', highlightbackground='#187db2', highlightthickness=0)
        self.frame1.place(relx=0.001, rely=0.001, relheight=1, relwidth=0.39)

        self.btSearch_image = PhotoImage(data=base64.b64decode(self.btSearch_image))
        self.btSearch_image = self.btSearch_image.subsample(3, 3)
        
        self.bt_searchProduct = Button(self.frame1, image=self.btSearch_image, bd=1, bg=btColor, command=self.decisao)
        self.bt_searchProduct.place(relx=0.82, rely=0.15, relheight=0.04, relwidth=0.16)

        self.input_search = Entry(self.frame1, font=(fontType, fontSize, 'bold'), justify=CENTER, bg='White', bd=0, foreground='Black')
        self.input_search.place(relx=0.01, rely=0.15, relheight=0.04, relwidth=0.8)
        self.input_search.focus()
        
        self.lb_search = Label(self.frame1, text='Consultar Produtos', font=(fontType, fontSize, 'bold'), bg='#3d4561', foreground='White')
        self.lb_search.place(relx=0.30, rely=0.005, relheight=0.04, relwidth=0.3)

        self.lb_search = Label(self.frame1, text='Pesquisar por:', font=(fontType, 12, 'bold'), bg='#3d4561', foreground='White')
        self.lb_search.place(relx=0.0001, rely=0.05, relheight=0.07, relwidth=0.17)

        self.tipvar1 = StringVar(self.frame1)
        self.tipv = ('Código', 'Produto', 'Preço', 'Tipo', 'Quantidade', 'Tamanho')
        self.tipvar1.set('Produto')
        self.popupMenu = OptionMenu(self.frame1, self.tipvar1, *self.tipv)
        self.popupMenu.configure(font=(fontType, 10, 'bold'))
        self.popupMenu.place(relx=0.01, rely=0.1, relheight=0.03, relwidth=0.2)
        self.popupMenu.config(background='White', highlightbackground='Gray', highlightthickness=0.5)


        style = ttk.Style()
        style.configure('trueview', background='blue', foreground='black', rowheight=100, fieldbackground='blue')
        style.map('Trueview', background=[('selected', 'gray')])
        style.theme_use('classic')

        self.trueview = ttk.Treeview(self.frame1, height=3, column=('col1', 'col2', 'col3', 'col4', 'col5', 'col6'))
        self.trueview.heading('#0', text='')
        self.trueview.heading('#1', text='Código')
        self.trueview.heading('#2', text='Nome')
        self.trueview.heading('#3', text='Tipo')
        self.trueview.heading('#4', text='Quantidade')
        self.trueview.heading('#5', text='Tamanho')
        self.trueview.heading('#6', text='Preço')


        self.trueview.column('#0', stretch=NO, minwidth=100, width=0, anchor="center")
        self.trueview.column('#1', stretch=YES, minwidth=75, width=75, anchor="center")
        self.trueview.column('#2', stretch=YES, minwidth=200, width=200, anchor="center")
        self.trueview.column('#3', stretch=YES, minwidth=200, width=200, anchor="center")
        self.trueview.column('#4', stretch=YES, minwidth=75, width=75, anchor="center")
        self.trueview.column('#5', stretch=YES, minwidth=50, width=75, anchor="center")
        self.trueview.column('#6', stretch=YES, minwidth=50, width=50, anchor="center")

        self.trueview.place(relx=0.01, rely=0.20, relwidth=0.95, relheight=0.8)

        self.scroolLista = Scrollbar(self.frame1, orient='vertical')
        self.trueview.configure(yscrollcommand=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.20, relwidth=0.02, relheight=0.8)
        self.trueview.bind('<Double-1>', self.onDoubleClickTrueview)

    def widgets_frame2(self):
        self.frame2 = Frame(self.root2, bd=0, bg='#3d4561', highlightbackground='#187db2', highlightthickness=0)
        self.frame2.place(relx=0.4, rely=0.001, relheight=1, relwidth=1)

        self.bt_addProduct = Button(self.frame2, font=(fontType, fontSize, 'bold'), text='Adicionar Produto', bg=btColor, command=self.addProduct)
        self.bt_addProduct.place(relx=0.01, rely=0.01, relheight=bt_height, relwidth=bt_widht)
        
        self.bt_removeProduct = Button(self.frame2, font=(fontType, fontSize, 'bold'), text='Remover Produto', bg=btColor, command=self.deleteProduct)
        self.bt_removeProduct.place(relx=0.12, rely=0.01, relheight=bt_height, relwidth=bt_widht)

        self.bt_changeProduct = Button(self.frame2, font=(fontType, fontSize, 'bold'), text='Alterar Produto', bg=btColor, command=self.change_product)
        self.bt_changeProduct.place(relx=0.23, rely=0.01, relheight=bt_height, relwidth=bt_widht)

        self.bt_cleanWindow = Button(self.frame2, text='Limpar Tela', font=(fontType, fontSize, 'bold'), bg=btColor, command=self.cleanWindow)
        self.bt_cleanWindow.place(relx=0.34, rely=0.01, relheight=bt_height, relwidth=bt_widht)

        self.bt_acess_FV = Button(self.frame2, text='Acessar Fv.Tupperware', font=(fontType, fontSize, 'bold'), bg=btColor, command=self.openFV)
        self.bt_acess_FV.place(relx=0.46, rely=0.95, relheight=bt_height, relwidth=0.13)

        #############################################################################################################################
        self.input_price = MaskedWidget(self.frame2, 'numeric', dec_sep=".", tho_sep='.', font=(fontType, fontSize, 'bold'))
        self.input_price.place(relx=0.15, rely=0.1, relheight=0.03, relwidth=0.16)

        self.input_registration = Entry(self.frame2, font=(fontType, fontSize, 'bold'))
        self.input_registration.place(relx=0.01, rely=0.1, relheight=0.03, relwidth=0.1)

        self.input_product_name = Entry(self.frame2, font=(fontType, fontSize, 'bold'))
        self.input_product_name.place(relx=0.01, rely=0.2, relheight=0.03, relwidth=0.3)



        self.tipvar = StringVar(self.frame2)
        self.tipv = ('Linha Freezer', 'Linha Microondas', 'Linha Armazenamento', 'Talher', 'Copo', 'Utilitario')
        self.popupMenu = OptionMenu(self.frame2, self.tipvar, *self.tipv)
        self.popupMenu.place(relx=0.15, rely=0.3, relheight=0.03, relwidth=0.16)
        self.popupMenu.config(background='White', highlightbackground='Gray', highlightthickness=0.5, font=(fontType, fontSize, 'bold'))

        self.input_product_size = Entry(self.frame2, font=(fontType, fontSize, 'bold'))
        self.input_product_size.place(relx=0.01, rely=0.3, relheight=0.03, relwidth=0.1)

        self.input_qtd = Entry(self.frame2, font=(fontType, fontSize, 'bold'))
        self.input_qtd.place(relx=0.01, rely=0.4, relheight=0.03, relwidth=0.1)

        '''self.image = Image.open()
        self.resize_image = self.image.resize((500, 500))
        self.img = ImageTk.PhotoImage(self.resize_image)'''
        self.lb_product_image = Label(self.frame2, text='PRODUTO', font=(fontType, 30, 'bold'))
        self.lb_product_image.place(relx=0.33, rely=0.1, relheight=0.5, relwidth=0.3)

        #############################################################################################################################

        self.lb_price = Label(self.frame2, text='Preço', font=(fontType, 12, 'bold'), bg='#3d4561', foreground='White')
        self.lb_price.place(relx=0.149, rely=0.075)
        
        self.lb_registration = Label(self.frame2, text='Código', font=(fontType, 12, 'bold'), bg='#3d4561', foreground='White')
        self.lb_registration.place(relx=0.009, rely=0.075)

        self.lb_product_name = Label(self.frame2, text='Nome', font=(fontType, 12, 'bold'), bg='#3d4561', foreground='White')
        self.lb_product_name.place(relx=0.009, rely=0.175)

        self.lb_type = Label(self.frame2, text='Tipo', font=(fontType, 12, 'bold'), bg='#3d4561', foreground='White')
        self.lb_type.place(relx=0.149, rely=0.275)

        self.lb_product_size = Label(self.frame2, text='Tamanho', font=(fontType, 12, 'bold'), bg='#3d4561', foreground='White')
        self.lb_product_size.place(relx=0.009, rely=0.275)
        
        self.lb_input_qtd = Label(self.frame2, text='Quantidade', font=(fontType, 12, 'bold'), bg='#3d4561', foreground='White')
        self.lb_input_qtd.place(relx=0.009, rely=0.375)
application()


