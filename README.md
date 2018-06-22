# Linqit !
A List-like type with robust functionality.<br>
Extents the builtin list with .NET's Language Intagrated Queries (Linq) and more.<br>
Develop with clean code using powerful syntax, instead of messy loops and conditions.


## LINQ selections:
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

# LYNQ Selections
old_people = people.where(lambda p: p.age > 40)                 [<Person name="Bill" age="41">, <Person name="Bob" age="77">, <Person name="Harry" age="55">]
old_people.first()                                              # <Person name="Bill" age="41">
old_people.last()                                               # <Person name="Harry" age="55">
old_people.any(lambda p: p.name.lower().startswith('b'))        # True
old_people.where(lambda p: p.age == 55)                         # [<Person name="Harry" age="55">]
old_people.skip(3).any()                                        # False
old_people.skip(2).first()                                      # <Person name="Harry" age="55">

# Adding people to the list in various ways
new_kids_in_town = [Person('Chris', 18), Person('Danny', 16)]
people = people.concat(new_kids_in_town)
people.append(Person('John', 17))

# More selections
teenagers = people.where(lambda p: 20 >= p.age >= 13)
teenagers_names = ['Chris', 'Danny', 'John']                    # ['Chris', 'Danny', 'John']
teenagers_average_age = teenagers.age.avg                       # 17
danny = teenagers.first(lambda t: t.name == 'Danny')            # <Person name="Danny" age="16">


oldest_teen = teenagers.last()                                  # <Person name="Chris" age="18">
names = people.name                                             # ['Avi', 'Bill', 'Bob', 'Harry', 'Chris', 'John']
ages = people.age                                               # [23, 41, 77, 55, 18, 17]
```