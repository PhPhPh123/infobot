"""
    Данный модуль отвечает за рандомизацию и выдачу в чат небольших случайных квестов
"""

from settings_imports_globalVariables import *
import craft.main_artifact_builder


def control_quests():
    """
    Данная функция является базовой точкой входа и управляющей элементом модуля
    """
    logger.info('[print]')

    chones_quest = choise_quest()

    quest_former = QuestFormer(chones_quest)
    quest_string = quest_former.start_form()

    return quest_string


def choise_quest():
    """
    Данная функция выбирает случайный тип квеста, на данный момент это один из списка из 4х:
    artifact_quest, kill_quest, delivery_quest, escort_quest
    """
    quests = tuple(bd_sqlite3_cursor.execute("SELECT group_name FROM quest_group"))[0]
    chones_quest = random.choice(quests)

    return chones_quest


class QuestFormer:
    """
    Данная класс выбирает один из методов, отвечающий за доступ в базу данных, достает оттуда значение и формирует
    на его основе экземпляр целевого финального квестового класса
    """

    def __init__(self, quest_name: str):
        self.quest_name = quest_name
        # Вызываю соответствующий статичный метод на основе принятого имя квеста(имя квеста и имя метода совпадают)
        self.quest_tuple = self.__getattribute__(quest_name)()

    def start_form(self):
        """
        Данная функция создает экземпляры класса на их основе и вызывает метод формирования итоговой строки квеста
        """
        quest = None

        if self.quest_name == 'artifact_quest':
            quest = ArtifactQuest(self.quest_tuple)
        elif self.quest_name == 'kill_quest':
            quest = KillQuest(self.quest_tuple)
        elif self.quest_name == 'delivery_quest':
            quest = DeliveryQuest(self.quest_tuple)
        elif self.quest_name == 'escort_quest':
            quest = EscortQuest(self.quest_tuple)

        quest_string = quest.form_quest()
        return quest_string

    @staticmethod
    def artifact_quest():
        artifact_quest_query = '''
        SELECT worlds.world_name, worlds.danger_name, worlds.class_name
        FROM worlds
        ORDER BY RANDOM()
        LIMIT 1'''
        artifact_quest_tuple = tuple(bd_sqlite3_cursor.execute(artifact_quest_query))[0]
        return artifact_quest_tuple

    @staticmethod
    def kill_quest():
        kill_quest_query = '''
        SELECT worlds.world_name, worlds.danger_name, worlds.class_name, enemies.group_name
        FROM worlds
        INNER JOIN worlds_enemies_relations ON worlds.world_name == worlds_enemies_relations.world_name
        INNER JOIN enemies ON worlds_enemies_relations.enemy_name == enemies.enemy_name
        WHERE worlds.danger_name != 'Нулевая угроза'
        AND enemies.group_name NOT NULL
        AND enemies.enemy_name NOT LIKE 'Кароч%'
        ORDER BY RANDOM()
        LIMIT 1'''
        kill_quest_tuple = tuple(bd_sqlite3_cursor.execute(kill_quest_query))
        return kill_quest_tuple

    @staticmethod
    def delivery_quest():
        delivery_quest_query = f'''
        SELECT worlds.world_name, worlds.danger_name, worlds.class_name, trade_import.import_name
        FROM worlds
        INNER JOIN worlds_trade_import_relations ON worlds.world_name == worlds_trade_import_relations.world_name
        INNER JOIN trade_import ON worlds_trade_import_relations.import_name == trade_import.import_name
        WHERE trade_import.import_name != 'Импорт-отсутствует'
        ORDER BY RANDOM()
        LIMIT 1'''

        delivery_quest_tuple = tuple(bd_sqlite3_cursor.execute(delivery_quest_query))

        return delivery_quest_tuple

    @staticmethod
    def escort_quest():
        escort_quest_query = f'''
        SELECT  world_name, danger_name, class_name, world_population
        FROM worlds
        WHERE world_population > 10000
        ORDER BY RANDOM()
        LIMIT 2'''

        delivery_escort_tuple = tuple(bd_sqlite3_cursor.execute(escort_quest_query))

        return delivery_escort_tuple


class Quest:
    """
    Данный класс является базовым и содержит в себе аттрибуты и методы, характерные для всех квестов
    """
    def __init__(self, quest_tuple):
        self.quest_tuple = quest_tuple
        self.quest_name = None
        self.quest_dict = None
        self.final_string = None

    def load_quest_to_file(self):
        """
        Данный метод будет записывать в файл текст квеста
        """

    @staticmethod
    def quest_tuple_to_dict(is_tuple: tuple):
        raise NotImplementedError

    def form_quest(self):
        raise NotImplementedError

    def get_quest_pattern_from_db(self):
        raise NotImplementedError

    def form_quest_string(self):
        raise NotImplementedError


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
        self.quest_description = None
        self.quest_subtype = None

    def form_artifact(self):
        grade_name = None
        if self.quest_dict['danger_name'] in ('Зеленая угроза', 'Нулевая угроза'):
            grade_name = 'зеленый'
        elif self.quest_dict['danger_name'] == 'Синяя угроза':
            grade_name = 'синий'
        elif self.quest_dict['danger_name'] == 'Фиолетовая угроза':
            grade_name = 'фиолетовый'
        elif self.quest_dict['danger_name'] == 'Красная угроза':
            grade_name = 'красный'

        request_dict = {'грейд': grade_name,
                        'группа': 'random',
                        'тип': 'random',
                        'особенность': 'random'}

        self.full_artifact_string = craft.main_artifact_builder.choise_class_objects(request_dict)

    def form_quest(self):
        """
        Данный метод будет формировать строку с квестом
        """
        self.form_artifact()
        self.get_quest_pattern_from_db()
        self.form_quest_string()

        return self.final_string

    def get_quest_pattern_from_db(self):
        quest_query = f"""
        SELECT quest_patterns.quest_name, quest_patterns.quest_text
        FROM quest_patterns
        INNER JOIN quest_patterns_danger_zone_relations ON quest_patterns.quest_name == quest_patterns_danger_zone_relations.quest_name
        INNER JOIN danger_zone ON quest_patterns_danger_zone_relations.danger_name == danger_zone.danger_name
        INNER JOIN quest_patterns_imperial_class_relations ON quest_patterns.quest_name == quest_patterns_imperial_class_relations.quest_name
        INNER JOIN imperial_class ON quest_patterns_imperial_class_relations.class_name == imperial_class.class_name
        WHERE imperial_class.class_name == '{self.quest_dict['class_name']}' 
          AND danger_zone.danger_name == '{self.quest_dict['danger_name']}'"""

        quest_tuple = tuple(bd_sqlite3_cursor.execute(quest_query))
        print(quest_tuple)
        self.quest_subtype = quest_tuple[0][0]
        self.quest_description = quest_tuple[0][1]

    def form_quest_string(self):
        quest_timer = random.randint(2, 5)

        formatted_description = self.quest_description.format(self.quest_dict['world_name'],
                                                              self.full_artifact_string.split("\n")[0],
                                                              quest_timer)

        self.final_string = formatted_description

    @staticmethod
    def quest_tuple_to_dict(is_tuple: tuple):
        dict_keys = ('world_name', 'danger_name', 'class_name')
        quest_dict = dict(zip(dict_keys, is_tuple))

        return quest_dict




class KillQuest(Quest):
    """
    Данный класс отвечает за формирование заказов на убийство и зачистку врагов
    """

    def __init__(self, quest_tuple):
        super().__init__(quest_tuple)
        self.quest_name = 'kill_quest'
        self.quest_dict = self.quest_tuple_to_dict(quest_tuple)

    def form_quest(self):
        """
        Данный метод будет формировать строку с квестом
        """
        pass

    @staticmethod
    def quest_tuple_to_dict(is_tuple: tuple):
        dict_keys = ('world_name', 'danger_name', 'class_name', 'enemy_name')
        quest_dict = dict(zip(dict_keys, is_tuple))

        return quest_dict


class DeliveryQuest(Quest):
    """
    Данный класс отвечает за формирование заказов на доставку торгового груза на определенный мир с повышенной
    стоимостью оплаты
    """

    def __init__(self, quest_tuple):
        super().__init__(quest_tuple)
        self.quest_name = 'delivery_quest'
        self.quest_dict = self.quest_tuple_to_dict(quest_tuple)

    def form_quest(self):
        """
        Данный метод будет формировать строку с квестом
        """
        pass

    @staticmethod
    def quest_tuple_to_dict(is_tuple: tuple):
        dict_keys = ('world_name', 'danger_name', 'class_name', 'import_name')
        quest_dict = dict(zip(dict_keys, is_tuple))

        return quest_dict


class EscortQuest(Quest):
    """
    Данный класс отвечает за формирование заказов на перевозку пассажира с одного мира на другой
    """

    def __init__(self, quest_tuple):
        super().__init__(quest_tuple)
        self.quest_name = 'escort_quest'
        self.quest_dict = self.quest_tuple_to_dict(quest_tuple)

    def form_quest(self):
        """
        Данный метод будет формировать строку с квестом
        """
        pass

    @staticmethod
    def quest_tuple_to_dict(is_tuple: tuple):
        dict_keys = ('world_name', 'danger_name', 'class_name', 'world_population')
        quest_dict = dict(zip(dict_keys, is_tuple))

        return quest_dict
