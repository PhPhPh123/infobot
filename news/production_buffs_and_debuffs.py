"""

"""

from settings_imports_globalVariables import *


def form_production_changes_news() -> str:
    """

    Объект курсора bd_sqlite3_cursor и объект коннекта bd_sqlite3_connect это МЕЖМОДУЛЬНЫЕ ГЛОБАЛЬНЫЕ переменные:
    :return: строка ответа ботом
    """
    # 1 этап
    all_worlds_with_production_level_tuple = form_tuple_from_db()

    # 2 этап
    list_with_worlds_whose_production_was_changed = change_prodiction(all_worlds_with_production_level_tuple)

    # 3 этап
    access_responce = form_string_answer(chosen_world)
    return access_responce


def form_tuple_from_db():
    select_string = """
SELECT worlds.world_name, export_overproduction.overproduction_level, import_needs.needs_level, danger_zone.danger_level
FROM worlds
INNER JOIN export_overproduction ON worlds.overproduction_name == export_overproduction.overproduction_name
INNER JOIN import_needs ON worlds.needs_name == import_needs.needs_name
INNER JOIN danger_zone ON worlds.danger_name = danger_zone.danger_name
WHERE export_overproduction.overproduction_level NOT NULL AND import_needs.needs_level NOT NULL"""

    tuple_from_db = tuple(bd_sqlite3_cursor.execute(select_string))

    return tuple_from_db


def change_prodiction(worlds_tuple: tuple) -> list:
    list_with_worlds_object = []

    for world in worlds_tuple:
        list_with_worlds_object.append(WorldClass(*world))


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

        if (roll + danger_negative_modifier) / 2 <= self.chance_export:
            return self.world_name, strong_up
        elif roll + danger_negative_modifier <= self.chance_export:
            return self.world_name, weak_up
        elif roll >= 100.0 - self.chance_export + danger_negative_modifier:
            return self.world_name, weak_fall
        elif roll >= 100 - (self.chance_export + danger_negative_modifier / 2):
            return self.world_name, strong_fall
        else:
            pass

    def import_needs_change_check(self):
        danger_negative_modifier = self.danger_level * 0.1
        strong_up = 2
        weak_up = 1
        weak_fall = -1
        strong_fall = -2

        roll = random.uniform(0.0, 100.0)

        if (roll + danger_negative_modifier) / 2 <= self.chance_export:
            return self.world_name, strong_up
        elif roll + danger_negative_modifier <= self.chance_export:
            return self.world_name, weak_up
        elif roll >= 100.0 - self.chance_export + danger_negative_modifier:
            return self.world_name, weak_fall
        elif roll >= 100 - (self.chance_export + danger_negative_modifier / 2):
            return self.world_name, strong_fall
        else:
            pass
