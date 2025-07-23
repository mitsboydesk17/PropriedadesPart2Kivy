from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from kivy.core.window import Window

Window.clearcolor = (1, 1, 1, 1)

class MovingBox(Widget):
    x_pos = NumericProperty(0)
    y_pos = NumericProperty(0)

    # Referência combinada para facilitar a manipulação do par (x, y)
    position = ReferenceListProperty(x_pos, y_pos)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (100, 100)

        with self.canvas:
            self.color = Color(0.2, 0.7, 0.3, 1)
            self.rect = Rectangle(size=self.size, pos=self.position)

        self.bind(pos=self.update_rect, size=self.update_rect)
        self.bind(x_pos=self.update_rect, y_pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = (self.x_pos, self.y_pos)
        self.rect.size = self.size

    def move_box(self):
        # Move de (0,0) para (200,300) com ReferenceListProperty
        anim = Animation(position=(200, 300), duration=0.5)
        anim.start(self)

class PositionScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        self.moving_box = MovingBox()
        self.add_widget(self.moving_box)

        btn = Button(
            text="Mover Quadrado",
            size_hint=(1, None),
            height=50,
            background_color=(0.1, 0.7, 0.5, 1),
            font_size=18
        )
        btn.bind(on_press=lambda x: self.moving_box.move_box())
        self.add_widget(btn)

class ReferenceListApp(App):
    def build(self):
        return PositionScreen()

if __name__ == '__main__':
    ReferenceListApp().run()
