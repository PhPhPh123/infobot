"""
    Данный пакет занимается формированием артефактов и подготовкой строковой информации для вывода ботов в чат.
    За вывод отвечает команда !arfifact. Команда требует как минимум указания грейда артефакта(цвета), а остальные
    две характеристики(группа артефакта, тип артефакта) по умолчанию выбираются случайно или указывается через пробел
    в строке команды. Работа пакета основана на создание объекта одного из 4х классов(броня, оружие-бб, оружие-дб
    бижутерия) которые наследуются от базового класса artifact, в модуле base_artifact, а классы оружия еще и от
    промежуточного базового класса оружие. Данные об артефактах, их параметры и все остальное хранится в БД и
    запрашивается оттуда соответствующими методами классов

----------------------------------------------------------------------------------------------------------------------
    Глоссарий специфический названий и обозначений использующихся в группе модулей:

    Артефакт: уникальный, процедурно генерируемый предмет высокой редкости с уникальными особенностями

    Грейд/grade: качество артефакта выращающееся в его цвете(синий, зеленый, фиолетовый, красный)

    Группа артефактов/group_name: 4 основных группы, на которые делятся артефакты, броня, бижутерия, оружие-бб(оружие ближнего боя)
    , оружие-дб(оружие дальнего боя)

    Тип артефакта/ art_type: конкретный вид артефакта внутри группы, например внутри оружия-бб могут быть одноручные пиломечи,
    силовые мечи, обычные клинки, пилотопоры, а в бижутерии серьги, амулеты, кольца итд

    Модификатор грейда/grade_modifier: множитель, на который умножаются некоторые численные характеристики артефакта

    Имя артефакта/name: процедурно сгенерированное имя на основе префикса, типа артефакта и суффикса, например
    Разведовательный лазган добивания

    Префикс/unique_prefix: первая уникальная особенность артефакта, выраженная в бонусе Удачи(возможности дважды бросик кубик навыка)
     к одной из характеристик согласно системе GURPS

    Суффикс/unique_suffix: вторая уникальная особенность артефакта, выраженное в уникальном боевом эффекте список которых разный
    для разных типов артефактов

    Требования/Требования силы/str_requeriments: необходимое количество силы, нужное для использования
    артефакта без штрафов

    Вес/ weight: масса артефакта

    Бонус бижутерии/jewelry_bonus: уникальный эффект, свойственный исключительно для бижутерии

    Броня, ВУ, Вычет урона, armor: модификатор брони, на который уменьшается весь входящий урон по игрокам/мобам

    Модификатор скорости/speed_modifier: модификатор бонуса/штрафа к передвижению для брони

    Модификатор уклонения/evasion_modifier модификатор бонуса/штрафа к уклонению для брони

    Урон/damage: повреждения оружия выращающиеся либо в int значении либо в преобразованном для ролки значении типа 10d6

    Пробитие/Игнор ВУ/penetration: модификатор полностью либо в 50% игнорирующий параметр брони

    Точность/prescision_modifier: модификатор добавляющий или снижающий точность в игре

    Скорость атаки/attack_speed: скорость стрельбы оружия дальнего боя

    Дальность/range: дальность стрельбы оружия дальнего боя

    Модификатор парирования/ parry_modifier: модификатор дающий бонус/штраф для парирования в игре в ближнем бою
-----------------------------------------------------------------------------------------------------------------------
    Структура отвечающей за формирование артефактов таблиц в базе данных:

    Таблицы базовой информации о группах артефактов и их основных характеристиках:

    ###artifact_armor### --- Броня
    Содержит столбцы с:
    названием типа брони, названием группы, базовой броней(ВУ),
    базовым весом, базовым требованием силы, базовой скоростью, базовым уклонением

    ###artifact_close_combat### --- Оружие ближнего боя
    Содержит столбцы с:
    названием типа оружия, названием группы, базовым уроном,
    базовой точностью, базовым бонусом к парированию, базовым весом, базовым требованием силы

    ###artifact_range_weapon### --- Оружие дальнего боя
    Содержит столбцы с:
    названием типа оружия, названием группы, базовым уроном,
    базовой точностью, базовой дальностью, базовой скоростью атаки, базовым весом, базовым требованием силы

    ###artifact_jewelry### --- Бижутерия
    Содержит столбцы с:
    названием типа бижутерии, названием группы, базовым весом, базовым требованием силы

    ###unique_suffix### - Суффиксы артефактов
    Содержит столбцы с:
    названием эффекта, текстовым описанием эффекта

    ###unique_prefix### - Префиксы артефактов
    Содержит столбцы с:
    названием эффекта, скиллом, на который он влияет

    Группа таблиц ###unique_suffix_*название группы артефактов*_relations
    Связующие таблицы многие ко многим связывающие типа артефактов с названиями суффиксов, которые могут быть
    выданы для нужного типа артефакта

    ###unique_jewelry_bonuses### - собственные бонусы бижутерии
    Содержит столбцы с:
    названием бонуса, текстовым описанием бонуса

    ###artifact_jewelry_unique_jewelry_bonuses_relations###
    Таблица со связью многие ко многим, обеспечивающая связь между названием типа бижутерии из таблицы artifact_jewelry
    и названием доступного ей бонуса из таблицы unique_jewelry_bonuses
-----------------------------------------------------------------------------------------------------------------------
"""