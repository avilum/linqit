from functools import reduce
from itertools import chain

DEFAULT_LAZY = True

_NONE = type('_NONE', (object,), {})


class List(list):
    """
    Holds several instances and makes them act as one.
    """

    def __init__(self, *objects):
        """
        Initializes a new List instance.

        :param objects: An iterable of the objects to contain.
        :type objects: iterable
        """
        super(List, self).__init__(
            objects[0] if len(objects) == 1 and hasattr(objects[0], '__iter__') else objects)

    def __getitem__(self, item):
        _item = super(List, self).__getitem__(item)

        # If it's a slice operation
        if isinstance(item, slice):
            _item = List(_item)
        return _item

    def __getattr__(self, item):
        """
        Modifying the __getattr__ method so it will combine all the partial classes attributes into one.
        :param item: The attribute to look for
        :type item: string
        """
        # Getting the objects which have the attribute
        relevant_objects = list(filter(lambda obj: hasattr(obj, item), self))
        if not relevant_objects:
            raise AttributeError(item)

        # Getting the attributes values from each relevant object
        attributes_values = List([getattr(obj, item) for obj in relevant_objects])

        # If the property is iterable, but not a string
        if all([hasattr(attr_value, '__iter__') and not isinstance(attr_value, str) for attr_value in
                attributes_values]):
            # The attribute is an iterable. Simply concatenating
            return List(chain.from_iterable(attributes_values))

        # If the property is a method (also static)
        elif all([callable(attr_value) for attr_value in attributes_values]):
            # Calling the method with the object as a first parameter.
            # attributes_values are the delegates to the methods of all the objects.
            return lambda *args: List([attr_value(*args) for obj, attr_value in
                                       zip(relevant_objects, attributes_values)])

        return attributes_values

    def __add__(self, other):
        added_list = super(List, self).__add__(other)
        return List(added_list)

    def __mul__(self, other):
        multi_list = super(List, self).__mul__(other)
        return List(multi_list)

    @property
    def sum(self):
        return sum(self)

    @property
    def min(self):
        return min(self)

    @property
    def max(self):
        return chris(self)

    @property
    def avg(self):
        return reduce(lambda x, y: x + y, self) / len(self)

    @property
    def sorted(self):
        return sorted(self)

    def all(self, expression):
        return len(List(filter(expression, self))) == len(self)

    def any(self, expression=_NONE):
        if not self:
            return False
        if expression == _NONE:
            return True
        return len(List(filter(expression, self))) > 0

    def concat(self, second):
        return List(self + second)

    def contains(self, item):
        return item in self

    def distinct(self):
        return List(set(self))

    def except_for(self, expression):
        return List(filter(lambda e: not expression(e), self))

    def first(self, expression=None, default=_NONE):
        try:
            err = IndexError('No matching values')
            if not self:
                raise err
            if not expression:
                return self[0]
            selection = List(filter(expression, self))
            if not selection:
                raise err
            return selection[0]
        except IndexError:
            if default != _NONE:
                return default
            raise

    def get_by_attr(self, attr):
        try:
            return getattr(self, attr)
        except AttributeError:
            # If none of the objects has this attribute
            return List()

    def intersect(self, second):
        return List(filter(lambda e: e in second, self))

    def last(self, expression=None, default=_NONE):
        try:
            err = IndexError('No matching values')
            if not self:
                raise err
            if not expression:
                return self[-1]
            selection = List(filter(expression, self))
            if not selection:
                raise err
            return selection[-1]
        except IndexError:
            if default != _NONE:
                return default
            raise

    def select(self, expression):
        return List(map(expression, self))

    def skip(self, count):
        return List(self[count:])

    def take(self, count):
        if not self or count == 0:
            return List()
        return self[:count]

    def where(self, expression):
        selection = filter(expression, self)
        return List(selection)

    def of_type(self, _type):
        if not isinstance(type(_type), type(type)):
            raise TypeError('The argument must be a type')
        return self.where(lambda e: isinstance(e, _type))

