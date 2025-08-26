from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.core.window import Window

Window.clearcolor = (0.95, 0.95, 0.95, 1)


class IdadeApp(App):
    def build(self):

        layout = BoxLayout(orientation='vertical', padding=25, spacing=20)

        titulo = Label(
            text="App de Idade e Acesso",
            font_size=28,
            bold=True,
            color=(0.1, 0.3, 0.5, 1),
            size_hint=(1, 0.2)
        )
        layout.add_widget(titulo)

        self.nome_input = TextInput(
            hint_text="Digite seu nome",
            multiline=False,
            size_hint=(1, 0.15),
            background_normal='',
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            padding=[10, 10, 10, 10],
            font_size=18
        )
        layout.add_widget(self.nome_input)

        self.idade_input = TextInput(
            hint_text="Digite sua idade",
            multiline=False,
            input_filter="int",
            size_hint=(1, 0.15),
            background_normal='',
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            padding=[10, 10, 10, 10],
            font_size=18
        )
        layout.add_widget(self.idade_input)

        layout.add_widget(Widget(size_hint=(1, 0.05)))

        self.botao = Button(
            text="Enviar",
            size_hint=(1, 0.18),
            background_normal='',
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size=20,
            bold=True
        )
        self.botao.bind(on_press=self.verificar_idade)
        layout.add_widget(self.botao)

        layout.add_widget(Widget(size_hint=(1, 0.05)))

        self.mensagem = Label(
            text="",
            font_size=20,
            halign="center",
            valign="middle",
            color=(0.1, 0.1, 0.1, 1),
            size_hint=(1, 0.25)
        )
        self.mensagem.bind(size=self.mensagem.setter('text_size'))
        layout.add_widget(self.mensagem)

        return layout

    def verificar_idade(self, instance):
        nome = self.nome_input.text.strip()
        idade_texto = self.idade_input.text.strip()

        if not nome or not idade_texto:
            self.mensagem.text = "[ERRO] Por favor, preencha todos os campos."
            self.mensagem.color = (0.8, 0.1, 0.1, 1)
            return
        
        try:
            idade = int(idade_texto)
        except ValueError:
            self.mensagem.text = "[ERRO] Digite uma idade válida (apenas números)."
            self.mensagem.color = (0.8, 0.1, 0.1, 1)
            return

        if idade < 18:
            self.mensagem.text = f"Olá, {nome}! Você é menor de idade."
            self.mensagem.color = (0.9, 0.4, 0.2, 1)
        elif idade >= 60:
            self.mensagem.text = f"Olá, {nome}! Você é idoso e merece muito respeito ❤️."
            self.mensagem.color = (0.2, 0.6, 0.3, 1)
        else:
            self.mensagem.text = f"Olá, {nome}! Você é maior de idade."
            self.mensagem.color = (0.2, 0.4, 0.7, 1)


if __name__ == "__main__":
    IdadeApp().run()
