"""

"""

from settings_imports_globalVariables import *


def form_production_changes_news() -> str:
    """

    Объект курсора bd_sqlite3_cursor и объект коннекта bd_sqlite3_connect это МЕЖМОДУЛЬНЫЕ ГЛОБАЛЬНЫЕ переменные:
    :return: строка ответа ботом
    """
    print('ПРИНТ')
    # 1 этап. Получение кортежа с кортежами с данными из БД
    all_worlds_with_production_level_tuple = form_tuple_from_db()

    # 2 этап. Создание списка с экземплярами класса WorldClass
    all_worlds_objects_list = form_world_object_list(all_worlds_with_production_level_tuple)

    # 3 этап. Создание списков с кортежами в котором будет название мира, значение изменения его уровня производства или
    # дефицита и текущий уровень ровня производства или дефицита
    world_list_with_export_overproduction_changes, world_list_with_import_needs_changes = check_production_changes(all_worlds_objects_list)

    # 4 этап. Аптейд в базу данных на основе сформированных кортежей
    update_db_with_production_changes(world_list_with_export_overproduction_changes, 'export_overproduction', 'overproduction_name')
    update_db_with_production_changes(world_list_with_import_needs_changes, 'import_needs', 'needs_name')

    return 'Готово!'


def form_tuple_from_db() -> tuple:
    select_string = """
SELECT worlds.world_name, export_overproduction.value_level, import_needs.value_level, danger_zone.danger_level
FROM worlds
INNER JOIN export_overproduction ON worlds.overproduction_name == export_overproduction.overproduction_name
INNER JOIN import_needs ON worlds.needs_name == import_needs.needs_name
INNER JOIN danger_zone ON worlds.danger_name = danger_zone.danger_name
WHERE export_overproduction.value_level NOT NULL AND import_needs.value_level NOT NULL"""

    tuple_from_db = tuple(bd_sqlite3_cursor.execute(select_string))

    return tuple_from_db


def form_world_object_list(worlds_tuple: tuple) -> list:
    list_with_worlds_object = []

    for world in worlds_tuple:
        list_with_worlds_object.append(WorldClass(*world))

    return list_with_worlds_object


def check_production_changes(all_worlds: list):
    world_objects_with_export_overproduction_changes = []
    world_objects_with_import_needs_changes = []

    for world in all_worlds:
        world_objects_with_export_overproduction_changes.append(world.export_overproduction_change_check())
        world_objects_with_import_needs_changes.append(world.import_needs_change_check())

    export_filtered_list = list(filter(lambda x: x if not None else False, world_objects_with_export_overproduction_changes))
    import_filtered_list = list(filter(lambda x: x if not None else False, world_objects_with_import_needs_changes))

    export_list_with_fixed_extreme_values = check_extreme_values(export_filtered_list)
    import_list_with_fixed_extreme_values = check_extreme_values(import_filtered_list)

    return export_list_with_fixed_extreme_values, import_list_with_fixed_extreme_values


def check_extreme_values(list_for_check):
    print(list_for_check)
    for world in list_for_check:
        if int(world[1]) + int(world[2]) < -2:
            world[1] = world[1] - world[2]

        if int(world[1]) + int(world[2]) > 2:
            world[1] = world[1] - world[2]

    return list_for_check


def update_db_with_production_changes(world_list, table_name, column_name):
    for world in world_list:

        query_string = f"""
        UPDATE worlds
        SET {column_name} == 
        (SELECT {column_name} FROM {table_name} WHERE value_level == {world[1] + world[2]})
        WHERE world_name == '{world[0]}'
        """

        bd_sqlite3_cursor.execute(query_string)
        bd_sqlite3_connect.commit()


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
            return self.world_name, strong_up, self.export_overproduction
        elif roll + danger_negative_modifier <= self.chance_export:
            return self.world_name, weak_up, self.export_overproduction
        elif roll >= 100.0 - self.chance_export + danger_negative_modifier:
            return self.world_name, weak_fall, self.export_overproduction
        elif roll >= 100 - ((self.chance_export + danger_negative_modifier) / 2):
            return self.world_name, strong_fall, self.export_overproduction
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
            return self.world_name, strong_up, self.import_needs
        elif roll + danger_negative_modifier <= self.chance_export:
            return self.world_name, weak_up, self.import_needs
        elif roll >= 100.0 - self.chance_export + danger_negative_modifier:
            return self.world_name, weak_fall, self.import_needs
        elif roll >= 100 - ((self.chance_export + danger_negative_modifier) / 2):
            return self.world_name, strong_fall, self.import_needs
        else:
            return None

