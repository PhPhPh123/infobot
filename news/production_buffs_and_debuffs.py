"""
    Данный модуль отвечает за создание новостей об изменениях в производстве внутри субсектора, а именно влияние
    на параметры import_needs и export_overprodiction. В нем есть центральная управляющая функция
    form_production_changes_news которая делегирует выполнение на другие функции и класс, которые готовят строковый
    ответ и заливают изменения в базу данных
"""

from settings_imports_globalVariables import *


def form_production_changes_news() -> str:
    """
    Данная функция управляет остальными и возвращает результат в 5 этапов
    Объект курсора bd_sqlite3_cursor и объект коннекта bd_sqlite3_connect это МЕЖМОДУЛЬНЫЕ ГЛОБАЛЬНЫЕ переменные:
    :return: строка ответа ботом
    """
    # 1 этап. Получение кортежа с кортежами с данными из БД
    all_worlds_with_production_level_tuple = form_tuple_from_db()

    # 2 этап. Создание списка с экземплярами класса WorldClass
    all_worlds_objects_list = form_world_object_list(all_worlds_with_production_level_tuple)

    # 3 этап. Создание списков с кортежами в котором будет название мира, значение изменения его уровня производства или
    # дефицита и текущий уровень ровня производства или дефицита
    world_list_with_export_overproduction_changes, world_list_with_import_needs_changes = check_production_changes(
        all_worlds_objects_list)

    # 4 этап. Аптейд в базу данных на основе сформированных кортежей
    update_db_with_production_changes(world_list_with_export_overproduction_changes, 'export_overproduction',
                                      'overproduction_name')
    update_db_with_production_changes(world_list_with_import_needs_changes, 'import_needs', 'needs_name')

    # 5 этап. Формирование строки для ответа ботом об изменениях производства в системах
    bot_answer = form_string_answer(world_list_with_export_overproduction_changes, world_list_with_import_needs_changes)

    return bot_answer


def form_tuple_from_db() -> tuple:
    """
    Данный метод делает запрос в БД для получения кортежа с кортежами
    :return: int число с количеством брони(ВУ)
    """

    # В данном селекте мне нужны кортежи из названия мира, уровня перепроизводства, уровня дефицита и уровня опасности,
    # где уровень перепроизводства и дефицита не равны нулю(а равны они на мирах, которые ничего не производят
    # и не покупают
    select_string = """
SELECT worlds.world_name, export_overproduction.value_level, import_needs.value_level, danger_zone.danger_level
FROM worlds
INNER JOIN export_overproduction ON worlds.overproduction_name == export_overproduction.overproduction_name
INNER JOIN import_needs ON worlds.needs_name == import_needs.needs_name
INNER JOIN danger_zone ON worlds.danger_name = danger_zone.danger_name
WHERE export_overproduction.value_level NOT NULL AND import_needs.value_level NOT NULL"""

    tuple_from_db = tuple(global_bd_sqlite3_cursor.execute(select_string))

    return tuple_from_db


def form_world_object_list(worlds_tuple: tuple) -> list:
    """
    Данный метод формирует параметр урона оружия
    :param worlds_tuple: кортеж с кортежами в которых 4 значения:
     название мира, уровень перепроизводства, уровень дефицита и уровень опасности
    :return: список с объектами класса WorldClass
    """

    list_with_worlds_object = []  # Инициализация списка

    for world in worlds_tuple:
        # В список добавляются все значения внутреннего кортежа(через *) которые будут инициализироваться в экземпляре
        list_with_worlds_object.append(WorldClass(*world))

    return list_with_worlds_object


def check_production_changes(all_worlds: list) -> tuple:
    """
    Данный функция работает с экземплярами класса WorldClass, вызывая их методы подтверждающие изменения и их обьём
    Функция содержит внутреннюю вспомогательную функцию check_extreme_values, проверяющую на экстремальные
    значения и корректирующую их
    :param all_worlds: список с экземплярами класса WorldClass
    :return: список с объектами класса WorldClass
    """

    # инициализация списков, куда будут включены списки из 3 значений: название мира, параметр изменения значения
    # производства или дефицита и текущий уровень дефицита или производства
    world_objects_with_export_overproduction_changes = []
    world_objects_with_import_needs_changes = []

    # Прохожу по списку всех миров и вызываю методы проверки для обоих списков, если проверка не прошла то идет pass
    # и внутренний список(из 3х значений) не добавляется в общий список
    for world in all_worlds:
        world_objects_with_export_overproduction_changes.append(world.export_overproduction_change_check())
        world_objects_with_import_needs_changes.append(world.import_needs_change_check())

    # Данные костыли фильтруют пустые внутренние списки, возникающие когда append сталкивается pass
    export_filtered_list = list(filter(lambda x: x if not None else False, world_objects_with_export_overproduction_changes))
    import_filtered_list = list(filter(lambda x: x if not None else False, world_objects_with_import_needs_changes))

    def check_extreme_values(list_for_check: list) -> list:
        """
    Данный внутренняя функция корректирует экстримальные значения, выходящие за пределы допустимых
    :param list_for_check: список со списками значения которых нужно подкорректировать
    :return: откорректированных список со списками
        """

        for world_elem in list_for_check:
            # Если текущее значение + значение изменения (отрицательные)
            if int(world_elem[1]) + int(world_elem[2]) < -2:
                # то модификатор изменения устанавливается как он сам минус текущее значение, например
                # -2 мод. изменения, а -2 текущее, соответственно изменения будет равно 0 чтобы не вышло за пределы
                # а если -2 изменение, а -1 текущее, то изменения устанавливается как -1 чтобы не привысить
                # разрешенный минимум равный -2
                world_elem[1] = world_elem[1] - world_elem[2]

            # тоже самое только для разрешенного максимума
            if int(world_elem[1]) + int(world_elem[2]) > 2:
                world_elem[1] = world_elem[1] - world_elem[2]

        return list_for_check

    # данный костыль фильтрует значения, внутреннего списка с параметром изменения, если путем прохода через функцию
    # check_extreme_values у него оказалось значение 0 из фактического изменения не произошло
    export_list_with_fixed_extreme_values = list(
        filter(lambda x: x if x[1] != 0 else False, check_extreme_values(export_filtered_list)))
    import_list_with_fixed_extreme_values = list(
        filter(lambda x: x if x[1] != 0 else False, check_extreme_values(import_filtered_list)))

    return export_list_with_fixed_extreme_values, import_list_with_fixed_extreme_values


def update_db_with_production_changes(world_list: list, table_name: str, column_name: str) -> None:
    for world in world_list:
        query_string = f"""
        UPDATE worlds
        SET {column_name} == 
        (SELECT {column_name} FROM {table_name} WHERE value_level == {world[1] + world[2]})
        WHERE world_name == '{world[0]}'
        """

        global_bd_sqlite3_cursor.execute(query_string)
        global_bd_sqlite3_connect.commit()


def form_string_answer(export_list: list, import_list: list) -> str:
    def convert_int_to_string(world_elem) -> str:
        changes_string = ''
        if world_elem[1] == 2:
            changes_string = 'сильное повышение'
        elif world_elem[1] == 1:
            changes_string = 'повышение'
        elif world_elem[1] == -1:
            changes_string = 'понижение'
        elif world_elem[1] == -2:
            changes_string = 'сильное понижение'
        return changes_string

    main_export = Template("""
[ИЗМЕНЕНИЕ ПРОИЗВОДСТВА] Торговый терминал сообщает об изменениях в экономической ситуации в субсекторе:

Изменения собственного производства на мирах:
{% if export_list %}
    {% for world in export_list %}
        {{ 'На мире {} {} уровня производства'.format(world[0], convert_func(world)) }}
    {% endfor %}
{% else %}
    {{ 'Изменения отсутствуют' }}
{% endif %}
Изменения дефицита товаров на мирах:
{% if import_list %}
    {% for world in import_list %}
        {{ 'На мире {} {} уровня дефицита'.format(world[0], convert_func(world)) }}
    {% endfor %}
{% else %}
    {{ 'Изменения отсутствуют' }}
{% endif %}""")

    main_export_render = main_export.render(export_list=export_list,
                                            import_list=import_list,
                                            convert_func=convert_int_to_string)

    return main_export_render


class WorldClass:
    base_chance = 1.5
    production_stabilizing_modifier = 0.2
    danger_stabilizing_modifier = 0.1

    def __init__(self, world_name, export_overproduction, import_needs, danger_level):
        self.world_name = world_name
        self.export_overproduction = export_overproduction
        self.import_needs = import_needs
        self.danger_level = danger_level
        self.chance_export, self.chance_import = self.count_chance()

    def count_chance(self):
        final_chance_export = self.base_chance + \
                              (abs(self.export_overproduction) * self.production_stabilizing_modifier) + \
                              (self.danger_level * self.danger_stabilizing_modifier)

        final_chance_import = self.base_chance + \
                              (abs(self.import_needs) * self.production_stabilizing_modifier) + \
                              (self.danger_level * self.danger_stabilizing_modifier)

        return final_chance_export, final_chance_import

    def export_overproduction_change_check(self):
        danger_negative_modifier = self.danger_level * 0.1
        strong_up = 2
        weak_up = 1
        weak_fall = -1
        strong_fall = -2

        roll = random.uniform(0.0, 100.0)

        if (roll + danger_negative_modifier) * 2 <= self.chance_export:
            return [self.world_name, strong_up, self.export_overproduction]
        elif roll + danger_negative_modifier <= self.chance_export:
            return [self.world_name, weak_up, self.export_overproduction]
        elif roll >= 100.0 - self.chance_export + danger_negative_modifier:
            return [self.world_name, weak_fall, self.export_overproduction]
        elif roll >= 100 - ((self.chance_export + danger_negative_modifier) / 2):
            return [self.world_name, strong_fall, self.export_overproduction]
        else:
            pass

    def import_needs_change_check(self):
        danger_negative_modifier = self.danger_level * 0.1
        strong_up = 2
        weak_up = 1
        weak_fall = -1
        strong_fall = -2

        roll = random.uniform(0.0, 100.0)

        if (roll + danger_negative_modifier) * 2 <= self.chance_export:
            return [self.world_name, strong_up, self.import_needs]
        elif roll + danger_negative_modifier <= self.chance_export:
            return [self.world_name, weak_up, self.import_needs]
        elif roll >= 100.0 - self.chance_export + danger_negative_modifier:
            return [self.world_name, weak_fall, self.import_needs]
        elif roll >= 100 - ((self.chance_export + danger_negative_modifier) / 2):
            return [self.world_name, strong_fall, self.import_needs]
        else:
            return None
