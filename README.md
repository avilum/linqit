# List
A python data structure for robust syntax.<br>
Write clean code with powerful syntax, instead of messy loops.<br>

## Lest have a closer look:
Let's say we have a custom python object:
```python
class Person(object):
    def __init__(self, first_name, last_name, hobby, age):
        self.first_name = first_name
        self.last_name = last_name
        self.hobby = hobby
        self.age = age
        self.full_name = ' '.join([self.first_name, self.last_name])

    def do_something(self):
        return '{name} is {what}.'.format(name=self.full_name, what=self.hobby.lower())

class Dog(object):
    color = 'Pink'
    
    def do_something(self):
        return 'Haw Haw!'
```

## Let's play with a container:
```python
john = Person('John', 'Doe', 'Coding', 27)
doggy = Dog()
bob = Person('Bob', 'Marley', 'Playing guitar', 33)

# Creating a container
container = List(john, doggy, bob)

# Powerful syntax
container.first_name  # ['John', 'Bob']
container.full_name  # ['John Doe', 'Bob Marley']
container.do_something()  # ['John Doe is coding', 'How How!', 'Bob Marley is playing guitar']
container.color  # ['Pink']

# Dynamic Runtime changes:
bob.birthday = datetime(year=1945, month=2, day=6)
container.birthday  # <class 'list'>: [datetime.datetime(1945, 2, 6, 0, 0)]
john.birthday = datetime(year=1970, month=1, day=1)
container.birthday  # <class 'list'>: [datetime.datetime(1970, 1, 1, 0, 0), datetime.datetime(1945, 2, 6, 0, 0)]
```

## LINQ selections:
```python
# Robust container methods.
assert bob == container.where(lambda p: p.age > 30)[0]
assert 'marley' == container.first(lambda p: p.age > 30).last_name.lower()
assert bob in container.where(lambda p: datetime.now() > p.birthday)
assert john == container.first(lambda p: 'd' in p.last_name.lower())
assert doggy == container.first(lambda p: isinstance(p, Dog))

# More to be implemented.
```