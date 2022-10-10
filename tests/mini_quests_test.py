import random

import pytest
from news.mini_quests import QuestFormer, choise_quest, control_quests, Quest, Reward


@pytest.fixture
def quest_former_fixture(connect_to_db_sqlite3):
    def dict_former():
        art_obj = QuestFormer('artifact_quest')
        kill_obj = QuestFormer('kill_quest')
        delivery_obj = QuestFormer('delivery_quest')
        escort_obj = QuestFormer('escort_quest')

        obj_tuple = (art_obj, kill_obj, delivery_obj, escort_obj)
        dict_keys = ('artifact_quest', 'kill_quest', 'delivery_quest', 'escort_quest')

        obj_dict = dict(zip(dict_keys, obj_tuple))
        return obj_dict

    list_with_dicts = []
    for _ in range(100):
        list_with_dicts.append(dict_former())

    return list_with_dicts


def test_control_quests():
    for _ in range(20):
        result = control_quests()
        assert type(result) == str


def test_choise_quest_func():
    list_of_quests = ['artifact_quest', 'kill_quest', 'delivery_quest', 'escort_quest']
    for _ in range(20):
        result = choise_quest()
        assert result in list_of_quests


def test_check_quest_former_empty_base_awswer():
    for _ in range(500):
        assert QuestFormer('artifact_quest').quest_tuple != ()
        assert QuestFormer('kill_quest').quest_tuple != ()
        assert QuestFormer('delivery_quest').quest_tuple != ()
        assert QuestFormer('escort_quest').quest_tuple != ()


def test_former_tuple_len(quest_former_fixture, all_worlds_names_fixture):
    for isdict in quest_former_fixture:
        assert len(isdict['artifact_quest'].quest_tuple) == 3
        assert len(isdict['kill_quest'].quest_tuple) == 4
        assert len(isdict['delivery_quest'].quest_tuple) == 4
        assert len(isdict['escort_quest'].quest_tuple) == 2


def test_quest_former_world_names(quest_former_fixture, all_worlds_names_fixture):
    for isdict in quest_former_fixture:
        for obj in isdict.values():
            world_name = obj.quest_tuple[0]
            assert world_name in all_worlds_names_fixture


def test_quest_former_world_tuple_elem_types(quest_former_fixture):
    for isdict in quest_former_fixture:
        for obj in isdict.values():
            for elem in obj.quest_tuple:
                assert type(elem) == str


def test_base_quest_form_quest_name():
    try:
        Quest(())
        abstract_cant_instantiate = False
    except TypeError:
        abstract_cant_instantiate = True
    assert abstract_cant_instantiate


def test_reward_mixin():
    for _ in range(20):
        min_reward = 100000
        max_reward = 320000
        rew_obj = Reward()
        quest_timers = [2, 3, 4, 5]
        quest_dangers = ['Зеленая угроза', 'Синяя угроза', 'Фиолетовая угроза', 'Красная угроза']
        quest_dict = {'danger_name': random.choice([quest_dangers])}

        rew_obj.quest_dict = quest_dict
        rew_obj.count_reward(random.choice(quest_timers))

        assert min_reward <= rew_obj.count_reward(random.choice(quest_timers)) <= max_reward

