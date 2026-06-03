import tkinter as tk 
import random
import json

words_file = "words.txt"
game_file = "game.json"

viselica = [
    """
       ┌─────────┐
       │         │
       │         
       │         
       │        
       │         
    ───┴─────────────
    """,
    """
       ┌─────────┐
       │         │
       │         O
       │         
       │        
       │         
    ───┴─────────────
    """,
    """
       ┌─────────┐
       │         │
       │         O
       │         │
       │        
       │         
    ───┴─────────────
    """,
    """
       ┌─────────┐
       │         │
       │         O
       │        /│
       │        
       │         
    ───┴─────────────
    """,
    """
       ┌─────────┐
       │         │
       │         O
       │        /│\\
       │        
       │         
    ───┴─────────────
    """,
    """
       ┌─────────┐
       │         │
       │         O
       │        /│\\
       │        / 
       │         
    ───┴─────────────
    """,
    """
       ┌─────────┐
       │         │
       │         O
       │        /│\\
       │        / \\
       │         
    ───┴─────────────
    """
]

class Hangman:
    def __init__(self, root):
        self.root = root #ссылка на главное окно
        self.root.title("Виселица") #установка заголовка окна
        self.root.geometry("700x600") #установка размеров окна
        self.root.resizable(False, False) #запрет изменения размера окна
        
        self.coins = self.load().get("coins", 0) #загрузка монет
        self.menu() #отображение главного меню при запуске
        
    #загрузка данных из JSON-файла
    def load(self):
        with open(game_file, "r", encoding="utf-8") as f:
            #открытие файла сохранения в режиме чтения
            return json.load(f) #преобразует содержимое файла в Python

    #сохранение данных в JSON-файл
    def save(self):
        with open(game_file, "w", encoding="utf-8") as f:
            #открытие файла сохранения в режиме записи
            json.dump({"coins": self.coins}, f) #записывает в JSON-файл
            
    #очистка окна от всех элементов
    def clear(self):
        for widget in self.root.winfo_children(): #список виджетов
            widget.destroy() #удаляет виджеты

    #показывает главное окно
    def menu(self):
        self.clear() #очищает окно
        
        tk.Label(self.root, text="ВИСЕЛИЦА", font=("Arial", 48, "bold")).pack(pady=60)
        #создается надпись "Виселица" с жирным шрифтом Arial 48 и отступом 60 пикселей
        #сверху и снизу
        tk.Button(self.root, text="Начать игру", font=("Arial", 24), 
                 command=self.start).pack(pady=20)
        #создается кнопка "Начать игру" со шрифтом Arial 24, при нажатии начинается игра
        #размещается кнопка с отступом 20 пикселей сверху и снизу
        tk.Button(self.root, text="Правила", font=("Arial", 18), 
                 command=self.pravila).pack(pady=10)
        #создается кнопка "Правила" со шрифтом Arial 18, при нажатии открывается экран правил
        #размещается кнопка с отступом 10 пикселей сверху и снизу

    #экран правил
    def pravila(self):
        self.clear() #очищается окно
        
        
        tk.Button(self.root, text="←", font=("Arial", 18), 
                 command=self.menu).place(x=10, y=10)
        #создается кнопка "←" со шрифтом Arial 18, при нажатии показывает главное окно
        #размещается кнопка 10 пикселей от левого края и 10 сверху
        
        tk.Label(self.root, text="📖 ПРАВИЛА ИГРЫ", font=("Arial", 32, "bold")).pack(pady=20)
        #создается надпись "Правила игры" с жирным шрифтом Arial 32, размещается 20 пикселей
        #сверху и снизу
        
        #текст правил
        text_pravil = (
            "Перед вами показывается алфавит, виселица и спрятанное слово.\n\n"
            "Вы должны угадать слово за 6 ходов, нажимая мышкой на буквы алфавита на экране.\n\n"
            "За каждую победу вы получаете 10 монеток.\n\n"
            "Вы можете открыть неограниченное количество букв по 5 монеток за каждую.\n\n"
            "Если Вы угадываете слово, то можете перейти дальше, либо выйти на главное меню."
        )
        
        tk.Label(self.root, text=text_pravil, font=("Arial", 14), justify="left", 
                wraplength=600).pack(pady=20, padx=30)
        #создается текст со шрифтом Arial 14 с выравниваем по левому краю, переносом слов
        #по ширине, если строка длиннее 600 пикселей, отступом 20 пикселей сверху и снизу
        #и 30 пикселей справа и слева

    #запуск новой игры
    def start(self):
        self.clear()#очищает экран
        self.zagadanoe_slovo = random.choice(open(words_file, encoding="utf-8").read().split())
        #открывает файл со словами, читает содержимое, разбивает строку на список слов
        #и выбирает случайное слово из списка
        self.used_letters = set() #множество использованных букв, не допускающее повторений
        self.oshibka = 0 #счётчик ошибок
        
        tk.Button(self.root, text="←", font=("Arial", 18), 
                 command=self.menu).place(x=10, y=10)
        #создается кнопка "←" со шрифтом Arial 18, при нажатии показывает главное окно
        #размещается кнопка 10 пикселей от левого края и 10 сверху
        
        self.coins_kartinka = tk.Label(self.root, text=f"🪙 {self.coins}", font=("Arial", 16))
        self.coins_kartinka.pack(pady=5)
        #создается надпись с количеством монет со шрифтом Arial 16
        #размещается с отступом 5 пикселей сверху и снизу
        
        self.word = tk.Label(self.root, text="", font=("Arial", 32, "bold"))
        self.word.pack(pady=10)
        #создается надпись с загаданным словом с жирным шрифтом Arial 32, отступом 10 
        #пикселей сверху и снизу
        
        self.hangman_kartinka = tk.Label(self.root, text=viselica[0], font=("Courier", 12), justify="left")
        self.hangman_kartinka.pack(pady=10)
        #создается надпись с картинкой виселицы, используется моноширинный шрифт, в котором
        #все буквы одинаковой ширины, используется выравнивание по левому краю
        #размещается с отступом 10 пикселей сверху и снизу
        
        keyboard_frame = tk.Frame(self.root) #создается рамка для клавиатуры
        keyboard_frame.pack(pady=15) #размещается с отступом 15 пикселей сверху и снизу
        self.used_knopka = {} #заносятся использованные буквы, чтобы отключать кнопку
        #после нажатия

        #создание кнопок
        for i, letter in enumerate("абвгдеёжзийклмнопрстуфхцчшщъыьэюя"):
            #enumerate возвращает индекс и значение 
            btn = tk.Button(keyboard_frame, text=letter.upper(), font=("Arial", 12),
                           width=3, command=lambda l=letter: self.click_letter(l))
            #создаются кнопки с заглавными буквами со шрифтом Arial 12, ширина 3 символа
            #лямбда обходит проблему замыкания в цикле, без нее все кнопки вызывали бы функцию для последней буквы
            btn.grid(row=i//10, column=i%10, padx=2, pady=2)
            #размещает кнопки по 10 в строку, с отступом 2 пикселя сверху и снизу, справа и слева
            self.used_knopka[letter] = btn #сохраняет кнопку для дальнейшего изменения ее состояния
        
        self.knopka_podskazki = tk.Button(self.root, text="💡", font=("Arial", 18), width=3,
                                 command=self.use_podskazku)
        #создается кнопка подсказки со шрифтом Arial 18, шириной 3 символа
        #при нажатии применяется подсказка
        self.knopka_podskazki.place(relx=0.98, rely=0.98, anchor="se")
        #размещается на расстоянии 98% от левой и верхней границы окна
        self.obnovlenie() #обновляет интерфейс

    def obnovlenie(self):
        #отображение слова с угаданными буквами
        display = " ".join(c.upper() if c in self.used_letters else "_" for c in self.zagadanoe_slovo)
        #для каждой угаданной буквы показывается заглавная, иначе "_", объединяется через пробел
        self.word.config(text=display)
        #обновление текста загаданного слова
        self.coins_kartinka.config(text=f"🪙 {self.coins}")
        #обновление кол-ва монет
        self.hangman_kartinka.config(text=viselica[self.oshibka])
        #обновление картинки виселицы по кол-ву ошибок
        self.knopka_podskazki.config(state="normal" if self.coins >= 5 else "disabled")
        #обновление кнопки подсказки, проверка кол-ва монет для подсказки

    def check_game_end(self):
        #проверка победы
        if all(c in self.used_letters for c in self.zagadanoe_slovo):
            #проверяется угаданы ли все буквы в слове или нет
            self.resultat(True)
            #если угаданы, показывается экран победы
            return True
        
        #проверка поражения
        if self.oshibka >= 6: #если кол-во ошибок 6 или больше, показывается экран поражения
            self.resultat(False)
            return True
        
        return False
    
    #обработка нажатия на букву
    def click_letter(self, letter):
        if letter in self.used_letters: #если буква уже нажималась, ничего не происходит
            return
            
        self.used_letters.add(letter)
        #добавление буквы в множество использованных
        self.used_knopka[letter].config(state="disabled", 
                                          bg="lightgreen" if letter in self.zagadanoe_slovo else "lightcoral")
        #отключение кнопки и подсветка цветом, светло-зеленый если буква есть в слове, светло-красный если нет
        if letter not in self.zagadanoe_slovo: #если буквы нет в загаданном слове
            self.oshibka += 1
        #то увеличение счетчика ошибок
        
        self.obnovlenie() #обновление интерфейса
        self.check_game_end() #проверка конца игры

    #использование подсказки
    def use_podskazku(self):
        if self.coins < 5: #если монет меньше 5, то ничего не происходит
            return
            
        close_letters = [c for c in self.zagadanoe_slovo if c not in self.used_letters]
        #собирает все буквы слова, которых нет в множестве использованных
        if not close_letters: #если все буквы открыты - выход
            return
            
        random_close = random.choice(close_letters) #случайная буква из неоткрытых
        self.used_letters.add(random_close) #добавление случайной буквы из неоткрытых в множество использованных
        self.used_knopka[random_close].config(state="disabled", bg="lightblue")
        #буква подсвечивается светло-голубым и становится неактивной
        self.coins -= 5 #уменьшает счётчик монет на 5
        self.save() #сохранение
        self.obnovlenie() #обновление интерфейса
        self.check_game_end() #проверка завершения игры

    def resultat(self, win):
        #отображение экрана результата
        self.clear() #очищается экран
        
        #заголовок результата
        result_text = "🎉 ПОБЕДА!" if win else "💀 ПОРАЖЕНИЕ"
        result_color = "green" if win else "red" #цвет тектса победы или поражения
        tk.Label(self.root, text=result_text, font=("Arial", 40, "bold"), fg=result_color).pack(pady=20)
        #создается надпись с результатом игры жирным шрифтом Arial 40
        #выбирается цвет в зависимости от результата
        #размещается с отступом 20 пикселей сверху и снизу
        
        tk.Label(self.root, text=f"Слово: {self.zagadanoe_slovo.upper()}", font=("Arial", 24)).pack(pady=10)
        #создается надпись с загаданным словом заглавными буквами шрифтом Arial 24
        #размещается с отступом 10 пикселей сверху и снизу
        
        if not win:
            tk.Label(self.root, text=viselica[6], font=("Courier", 12), justify="left").pack(pady=10)
        #если поражение, создается надпись с рисунком итоговой виселицы со шрифтом Courier 12
        #выравниванием по левому краю, отступом 10 пикселей сверху и снизу
        
        if win: #если победа
            self.coins += 10 #начисляется 10 монет
            self.save() #сохранение
            tk.Label(self.root, text=f"+10 монет 🪙 (Всего: {self.coins})", 
                    font=("Arial", 18), fg="gold").pack(pady=10)
            #создается надпись с начислением 10 монет и итоговым кол-вом шрифтом Arial 18
            #желтым цветом и размещается с отступом 10 пикселей сверху и снизу
            
        btn_frame = tk.Frame(self.root) #создается рамка для кнопок
        btn_frame.pack(pady=30) #размещаются с отступом 30 пикселей сверху и снизу
        
        tk.Button(btn_frame, text="Новая игра", font=("Arial", 18), 
                 command=self.start, width=12).grid(row=0, column=0, padx=10)
        #создается кнопка "Новая игра" со шрифтом Arial 18, при нажатии
        #начинается новая игра, шириной 12 символов, размещаются кнопки в одну строку рядом
        #с отступом 10 пикселей слева и справа
        tk.Button(btn_frame, text="В меню", font=("Arial", 18), 
                 command=self.menu, width=12).grid(row=0, column=1, padx=10)
        #создается кнопка "В меню" со шрифтом Arial 18, при нажатии
        #переход в главное меню, ширина 12 символов, размещается справа от кнопки "Новая игра"
        #с отступом 10 пикселей слева и справа

if __name__ == "__main__": #проверка, что игра запущена как основная программа
    root = tk.Tk() #создание интерфейса главного окна
    Hangman(root) #создание экземпляра игры
    root.mainloop() #ожидание действия пользователя
