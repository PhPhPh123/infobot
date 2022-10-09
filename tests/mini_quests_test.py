import pytest
from news.mini_quests import QuestFormer


@pytest.fixture
def quest_former_fixture(connect_to_db_sqlite3):
    art_obj = QuestFormer('artifact_quest')
    kill_obj = QuestFormer('kill_quest')
    delivery_obj = QuestFormer('delivery_quest')
    escort_obj = QuestFormer('escort_quest')

    obj_tuple = (art_obj, kill_obj, delivery_obj, escort_obj)
    dict_keys = ('artifact_quest', 'kill_quest', 'delivery_quest', 'escort_quest')

    obj_dict = dict(zip(dict_keys, obj_tuple))
    return obj_dict


def test_quest_former_tuple_len(quest_former_fixture, all_worlds_names_fixture):
    assert len(quest_former_fixture['artifact_quest'].quest_tuple) == 3
    assert len(quest_former_fixture['kill_quest'].quest_tuple) == 4
    assert len(quest_former_fixture['delivery_quest'].quest_tuple) == 4
    assert len(quest_former_fixture['escort_quest'].quest_tuple) == 2


def test_quest_former_world_names(quest_former_fixture, all_worlds_names_fixture):
    for obj in quest_former_fixture.values():
        world_name = obj.quest_tuple[0]
        assert world_name in all_worlds_names_fixture


def test_check_world_tuple_elem_types(quest_former_fixture):
    for obj in quest_former_fixture.values():
        for elem in obj.quest_tuple:
            assert type(elem) == str


# class QuestFormerTest(TestCase):
#     pass
#
#
# class QuestTest(TestCase):
#     pass
#
#
# class ArtifactQuestTest(TestCase):
#     pass
#
#
# class KillQuestTest(TestCase):
#     pass
#
#
# class DeliveryQuestTest(TestCase):
#     pass
#
#
# class EscortQuestTest(TestCase):
#     pass

