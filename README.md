# Linqit!
Extends python's list builtin with fun, robust functionality - .NET's Language Integrated Queries (Linq) and more.<br>
Write clean code with powerful syntax.<br><br>
```shell script
pip install linqit
```
<center>
<img src="https://img.shields.io/badge/Test Coverage-96%25-brightgreen">
</center>
<br>


Stop using loops, complex conditions, list comprehension and filters.<br>
Doesn't it looks better? <br>
```python
from seven_dwwarfs import Grumpy, Happy, Sleepy, Bashful, Sneezy, Dopey, Doc
from linqit import List

# Go ahead and fill the list with whatever you want... like a list of <Programmer> objects.
programmers = List()
Avi = type("Avi", (), {})
elon_musk = Entrepreneur(talented=True)

# Then play:
last_hot_pizza_slice = (
    programmers.where(lambda e: e.experience > 15)
    .except_for(elon_musk)
    .of_type(Avi)
    .take(3)  # [<Avi>, <Avi>, <Avi>]
    .select(lambda avi: avi.lunch)  # [<Pizza>, <Pizza>, <Pizza>]
    .where(lambda p: p.is_hot() and p.origin != "Pizza Hut")
    .last()  # <Pizza>
    .slices.last()  # <PizzaSlice>
)

# What do you think?
```

We all use multiple aggregations in our code, while multiple filters/comprehensions are not pythonic at all.<br>
The whole idea is is to use it for nested, multiple filters/modifications :).<br>
Some of the methods might look ridiculous for a single calls, comparing to the regular python syntax.<br>
Here are some use cases: <br>

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

## Deeper - Let's play with a list of people, a custom type.
```python
import List

class Person():
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f'Person(name="{self.name}", age={self.age})')


# Creating a list of people
avi, bill, bob, harry = Person('Avi', 23), Person('Bill', 41), Person('Bob', 77), Person('Harry', 55)

people = List(avi, bill, bob, harry)
```

## Use LINQ selections, write cleaner code
```python
people = people.where(lambda p: p.age > 23) # [<Person name="Bill" age="41">, <Person name="Bob" age="77">, <Person name="Harry" age="55">]
people.first()                                              # <Person name="Bill" age="41">
people.last()                                               # <Person name="Harry" age="55">
people.any(lambda p: p.name.lower().startswith('b'))        # True
people.where(age=55)                         # [<Person name="Harry" age="55">]
people.skip(3).any()                                        # False
people.skip(2).first()                                      # <Person name="Harry" age="55">

# Isn't it better than "for", "if", "else", "filter", "map" and list comprehensions in the middle of your code?

```
## More selections
```python
new_kids_in_town = [Person('Chris', 18), Person('Danny', 16), Person('John', 17)]
people += new_kids_in_town # Also works: people = people.concat(new_kids_in_town)

teenagers = people.where(lambda p: 20 >= p.age >= 13)
danny = teenagers.first(lambda t: t.name == 'Danny')            # <Person name="Danny" age="16">
oldest_teen = teenagers.order_by(lambda t: t.age).last()                                  # <Person name="John" age="17">
```

## Let's make python more dynamic
```python
names = people.name                                             # ['Avi', 'Bill', 'Bob', 'Harry', 'Chris', 'John']
ages = people.age                                               # [23, 41, 77, 55, 18, 17]
teenagers_names = teenagers.name                                # ['Chris', 'Danny', 'John']
teenagers_names.take(2).except_for(lambda n: n == 'Danny')      # ['Chris']
teenagers.age.min                                               # 16
teenagers.age.avg                                               # 17
teenagers.age.max                                               # 18
```

# Test Coverage
```python
➜  linqit git:(master) ✗ coverage report                    
Name                  Stmts   Miss  Cover
-----------------------------------------
linqit/__init__.py        2      0   100%
linqit/linq_list.py     101     11    89%
tests/__init__.py         0      0   100%
tests/test_list.py      203      0   100%
-----------------------------------------
TOTAL                   306     11    96%
```
