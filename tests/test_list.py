from datetime import (
    datetime,
)
from unittest import (
    TestCase,
)

from linqit import (
    List,
)


class Mock(object):
    pass


counter = 0


def func_samson(x):
    global counter
    counter += 1
    return x.last_name == "samson"


def func_lee(x):
    global counter
    counter += 1
    return x.last_name == "lee"


class Person(object):
    def __init__(
        self,
        first_name,
        last_name,
        hobby,
        age,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.hobby = hobby
        self.age = age
        self.full_name = " ".join(
            [
                self.first_name,
                self.last_name,
            ]
        )

    def do_something(
        self,
    ):
        return "{name} is {what}.".format(
            name=self.full_name,
            what=self.hobby.lower(),
        )


class ListTests(TestCase):
    """
    UnitTests (edge cases tests) of the List class
    """

    def setUp(self):
        self.list = self._get_dynamic_list_with_mocks()

    def _get_dynamic_list_with_mocks(
        self,
    ):
        a, b = (
            Mock(),
            Mock(),
        )
        a.name = "bob"
        a.age = 20
        b.name = "john"
        b.age = 20
        return List(a, b)

    # Sanity and edge cases tests

    def test_get_list_properties_should_combine_values(
        self,
    ):
        a, b = (
            Mock(),
            Mock(),
        )
        a.phones = [
            1,
            2,
            123321,
            4,
        ]
        b.phones = [
            1,
            2,
            5,
            789,
        ]
        self.list = List(a, b)
        self.assertEqual(
            self.list.phones.sort(),
            [
                1,
                2,
                123321,
                4,
                1,
                2,
                5,
                789,
            ].sort(),
        )
        self.assertEqual(
            len(self.list.phones),
            8,
        )

    def test_non_list_properties_should_combine_values(
        self,
    ):
        a, b = (
            Mock(),
            Mock(),
        )
        a.foo = 1
        b.foo = 2
        self.list = List(a, b)
        self.assertEqual(
            self.list.foo,
            [1, 2],
        )

    def test_non_list_peoperties_with_unique_object_peoperty(
        self,
    ):
        a, b = (
            Mock(),
            Mock(),
        )
        a.foo = 1
        b.bar = 2
        self.list = List(a, b)
        self.assertEqual(
            self.list.foo,
            [1],
        )
        self.assertEqual(
            self.list.bar,
            [2],
        )

    def test_list_peoperties_with_unique_object_peoperty(
        self,
    ):
        a, b = (
            Mock(),
            Mock(),
        )
        a.foo = [1]
        b.bar = [2]
        self.list = List(a, b)
        self.assertEqual(
            self.list.foo,
            [1],
        )
        self.assertEqual(
            self.list.bar,
            [2],
        )

    def test_init_with_several_items(
        self,
    ):
        dynamic_list = List(
            Mock(),
            Mock(),
            Mock(),
        )
        self.assertTrue(dynamic_list)

    def test_different_types_sanity(
        self,
    ):
        a, b = (
            Mock(),
            Mock(),
        )
        a.foo = "a"
        b.foo = 1
        self.list = List(a, b)
        self.assertTrue("a" in self.list.foo)
        self.assertTrue(1 in self.list.foo)
        self.assertTrue(len(self.list.foo) == 2)

    def test_runtime_changes_apply(
        self,
    ):
        john = Person(
            "John",
            "Doe",
            "Coding",
            27,
        )
        bob = Person(
            "Bob",
            "Marley",
            "Playing guitar",
            33,
        )

        # Creating a dynamic_list
        dynamic_list = List(
            john,
            bob,
        )

        # Powerful functionality
        dynamic_list.first_name  # ['John', 'Bob']
        dynamic_list.full_name  # ['John Doe', 'Bob Marley']
        dynamic_list.do_something()  # ['John Doe is coding', 'Bob Marley is playing guitar']

        # Dynamic Runtime changes:
        bob.birthday = datetime(
            year=1945,
            month=2,
            day=6,
        )
        dynamic_list.birthday  # datetime.datetime(1945, 2, 6, 0, 0)
        john.birthday = datetime(
            year=1970,
            month=1,
            day=1,
        )
        dynamic_list.birthday  # <class 'list'>: [datetime.datetime(1970, 1, 1, 0, 0), datetime.datetime(1945, 2, 6, 0, 0)]
        self.assertTrue(len(dynamic_list.birthday) == 2)

    def test_add_method(
        self,
    ):
        added_list = self.list + self.list
        self.assertTrue(len(added_list) == 4)
        self.assertTrue(
            isinstance(
                added_list,
                List,
            )
        )

    def test_times_method(
        self,
    ):
        timed_list = self.list * 3
        self.assertTrue(len(timed_list) == 6)
        self.assertTrue(
            isinstance(
                timed_list,
                List,
            )
        )

    def test_slice_method(
        self,
    ):
        sliced_list = self.list[:-1]
        self.assertTrue(len(sliced_list) == 1)
        self.assertTrue(
            isinstance(
                sliced_list,
                List,
            )
        )

    def test_non_existing_attribute_raises_attribute_error(
        self,
    ):
        self.assertRaises(
            AttributeError,
            self.list.__getattribute__,
            "blabla",
        )

    # LINQ Methods tests

    def test_where_method(
        self,
    ):
        self.assertEqual(
            self.list.where(lambda p: p.name == "bob")[0],
            self.list[0],
        )

    def test_where_method_without_expression(
        self,
    ):
        self.assertEqual(
            self.list.where(),
            self.list,
        )

    def test_where_method_with_filter_kwargs(
        self,
    ):
        self.assertEqual(
            self.list.where(name="bob")[0],
            self.list[0],
        )

    def test_where_method_with_expression_and_filter_kwargs(
        self,
    ):
        self.assertEqual(
            self.list.where(
                lambda x: len(x.name) == 4,
                age=20,
            )[0],
            self.list[1],
        )

    def test_where_method_with_multiple_filter_kwargs(
        self,
    ):
        self.assertEqual(
            self.list.where(
                name="bob",
                age=15,
            ),
            [],
        )

    def test_first_method(
        self,
    ):
        self.assertEqual(
            self.list.first(lambda p: p.name == "bob"),
            self.list[0],
        )

    def test_first_method_with_nonexisisting_value_raises_indexerror(
        self,
    ):
        self.assertRaises(
            IndexError,
            self.list.first,
            lambda p: p.name == "id that dont exist",
        )

    def test_first_method_with_nonexisisting_value_returns_none(
        self,
    ):
        self.assertEqual(
            None,
            self.list.first(
                lambda p: p.name == "danny",
                None,
            ),
        )

    def test_any_method(
        self,
    ):
        self.assertEqual(
            True,
            self.list.any(lambda p: p.name == "bob"),
        )

    def test_any_method_with_all_false(
        self,
    ):
        self.assertEqual(
            False,
            self.list.any(lambda p: p.name == "danny"),
        )

    def test_any_method_without_expression(
        self,
    ):
        self.assertEqual(
            True,
            self.list.any(),
        )

    def test_any_method_without_expression_and_empty_list(
        self,
    ):
        empty = List()
        self.assertEqual(
            False,
            empty.any(),
        )

    def test_all_method(
        self,
    ):
        self.assertEqual(
            True,
            self.list.all(lambda p: p.age == 20),
        )

    def test_all_method_with_false_arguments(
        self,
    ):
        self.assertEqual(
            False,
            self.list.all(lambda p: p.age == 19),
        )

    def test_contains_method_with_existing_item(
        self,
    ):
        self.assertTrue(self.list.contains(self.list[0]))

    def test_contains_method_with_non_existing_item(
        self,
    ):
        self.assertFalse(self.list.contains("123"))

    def test_sum_method(
        self,
    ):
        self.list = List(
            1,
            2,
            3,
            4,
            5,
        )
        self.assertEqual(
            self.list.sum,
            15,
        )

    def test_min_method(
        self,
    ):
        self.list = List(
            1,
            2,
            3,
            4,
            5,
        )
        self.assertEqual(
            self.list.min,
            1,
        )

    def test_max_method(
        self,
    ):
        self.list = List(
            1,
            2,
            3,
            4,
            5,
        )
        self.assertEqual(
            self.list.max,
            5,
        )

    def test_avg_method(
        self,
    ):
        self.list = List(
            1,
            2,
            3,
            4,
            5,
        )
        self.assertEqual(
            self.list.avg,
            3,
        )

    def test_select_method(
        self,
    ):
        def expression(
            e,
        ):
            return e.name

        self.assertEqual(
            self.list.select(expression),
            self.list.name,
        )

    def test_skip_method(
        self,
    ):
        self.assertEqual(
            self.list.skip(1)[0],
            self.list[1],
        )

    def test_take_method(
        self,
    ):
        self.list = self.list * 6
        taken_elements = self.list.take(2)
        self.assertEqual(
            taken_elements,
            self.list[:2],
        )

    def test_concat_method(
        self,
    ):
        m = Mock()
        m.name = "Avi"
        l2 = List(m)
        concatinated_list = self.list.concat(l2)
        self.assertEqual(
            len(concatinated_list),
            3,
        )
        self.assertEqual(
            concatinated_list[-1],
            m,
        )

    def test_intersect_method(
        self,
    ):
        e1 = self.list[0]
        l2 = List(e1)
        intersected = self.list.intersect(l2)
        self.assertEqual(
            len(intersected),
            1,
        )
        self.assertEqual(
            intersected[0],
            e1,
        )

    def test_except_for_method(
        self,
    ):
        excepted_list = self.list.except_for(lambda x: x.name.lower().startswith("b"))
        self.assertEqual(
            len(excepted_list),
            1,
        )
        self.assertEqual(
            excepted_list[0],
            self.list[1],
        )

    def test_one_liner(
        self,
    ):
        self.assertEqual(
            20,
            self.list.concat(self.list)
            .where(lambda e: e.name.lower() == "john")
            .skip(1)
            .select(lambda x: x.age)
            .avg,
        )
        self.list[1].age = 89
        self.list[1].name = "Bobby Brown"
        self.assertEqual(
            self.list[1].name,
            self.list.concat(self.list)
            .where(lambda e: e.age > 18)
            .skip(1)
            .except_for(lambda e: e.name == "bob")
            .select(lambda x: x.name)
            .last(),
        )

    def test_order_by_bare(
        self,
    ):
        data = [
            1,
            -1,
            7,
            200,
            4,
            3,
        ]
        sorted_data = sorted(data)

        linq_data = List(data).order_by()
        self.assertEqual(
            sorted_data,
            linq_data,
        )

    def test_order_by_complex(
        self,
    ):
        data = [
            Person(
                "jake",
                "samson",
                None,
                32,
            ),
            Person(
                "sam",
                "thompson",
                None,
                44,
            ),
            Person(
                "sarah",
                "smith",
                None,
                41,
            ),
            Person(
                "zoe",
                "lee",
                None,
                27,
            ),
        ]
        sorted_data = sorted(
            data,
            key=lambda p: p.age,
            reverse=True,
        )

        linq_data = List(data).order_by(lambda p: -p.age)
        self.assertEqual(
            sorted_data,
            linq_data,
        )

    def test_any_method_short_circuit(
        self,
    ):
        data = [
            Person(
                "jake",
                "samson",
                None,
                32,
            ),
            Person(
                "sam",
                "thompson",
                None,
                44,
            ),
            Person(
                "sarah",
                "smith",
                None,
                41,
            ),
            Person(
                "zoe",
                "lee",
                None,
                27,
            ),
        ]

        global counter
        counter = 0
        linq_data = List(data).any(func_samson)
        self.assertEqual(
            linq_data,
            True,
        )
        self.assertEqual(
            counter,
            1,
        )

        counter = 0
        linq_data = List(data).any(func_lee)
        self.assertEqual(
            linq_data,
            True,
        )
        self.assertEqual(
            counter,
            4,
        )

    def test_all_method_short_circuit(
        self,
    ):
        data = [
            Person(
                "jake",
                "samson",
                None,
                32,
            ),
            Person(
                "sam",
                "james",
                None,
                44,
            ),
            Person(
                "sarah",
                "smith",
                None,
                41,
            ),
            Person(
                "zoe",
                "lee",
                None,
                27,
            ),
        ]

        global counter
        counter = 0
        linq_data = List(data).all(func_samson)
        self.assertEqual(
            linq_data,
            False,
        )
        self.assertEqual(
            counter,
            2,
        )  # One true, then false

        data = [
            Person(
                "jake",
                "samson",
                None,
                32,
            ),
            Person(
                "sam",
                "samson",
                None,
                44,
            ),
            Person(
                "sarah",
                "samson",
                None,
                41,
            ),
            Person(
                "zoe",
                "samson",
                None,
                27,
            ),
        ]

        counter = 0
        linq_data = List(data).all(func_samson)
        self.assertEqual(
            linq_data,
            True,
        )
        self.assertEqual(
            counter,
            4,
        )  # all 4 true
