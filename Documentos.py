from tkinter import *
from tkinter import ttk
from tkinter.constants import *
import sqlite3

############################################################

# Variavel global root que usa o Tkinter
root = Tk()
root.iconbitmap("icon.ico")

class Functions():
    # Função para limpar as Entrys:

    def limpa_tela(self):
        self.entry_nome.delete(0, END)
        self.entry_numdoc.delete(0, END)

    # Função para Conectar ao banco de dados:

    def conecta_bd(self):

        self.conn = sqlite3.connect("docperdidos.bd")
        self.cursor = self.conn.cursor()

    # Função para desconectar do banco de dados:
    def disconnect_bd(self):

        self.conn.close()

    # Função para criar o banco de dados local:

    def cria_banco(self):
        self.conecta_bd()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS docperdidos (
                nome STRING,
                numero STRING,
                documento STRING,
                posto STRING
            );
        """)
        self.conn.commit()
        self.disconnect_bd()

    # Função que carrega as variaveis das fun.:

    def variables(self):
        self.nome = self.entry_nome.get()
        self.numero = self.entry_numdoc.get()
        self.tipo_doc = self.lista_docu.get()
        self.posto = self.lista_postos.get()


    # Função para cadastrar novos :

    def perdido(self):
        self.variables()

        self.conecta_bd()

        self.cursor.execute("""INSERT INTO docperdidos(nome, numero, documento, posto)
         VALUES
                    (?, ?, ?, ?)""", (self.nome, self.numero, self.tipo_doc, self.posto))

        self.conn.commit()
        self.select_lista()
        self.limpa_tela()

    # Função para inserir os dados na TreeView:
    def select_lista(self):
        self.variables()
        self.lista.delete(*self.lista.get_children())
        self.conecta_bd()

        lista = self.cursor.execute(""" SELECT documento, numero, nome, posto FROM docperdidos""")

        for i in lista:
            self.lista.insert("", END, values=i)

    def onDoubleClick(self, event):
        self.limpa_tela()
        self.lista.selection()

        for n in self.lista.selection():
            col1, col2, col3, col4 = self.lista.item(n, 'values')
            self.lista_docu.insert(END, col1)
            self.entry_numdoc.insert(END, col2)
            self.entry_nome.insert(END, col3)
            self.lista_postos.insert(END, col4)

    # Função para apagar um documento perdido:

    def delete_person(self):
        self.variables()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM docperdidos WHERE nome = (?) """, [self.nome])
        self.conn.commit()
        self.limpa_tela()
        self.select_lista()

    # Função para buscar um nome na lista:

    def search_btn(self):
        self.conecta_bd()
        self.lista.delete(*self.lista.get_children())

        self.entry_nome.insert(END, '%')
        nome = self.entry_nome.get()
        self.cursor.execute("""SELECT documento, numero, nome, posto FROM docperdidos WHERE nome LIKE '%s' ORDER BY nome ASC""" % nome)
        searchName = self.cursor.fetchall()
        for i in searchName:
            self.lista.insert("", END, values=i)
        self.limpa_tela()
        self.disconnect_bd()


############################################################

# Classe que englobla e organiza as funções do programa

class App(Functions):

    ############################################################

    # Ao iniciar:
    def __init__(self):
        self.root = root
        self.screen()
        self.frames()
        self.widgets_f1()
        self.widgets_f2()
        self.cria_banco()
        self.select_lista()
        root.mainloop()


    ############################################################

    # Configurações de tela e título:
    def screen(self):
        # Título:
        self.root.title("Cadastro achados e perdidos")

        # Background:
        self.root.configure(background='#FFF5CF')

        # Ajustes de fundo e ajustamento do usuário:
        self.root.wm_maxsize(1280, 1080)
        self.root.wm_minsize(720, 480)
        self.root.resizable(True, True)

    ############################################################

    # Configurações de frames de fundo na tela:
    def frames(self):
        # Frame superior:
        self.frame1 = Frame(self.root, bd=4, highlightbackground='black', highlightthickness=0.7)
        self.frame1.place(relx=0.01, rely=0.02, relwidth=0.98, relheight=0.49)
        self.frame1.configure(background='white')

        # Frame inferior:
        self.frame2 = Frame(self.root, bd=4, highlightbackground='black', highlightthickness=0.7)
        self.frame2.place(relx=0.01, rely=0.58, relwidth=0.98, relheight=0.4)
        self.frame2.configure(background='white')

    ############################################################

    # Criação de widgets do PRIMEIRO frame:
    def widgets_f1(self):
        # Botão de cadastrar:
        self.bt_cadastro = Button(self.frame1, text='Cadastrar', command=self.perdido)
        self.bt_cadastro.place(relx=0.01, rely=0.34, relwidth=0.1, relheight=0.15)

        # Botão de remover:
        self.bt_remover = Button(self.frame1, text='Remover', command=self.delete_person)
        self.bt_remover.place(relx=0.12, rely=0.34, relwidth=0.1, relheight=0.15)

        # Lista de documentos para selecionar:
        lista_documentos=[
            "CPF",
            "RG",
            "Cartão SUS",
            "Outros"
        ]

        # ComboBox de documentos:
        self.lista_docu=ttk.Combobox(self.frame1, values=lista_documentos, font=('verdana', 8), state='readonly')
        self.lista_docu.place(relx=0.23, rely=0.34, relwidth=0.13, relheight=0.15)
        self.lista_docu.set('CPF')

        # Label nome no documento:
        self.lab_nome = Label(self.frame1, text='Nome no documento', background= 'white', font=('verdana', 10, 'bold'))
        self.lab_nome.place(relx=0.01, rely=0.02, relwidth=0.25, relheight=0.15)

        # Entry para inserir o nome:
        self.entry_nome = Entry(self.frame1, font=('verdana', 8))
        self.entry_nome.place(relx=0.01, rely=0.15, relwidth=0.35, relheight=0.15)

        # Lista Sedes de Saúde

        lista_postos=[
            'UBS Maringá Velho',
            'UBS Zona 06',
            'UBS Zona 07',
            'UBS Aclimação',
            'UBS Tuiuti',
            'UBS Vila Operária',
            'UBS Vila Esperança',
            'Posto Parigot de Souza',
            'UBS Mandacaru',
            'UBS Iguaçu',
            'UBS Cidade Alta',
            'UBS Jardim Paris',
            'UBS Quebec',
            'UBS Céu Azul',
            'Unidade Básica Iguatemi',
            'Posto Municipal Mandacaru',
            'UBS Portal das Torres',
            'UBS Pinheiros',
            'Unidade Básica Internorte',
            'UBS Piatã'
        ]

        # Combo Postos de Saúde:

        self.lista_postos=ttk.Combobox(self.frame1, values=lista_postos, font=('verdana', 8), state='readonly')
        self.lista_postos.place(relx=0.39, rely=0.34, relwidth=0.25, relheight=0.15)
        self.lista_postos.set('UBS Maringá Velho')

        # Label número do documento:
        self.lab_numdoc = Label(self.frame1, text='Número do documento', background= 'white', font=('verdana', 10, 'bold'))
        self.lab_numdoc.place(relx=0.45, rely=0.02, relwidth=0.25, relheight=0.15)

        # Entry para inserir o número do documento:
        self.entry_numdoc = Entry(self.frame1, font=('verdana', 8))
        self.entry_numdoc.place(relx=0.39, rely=0.15, relwidth=0.35, relheight=0.15)






        # Botão de limpar:
        self.bt_limpar = Button(self.frame1, text='Limpar', command=self.limpa_tela)
        self.bt_limpar.place(relx=0.79, rely=0.12, relwidth=0.1, relheight=0.15)

        # Botão de buscar:
        self.bt_busca = Button(self.frame1, text='Buscar', command=self.search_btn)
        self.bt_busca.place(relx=0.89, rely=0.12, relwidth=0.1, relheight=0.15)


    ############################################################

    # Criação de widgets do SEGUNDO frame:
    def widgets_f2(self):
        # Criar a TreeView + Config. das colunas:
        self.lista = ttk.Treeview(self.frame2, height=3, columns=('col1', 'col2', 'col3', 'col4'))
        self.lista.heading('#0', text='')
        self.lista.heading('#1', text='Documento')
        self.lista.heading('#2', text='Número')
        self.lista.heading('#3', text='Nome')
        self.lista.heading('#4', text='Posto')

        # Largura das colunas:
        self.lista.column('#0', width=1)
        self.lista.column('#1', width=50)
        self.lista.column('#2', width=200)
        self.lista.column('#3', width=125)
        self.lista.column('#4', width=180)

        # Local das colunas:
        self.lista.place(relheight=1, relwidth=1)

        # Criação do scroll:
        self.scroolLista= Scrollbar(self.frame2, orient='vertical')
        self.lista.configure(yscrollcommand=self.scroolLista.set)
        self.scroolLista.place(relx=0.97, rely=0.01, relheight=0.98)

        # Evento do double click:
        self.lista.bind("<Double-1>", self.onDoubleClick)


App()
