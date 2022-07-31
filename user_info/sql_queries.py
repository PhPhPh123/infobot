"""
Этом модуле хранятся в виде словаря основные тела sql-запросов для БД которыми пользуются разные модули. На каждый
модуль свой словарь, ключи словаря совпадают с названиями таблиц, для которых создан запрос
"""

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

