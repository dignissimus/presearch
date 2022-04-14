# Presearch
A tool to syntactically query Python source code

# Installation
This project can be installed through pip by running `pip install presearch`


# Usage
Once installed, the program can be run by executing `presearch`
```bash
usage: presearch [-h] --file FILE directory

Syntactically query python source code

positional arguments:
  directory             The directory containing the source code to query

options:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  The file containing query to execute
```

# Examples
## Finding files that import the `ast` library
The following query matches files that import the `ast` library
```python
from presearch.query import MatchQuery

# Matches files that import the `ast` library
query = MatchQuery(lambda module: module.imports("ast"))
```
## Finding classes that explicitly define `__init__`
The following query searches for class definitions, then reports back with the number of those class definitions that explicitly define `__init__`.
```python
from presearch.tree import ClassDef
from presearch.query import Domain, StatisticalQuery

# Calculates the percentage of classes that define `__init__`
query = StatisticalQuery(
    lambda klass: klass.defines("__init__"),
    domain=Domain(ClassDef),
    domain_description="class definitions",
    match_description="classes that explicitly define __init__",
)
```
## Finding `__init__` definitions that directly store all of their non-self arguments as attributes
This query finds all classes that define `__init__` then reports the number of `__init__` definitions that assign all of its arguments to attributes (i.e. run `self.argument = argument` for all arguments)
```python
from presearch.query import Domain, StatisticalQuery
from presearch.constraints import ContainsMethodDefinition
from presearch.tree import ClassDef, Self


def assigns_all_arguments_to_attributes(class_def):
    init_function = class_def.function("__init__")
    for argument in init_function.non_self_arguments:
        if not init_function.contains(Self.attribute(argument.name).assign(argument)):
            return False

    return True


# Calculates the proportion of class `__init__` definitions
# that assign all their non-self arguments as attributes
query = StatisticalQuery(
    assigns_all_arguments_to_attributes,
    domain=Domain(ClassDef, constraints=[ContainsMethodDefinition("__init__")]),
    domain_description="classes defining __init__",
    match_description="classes whose __init__ functions assigned all non-self arguments as attributes",
)
```
# Installing from source
This project can be installed from the source code
1. Clone the repository by running `git clone https://github.com/dignissimus/presearch`
2. Install using `pip install .`
