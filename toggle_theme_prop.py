from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

class ThemeBox(BoxLayout):
    dark_mode = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 20

        with self.canvas.before:
            self.bg_color = Color(1, 1, 1, 1)  # branco
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_bg, size=self.update_bg)
        self.bind(dark_mode=self.on_theme_change)

        self.label = Label(
            text="Modo Claro Ativo",
            font_size=22,
            color=(0, 0, 0, 1),
            size_hint=(1, None),
            height=40
        )

        self.button = Button(
            text="Alternar Modo",
            size_hint=(1, None),
            height=50,
            font_size=18
        )
        self.button.bind(on_press=self.toggle_theme)

        self.add_widget(self.label)
        self.add_widget(self.button)

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def toggle_theme(self, instance):
        self.dark_mode = not self.dark_mode

    def on_theme_change(self, instance, value):
        if value:
            self.bg_color.rgb = (0.1, 0.1, 0.1)  # escuro
            self.label.text = "Modo Escuro Ativo"
            self.label.color = (1, 1, 1, 1)
        else:
            self.bg_color.rgb = (1, 1, 1)  # claro
            self.label.text = "Modo Claro Ativo"
            self.label.color = (0, 0, 0, 1)

class BooleanPropApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return ThemeBox()

if __name__ == '__main__':
    BooleanPropApp().run()
