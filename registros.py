import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.properties import BooleanProperty
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.popup import Popup

TASK_FILE = "tasks.json"
Window.size = (450, 700)


class TaskItem(BoxLayout):
    completed = BooleanProperty(False)

    def __init__(self, text, index, toggle_callback, delete_callback, **kwargs):
        super().__init__(orientation='horizontal',
                         size_hint_y=None,
                         height=dp(60),
                         padding=(dp(12), 0, dp(12), 0),
                         spacing=dp(10),
                         **kwargs)
        self.text = text
        self.index = index
        self.toggle_callback = toggle_callback
        self.delete_callback = delete_callback

        with self.canvas.before:
            self.bg_color = Color(0.95, 0.95, 0.97, 1)
            self.bg_rect = RoundedRectangle(radius=[dp(12)]*4)
        self.bind(pos=self._update_bg, size=self._update_bg)

        self.label = Label(text=f"{index}. {text}", halign='left', valign='middle',
                           markup=True, color=(0.1,0.1,0.12,1))
        self.label.bind(size=self._update_label)
        self.add_widget(self.label)

        self.btn_done = Button(text="✔", size_hint_x=None, width=dp(40),
                               background_normal='', background_color=(0.2,0.6,1,1),
                               color=(1,1,1,1), bold=True)
        self.btn_done.bind(on_release=self.on_toggle)
        self.add_widget(self.btn_done)

        self.btn_delete = Button(text="✖", size_hint_x=None, width=dp(40),
                                 background_normal='', background_color=(1,0.3,0.35,1),
                                 color=(1,1,1,1), bold=True)
        self.btn_delete.bind(on_release=self.on_delete)
        self.add_widget(self.btn_delete)

        if kwargs.get("completed", False):
            self.completed = True
            self.label.text = f"{self.index}. [s]{self.text}[/s]"

    def _update_bg(self, *_):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def _update_label(self, *_):
        self.label.text_size = (self.label.width - dp(10), None)

    def on_toggle(self, *_):
        self.completed = not self.completed
        self.label.text = f"{self.index}. [s]{self.text}[/s]" if self.completed else f"{self.index}. {self.text}"
        self.toggle_callback(self.index-1, self.completed)

    def on_delete(self, *_):
        self.delete_callback(self.index-1)


class TodoAppUI(BoxLayout):
    """Interface principal"""

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=dp(16), spacing=dp(12), **kwargs)

        self.header = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(80))
        self.title_label = Label(text="[b]Minha Lista de Tarefas[/b]",
                                 markup=True, font_size='22sp', color=(0.1,0.1,0.12,1),
                                 size_hint_y=None, height=dp(36))
        self.counter_label = Label(text="0 tarefas", size_hint_y=None, height=dp(20),
                                   font_size='14sp', color=(0.3,0.3,0.35,1))
        self.header.add_widget(self.title_label)
        self.header.add_widget(self.counter_label)
        self.add_widget(self.header)

        # Input row
        self.input_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(8))
        self.input = TextInput(hint_text="Digite uma tarefa...",
                               multiline=False, size_hint_x=0.62,
                               background_normal='', background_active='',
                               background_color=(1,1,1,1),
                               foreground_color=(0.1,0.1,0.12,1),
                               cursor_color=(0.2,0.4,1,1))
        self.btn_add = Button(text="Adicionar", bold=True, size_hint_x=0.19,
                              background_normal='', background_color=(0.2,0.6,1,1), color=(1,1,1,1))
        self.btn_add.bind(on_release=self.on_add)
        self.btn_clear = Button(text="Limpar tudo", bold=True, size_hint_x=0.19,
                                background_normal='', background_color=(1,0.3,0.35,1), color=(1,1,1,1))
        self.btn_clear.bind(on_release=self.on_clear_confirm)
        self.input_row.add_widget(self.input)
        self.input_row.add_widget(self.btn_add)
        self.input_row.add_widget(self.btn_clear)
        self.add_widget(self.input_row)

        self.feedback = Label(text='', color=(0.85,0.1,0.1,1), size_hint_y=None, height=dp(18), font_size='13sp')
        self.add_widget(self.feedback)

        self.scroll = ScrollView(size_hint=(1,1))
        self.task_list = GridLayout(cols=1, spacing=dp(10), size_hint_y=None, padding=(0,dp(4)))
        self.task_list.bind(minimum_height=self.task_list.setter('height'))
        self.scroll.add_widget(self.task_list)
        self.add_widget(self.scroll)

        self.tasks = []
        self.load_tasks()
        self.render_tasks()

    def on_add(self, *_):
        text = (self.input.text or '').strip()
        if not text:
            self.show_feedback("Insira uma tarefa válida")
            return
        self.tasks.append({"text": text, "completed": False})
        self.save_tasks()
        self.input.text = ''
        self.render_tasks()
        self.scroll.scroll_y = 1
        self.show_feedback("Tarefa adicionada!")

    def on_clear_confirm(self, *_):
        popup = Popup(title="Confirmação", size_hint=(0.7,0.3))
        box = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(12))
        box.add_widget(Label(text="Deseja realmente limpar toda a lista?"))
        btn_box = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(12))
        btn_yes = Button(text="Sim")
        btn_no = Button(text="Não")
        btn_yes.bind(on_release=lambda x: (self.on_clear(), popup.dismiss()))
        btn_no.bind(on_release=popup.dismiss)
        btn_box.add_widget(btn_yes)
        btn_box.add_widget(btn_no)
        box.add_widget(btn_box)
        popup.content = box
        popup.open()

    def on_clear(self, *_):
        self.tasks.clear()
        self.save_tasks()
        self.render_tasks()
        self.show_feedback("Lista limpa!")

    def toggle_completed(self, index, completed):
        self.tasks[index]["completed"] = completed
        self.save_tasks()
        self.update_counter()

    def delete_task(self, index):
        del self.tasks[index]
        self.save_tasks()
        self.render_tasks()
        self.show_feedback("Tarefa removida!")

    def render_tasks(self):
        self.task_list.clear_widgets()
        for i, t in enumerate(self.tasks, start=1):
            item = TaskItem(t["text"], i,
                            toggle_callback=self.toggle_completed,
                            delete_callback=self.delete_task,
                            completed=t.get("completed", False))
            self.task_list.add_widget(item)
        self.update_counter()

    def show_feedback(self, message, duration=2.0):
        self.feedback.text = message
        if not message: return
        Clock.unschedule(self.clear_feedback)
        Clock.schedule_once(self.clear_feedback, duration)

    def clear_feedback(self, *_):
        self.feedback.text = ''

    def update_counter(self):
        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t.get("completed"))
        self.counter_label.text = f"{total} tarefas ({done} concluídas)"

    def save_tasks(self):
        try:
            with open(TASK_FILE, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Erro ao salvar tarefas:", e)

    def load_tasks(self):
        if os.path.exists(TASK_FILE):
            try:
                with open(TASK_FILE, "r", encoding="utf-8") as f:
                    self.tasks = json.load(f)
            except Exception:
                self.tasks = []
        else:
            self.tasks = []


class TodoApp(App):
    title = "Lista de Tarefas Interativa"

    def build(self):
        Window.clearcolor = (0.97,0.97,1,1)
        return TodoAppUI()


if __name__ == '__main__':
    TodoApp().run()
