# Linqit !
A list-like type with fun functionality.<br>
Extends the builtin list with .NET's Language Integrated Queries (Linq) and more.<br>
Write clean code with powerful syntax. Forget about messy loops, conditions and nested list comprehensions.<br>
Multiple filter/map/list-comprehensions, aggregating on on another, are not readable.<br>
I love python, but sometimes - python can be SO NOT PYTHONIC. Some of the methods might look rediculous for a simgle call comparing to the regular python syntax. The whole idea is is to use it for nested, multiple filters/modifications :).<br>
Here are some use cases:

#### Methods:
```
all
any
concat
contains
distinct
except_for
first
get_by_attr
intersect
last
select
skip
take
where
of_type
```
#### Properties:
```
sum
min
max
avg
sorted
```

## Creating a list of people
```
import List

class Person():
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return '<Person name="{}" age="{}">'.format(self.name, self.age)


# Creating a list of people
avi, bill, bob, harry = Person('Avi', 23), Person('Bill', 41), Person('Bob', 77), Person('Harry', 55)

people = List(avi, bill, bob, harry)
```

## LINQ selections, cleaner code
```python
old_people = people.where(lambda p: p.age > 23) # It's a joke! :) [<Person name="Bill" age="41">, <Person name="Bob" age="77">, <Person name="Harry" age="55">]
old_people.first()                                              # <Person name="Bill" age="41">
old_people.last()                                               # <Person name="Harry" age="55">
old_people.any(lambda p: p.name.lower().startswith('b'))        # True
old_people.where(lambda p: p.age == 55)                         # [<Person name="Harry" age="55">]
old_people.skip(3).any()                                        # False
old_people.skip(2).first()                                      # <Person name="Harry" age="55">

# Isn't it better than "for", "if", "else", "filter", "map" and list comprehensions in the middle of your code?

```
## More selections
```python
new_kids_in_town = [Person('Chris', 18), Person('Danny', 16), Person('John', 17)]
people += new_kids_in_town # Also works: people = people.concat(new_kids_in_town)

teenagers = people.where(lambda p: 20 >= p.age >= 13)
danny = teenagers.first(lambda t: t.name == 'Danny')            # <Person name="Danny" age="16">
oldest_teen = teenagers.last()                                  # <Person name="John" age="17">
```

## Dynamic attributes
```python
names = people.name                                             # ['Avi', 'Bill', 'Bob', 'Harry', 'Chris', 'John']
ages = people.age                                               # [23, 41, 77, 55, 18, 17]
teenagers_names = teenagers.name                                # ['Chris', 'Danny', 'John']
teenagers_names.take(2).except_for(lambda n: n == 'Danny')      # ['Chris']
teenagers.age.min                                               # 16
teenagers.age.avg                                               # 17
teenagers.age.max                                               # 18
```
