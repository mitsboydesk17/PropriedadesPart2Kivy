import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window

Window.size = (400, 600)
Window.clearcolor = (0.1, 0.1, 0.1, 1)


class FilmeSorteador:
    def __init__(self):
        self.filmes = {
            "Ação": [("Matrix", 1999), ("Vingadores: Ultimato", 2019), ("Homem-Aranha", 2002)],
            "Animação": [("Toy Story", 1995), ("O Rei Leão", 1994), ("Shrek", 2001)],
            "Ficção": [("Avatar", 2009), ("Interestelar", 2014), ("Jurassic Park", 1993)],
            "Romance": [("Titanic", 1997), ("A Culpa é das Estrelas", 2014)],
            "Comédia": [("Shrek", 2001), ("De Volta para o Futuro", 1985)],
        }

    def sortear(self, genero):
        if genero in self.filmes:
            return random.choice(self.filmes[genero])
        else:
            return ("Nenhum filme disponível", "")


class CardFilme(BoxLayout):
    def __init__(self, texto, **kwargs):
        super().__init__(orientation="vertical", size_hint_y=None, height=100, padding=10, spacing=10, **kwargs)
        with self.canvas.before:
            Color(0.2, 0.6, 1, 1)
            self.rect = RoundedRectangle(radius=[15])
        self.bind(pos=self.update_rect, size=self.update_rect)

        self.label = Label(
            text=texto,
            font_size=16,
            halign="center",
            valign="middle",
            color=(1, 1, 1, 1)
        )
        self.label.bind(size=self.label.setter('text_size'))
        self.add_widget(self.label)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class FilmeUI(BoxLayout):
    def __init__(self, sorteador: FilmeSorteador, **kwargs):
        super().__init__(orientation="vertical", spacing=15, padding=20, **kwargs)
        self.sorteador = sorteador

        self.titulo = Label(
            text="! Sugestão de Filmes !",
            font_size=28,
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.1)
        )
        self.add_widget(self.titulo)

        self.nome_input = TextInput(
            hint_text="Digite seu nome",
            multiline=False,
            size_hint=(1, 0.1),
            font_size=16,
            foreground_color=(1, 1, 1, 1),
            background_color=(0.15, 0.15, 0.15, 1),
            cursor_color=(1, 1, 1, 1)
        )
        self.add_widget(self.nome_input)

        self.spinner = Spinner(
            text="Escolha o gênero",
            values=list(self.sorteador.filmes.keys()),
            size_hint=(1, 0.1),
            background_color=(0.15, 0.15, 0.15, 1),
            color=(1, 1, 1, 1),
            font_size=16
        )
        self.add_widget(self.spinner)

        self.botao = Button(
            text="Sugerir Filme",
            size_hint=(1, 0.1),
            background_color=(1, 0.5, 0, 1),
            font_size=18,
            bold=True
        )
        self.botao.bind(on_press=self.on_sugerir)
        self.add_widget(self.botao)

        self.scroll = ScrollView(size_hint=(1, 0.6))
        self.grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll.add_widget(self.grid)
        self.add_widget(self.scroll)

    def on_sugerir(self, instance):
        nome = self.nome_input.text.strip()
        genero = self.spinner.text

        if not nome:
            card = CardFilme("! Por favor, digite seu nome!")
        elif genero == "Escolha o gênero":
            card = CardFilme("! Por favor, selecione um gênero!")
        else:
            filme, ano = self.sorteador.sortear(genero)
            card = CardFilme(f"Olá, {nome}! Sua sugestão de filme é: {filme} ({ano})")

        self.grid.add_widget(card)
        self.nome_input.text = ""


class FilmeApp(App):
    def build(self):
        sorteador = FilmeSorteador()
        return FilmeUI(sorteador)


if __name__ == "__main__":
    FilmeApp().run()
