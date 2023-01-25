# For the introduction (first lecture)

We will fill up the notebook in the folder `notebooks`.
It simply requires numpy: you can either install it "globally":

```bash
python3 -m pip install numpy
```

or create a virtualenv and install it

```bash
virtualenv dev_env
source dev_env/bin/activate
python3 -m pip install numpy
```
# A quantum circuit simulation library

The code is already packaged. First create and activate a virtualenv :
```bash
virtualenv dev_env
source dev_env/bin/activate
```
Then install the package in place (dirty but efficient):
```bash
python setup.py install -e .
```

You should then be able to run the tests (that will fail, all good):
```bash
python -m pytest tests/testing.py
```

# Development

We will develop (at least) three simulators, each in its own file (under `src/qps`)

I strongly recommend to use vscode :)
