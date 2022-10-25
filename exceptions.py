"""
Пользовательские исключения
"""


class NotCallableModuleException(Exception):
    """
    Исключение при вызове модулей которые не должны вызываться отдельно
    """
    def __str__(self):
        return 'Данный модуль не допускает отдельный вызов'


class NotImportedModuleException(Exception):
    """
    Исключение при вызове модулей которые не должны импортироваться
    """
    def __str__(self):
        return 'Данный модуль не допускает импорт'
