# MetaContainer
Make python instances act as one with a robust container.<br>
No more loops, No more lists of objects.

# Example
Create your custom type:
```python
class Person(object):
    def __init__(self, first_name, last_name):
        self._first_name = first_name
        self._last_name = last_name

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def full_name(self):
        return ' '.join([self._first_name, self._last_name])

    def json(self):
        import json
        return json.dumps(self.__dict__)

    def do(self, what):
        return '{name} is doing {what}'.format(name=self.full_name, what=what)
```

Create a container of Persons:
```python
from metacontainer import MetaContainer

john, bob = Person('John', 'Doe'), Person('Bob', 'Marley')
c = MetaContainer(john, bob)

# Powerful functionality
c.first_name # ['John', 'Bob']
c.full_name # ['John Doe', 'Bob Marley']
c.do('Dishes') # ['John Doe is doing Dishes', 'Bob Marley is doing Dishes']
c.json() # ['{"_first_name": "John", "_last_name": "Doe"}', '{"_first_name": "Bob", "_last_name": "Marley"}']

# Dynamic during runtime
bob.skill = 'Reggae'
c.skill # 'Reggae'
john.skill = 'Programming'
c.skill # ['Programming', 'Reggae']

```