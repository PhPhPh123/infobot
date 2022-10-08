from unittest import TestCase, main


class FunctionsTest(TestCase):
    def test_choise_quest(self):
        self.assertEqual(calc(2), 4)


def calc(a):
    res = a ** 2
    print('lol')
    return res
#
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


if __name__ == '__main__':
    main()
