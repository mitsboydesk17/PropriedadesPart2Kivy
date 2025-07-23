from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty, AliasProperty
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button

# Fundo da janela
Window.clearcolor = (1, 1, 1, 1)

class CalculatorWidget(BoxLayout):
    num1 = NumericProperty(10)
    num2 = NumericProperty(5)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 15
        self.padding = 30

        self.title = Label(
            text="Calculadora com AliasProperty",
            font_size=24,
            color=(0.1, 0.2, 0.6, 1),
            size_hint=(1, None),
            height=40
        )
        self.add_widget(self.title)

        # Entrada de número 1
        self.input1 = TextInput(
            text=str(self.num1),
            multiline=False,
            input_filter='int',
            font_size=20,
            hint_text='Número 1'
        )
        self.input1.bind(text=self.on_input1_change)
        self.add_widget(self.input1)

        # Entrada de número 2
        self.input2 = TextInput(
            text=str(self.num2),
            multiline=False,
            input_filter='int',
            font_size=20,
            hint_text='Número 2'
        )
        self.input2.bind(text=self.on_input2_change)
        self.add_widget(self.input2)

        # Resultado da soma
        self.result_label = Label(
            text=self.get_sum_result(),
            font_size=22,
            color=(0, 0, 0, 1),
            bold=True
        )
        self.add_widget(self.result_label)

        # Atualiza o texto do resultado sempre que valores mudam
        self.bind(num1=self.update_result)
        self.bind(num2=self.update_result)

    def on_input1_change(self, instance, value):
        try:
            self.num1 = int(value)
        except:
            pass

    def on_input2_change(self, instance, value):
        try:
            self.num2 = int(value)
        except:
            pass

    # AliasProperty getter
    def get_sum_result(self):
        return f"Soma: {self.num1 + self.num2}"

    # AliasProperty (sem setter, apenas leitura)
    sum_result = AliasProperty(get_sum_result, None, bind=('num1', 'num2'))

    def update_result(self, *args):
        self.result_label.text = self.get_sum_result()

class AliasPropApp(App):
    def build(self):
        return CalculatorWidget()

if __name__ == '__main__':
    AliasPropApp().run()
