from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window
import re

Window.clearcolor = (1, 1, 1, 1)

class ValidatedInputWidget(BoxLayout):
    validated_text = StringProperty("Texto válido aparecerá aqui.")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 20
        self.padding = 30

        self.title = Label(
            text="Validador de Texto (sem números e mínimo 5 letras)",
            font_size=20,
            bold=True,
            color=(0.2, 0.2, 0.5, 1),
            size_hint=(1, None),
            height=40
        )
        self.add_widget(self.title)

        self.input_field = TextInput(
            hint_text="Digite aqui...",
            multiline=False,
            font_size=18,
            size_hint=(1, None),
            height=50
        )
        self.input_field.bind(text=self.validate_input)
        self.add_widget(self.input_field)

        self.output_label = Label(
            text=self.validated_text,
            font_size=18,
            color=(0, 0, 0, 1),
            size_hint=(1, None),
            height=40
        )
        self.add_widget(self.output_label)

        # Vincula mudanças da propriedade ao método que atualiza o Label
        self.bind(validated_text=self.update_label)

    def validate_input(self, instance, value):
        if len(value) >= 5 and not re.search(r'\d', value):
            self.validated_text = value
        else:
            # opcional: mensagem temporária ou não fazer nada
            pass

    def update_label(self, instance, value):
        self.output_label.text = f"Texto validado: {value}"

class ValidationPropApp(App):
    def build(self):
        return ValidatedInputWidget()

if __name__ == "__main__":
    ValidationPropApp().run()
