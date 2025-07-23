from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

Window.clearcolor = (1, 1, 1, 1)  # Fundo branco

class StatusIndicator(BoxLayout):
    is_active = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Pode ser expandido com gráficos, animações etc., mas simples para demo

class MainControlWidget(BoxLayout):
    status_obj = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 20

        # Instancia o status_obj
        self.status_obj = StatusIndicator()

        # Label que reage a status_obj.is_active
        self.status_label = Label(
            text=self._get_status_text(),
            font_size=24,
            bold=True,
            size_hint=(1, None),
            height=50,
            color=self._get_status_color()
        )
        self.add_widget(self.status_label)

        # Botão para alternar o status
        self.toggle_button = Button(
            text="Alternar Status",
            size_hint=(1, None),
            height=50,
            background_color=(0.3, 0.5, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size=18
        )
        self.toggle_button.bind(on_release=self.toggle_status)
        self.add_widget(self.toggle_button)

        # Atualiza label sempre que status_obj.is_active mudar
        self.status_obj.bind(is_active=self.update_label)

    def _get_status_text(self):
        return "Ativo" if self.status_obj.is_active else "Inativo"

    def _get_status_color(self):
        return (0, 0.6, 0, 1) if self.status_obj.is_active else (0.6, 0, 0, 1)

    def toggle_status(self, *args):
        self.status_obj.is_active = not self.status_obj.is_active

    def update_label(self, instance, value):
        self.status_label.text = self._get_status_text()
        self.status_label.color = self._get_status_color()

class NestedPropApp(App):
    def build(self):
        return MainControlWidget()

if __name__ == "__main__":
    NestedPropApp().run()
