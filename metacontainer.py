from itertools import chain

DEFAULT_LAZY = True


class MetaContainer(object):
    """
    Holds several instances and makes them act as one.


    >>> john, bob = Person('John', 'Doe'), Person('Bob', 'Marley')
    >>> c = MetaContainer(john, bob)
    >>> c.first_name # ['John', 'Bob']
    >>> c.full_name # ['John Doe', 'Bob Marley']
    >>> c.do('Dishes') # ['John Doe is doing Dishes', 'Bob Marley is doing Dishes']

    >>> bob.skill = 'Reggae'
    >>> c.skill # 'Reggae'

    >>> john.skill = 'Programming'
    >>> c.skill # ['Programming', 'Reggae']
    """

    def __init__(self, *metadatas):
        """
        Initializes a new MetaContainer instance.

        :param metadatas: An iterable of the metadatas to contain.
        :type metadatas: iterable
        """
        self._metadatas = [metadatas[0]] if len(metadatas) == 1 else metadatas

    @property
    def metadatas(self):
        return self._metadatas

    @metadatas.setter
    def metadatas(self, value):
        self._metadatas = value

    def append(self, metadata):
        self._metadatas += metadata

    def __getattr__(self, item):
        """
        Modifying the __getattr__ method so it will combine all the partial classes attributes into one.
        :param item: The attribute to look for
        :type item: string
        """
        # Getting the metadatas which have the attribute
        relevant_metadatas = [m for m in self._metadatas if hasattr(m, item)]
        if not relevant_metadatas:
            raise AttributeError(item)

        # Getting the attributes values from each relevant metadata
        values = [getattr(metadata, item) for metadata in relevant_metadatas]

        # If the property is iterable, but not a string
        if all([hasattr(attr_value, '__iter__') and not isinstance(attr_value, str) for attr_value in values]):
            # The attribute is an iterable. Simply concatenating
            return list(chain.from_iterable(values))

        # If the property is a method (also static)
        elif all([callable(attr_value) for attr_value in values]):
            # Calling the method with the metadata as a first parameter.
            return lambda *args: MetaContainer([attr_value(*args) for metadata, attr_value in
                                                zip(relevant_metadatas, values)])

        return values

    def __repr__(self):
        return repr(self._metadatas)

    def __iter__(self):
        return iter(self._metadatas)

    def where(self, expression):
        selection = filter(expression, self._metadatas)
        return list(selection)

    def first(self, expression, default=None):
        selection = list(filter(expression, self._metadatas))
        return selection[0] if selection else default

