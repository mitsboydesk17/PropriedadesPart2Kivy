import sqlite3
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

con = sqlite3.connect("filmes.db")
cur = con.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS filmes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    genero TEXT,
    ano INTEGER
)
""")
con.commit()

class CadastroScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.titulo_input = TextInput(hint_text="Título", size_hint_y=None, height=40)
        self.genero_input = TextInput(hint_text="Gênero", size_hint_y=None, height=40)
        self.ano_input = TextInput(hint_text="Ano de lançamento", input_filter="int", size_hint_y=None, height=40)

        btn_salvar = Button(text="Salvar", background_color=(0, 0.5, 0, 1), size_hint_y=None, height=50)
        btn_salvar.bind(on_release=lambda x: self.adicionar_filme())

        btn_listar = Button(text="Ir para Listagem", background_color=(0, 0.3, 0.7, 1), size_hint_y=None, height=50)
        btn_listar.bind(on_release=lambda x: self.manager.current == "listagem" or setattr(self.manager, "current", "listagem"))

        layout.add_widget(self.titulo_input)
        layout.add_widget(self.genero_input)
        layout.add_widget(self.ano_input)
        layout.add_widget(btn_salvar)
        layout.add_widget(btn_listar)

        self.add_widget(layout)

    def adicionar_filme(self):
        titulo = self.titulo_input.text
        genero = self.genero_input.text
        ano = self.ano_input.text

        if titulo and genero and ano.isdigit():
            cur.execute("INSERT INTO filmes (titulo, genero, ano) VALUES (?, ?, ?)", 
                        (titulo, genero, int(ano)))
            con.commit()
            self.titulo_input.text = ""
            self.genero_input.text = ""
            self.ano_input.text = ""
            self.manager.current = "listagem"


class ListagemScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.scroll = ScrollView()
        self.grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll.add_widget(self.grid)

        btn_novo = Button(text="Novo Filme", background_color=(0.2, 0.6, 1, 1), size_hint_y=None, height=50)
        btn_novo.bind(on_release=lambda x: setattr(self.manager, "current", "cadastro"))

        self.layout.add_widget(self.scroll)
        self.layout.add_widget(btn_novo)
        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.listar_filmes()

    def listar_filmes(self):
        self.grid.clear_widgets()
        cur.execute("SELECT * FROM filmes")
        filmes = cur.fetchall()
        for filme in filmes:
            item = FilmeItem(id_filme=filme[0], titulo=filme[1], genero=filme[2], ano=filme[3])
            self.grid.add_widget(item)

    def deletar_filme(self, id_filme):
        cur.execute("DELETE FROM filmes WHERE id = ?", (id_filme,))
        con.commit()
        self.listar_filmes()

    def editar_filme(self, id_filme, titulo, genero, ano):
        tela_edicao = self.manager.get_screen("edicao")
        tela_edicao.carregar_dados(id_filme, titulo, genero, ano)
        self.manager.current = "edicao"

class EdicaoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.id_label = Label(text="", size_hint_y=None, height=30)
        self.titulo_edit = TextInput(hint_text="Título", size_hint_y=None, height=40)
        self.genero_edit = TextInput(hint_text="Gênero", size_hint_y=None, height=40)
        self.ano_edit = TextInput(hint_text="Ano de lançamento", input_filter="int", size_hint_y=None, height=40)

        btn_salvar = Button(text="Salvar Alterações", background_color=(0, 0.5, 0, 1), size_hint_y=None, height=50)
        btn_salvar.bind(on_release=lambda x: self.salvar_edicao())

        btn_voltar = Button(text="Voltar", background_color=(0.7, 0, 0, 1), size_hint_y=None, height=50)
        btn_voltar.bind(on_release=lambda x: setattr(self.manager, "current", "listagem"))

        layout.add_widget(self.id_label)
        layout.add_widget(self.titulo_edit)
        layout.add_widget(self.genero_edit)
        layout.add_widget(self.ano_edit)
        layout.add_widget(btn_salvar)
        layout.add_widget(btn_voltar)

        self.add_widget(layout)

    def carregar_dados(self, id_filme, titulo, genero, ano):
        self.id_label.text = str(id_filme)
        self.titulo_edit.text = titulo
        self.genero_edit.text = genero
        self.ano_edit.text = str(ano)

    def salvar_edicao(self):
        id_filme = int(self.id_label.text)
        titulo = self.titulo_edit.text
        genero = self.genero_edit.text
        ano = self.ano_edit.text

        if titulo and genero and ano.isdigit():
            cur.execute("UPDATE filmes SET titulo=?, genero=?, ano=? WHERE id=?",
                        (titulo, genero, int(ano), id_filme))
            con.commit()
            self.manager.current = "listagem"

class FilmeItem(BoxLayout):
    def __init__(self, id_filme, titulo, genero, ano, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 40

        ibl = Label(text=f"{titulo} - {genero} ({ano})", halign="left")
        btn_editar = Button(text="Editar", size_hint_x=0.2, background_color=(0.8, 0.6, 0, 1))
        btn_excluir = Button(text="Excluir", size_hint_x=0.2, background_color=(0.9, 0, 0, 1))

        btn_editar.bind(on_release=lambda x: App.get_running_app().root.get_screen('listagem').editar_filme(id_filme, titulo, genero, ano))
        btn_excluir.bind(on_release=lambda x: App.get_running_app().root.get_screen("listagem").deletar_filme(id_filme))

        self.add_widget(ibl)
        self.add_widget(btn_editar)
        self.add_widget(btn_excluir)

class Gerenciador(ScreenManager):
    pass

class CRUDApp(App):
    def build(self):
        sm = Gerenciador()
        sm.add_widget(CadastroScreen(name="cadastro"))
        sm.add_widget(ListagemScreen(name="listagem"))
        sm.add_widget(EdicaoScreen(name="edicao"))
        return sm
    
if __name__ == "__main__":
    CRUDApp().run()
