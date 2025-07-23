from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import NumericProperty
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

Window.clearcolor = (1, 1, 1, 1)

class AnimatedBox(Widget):
    box_size = NumericProperty(100)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.color = Color(0.2, 0.6, 0.8, 1)  # Azul
            self.rect = Rectangle(size=(self.box_size, self.box_size), pos=self.center)

        self.bind(pos=self.update_rect, size=self.update_rect)
        self.bind(box_size=self.update_rect)

    def update_rect(self, *args):
        # Centraliza o quadrado e atualiza o tamanho com base na box_size
        self.rect.size = (self.box_size, self.box_size)
        self.rect.pos = (
            self.center_x - self.box_size / 2,
            self.center_y - self.box_size / 2
        )

    def animate_box(self):
        # Anima para 200px e depois volta para 100px em sequência
        anim = Animation(box_size=200, duration=0.3) + Animation(box_size=100, duration=0.3)
        anim.start(self)

class AnimationScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 20

        self.animated_box = AnimatedBox()
        self.add_widget(self.animated_box)

        self.button = Button(
            text="Animar Quadrado",
            size_hint=(1, None),
            height=50,
            font_size=18,
            background_color=(0.3, 0.7, 0.9, 1)
        )
        self.button.bind(on_press=lambda x: self.animated_box.animate_box())
        self.add_widget(self.button)

class AnimationPropApp(App):
    def build(self):
        return AnimationScreen()

if __name__ == "__main__":
    AnimationPropApp().run()
