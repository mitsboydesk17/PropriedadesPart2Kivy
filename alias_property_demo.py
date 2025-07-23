from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.properties import NumericProperty, AliasProperty

class AreaBox(BoxLayout):
    largura = NumericProperty(0)
    altura = NumericProperty(0)

    def get_area(self):
        return self.largura * self.altura

    area = AliasProperty(get_area, bind=('largura', 'altura'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 20

        self.label_area = Label(
            text="Área: 0",
            font_size=22,
            size_hint=(1, None),
            height=40
        )

        self.slider_largura = Slider(min=0, max=100, value=10)
        self.slider_altura = Slider(min=0, max=100, value=10)

        self.slider_largura.bind(value=self.update_largura)
        self.slider_altura.bind(value=self.update_altura)

        self.add_widget(Label(text="Largura", font_size=18, size_hint=(1, None), height=30))
        self.add_widget(self.slider_largura)

        self.add_widget(Label(text="Altura", font_size=18, size_hint=(1, None), height=30))
        self.add_widget(self.slider_altura)

        self.add_widget(self.label_area)

        # Inicializa com os valores dos sliders
        self.update_largura(self.slider_largura, self.slider_largura.value)
        self.update_altura(self.slider_altura, self.slider_altura.value)

    def update_largura(self, instance, value):
        self.largura = value
        self.label_area.text = f"Área: {self.area:.1f}"

    def update_altura(self, instance, value):
        self.altura = value
        self.label_area.text = f"Área: {self.area:.1f}"

class AliasPropertyApp(App):
    def build(self):
        return AreaBox()

if __name__ == '__main__':
    AliasPropertyApp().run()
