"""
Данный модуль стартует основной асинхронный цикл бота
За исключением модулей в каталоге separatly_started_modules, является единственным запускаемым
напрямую. Все остальные импортируются и отдельного вызова не допускают. Все команды и циклы для бота находятся в
соответствующем пакете commands
"""

import exceptions
if __name__ == '__main__':
    # импортируются настройки бота
    from bot_settings import *

    # импортируются модули с командами для бота
    from commands.artifact_commands import *
    from commands.economic_commands import *
    from commands.other_commands import *
    from commands.special_loot_commands import *
    from commands.roll_commands import *

    infobot.run(settings['token'])  # запуск основного асинхронного цикла бота
else:
    raise exceptions.NotImportedModuleException  # модуль не подразумевает импорт, он вызывается только непосредственно
