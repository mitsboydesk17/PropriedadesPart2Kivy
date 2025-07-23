from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import DictProperty
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

# Configura a janela
Window.clearcolor = (0.95, 0.95, 1, 1)  # fundo claro

class UserProfileWidget(BoxLayout):
    user_data = DictProperty({
        'name': 'João',
        'age': 30,
        'city': 'São Paulo'
    })

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 20

        # Fundo estilizado
        with self.canvas.before:
            Color(0.95, 0.95, 1, 1)  # azul clarinho
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Título
        self.title_label = Label(
            text="Perfil do Usuário",
            font_size=26,
            bold=True,
            color=(0.2, 0.2, 0.5, 1),
            size_hint=(1, None),
            height=40
        )
        self.add_widget(self.title_label)

        # Labels dinâmicos
        self.name_label = Label(font_size=20, color=(0, 0, 0, 1))
        self.age_label = Label(font_size=20, color=(0, 0, 0, 1))
        self.city_label = Label(font_size=20, color=(0, 0, 0, 1))
        self.add_widget(self.name_label)
        self.add_widget(self.age_label)
        self.add_widget(self.city_label)

        # Botão para atualizar idade
        self.update_button = Button(
            text="Aumentar Idade",
            size_hint=(1, None),
            height=50,
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            font_size=18
        )
        self.update_button.bind(on_release=lambda x: self.update_age())
        self.add_widget(self.update_button)

        # Inicializa os dados nos labels
        self.update_labels()

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_labels(self):
        self.name_label.text = f"Nome: {self.user_data['name']}"
        self.age_label.text = f"Idade: {self.user_data['age']}"
        self.city_label.text = f"Cidade: {self.user_data['city']}"

    def update_age(self):
        self.user_data['age'] += 1
        self.update_labels()

class DictPropApp(App):
    def build(self):
        return UserProfileWidget()

if __name__ == '__main__':
    DictPropApp().run()
