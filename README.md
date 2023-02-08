# infobot
_____
![alt None](/static/image/README_main_image.png)
------
Данный проект является скриптовым дополнением для настольной ролевой игры
по мотивам вселенной Warhammer40000 в виде текстового бота для месседжера
discord и набором управляющих команд. Главной целью проекта является упрощение
работы гейм-мастера, внесение дополнительного функционала и фактора неожиданности
в игру. Проект является полностью некоммерческим хобби-проектом
_______
## Установка
Для установки бота необходимо:
1. Клонировать репозиторий в необходимую директорию 
`git clone https://github.com/PhPhPh123/infobot.git`

2. Установить зависимости `pip install -r requirements.txt`
3. Зарегистрировать бота в приложении discord https://discord.com/developers/applications и получить его token, id и имя
4. Разместить в основной директории файл `.env` с полученными данными. `.env` файл можно либо создать самому либо переместить
из папки additinal_files в основной директории. Каждое из трёх значений нужно заполнить полученными из приложения discord данными токена, id
и имени.
#### Пример: 
```
TOKEN=fDFf1312dfjdkfjs123214323
NAME=example_bot
ID=001122334455667788
```
-----------
## Запуск
Старт бота осуществляется путем запуска основного файла bot_main.py

Для получения списка всех команд необходимо после запуска ввести `!helpme` в текущий чат
в котором присутствует бот

------------
## Возможности
* Запрос всей необходимой информации по одному из имеющихся в базе данных миров или систем
* Запрос списка всех видимых миров
* Запрос графиков распределения импорта и экспорта по субсектору
* Запрос ценовой информации известным ценам на определенные группы товаров
* Запуск цикла новостей в котором имеются:
  * Новости о повышении уровня видимости миров
  * Новости о наличии врагах в системах
  * Новости о делах в субсекторе или общелорные
  * Процедурно генерируемые квесты
  * Изменение уровня спроса и предложения на отдельных мирах внутри торговой системы
  * Уникальные новости, внесенные гейм-мастером через отдельный интерфейс
* Создание процедурно сгенерирированных артефактов
* Создание процедурно сгенерированных случайных событий
* Рандомизация особенностей для противников
* Броски кубиков
-----------------

## Модификация
В основной базе данных бота уже прописаны конкретные миры, а часть случайных
событий заточены под одну конкретную ролку и ее сюжет. Для адаптации бота под
другую игру необходимо будет изменить базы данных удалив из них ненужные события и миры 
и заменить собственными


