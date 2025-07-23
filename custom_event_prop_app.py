from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window

Window.clearcolor = (1, 1, 1, 1)  # fundo branco

class MyCustomWidget(BoxLayout):
    message = StringProperty("")

    # Declara evento personalizado
    __events__ = ('on_message_changed',)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 20

        self.title_label = Label(
            text="Evento Personalizado - on_message_changed",
            font_size=22,
            color=(0.1, 0.2, 0.6, 1),
            size_hint=(1, None),
            height=40
        )
        self.add_widget(self.title_label)

        self.input_message = TextInput(
            multiline=False,
            hint_text="Digite uma mensagem",
            font_size=18,
            size_hint=(1, None),
            height=40
        )
        self.add_widget(self.input_message)

        self.update_button = Button(
            text="Atualizar Mensagem",
            size_hint=(1, None),
            height=50,
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            font_size=18
        )
        self.update_button.bind(on_release=self.change_message)
        self.add_widget(self.update_button)

        self.log_label = Label(
            text="Log do Evento:",
            font_size=18,
            color=(0, 0, 0, 1),
            size_hint=(1, None),
            height=60
        )
        self.add_widget(self.log_label)

        # Vincula o evento personalizado a um método
        self.bind(on_message_changed=self.on_message_changed)

    def change_message(self, *args):
        new_msg = self.input_message.text.strip()
        self.message = new_msg

    def on_message_changed(self, instance, value):
        # Atualiza o log quando o evento é disparado
        self.log_label.text = f"Log do Evento: {value}"

    # Sobrescreve o setter da propriedade para disparar evento
    def on_message(self, instance, value):
        self.dispatch('on_message_changed', value)

class CustomEventPropApp(App):
    def build(self):
        return MyCustomWidget()

if __name__ == "__main__":
    CustomEventPropApp().run()
