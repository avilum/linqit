from itertools import chain


class MetaContainer(object):
    """
    Holds several instances and makes them act as one.

    >>> class Foo(object):
    >>>     pass
    >>>
    >>> a, b = Foo(), Foo()
    >>>
    >>> a.foo = 1
    >>> b.foo = 2
    >>> container = MetaContainer(a, b)
    >>> container.foo
    >>> [1, 2]
    >>>
    >>> a.bar = ["a@b.com"]
    >>> b.bar = ["c@d.com"]
    >>> container.bar
    >>> ["a@b.com", "c@d.com"]
    >>>
    >>> b.bar += 'new@email.com'
    >>> c.bar
    >>> ["a@b.com", "c@d.com", "new@email.com"]

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

    def __getattr__(self, item):
        """
        Modifying the __getattr__ method so it will combine all the partial classes attributes into one.
        :param item: The attribute to look for
        :type item: string
        """
        relevant_metadatas = [m for m in self._metadatas if hasattr(m, item)]
        if not relevant_metadatas:
            raise AttributeError(item)

        values = [getattr(metadata, item) for metadata in relevant_metadatas]

        # If the property is iterable
        if all([hasattr(x, '__iter__') for x in values]):
            # The attribute is an iterable. Simply contacting
            return list(chain.from_iterable(values))

        return values[0] if len(values) == 1 else values

    def __repr__(self):
        return "<{name} with {metadatas_count} metadatas>".format(name=self.__class__.__name__,
                                                                  metadatas_count=len(self._metadatas))

