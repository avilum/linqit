from unittest import TestCase

from metacontainer import MetaContainer


class Mock(object):
    pass


class MetaContainerTests(TestCase):
    """
    Tests the edge cases of the MetaContainer class
    """

    def test_get_list_properties_should_combine_values(self):
        a = Mock()
        b = Mock()
        a.phones = [1, 2, 123321, 4]
        b.phones = [1, 2, 5, 789]
        self._container = MetaContainer(a, b)
        self.assertEqual(self._container.phones.sort(), [1, 2, 123321, 4, 1, 2, 5, 789].sort())
        self.assertEqual(len(self._container.phones), 8)


    def test_non_list_properties_should_combine_values(self):
        a = Mock()
        b = Mock()
        a.foo = 1
        b.foo = 2
        self._container = MetaContainer(a, b)
        self.assertEqual(self._container.foo, [1, 2])

    def test_non_list_peoperties_with_unique_metadata_peoperty(self):
        a = Mock()
        b = Mock()
        a.foo = 1
        b.bar = 2
        self._container = MetaContainer(a, b)
        self.assertEqual(self._container.foo, 1)
        self.assertEqual(self._container.bar, 2)

    def test_list_peoperties_with_unique_metadata_peoperty(self):
        a = Mock()
        b = Mock()
        a.foo = [1]
        b.bar = [2]
        self._container = MetaContainer(a, b)
        self.assertEqual(self._container.foo, [1])
        self.assertEqual(self._container.bar, [2])

    def test_init_with_several_items(self):
        container = MetaContainer(Mock(), Mock(), Mock())
        self.assertTrue(container)


    def test_different_types_sanity(self):
        a = Mock()
        b = Mock()
        a.foo = 'a'
        b.foo = 1
        self._container = MetaContainer(a, b)
        self.assertTrue('a' in self._container.foo)
        self.assertTrue(1 in self._container.foo)
        self.assertTrue(len(self._container.foo) == 2)
