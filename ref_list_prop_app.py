from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.core.window import Window

# Configura a cor do fundo da janela
Window.clearcolor = (1, 1, 1, 1)  # branco

class MovableDot(Widget):
    # Propriedades para a posição
    pos_x = NumericProperty(100)
    pos_y = NumericProperty(100)

    # Propriedade combinada para usar como coordenada
    dot_pos = ReferenceListProperty(pos_x, pos_y)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dot_size = 40
        with self.canvas:
            Color(0.2, 0.6, 1, 1)  # Azul claro
            self.dot = Ellipse(pos=self.dot_pos, size=(self.dot_size, self.dot_size))

        self.bind(dot_pos=self.update_dot_position)

    def update_dot_position(self, *args):
        self.dot.pos = self.dot_pos

    def move_left(self):
        self.pos_x -= 10

    def move_right(self):
        self.pos_x += 10

    def move_up(self):
        self.pos_y += 10

    def move_down(self):
        self.pos_y -= 10

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 20

        # Widget com o ponto
        self.dot_widget = MovableDot()
        self.dot_widget.size_hint = (1, 0.8)
        self.add_widget(self.dot_widget)

        # Layout para botões de controle
        controls = BoxLayout(size_hint=(1, 0.2), spacing=10)

        controls.add_widget(Button(text="⬅️ Esquerda", on_release=lambda x: self.dot_widget.move_left()))
        controls.add_widget(Button(text="⬆️ Cima", on_release=lambda x: self.dot_widget.move_up()))
        controls.add_widget(Button(text="⬇️ Baixo", on_release=lambda x: self.dot_widget.move_down()))
        controls.add_widget(Button(text="➡️ Direita", on_release=lambda x: self.dot_widget.move_right()))

        self.add_widget(controls)

class RefListPropApp(App):
    def build(self):
        return MainLayout()

if __name__ == '__main__':
    RefListPropApp().run()
