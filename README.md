# Linqit!
Extends python's list builtin with fun, robust functionality - .NET's Language Integrated Queries (Linq) and more.<br>
Write clean code with powerful syntax.<br><br>
```shell script
pip install linqit
```
Stop using loops, complex conditions, list comperhension and filters.<br>
Doesn't it looks better? <br>
```python
from linqit import List


programmers = List()
Avi = type('Avi', (), {})

# Go ahead and fill the list with whatever you want... like a list of <Programmer> objects.

# Then play:
last_hot_pizza_slice = programmers.where(lambda e:e.experience > 15)
                      .except_for(elon_musk)
                      .of_type(Avi)
                      .take(3) # [<Avi>, <Avi>, <Avi>]
                      .select(lambda avi:avi.lunch) # [<Pizza>, <Pizza>, <Pizza>]
                      .where(lambda p:p.is_hot() and p.origin != 'Pizza Hut').
                      .last() # <Pizza>
                      .slices.last() # <PizzaSlice>
                      
# What do you think?
```

We all use multiple aggregations in our code, while multiple filters/comprehentions are not pythonic at all.<br>
The whole idea is is to use it for nested, multiple filters/modifications :).<br>
Some of the methods might look rediculous for a single call, comparing to the regular python syntax.<br>
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
        return 'Person(name="{}", age={})'.format(self.name, self.age)


# Creating a list of people
avi, bill, bob, harry = Person('Avi', 23), Person('Bill', 41), Person('Bob', 77), Person('Harry', 55)

people = List(avi, bill, bob, harry)
```

## Use LINQ selections, write cleaner code
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
