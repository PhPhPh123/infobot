"""
    Данный модуль отвечает за рандомизацию и выдачу в чат небольших случайных квестов. Модуль реализует шаблон
    шаблон проектирования Фасад в своей первой функции control_quests. Квесты выдаются в рамках работы новостной сессии
    бота, но API через control_quests позволяет получать новость независимо. Принцип работы модуля следующий:
    выбирается случайный тип новости и передается в квестовую фабрику которая собирает предварительную информацию
    и создает заготовку квеста, которую, затем, соответствующие классы достраивают до готового состояния и в конце,
    фабрика формирует из экземляра квеста строку
"""

import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

from settings_imports_globalVariables import *
import craft.main_artifact_factory


def control_quests() -> str:
    """
    Данная функция является управляющим элементом модуля и реализует шаблон проектирования Фасад
    """
    # Вызывается функция, случайно выбирающая тип квеста
    chosen_quest = choise_quest_group()

    # создает экземпляр класса квестовой фабрики
    quest_former = QuestFactory(chosen_quest)

    # Запуск основгого фабричного метода, который затем запускает строителей отдельных классов
    quest_string = quest_former.start_form()

    return quest_string


def choise_quest_group() -> str:
    """
    Данная функция выбирает случайную группу квеста, например artifact_quest, kill_quest, delivery_quest.
    Она работает с глобальной межмодульной переменной курсора
    """
    quests = tuple(global_bd_sqlite3_cursor.execute("SELECT group_name FROM quest_group"))

    # Квестовые группы добавляются в список
    quests_list = []
    for istuple in quests:
        quests_list.append(istuple[0])

    # Из списка выбирается случайная группа
    chones_quest = random.choice(quests_list)
    return chones_quest


class QuestFactory:
    """
    Данный класс реализует паттерн проектирования Фабрика.
    Он подготавливает предварительную информацию выбором одного из методов, отвечающий за доступ в базу данных,
    достает оттуда значения в виде квестового кортежа и затем, в главном фабричном методе start_form, формирует
    заготовки квестов путем их создания, а затем вызывает метод build_quest для экземляра-заготовки, который достраивает
    их до итоговово состояния. В конце из готового экземляра забирается финальная строка ответа
    """

    def __init__(self, quest_name: str):
        self.quest_name = quest_name
        # Вызываю соответствующий статичный метод на основе принятого имя квеста(имя квеста и имя метода совпадают)
        self.quest_tuple = self.__getattribute__(quest_name)()

    def start_form(self) -> str:
        """
        Данная метод является основным в данном классе-фабрике. Он поэтапно создает экземляр, вызывает метод строитель
        экземпляра и забирает из него строку которую затем возвращает в фасадную функцию control_quests
        """
        quest = None

        # Формирование заготовки
        if self.quest_name == 'artifact_quest':
            quest = ArtifactQuest(self.quest_tuple)
        elif self.quest_name == 'kill_quest':
            quest = KillQuest(self.quest_tuple)
        elif self.quest_name == 'delivery_quest':
            quest = DeliveryQuest(self.quest_tuple)
        elif self.quest_name == 'escort_quest':
            quest = EscortQuest(self.quest_tuple)

        # Вызов строителя
        quest.build_quest()

        # Изъятие итоговой строки
        quest_string = quest.final_string
        return quest_string

    @staticmethod
    def artifact_quest() -> tuple:
        """
        Данный метод достает из базы данных, используя глобальную междумодульную переменную курсора, один единственный
        мир на основе применения сортирующей функции RANDOM() и LIMIT 1. Исключения в блоке WHERE нужны,
        чтобы в отборы не попали квесты, где я не планировал проводить квесты в связи с особым статусом данных классов
        миров. Именно отобранном мире будет находиться артефакт, который необходимо отыскать
        @return: строка-заготовка квеста
        """
        artifact_quest_query = '''
        SELECT worlds.world_name, worlds.danger_name, worlds.class_name
        FROM worlds
        WHERE worlds.class_name != 'Мир-Горка-Стопудова' AND worlds.class_name != 'Мир-смерти'
        ORDER BY RANDOM()
        LIMIT 1'''
        artifact_quest_tuple = tuple(global_bd_sqlite3_cursor.execute(artifact_quest_query))[0]

        assert artifact_quest_tuple, 'база должна вернуть непустое значение'

        return artifact_quest_tuple

    @staticmethod
    def kill_quest() -> tuple:
        """
        Данный метод достает из базы данных, используя глобальную междумодульную переменную курсора, один единственный
        мир на основе применения сортирующей функции RANDOM() и LIMIT 1. Исключения в блоке WHERE нужны,
        чтобы в отборы не попали квесты, где я не планировал проводить квесты в связи с особым статусом данных классов
        миров, не попали миры с нулевой угрозой т.к. там нет врагов и не попали особые типы врагов, которые не являются
        врагами в строгом смысле этого слова(угроза стихийных бедствий), за отсеивание таких угрозы отвечает
        строчка enemies.group_name NOT NULL т.к. группа у этих врагов именно NULL. Именно на отобранном мире будут враги
        которых по квесту нужно уничтожить
        @return: строка-заготовка квеста
        """
        kill_quest_query = '''
        SELECT worlds.world_name, worlds.danger_name, worlds.class_name, enemies.group_name
        FROM worlds
        INNER JOIN worlds_enemies_relations ON worlds.world_name == worlds_enemies_relations.world_name
        INNER JOIN enemies ON worlds_enemies_relations.enemy_name == enemies.enemy_name
        WHERE worlds.danger_name != 'Нулевая угроза'
        AND enemies.group_name NOT NULL
        AND worlds.class_name != 'Мир-Горка-Стопудова' AND worlds.class_name != 'Мир-смерти'
        ORDER BY RANDOM()
        LIMIT 1'''
        kill_quest_tuple = tuple(global_bd_sqlite3_cursor.execute(kill_quest_query))[0]

        assert kill_quest_tuple, 'база должна вернуть непустое значение'

        return kill_quest_tuple

    @staticmethod
    def delivery_quest() -> tuple:
        """
        Данный метод достает из базы данных, используя глобальную междумодульную переменную курсора, один единственный
        мир на основе применения сортирующей функции RANDOM() и LIMIT 1. Исключения в блоке WHERE нужны,
        чтобы в отборы не попали квесты, где я не планировал проводить квесты в связи с особым статусом данных классов
        миров, а также миры, на которых отсутствует импорт. Именно на отобранный мир будет осуществляться доставка
        @return: строка-заготовка квеста
        """
        delivery_quest_query = f'''
        SELECT worlds.world_name, worlds.danger_name, worlds.class_name, trade_import.import_name
        FROM worlds
        INNER JOIN worlds_trade_import_relations ON worlds.world_name == worlds_trade_import_relations.world_name
        INNER JOIN trade_import ON worlds_trade_import_relations.import_name == trade_import.import_name
        WHERE trade_import.import_name != 'Импорт-отсутствует' 
        AND worlds.class_name != 'Мир-Горка-Стопудова' AND worlds.class_name != 'Мир-смерти'
        ORDER BY RANDOM()
        LIMIT 1'''

        delivery_quest_tuple = tuple(global_bd_sqlite3_cursor.execute(delivery_quest_query))[0]
        assert delivery_quest_tuple, 'база должна вернуть непустое значение'

        return delivery_quest_tuple

    @staticmethod
    def escort_quest() -> tuple[tuple, tuple]:
        """
        Данный метод достает из базы данных, используя глобальную междумодульную переменную курсора, два мира, первый из
        которых будет отправной точкой, а второй - точкой прибытия на основе применения
        сортирующей функции RANDOM() и LIMIT 2. Отсеивание ненужных миров производится через стандартные 2 типа мира,
        на которых не будет ни одного квеста, миры с населением меньше 10000 и слишком опасные миры, где красная угроза
        Исключения в блоке WHERE нужны, чтобы в отборы не попали квесты, где я не планировал проводить квесты в связи с
        особым статусом данных классов миров, а также миры, на которых отсутствует импорт, также миры со слишком малым
        населением или боевые зоны тоже должны быть исключены
        @return: строка-заготовка квеста
        """
        escort_quest_query = f'''
        SELECT  world_name, danger_name
        FROM worlds
        WHERE world_population > 10000 
        AND danger_name != 'Красная угроза'
        AND worlds.class_name != 'Мир-Горка-Стопудова'  
        AND worlds.class_name != 'Мир-смерти'
        ORDER BY RANDOM()
        LIMIT 2'''

        # Здесь, в отличии от остальных квестов, я получаю полностью кортеж с кортежами, а не достаю с кортежа значение
        # с нулевым индексом
        delivery_escort_tuple = tuple(global_bd_sqlite3_cursor.execute(escort_quest_query))
        assert delivery_escort_tuple, 'база должна вернуть непустое значение'

        return delivery_escort_tuple


class Quest(ABC):
    """
    Данный абстрактный класс является базовым и содержит в себе аттрибуты и методы, характерные для всех квестов.
    Данный класс реализует паттерн проектирования Шаблонный метод - он имеет методы, которые прямо наследуются
    дочерними классами и реализуются ими т.к. являются для всех дочерних классов общими так и абстрактные методы
    которые необходимо реализовывать в каждом классе самостоятельно
    """

    def __init__(self, quest_tuple):
        self.quest_tuple = quest_tuple
        self.quest_name = None

        self.quest_dict = None
        self.quest_description = None
        self.quest_subtype = None

        self.final_string = None

    def load_quest_to_log(self) -> None:
        """
        Данный метод записывает в файл-лога текст квеста используя соответствующий тэг
        @return: None
        """
        logger.info('[quest]' + self.final_string)

    def form_quest_name(self) -> None:
        """
        Данный метод формирует строку имени квеста используя для этого текущую дату времени(реального). Может быть
        переопределен в дочернем классе если того требует ситуация
        @return: None
        """
        current_date = date.today()
        self.quest_name = f"{self.quest_dict['world_name']}. {self.quest_subtype.capitalize()}. Получение: {current_date}\r\r"

    @staticmethod
    @abstractmethod
    def quest_tuple_to_dict(is_tuple: tuple) -> dict:
        """
        Данный абстрактный метод конвертирует кортеж в словарь. Методы их реализации чуть отличаются и поэтому пусть
        отдельно реализовываются в каждом классе
        @param is_tuple: собственно кортеж с данными по миру/мирам
        @return: кортеж переделанный в словарь с соответствующими ключами
        """
        pass

    @abstractmethod
    def build_quest(self) -> None:
        """
        Основной абстрактный метод, реализующий паттерн проектирования Строитель. Выполняется в виде последовательного
        вызова соответствующий методов, достраивающих аттрибуты
        @return: None
        """
        pass

    @abstractmethod
    def get_quest_pattern_from_db(self) -> None:
        """
        Данный абстрактный метод достает из базы данных нужный паттерн квеста
        @return: строка с шаблоном квеста
        """
        pass

    @abstractmethod
    def form_quest_string(self) -> None:
        """
        Данный метод формирует итоговую строку ответа ботом
        @return: None
        """
        pass


class Reward:
    """
    Данный класс является классом миксином и добавляется как объект множественного наследовнаия в дочерний класс,
    если в нем требуется реализовать стандартную награду за квест в кредитах
    """
    def __init__(self):
        self.quest_dict = None

    def count_reward(self, quest_timer: int) -> int:
        """
        Основной метод класса миксина, подсчитывающий награду за квест
        @param quest_timer: время, за которое игрокам необходимо выполнить квест
        @return: целое число, определяющее награду в кредитах
        """
        base_reward = 100000  # Базовая награда, геймплейно обоснованная в ролке

        timer_modifier = None  # инициализация модификатора
        danger_modifier = 1  # инициализация модификатора, а также его значение при нулевой угрозе

        # Чем выше уровень угрозы, от зеленой к красной, тем выше модификатор и, соответственно, награда
        if self.quest_dict['danger_name'] == 'Зеленая угроза':
            danger_modifier = 1.15
        elif self.quest_dict['danger_name'] == 'Синяя угроза':
            danger_modifier = 1.40
        elif self.quest_dict['danger_name'] == 'Фиолетовая угроза':
            danger_modifier = 1.70
        elif self.quest_dict['danger_name'] == 'Красная угроза':
            danger_modifier = 2

        # Чем меньше времени на выполнение квеста, тем выше модификатор и, соответственно, награда
        if quest_timer == 5:
            timer_modifier = 1.0
        elif quest_timer == 4:
            timer_modifier = 1.2
        elif quest_timer == 3:
            timer_modifier = 1.4
        elif quest_timer == 2:
            timer_modifier = 1.6

        # Базовая награда умножается на модификаторы
        final_reward = int(base_reward * danger_modifier * timer_modifier)
        return final_reward


class ArtifactQuest(Quest):
    """
    Данный класс отвечает за формирование квестом поиска артефактов. Он создает запрос в соседний модуль на
    формирование артефакта и выдачу квестом его названия, а параметры сохраняются в отдельном текстовом файле
    для ГМа
    """

    def __init__(self, quest_tuple: tuple):
        """
        :param quest_tuple: название мира, опасности мира и имперского класса (world_name, danger_name, class_name)
        """
        super().__init__(quest_tuple)
        self.quest_name = 'artifact_quest'
        self.quest_dict = self.quest_tuple_to_dict(quest_tuple)

        self.full_artifact_string = None

    def form_artifact(self) -> None:
        """
        Данный метод реализует шаблон проектирования Адаптер. Он создает иммитацию пользовательского ввода и формирует
        словарь, который отправдаяется в модуль модуль формирования артефактов с целью получить от него строку
        с готовым артефактом
        @return: None
        """
        # грейд артефакта устанавливает прямо-пропорциональную зависимость от сложности мира, на котором будет
        # выполняться квест. Чем сложнее мир тем выше грейд артефакта
        grade_name = None
        if self.quest_dict['danger_name'] in ('Зеленая угроза', 'Нулевая угроза'):
            grade_name = 'зеленый'
        elif self.quest_dict['danger_name'] == 'Синяя угроза':
            grade_name = 'синий'
        elif self.quest_dict['danger_name'] == 'Фиолетовая угроза':
            grade_name = 'фиолетовый'
        elif self.quest_dict['danger_name'] == 'Красная угроза':
            grade_name = 'красный'

        # собственно словарь для API клестового модуля, в будущем можно будет реализовать настройку данного словаря
        # чтобы получить конкретные виды и типы артефактов, но, пока что, я в этом смысла не вижу
        request_dict = {'грейд': grade_name,
                        'группа': 'random',
                        'тип': 'random',
                        'особенность': 'random'}

        self.full_artifact_string = craft.main_artifact_factory.choise_class_objects(request_dict)

    def build_quest(self) -> None:
        """
        Основной метод строитель, поэтапно вызывает все нужные методы построения квеста
        @return: None
        """
        self.form_artifact()
        self.get_quest_pattern_from_db()
        self.form_quest_name()
        self.form_quest_string()
        self.load_artifact_to_log()
        self.load_quest_to_log()

    def get_quest_pattern_from_db(self) -> None:
        """
        Данный метод переопределяет наследован от абстрактного метода класса Quest. Он достает из БД нужный квест.
        В запросе таблица quest_patterns джойниться со всеми связанными таблицами, в т.ч. связью многие ко многим.
        Затем делается отбор на квесты, в которых допустим соответствующий имперский класс и уровень опасности, а группа
        является артефактной. Все это сортируется рандомом и забирается одно значение лимитом 1
        @return:
        """
        quest_query = f"""
        SELECT DISTINCT quest_patterns.quest_name, quest_patterns.quest_text
        FROM quest_patterns
        INNER JOIN quest_patterns_danger_zone_relations USING(quest_name)       
        INNER JOIN danger_zone USING(danger_name)    
        INNER JOIN quest_patterns_imperial_class_relations USING(quest_name)
        INNER JOIN imperial_class USING(class_name)
        WHERE imperial_class.class_name == '{self.quest_dict['class_name']}' 
          AND danger_zone.danger_name == '{self.quest_dict['danger_name']}'
          AND quest_patterns.group_name == 'artifact_quest'
        ORDER BY RANDOM()
        LIMIT 1"""

        # Достается из БД кортеж, используя глобальную переменную курсора
        quest_tuple = tuple(global_bd_sqlite3_cursor.execute(quest_query))
        assert quest_tuple, f'база должна вернуть непустое значение. Неверный запрос: {quest_query}'

        self.quest_subtype = quest_tuple[0][0]  # по факту это quest_patterns.quest_name
        self.quest_description = quest_tuple[0][1]  # по факту это quest_patterns.quest_text

    def form_quest_string(self) -> None:
        """
        Данный метод формирует итоговую строку квеста используя метод format. Самой строке шаблона квеста, хранимой в БД
        фрагменты вставки значений указаны как {} в нужных местах и количество, а также порядок данных вставок зависят
        от квестовой группы
        @return: None
        """
        quest_timer = random.randint(2, 5)  # срок выполнения квеста. В игре он представляет собой количество
        # полноценных сессий игры(4часа реального времени)

        # При создании новых шаблонов квестов в базе данных нужно придерживаться следующей последовательности
        # вставок {} для формата: название мире->имя артефакта->срок выполнения квеста
        formatted_description = self.quest_description.format(self.quest_dict['world_name'],
                                                              self.full_artifact_string.split("\n")[0],
                                                              quest_timer)

        self.final_string = f"[КВЕСТ] {self.quest_name}{formatted_description}"

    @staticmethod
    def quest_tuple_to_dict(is_tuple: tuple) -> dict:
        """
        Данный метод преобразует квестовый кортеж в квестовый словарь, он переопределяется от абстрактного метода в
        классе Quest
        @param is_tuple: кортеж со строками внутри
        @return: словарь
        """

        # ключи для словаря
        dict_keys = ('world_name', 'danger_name', 'class_name')
        quest_dict = dict(zip(dict_keys, is_tuple))  # связывание ключей и значений в кортеже

        assert len(quest_dict) == 3, 'ключ-значений должно быть 3'

        return quest_dict

    def load_artifact_to_log(self) -> None:
        """
        Данный метод является собственным методом данного класса и ответственен за запись в лог-файл полной строки
        квеста для того, чтобы ее можно было потом копировать оттуда и вставлять в игру
        @return: None
        """
        logger.info('[artifact_for_quest]' + self.quest_name + self.full_artifact_string)


class KillQuest(Quest, Reward):
    """
    Данный класс отвечает за формирование заказов на убийство и зачистку врагов, он наследует класс миксин Reward для
    определения стандартной награды за выполнение квеста
    """

    def __init__(self, quest_tuple: tuple):
        """
        @param quest_tuple: название мира, опасности мира, имперского класса и названия группы врагов (world_name,
        danger_name, class_name, group_name)
        """
        super().__init__(quest_tuple)
        self.quest_name = 'kill_quest'
        self.quest_dict = self.quest_tuple_to_dict(quest_tuple)

    def build_quest(self) -> None:
        """
        Основной метод строитель, поэтапно вызывает все нужные методы построения квеста
        @return: None
        """
        self.get_quest_pattern_from_db()
        self.form_quest_name()
        self.form_quest_string()
        self.load_quest_to_log()

    @staticmethod
    def quest_tuple_to_dict(is_tuple: tuple) -> dict:
        """
        Данный метод преобразует квестовый кортеж в квестовый словарь, он переопределяется от абстрактного метода в
        классе Quest
        @param is_tuple: кортеж со строками внутри
        @return: словарь
        """

        # ключи для словаря
        dict_keys = ('world_name', 'danger_name', 'class_name', 'enemy_name')
        quest_dict = dict(zip(dict_keys, is_tuple))  # связывание ключей и значений из кортежа

        assert len(quest_dict) == 4, 'ключ-значений должно быть 4'

        return quest_dict

    def get_quest_pattern_from_db(self) -> None:
        """
        Данный метод переопределяет наследован от абстрактного метода класса Quest. Он достает из БД нужный квест.
        В запросе таблица quest_patterns джойниться со всеми связанными таблицами, в т.ч. связью многие ко многим.
        Затем делается отбор на квесты, в которых есть соответствующий уровень опасности и связанные враги, а группа
        является убийственной. Все это сортируется рандомом и забирается одно значение лимитом 1
        @return: None
        """
        quest_query = f"""
        SELECT DISTINCT quest_patterns.quest_name, quest_patterns.quest_text
        FROM quest_patterns
        INNER JOIN quest_patterns_danger_zone_relations USING(quest_name)       
        INNER JOIN danger_zone USING(danger_name)    
        INNER JOIN quest_patterns_enemies_relations USING(quest_name)    
        INNER JOIN enemies USING(enemy_name)
        WHERE danger_zone.danger_name == '{self.quest_dict['danger_name']}'
        AND enemies.group_name == '{self.quest_dict['enemy_name']}'
        AND quest_patterns.group_name == 'kill_quest'
        ORDER BY RANDOM()
        LIMIT 1"""

        # Достается из БД кортеж, используя глобальную переменную курсора
        quest_tuple = tuple(global_bd_sqlite3_cursor.execute(quest_query))
        assert quest_tuple, 'база должна вернуть непустое значение'

        self.quest_subtype = quest_tuple[0][0]  # по факту это quest_patterns.quest_name
        self.quest_description = quest_tuple[0][1]  # по факту это quest_patterns.quest_text

    def form_quest_string(self):
        """
        Данный метод формирует итоговую строку квеста используя метод format. Самой строке шаблона квеста, хранимой в БД
        фрагменты вставки значений указаны как {} в нужных местах и количество, а также порядок данных вставок зависят
        от квестовой группы
        @return: None
        """

        quest_timer = random.randint(2, 5)  # срок выполнения квеста. В игре он представляет собой количество
        # полноценных сессий игры(4часа реального времени)

        quest_reward = self.count_reward(quest_timer)  # вычисление стандартной награды через класс миксин

        # При создании новых шаблонов квестов в базе данных нужно придерживаться следующей последовательности
        # вставок {} для формата: название мире -> название врагов -> объём награды -> срок выполнения квеста
        formatted_description = self.quest_description.format(self.quest_dict['world_name'],
                                                              self.quest_dict['enemy_name'],
                                                              quest_reward,
                                                              quest_timer)

        self.final_string = f"[КВЕСТ] {self.quest_name}{formatted_description}"


class DeliveryQuest(Quest):
    """
    Данный класс отвечает за формирование заказов на доставку торгового груза на определенный мир с повышенной
    стоимостью оплаты
    """

    def __init__(self, quest_tuple: tuple):
        """
        @param quest_tuple: название мира, опасности мира, имперского класса и названия импортируемого товара
        (world_name, danger_name, class_name, import_name)
        """
        super().__init__(quest_tuple)
        self.quest_name = 'delivery_quest'
        self.quest_dict = self.quest_tuple_to_dict(quest_tuple)

    def build_quest(self) -> None:
        """
        Основной метод строитель, поэтапно вызывает все нужные методы построения квеста
        @return: None
        """
        self.get_quest_pattern_from_db()
        self.form_quest_name()
        self.form_quest_string()
        self.load_quest_to_log()

    @staticmethod
    def quest_tuple_to_dict(is_tuple: tuple) -> dict:
        """
        Данный метод преобразует квестовый кортеж в квестовый словарь, он переопределяется от абстрактного метода в
        классе Quest
        @param is_tuple: кортеж со строками внутри
        @return: словарь
        """

        # Ключи для словаря
        dict_keys = ('world_name', 'danger_name', 'class_name', 'import_name')
        quest_dict = dict(zip(dict_keys, is_tuple))  # Связывание ключей и значений из кортежа

        assert len(quest_dict) == 4, 'ключ-значений должно быть 4'

        return quest_dict

    def get_quest_pattern_from_db(self) -> None:
        """
        Данный метод переопределяет наследованный от абстрактного метода класса Quest. Он достает из БД нужный квест.
        В запросе таблица quest_patterns ни с чем не джойнится, а просто отбираются квесты у которой группа
        соответствует квесту доставки. Все это сортируется рандомом и забирается одно значение лимитом 1
        @return: None
        """
        quest_query = f"""
        SELECT DISTINCT quest_patterns.quest_name, quest_patterns.quest_text
        FROM quest_patterns
        WHERE quest_patterns.group_name == 'delivery_quest'
        ORDER BY RANDOM()
        LIMIT 1"""

        # Достается из БД кортеж, используя глобальную переменную курсора
        quest_tuple = tuple(global_bd_sqlite3_cursor.execute(quest_query))
        assert quest_tuple, 'база должна вернуть непустое значение'

        self.quest_subtype = quest_tuple[0][0]  # по факту это quest_patterns.quest_name
        self.quest_description = quest_tuple[0][1]  # по факту это quest_patterns.quest_text

    def form_quest_string(self) -> None:
        """
        Данный метод формирует итоговую строку квеста используя метод format. Самой строке шаблона квеста, хранимой в БД
        фрагменты вставки значений указаны как {} в нужных местах и количество, а также порядок данных вставок зависят
        от квестовой группы
        @return: None
        """

        quest_timer = random.randint(2, 5)  # срок выполнения квеста. В игре он представляет собой количество
        # полноценных сессий игры(4часа реального времени)
        goods_amount = random.randint(2, 8)  # объем запрашиваемого товара

        # При создании новых шаблонов квестов в базе данных нужно придерживаться следующей последовательности
        # вставок {} для формата: название мире -> название необходимого товара -> количество контейнеров с товаром
        # -> срок выполнения квеста
        formatted_description = self.quest_description.format(self.quest_dict['world_name'],
                                                              self.quest_dict['import_name'],
                                                              goods_amount,
                                                              quest_timer)

        self.final_string = f"[КВЕСТ]{self.quest_name}{formatted_description}"


class EscortQuest(Quest, Reward):
    """
    Данный класс отвечает за формирование заказов на перевозку пассажира с одного мира на другой
    """

    def __init__(self, quest_tuple: tuple[tuple, tuple]):
        """
        @param quest_tuple: кортеж из кортежей (world_name, danger_name)(world_name, danger_name)
        """
        super().__init__(quest_tuple)
        self.quest_name = 'escort_quest'
        self.quest_dict, self.place_of_delivery_dict = self.quest_tuple_to_dict(quest_tuple)

    def build_quest(self) -> None:
        """
        Основной метод строитель, поэтапно вызывает все нужные методы построения квеста
        @return: None
        """
        self.get_quest_pattern_from_db()
        self.form_quest_name()
        self.form_quest_string()
        self.load_quest_to_log()

    @staticmethod
    def quest_tuple_to_dict(is_tuple: tuple) -> tuple[dict, dict]:
        """
        Данный метод преобразует квестовый кортеж из кортежей в 2 квестовый словаря,
        метод переопределяется от абстрактного метода в классе Quest
        @param is_tuple: кортеж со кортежами внутри(во внутренних кортежах строки)
        @return: 2 словаря
        """

        assert len(is_tuple) == 2, 'кортежей должно быть 2'

        # ключи для обоих словарей
        dict_keys = ('world_name', 'danger_name')

        quest_dict = dict(zip(dict_keys, is_tuple[0]))  # Словарь для пункта отправки
        place_of_delivery_dict = dict(zip(dict_keys, is_tuple[1]))  # Словарь для пункта прибытия

        assert len(quest_dict) == 2 and len(place_of_delivery_dict) == 2, 'ключ-значений должно быть 2'

        return quest_dict, place_of_delivery_dict

    def get_quest_pattern_from_db(self) -> None:
        """
        Данный метод переопределяет наследованный от абстрактного метода класса Quest. Он достает из БД нужный квест.
        В запросе таблица quest_patterns ни с чем не джойнится, а просто отбираются квесты у которой группа
        соответствует квесту доставки. Все это сортируется рандомом и забирается одно значение лимитом 1
        @return: None
        """
        quest_query = f"""
        SELECT DISTINCT quest_patterns.quest_name, quest_patterns.quest_text
        FROM quest_patterns
        WHERE quest_patterns.group_name == 'escort_quest'
        ORDER BY RANDOM()
        LIMIT 1"""

        # Достается из БД кортеж, используя глобальную переменную курсора
        quest_tuple = tuple(global_bd_sqlite3_cursor.execute(quest_query))
        assert quest_tuple, 'база должна вернуть непустое значение'

        self.quest_subtype = quest_tuple[0][0]  # по факту это quest_patterns.quest_name
        self.quest_description = quest_tuple[0][1]  # по факту это quest_patterns.quest_text

    def form_quest_name(self) -> None:
        """
        У данного класса переопределяется данный метод, а не используется наследованный от класса Quest т.к. в нем
        указывается и место отправки и пункт назначения. В отличие от остальных, в которых все происходит на 1 мире
        @return: None
        """
        current_date = date.today()  # Текущая дата реального времени
        self.quest_name = f"""[КВЕСТ] {self.quest_dict['world_name']} -> {self.place_of_delivery_dict['world_name']}
{self.quest_subtype.capitalize()}. Получение: {current_date} \r\r"""

    def form_quest_string(self) -> None:
        """
        Данный метод формирует итоговую строку квеста используя метод format. Самой строке шаблона квеста, хранимой в БД
        фрагменты вставки значений указаны как {} в нужных местах и количество, а также порядок данных вставок зависят
        от квестовой группы
        @return: None
        """
        quest_timer = random.randint(2, 5)  # срок выполнения квеста. В игре он представляет собой количество
        # полноценных сессий игры(4часа реального времени)
        quest_reward = self.count_reward(quest_timer)  # вычисление стандартной награды через класс миксин

        # При создании новых шаблонов квестов в базе данных нужно придерживаться следующей последовательности
        # вставок {} для формата: название мира отправки -> название мира пункта назначения
        # -> награда в кредитах -> срок выполнения квеста
        formatted_description = self.quest_description.format(self.quest_dict['world_name'],
                                                              self.place_of_delivery_dict['world_name'],
                                                              quest_reward,
                                                              quest_timer)

        self.final_string = f"{self.quest_name}{formatted_description}"

