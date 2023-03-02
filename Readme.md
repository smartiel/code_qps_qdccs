# For the introduction (first lecture)

We will fill up the notebook in the folder `notebooks`.
It simply requires numpy: you can either install it "globally":

```bash
python3 -m pip install numpy opt_einsum networkx
```

or create a virtualenv and install it

```bash
virtualenv dev_env
source dev_env/bin/activate
python3 -m pip install numpy opt_einsum networkx
```


# A quantum circuit simulation library

The code is already packaged. First create and activate a virtualenv :
```bash
virtualenv dev_env
source dev_env/bin/activate
```
Then install the package in place (dirty but efficient):
```bash
python -m pip install -e .
```


# Testing

You can run the tests using the following command line (requires pytest):

```bash
python -m pytest tests/testing.py
```

In order to restrict tests to a single simulator you can use the `-k` option:

```bash
python -m pytest tests/testing.py -k Direct
```

You can cumulate filters. The following line will run test uniform_distrib_n for simulator Direct and restricted to n=3.

```bash
python -m pytest tests/testing.py -k "Direct and uniform_distrib_n and 3"
```





# Development

We will develop (at least) three simulators, each in its own file (under `src/qps`)

I strongly recommend to use vscode :)
