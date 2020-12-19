from functools import reduce
from itertools import chain

DEFAULT_LAZY = True

# A default variable for the function, so None as an argument will be valid, but not default.
_NONE = type('_NONE', (object,), {})

# Allows truthy filters
_NO_EXPR = lambda x:x

class List(list):
    """
    Extends python's list builtin with fun, robust functionality - .NET's Language Integrated Queries (Linq).
    This instance wraps an iterable of objects, and makes them act as one.
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
        if all(hasattr(attr_value, '__iter__') and not isinstance(attr_value, str) for attr_value in
               attributes_values):
            # The attribute is an iterable. Simply concatenating
            return List(chain.from_iterable(attributes_values))

        # If the property is a method (also static)
        elif all(callable(attr_value) for attr_value in attributes_values):
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
        """
        Returns a sum of all the values in the sequence.
        """
        return sum(self)

    @property
    def min(self):
        """
        Returns lowest value in the sequence.
        """
        return min(self)

    @property
    def max(self):
        """
        Returns highest value in the sequence.
        """
        return max(self)

    @property
    def avg(self):
        """
        Returns the average of the sequence's items.
        The objects must be numerical in order to use this method (int, float interfaces).
        """
        return reduce(lambda x, y: x + y, self) / len(self)

    @property
    def sorted(self):
        """
        Returns a sorted list of the elements.
        Make sure to your objects implement the __eq__, __gt__, __lt__, __ne__ methods.
        """
        return sorted(self)

    def all(self, expression=_NO_EXPR):
        """
        Returns False if all of the objects fail the expression. Returns True otherwise.
        """
        if self:
            for i in self:
                if not expression(i):
                    return False
        return True

    def any(self, expression=_NO_EXPR):
        """
        Returns True if any of the objects fulfill the expression. Returns False otherwise.
        """
        if self:
            for i in self:
                if expression(i):
                    return True
        return False  # for an empty iterable, all returns False!

    def concat(self, second):
        """
        Returns a sequence containing this list and 'second' together (Addition).
        """
        return List(self + second)

    def contains(self, item):
        """
        Returns True if the object 'item' is in the sequence, False otherwise.
        """
        return item in self

    def distinct(self):
        """
        Returns a distincted list, with no duplications between the object.
        Please make sure the __hash__ method is implemented.
        """
        return List(set(self))

    def except_for(self, expression):
        """
        Contrary to 'where' - Returns all the objects that does not fulfill the expression.
        """
        return List(filter(lambda e: not expression(e), self))

    def first(self, expression=_NO_EXPR, default=_NONE):
        """
        Returns the first object that fulfills an expression.
        If the expression is not specified, returns the first element.
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
        Returns all the objects that has a specified attribute 'attr'.
        """
        try:
            return getattr(self, attr)
        except AttributeError:
            # If none of the objects has this attribute
            return List()

    def intersect(self, second):
        """
        Returns a sequence of the objects that intersect with (found in) list 'second'.
        """
        return List(filter(lambda e: e in second, self))

    def last(self, expression=_NO_EXPR, default=_NONE):
        """
        Returns the last object that fulfills an expression.
        If the expression is not specified, returns the last element.
        """
        return List(reversed(self)).first(expression,default)

    def order_by(self, expression=None):
        """
        Returns a List of data, sorted according to expression. If no expression is given, the default sort is used.
        """
        sorted_data = sorted(self, key=expression)
        return List(sorted_data)

    def select(self, expression):
        """
        Returns a list of the values of the expression, from all the wrapped elements.
        """
        return List(map(expression, self))

    def skip(self, count):
        """
        Returns a slice of the elements, starting from n index. equivalent to [n:]
        """
        return List(self[count:])

    def take(self, count):
        """
        Returns a alice of the first n elements. equivalent to [:n]
        """
        if not self or count == 0:
            return List()
        return self[:count]

    def where(self, expression):
        """
        Returns all the objects that fulfill an expression (objects that return True for the expression).
        """
        selection = filter(expression, self)
        return List(selection)

    def of_type(self, _type):
        """
        Returns all the objects of a specified type
        """
        if not isinstance(type(_type), type(type)):
            raise TypeError('The argument must be a type')
        return self.where(lambda e: isinstance(e, _type))


__all__ = [List]
