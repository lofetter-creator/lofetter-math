from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.clock import Clock
import random
import time

Window.clearcolor = (0.96, 0.9, 0.83, 1)  # Теплий бежевий фон

class MathGameApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.difficulty = None
        self.current_round = 0
        self.correct_answers = 0
        self.current_answer = None
        self.start_time = None
        self.total_time = 0
        self.all_problems = []
    
    def build(self):
        self.title = 'Швидкий Рахунок'
        return self.create_menu()
    
    def create_menu(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Заголовок
        title = Label(
            text='Швидкий Рахунок',
            font_size='28sp',
            bold=True,
            color=(0.24, 0.18, 0.12, 1),
            size_hint=(1, 0.2)
        )
        layout.add_widget(title)
        
        subtitle = Label(
            text='Обирай рівень, козаче!',
            font_size='16sp',
            color=(0.42, 0.35, 0.28, 1),
            size_hint=(1, 0.1)
        )
        layout.add_widget(subtitle)
        
        # Кнопки рівнів
        levels = [
            ('ЛЕГКИЙ', 'easy', (0.5, 0.65, 0.31, 1)),
            ('ВАЖКИЙ', 'hard', (0.83, 0.65, 0.45, 1)),
            ('НАДВАЖКИЙ', 'extreme', (0.79, 0.44, 0.39, 1))
        ]
        
        for text, level, color in levels:
            btn = Button(
                text=text,
                font_size='18sp',
                bold=True,
                background_color=color,
                background_normal='',
                size_hint=(1, 0.15)
            )
            btn.bind(on_press=lambda x, l=level: self.start_game(l))
            layout.add_widget(btn)
        
        info = Label(
            text='Нескінченний режим!',
            font_size='14sp',
            italic=True,
            color=(0.5, 0.65, 0.31, 1),
            size_hint=(1, 0.1)
        )
        layout.add_widget(info)
        
        return layout
    
    def generate_all_problems(self):
        problems = []
        
        if self.difficulty == "easy":
            for a in range(10, 100):
                for b in range(10, 100):
                    for op in ['+', '-']:
                        problems.append((f"{a} {op} {b}", eval(f"{a} {op} {b}")))
            
            for a in range(2, 13):
                for b in range(2, 13):
                    problems.append((f"{a} * {b}", a * b))
        
        elif self.difficulty == "hard":
            for _ in range(10000):
                a = random.randint(100, 999)
                b = random.randint(100, 999)
                c = random.randint(100, 999)
                op1 = random.choice(['+', '-'])
                op2 = random.choice(['+', '-'])
                expr = f"{a} {op1} {b} {op2} {c}"
                problems.append((expr, eval(expr)))
        
        else:  # extreme
            for _ in range(10000):
                a = random.randint(1000, 9999)
                b = random.randint(1000, 9999)
                c = random.randint(1000, 9999)
                d = random.randint(1000, 9999)
                
                op1 = random.choice(['+', '-'])
                op2 = random.choice(['+', '-'])
                op3 = random.choice(['+', '-'])
                
                structures = [
                    f"({a} {op1} {b}) {op2} ({c} {op3} {d})",
                    f"{a} {op1} ({b} {op2} {c}) {op3} {d}",
                    f"({a} {op1} {b} {op2} {c}) {op3} {d}"
                ]
                expr = random.choice(structures)
                problems.append((expr, eval(expr)))
        
        random.shuffle(problems)
        return problems
    
    def start_game(self, difficulty):
        self.difficulty = difficulty
        self.current_round = 0
        self.correct_answers = 0
        self.total_time = 0
        self.all_problems = self.generate_all_problems()
        self.next_question()
    
    def next_question(self):
        if self.current_round >= len(self.all_problems):
            self.show_results(completed=True)
            return
        
        self.current_round += 1
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Прогрес
        progress = Label(
            text=f'Приклад {self.current_round} / {len(self.all_problems)}',
            font_size='14sp',
            color=(0.54, 0.45, 0.33, 1),
            size_hint=(1, 0.08)
        )
        layout.add_widget(progress)
        
        # Приклад
        expression, answer = self.all_problems[self.current_round - 1]
        self.current_answer = answer
        self.start_time = time.time()
        
        font_size = self.get_font_size(expression)
        
        problem = Label(
            text=expression,
            font_size=f'{font_size}sp',
            bold=True,
            color=(0.24, 0.18, 0.12, 1),
            size_hint=(1, 0.25)
        )
        layout.add_widget(problem)
        
        # Поле вводу
        self.answer_input = TextInput(
            hint_text='Твоя відповідь',
            font_size='20sp',
            multiline=False,
            input_filter='int',
            size_hint=(1, 0.12),
            background_color=(1, 1, 1, 1),
            foreground_color=(0.24, 0.18, 0.12, 1)
        )
        self.answer_input.bind(on_text_validate=self.check_answer)
        layout.add_widget(self.answer_input)
        
        # Кнопка відповіді
        submit_btn = Button(
            text='Відповісти',
            font_size='18sp',
            bold=True,
            background_color=(0.5, 0.65, 0.31, 1),
            background_normal='',
            size_hint=(1, 0.15)
        )
        submit_btn.bind(on_press=self.check_answer)
        layout.add_widget(submit_btn)
        
        # Статистика
        stats = Label(
            text=f'Правильних: {self.correct_answers}',
            font_size='14sp',
            color=(0.5, 0.65, 0.31, 1),
            size_hint=(1, 0.08)
        )
        layout.add_widget(stats)
        
        # Кнопка меню
        menu_btn = Button(
            text='<- Меню',
            font_size='14sp',
            background_color=(0.79, 0.44, 0.39, 1),
            background_normal='',
            size_hint=(1, 0.1)
        )
        menu_btn.bind(on_press=self.confirm_exit)
        layout.add_widget(menu_btn)
        
        self.root.clear_widgets()
        self.root.add_widget(layout)
    
    def get_font_size(self, text):
        length = len(text)
        if self.difficulty == "extreme":
            if length <= 15:
                return 24
            elif length <= 25:
                return 20
            elif length <= 35:
                return 16
            else:
                return 14
        else:
            if length <= 7:
                return 32
            elif length <= 12:
                return 28
            elif length <= 20:
                return 24
            else:
                return 20
    
    def check_answer(self, instance):
        try:
            user_answer = int(self.answer_input.text)
            elapsed = time.time() - self.start_time
            self.total_time += elapsed
            
            if user_answer == self.current_answer:
                self.correct_answers += 1
                self.show_feedback(True, elapsed)
            else:
                self.show_feedback(False, elapsed)
        except:
            self.show_popup('Ой!', 'Введи число, козаче!')
    
    def show_feedback(self, correct, elapsed):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        if correct:
            emoji = '[+]'
            text = 'Правильно!'
            color = (0.5, 0.65, 0.31, 1)
        else:
            emoji = '[-]'
            text = f'Неправильно!\nПравильна відповідь: {self.current_answer}'
            color = (0.79, 0.44, 0.39, 1)
        
        feedback = Label(
            text=f'{emoji}\n{text}',
            font_size='24sp',
            bold=True,
            color=color,
            size_hint=(1, 0.6)
        )
        layout.add_widget(feedback)
        
        time_label = Label(
            text=f'Час: {elapsed:.2f}с',
            font_size='18sp',
            color=(0.54, 0.45, 0.33, 1),
            size_hint=(1, 0.2)
        )
        layout.add_widget(time_label)
        
        self.root.clear_widgets()
        self.root.add_widget(layout)
        
        Clock.schedule_once(lambda dt: self.next_question(), 1.5)
    
    def show_results(self, completed=False):
        accuracy = (self.correct_answers / self.current_round) * 100 if self.current_round > 0 else 0
        avg_time = self.total_time / self.current_round if self.current_round > 0 else 0
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title = Label(
            text='Твої результати',
            font_size='24sp',
            bold=True,
            color=(0.24, 0.18, 0.12, 1),
            size_hint=(1, 0.15)
        )
        layout.add_widget(title)
        
        if completed:
            congrats = Label(
                text='Пройшов усі комбінації!',
                font_size='16sp',
                bold=True,
                color=(0.5, 0.65, 0.31, 1),
                size_hint=(1, 0.08)
            )
            layout.add_widget(congrats)
        
        stats_text = f'''Правильних: {self.correct_answers}/{self.current_round}
Точність: {accuracy:.1f}%
Середній час: {avg_time:.2f}с
Загальний час: {self.total_time:.1f}с'''
        
        stats = Label(
            text=stats_text,
            font_size='16sp',
            color=(0.24, 0.18, 0.12, 1),
            size_hint=(1, 0.25)
        )
        layout.add_widget(stats)
        
        if accuracy == 100 and avg_time < 5:
            message = 'КРАСАВА! Ти машина!'
        elif accuracy >= 80:
            message = 'Непогано, козаче!'
        elif accuracy >= 50:
            message = 'Є куди рости!'
        else:
            message = 'Треба тренуватись більше!'
        
        feedback = Label(
            text=message,
            font_size='18sp',
            bold=True,
            color=(0.83, 0.65, 0.45, 1),
            size_hint=(1, 0.12)
        )
        layout.add_widget(feedback)
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.15))
        
        again_btn = Button(
            text='Ще раз',
            font_size='16sp',
            bold=True,
            background_color=(0.5, 0.65, 0.31, 1),
            background_normal=''
        )
        again_btn.bind(on_press=lambda x: self.start_game(self.difficulty))
        btn_layout.add_widget(again_btn)
        
        menu_btn = Button(
            text='Меню',
            font_size='16sp',
            bold=True,
            background_color=(0.83, 0.65, 0.45, 1),
            background_normal=''
        )
        menu_btn.bind(on_press=lambda x: self.go_to_menu())
        btn_layout.add_widget(menu_btn)
        
        layout.add_widget(btn_layout)
        
        self.root.clear_widgets()
        self.root.add_widget(layout)
    
    def confirm_exit(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        msg = Label(text='Вийти в меню?\nПрогрес буде втрачено.', font_size='16sp')
        content.add_widget(msg)
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.3))
        
        yes_btn = Button(text='Так', font_size='16sp')
        no_btn = Button(text='Ні', font_size='16sp')
        
        popup = Popup(title='Вихід', content=content, size_hint=(0.8, 0.4))
        
        yes_btn.bind(on_press=lambda x: self.exit_to_menu(popup))
        no_btn.bind(on_press=popup.dismiss)
        
        btn_layout.add_widget(yes_btn)
        btn_layout.add_widget(no_btn)
        content.add_widget(btn_layout)
        
        popup.open()
    
    def exit_to_menu(self, popup):
        popup.dismiss()
        self.go_to_menu()
    
    def go_to_menu(self):
        self.root.clear_widgets()
        self.root.add_widget(self.create_menu())
    
    def show_popup(self, title, message):
        content = Label(text=message, font_size='16sp')
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.3))
        popup.open()

if __name__ == '__main__':
    MathGameApp().run()
