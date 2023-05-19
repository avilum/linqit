from functools import (
    reduce,
)
from itertools import (
    chain,
)

_DEFAULT_LAZY = True
_NO_EXPR = lambda x:x

# A default variable for the function, so None as an argument will be valid, but not default.
_NONE = type('_NONE', (object,), {})

class List(list):
    """
    Extends Python's built-in list with additional functionality.
    Inspired by .NET's Language Integrated Queries (LINQ).
    This class wraps an iterable of objects.
    It enables them to be manipulated as a single entity.
    """

    def __init__(self, *objects):
        """
        Initializes a new List instance.

        :param objects: An iterable of objects to be contained.
        :type objects: iterable
        """
        super(List, self,).__init__(
            objects[0]
            if len(objects) == 1
            and hasattr(
                objects[0],
                "__iter__",
            )
            else objects
        )

    def __getitem__(self, item):
        """
        Retrieves the item(s) from the list at the specified index or slice.

        :param item: Index or slice specifying the item(s) to retrieve.
        :type item: int or slice
        :return: The item(s) from the list.
        :rtype: List or object
        """
        _item = super(
            List,
            self,
        ).__getitem__(item)

        if isinstance(
            item,
            slice,
        ):
            _item = List(_item)
        return _item

    def __getattr__(self, item):
        """
        Retrieves the attribute(s) with the specified name from the objects in the list.

        :param item: The attribute to retrieve.
        :type item: str
        :return: The attribute(s) from the objects in the list.
        :rtype: List or object
        :raises AttributeError: If the attribute does not exist in any object.
        """
        relevant_objects = list(
            filter(
                lambda obj: hasattr(
                    obj,
                    item,
                ),
                self,
            )
        )
        if not relevant_objects:
            raise AttributeError(item)

        attributes_values = List(
            [
                getattr(
                    obj,
                    item,
                )
                for obj in relevant_objects
            ]
        )

        if all(
            hasattr(
                attr_value,
                "__iter__",
            )
            and not isinstance(
                attr_value,
                str,
            )
            for attr_value in attributes_values
        ):
            return List(chain.from_iterable(attributes_values))
        elif all(callable(attr_value) for attr_value in attributes_values):
            return lambda *args: List(
                [
                    attr_value(*args)
                    for obj, attr_value in zip(
                        relevant_objects,
                        attributes_values,
                    )
                ]
            )

        return attributes_values

    def __add__(self, other):
        """
        Concatenates this list with another list or iterable.

        :param other: The list or iterable to concatenate.
        :type other: list or iterable
        :return: A new List containing the concatenated items.
        :rtype: List
        """
        added_list = super(
            List,
            self,
        ).__add__(other)
        return List(added_list)

    def __mul__(self, other):
        """
        Multiplies this list by an integer value.

        :param other: The integer value to multiply the list.
        :type other: int
        :return: A new List containing the multiplied items.
        :rtype: List
        """
        multi_list = super(
            List,
            self,
        ).__mul__(other)
        return List(multi_list)

    @property
    def sum(self):
        """
        Calculates the sum of all the values in the list.

        :return: The sum of the values.
        :rtype: object
        """
        return sum(self)

    @property
    def min(self):
        """
        Finds the lowest value in the list.

        :return: The lowest value.
        :rtype: object
        """
        return min(self)

    @property
    def max(self):
        """
        Finds the highest value in the list.

        :return: The highest value.
        :rtype: object
        """
        return max(self)

    @property
    def avg(self):
        """
        Calculates the average of the numerical values in the list.
        :return: The average of the values.
        :rtype: float
        """
        return reduce(
            lambda x, y: x + y,
            self,
        ) / len(self)

    @property
    def sorted(
        self,
    ):
        """
        Returns a new sorted list of the elements.

        :return: A new sorted list.
        :rtype: List
        """
        return sorted(self)

    def all(
        self,
        expression=_NO_EXPR,
    ):
        """
        Checks if all objects in the list satisfy the given expression.

        :param expression: The expression to evaluate for each object.
        :type expression: function
        :return: True if all objects satisfy the expression, False otherwise.
        :rtype: bool
        """
        if self:
            for i in self:
                if not expression(i):
                    return False
        return True


    def any(
        self,
        expression=_NO_EXPR,
    ):
        """
        Checks if any object in the list satisfies the given expression.

        :param expression: The expression to evaluate for each object.
        :type expression: function
        :return: True if any object satisfies the expression, False otherwise.
        :rtype: bool
        """
        if self:
            for i in self:
                if expression(i):
                    return True
        return False  # for an empty iterable, all returns False!

    def concat(self, second):
        """
        Concatenates this list with another list or iterable.

        :param second: The list or iterable to concatenate.
        :type second: list or iterable
        :return: A new List containing the concatenated items.
        :rtype: List
        """
        return List(self + second)

    def contains(self, item):
        """
        Checks if the list contains the specified item.

        :param item: The item to check for.
        :return: True if the item is in the list, False otherwise.
        :rtype: bool
        """
        return item in self

    def distinct(
        self,
    ):
        """
        Returns a new list with no duplicate items.

        :return: A new list with distinct items.
        :rtype: List
        """
        return List(set(self))

    def except_for(
        self,
        expression,
    ):
        """
        Returns a new list containing the objects that do not satisfy the given expression.

        :param expression: The expression to evaluate for each object.
        :type expression: function
        :return: A new List containing the filtered objects.
        :rtype: List
        """
        return List(
            filter(
                lambda e: not expression(e),
                self,
            )
        )

    def first(
        self,
expression=_NO_EXPR, default=_NONE
    ):
        """
        Returns the first object that satisfies the given expression, or the first element if no expression is provided.

        :param expression: The expression to evaluate for each object.
        :type expression: function or None
        :param default: The default value to return if no matching value is found.
        :return: The first matching object or the default value.
        :rtype: object
        :raises IndexError: If no matching value is found and no default value is provided.
        """
        if self:
            for el in self:
                if expression(el):
                    return(el)
        if default != _NONE:
            return default
        else:
            raise IndexError('No matching values')


    def get_by_attr(self, attr):
        """
        Retrieves all objects in the list that have the specified attribute.

        :param attr: The attribute name.
        :type attr: str
        :return: A new List containing the objects with the attribute.
        :rtype: List
        """
        try:
            return getattr(
                self,
                attr,
            )
        except AttributeError:
            return List()

    def intersect(self, second):
        """
        Returns a new list containing the objects that are present in both this list and the second list.

        :param second: The list or iterable to intersect with.
        :type second: list or iterable
        :return: A new List containing the intersecting objects.
        :rtype: List
        """
        return List(
            filter(
                lambda e: e in second,
                self,
            )
        )

    def last(
        self,
        expression=_NO_EXPR,
        default=_NONE,
    ):
        """
        Returns the last object that satisfies the given expression, or the last element if no expression is provided.

        :param expression: The expression to evaluate for each object.
        :type expression: function or None
        :param default: The default value to return if no matching value is found.
        :return: The last matching object or the default value.
        :rtype: object
        :raises IndexError: If no matching value is found and no default value is provided.
        """
        return List(reversed(self)).first(
            expression,
            default,
        )

    def order_by(
        self,
        expression=None,
    ):
        """
        Returns a new list of objects sorted according to the provided expression.
        If no expression is given, the default sort is used.

        :param expression: The expression to determine the sorting order.
        :type expression: function or None
        :return: A new sorted List.
        :rtype: List
        """
        sorted_data = sorted(
            self,
            key=expression,
        )
        return List(sorted_data)

    def select(
        self,
        expression,
    ):
        """
        Returns a new list containing the values obtained by applying the expression to each object in the list.

        :param expression: The expression to transform each object.
        :type expression: function
        :return: A new List containing the transformed values.
        :rtype: List
        """
        return List(
            map(
                expression,
                self,
            )
        )

    def skip(self, count):
        """
        Returns a new list containing the elements starting from the specified index.

        :param count: The number of elements to skip.
        :type count: int
        :return: A new List containing the remaining elements.
        :rtype: List
        """
        return List(self[count:])

    def take(self, count):
        """
        Returns a new list containing the first n elements.

        :param count: The number of elements to take.
        :type count: int
        :return: A new List containing the first n elements.
        :rtype: List
        """
        if not self or count == 0:
            return List()
        return self[:count]

    def where(self, expression=None, **filters):
        """
        Returns a new list containing the objects that satisfy the given expression and filters.

        :param expression: The expression to evaluate for each object.
        :type expression: function or None
        :param filters: Additional attribute filters to apply.
        :type filters: dict
        :return: A new List containing the filtered objects.
        :rtype: List
        """

        def filter_function(
            x,
        ):
            return (expression is None or expression(x)) and all(
                [
                    getattr(
                        x,
                        key,
                    )
                    == value
                    for key, value in filters.items()
                ]
            )

        selection = filter(
            filter_function,
            self,
        )
        return List(selection)

    def of_type(self, _type):
        """
        Returns a new list containing the objects of the specified type.

        :param _type: The type of objects to filter.
        :type _type: type
        :return: A new List containing the filtered objects.
        :rtype: List
        :raises TypeError: If the argument is not a type.
        """
        if not isinstance(
            _type,
            type,
        ):
            raise TypeError("The argument must be a type")
        return self.where(
            lambda e: isinstance(
                e,
                _type,
            )
        )
