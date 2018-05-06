from datetime import datetime
from unittest import TestCase
from metacontainer import MetaContainer


class Mock(object):
    pass


class Person(object):
    def __init__(self, first_name, last_name, hobby, age):
        self.first_name = first_name
        self.last_name = last_name
        self.hobby = hobby
        self.age = age
        self.full_name = ' '.join([self.first_name, self.last_name])

    def do_something(self):
        return '{name} is {what}.'.format(name=self.full_name, what=self.hobby.lower())


class MetaContainerTests(TestCase):
    """
    UnitTests (edge cases tests) of the MetaContainer class
    """

    def test_get_list_properties_should_combine_values(self):
        a, b = Mock(), Mock()
        a.phones = [1, 2, 123321, 4]
        b.phones = [1, 2, 5, 789]
        self._container = MetaContainer(a, b)
        self.assertEqual(self._container.phones.sort(), [1, 2, 123321, 4, 1, 2, 5, 789].sort())
        self.assertEqual(len(self._container.phones), 8)


    def test_non_list_properties_should_combine_values(self):
        a, b = Mock(), Mock()
        a.foo = 1
        b.foo = 2
        self._container = MetaContainer(a, b)
        self.assertEqual(self._container.foo, [1, 2])

    def test_non_list_peoperties_with_unique_metadata_peoperty(self):
        a, b = Mock(), Mock()
        a.foo = 1
        b.bar = 2
        self._container = MetaContainer(a, b)
        self.assertEqual(self._container.foo, [1])
        self.assertEqual(self._container.bar, [2])

    def test_list_peoperties_with_unique_metadata_peoperty(self):
        a, b = Mock(), Mock()
        a.foo = [1]
        b.bar = [2]
        self._container = MetaContainer(a, b)
        self.assertEqual(self._container.foo, [1])
        self.assertEqual(self._container.bar, [2])

    def test_init_with_several_items(self):
        container = MetaContainer(Mock(), Mock(), Mock())
        self.assertTrue(container)

    def test_different_types_sanity(self):
        a, b = Mock(), Mock()
        a.foo = 'a'
        b.foo = 1
        self._container = MetaContainer(a, b)
        self.assertTrue('a' in self._container.foo)
        self.assertTrue(1 in self._container.foo)
        self.assertTrue(len(self._container.foo) == 2)

    def test_where_method_sanity(self):
        a, b = Mock(), Mock()
        a.name = 'bob'
        b.name = 'john'
        self._container = MetaContainer(a, b)
        self.assertEqual(self._container.where(lambda p:p.name == 'bob')[0], a)

    def test_where_method(self):
        john = Person('John', 'Doe', 'Coding', 27)
        bob = Person('Bob', 'Marley', 'Playing guitar', 33)

        # Creating a container
        container = MetaContainer(john, bob)

        # Powerful functionality
        container.first_name  # ['John', 'Bob']
        container.full_name  # ['John Doe', 'Bob Marley']
        container.do_something()  # ['John Doe is coding', 'Bob Marley is playing guitar']

        # Dynamic Runtime changes:
        bob.birthday = datetime(year=1945, month=2, day=6)
        container.birthday  # datetime.datetime(1945, 2, 6, 0, 0)
        john.birthday = datetime(year=1970, month=1, day=1)
        container.birthday  # <class 'list'>: [datetime.datetime(1970, 1, 1, 0, 0), datetime.datetime(1945, 2, 6, 0, 0)]

        self.assertEqual(john, container.first(lambda p: 'd' in p.last_name.lower()))
        self.assertIn(bob, container.where(lambda p: datetime.now() > p.birthday))
        self.assertEqual('bob', container.first(lambda p: p.age > 30).first_name.lower())
