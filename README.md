# presearch
A python program syntactically query Python source code

# Instalation
1. Clone the repository by running `git clone https://github.com/dignissimus/presearch`
2. Install the requirements using `pip install -r requirements.txt`

# Usage
Currently the program can be run by executing `python -m presearch`
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
## Finding files that import the `ast`
The following query matches files that import the `ast` library
```python
from presearch.query import MatchQuery

# Matches files that import the `ast` library
query = MatchQuery(lambda module: module.imports("ast"))
```
#
