"""
Этом модуле хранятся в виде словаря основные тела sql-запросов для БД которыми пользуются разные модули. На каждый
модуль свой словарь, ключи словаря совпадают с названиями таблиц, для которых создан запрос
"""

import exceptions
if __name__ == '__main__':
    raise exceptions.NotCallableModuleException

info_main_query_dict = {'worlds': """
    SELECT * FROM worlds WHERE worlds.world_name == '{}'""",

                        'terrains': """
    SELECT terrains.terrain_name FROM worlds
    INNER JOIN worlds_terrains_relations ON worlds.world_name==worlds_terrains_relations.world_name
    INNER JOIN terrains ON worlds_terrains_relations.terrain_name==terrains.terrain_name
    WHERE worlds.world_name =='{}'""",

                        'enemies': """
    SELECT enemies.enemy_name FROM worlds
    INNER JOIN worlds_enemies_relations ON worlds.world_name==worlds_enemies_relations.world_name
    INNER JOIN enemies ON worlds_enemies_relations.enemy_name==enemies.enemy_name
    WHERE worlds.world_name =='{}'""",

                        'export': """
    SELECT trade_export.export_name FROM worlds
    INNER JOIN worlds_trade_export_relations ON worlds.world_name==worlds_trade_export_relations.world_name
    INNER JOIN trade_export ON worlds_trade_export_relations.export_name==trade_export.export_name
    WHERE worlds.world_name =='{}'""",

                        'import': """
    SELECT trade_import.import_name FROM worlds
    INNER JOIN worlds_trade_import_relations ON worlds.world_name==worlds_trade_import_relations.world_name
    INNER JOIN trade_import ON worlds_trade_import_relations.import_name==trade_import.import_name
    WHERE worlds.world_name =='{}'""",
                        }

import_and_export_query_dict = {
                        'export': """
    SELECT trade_export.export_name, (base_price * overproduction_multiplier * danger_multiplier_export)
    worlds.access_level
    FROM worlds
    INNER JOIN worlds_trade_export_relations ON worlds.world_name == worlds_trade_export_relations.world_name
    INNER JOIN trade_export ON worlds_trade_export_relations.export_name == trade_export.export_name
    INNER JOIN export_overproduction ON worlds.overproduction_name == export_overproduction. overproduction_name
    INNER JOIN danger_zone ON worlds.danger_name == danger_zone.danger_name
    WHERE worlds.world_name =='{}'""",

                        'import': """
    SELECT trade_import.import_name, (base_price * need_multiplier * danger_multiplier_import),
    worlds.access_level
    FROM worlds
    INNER JOIN worlds_trade_import_relations ON worlds.world_name == worlds_trade_import_relations.world_name
    INNER JOIN trade_import ON worlds_trade_import_relations.import_name == trade_import.import_name
    INNER JOIN import_needs ON worlds.needs_name == import_needs.needs_name
    INNER JOIN danger_zone ON worlds.danger_name == danger_zone.danger_name
    WHERE worlds.world_name =='{}'"""

}

info_goods_query_dict = {
                        'export': """
    SELECT worlds.world_name, (trade_export.base_price * export_overproduction.overproduction_multiplier * danger_zone.danger_multiplier_export) AS price
    FROM worlds
    INNER JOIN worlds_trade_export_relations ON worlds.world_name == worlds_trade_export_relations.world_name
    INNER JOIN trade_export ON worlds_trade_export_relations.export_name == trade_export.export_name
    INNER JOIN export_overproduction ON worlds.overproduction_name == export_overproduction.overproduction_name
    INNER JOIN danger_zone ON worlds.danger_name == danger_zone.danger_name
    WHERE trade_export.export_name == '{{ goods_name }}' AND worlds.access_level == 3
    ORDER BY price DESC""",

                        'import': """
    SELECT worlds.world_name, (base_price * need_multiplier * danger_multiplier_import) AS price
    FROM worlds
    INNER JOIN worlds_trade_import_relations ON worlds.world_name == worlds_trade_import_relations.world_name
    INNER JOIN trade_import ON worlds_trade_import_relations.import_name == trade_import.import_name
    INNER JOIN import_needs ON worlds.needs_name == import_needs.needs_name
    INNER JOIN danger_zone ON worlds.danger_name == danger_zone.danger_name
    WHERE trade_import.import_name == '{{ goods_name }}' AND worlds.access_level == 3
    ORDER BY price"""
}
