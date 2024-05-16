# README for Python Setup

## Getting Started
### Package Mgmt
- Pip is the preferred Python Package Manager
- Homebrew will work for some stuff, but Pip is far more dominate in community
- Using Pip requires using a Python Virtual Env:
  `python3 -m venv .venv`

- Then activating that env:
  `source .venv/bin/activate`

- Finally installing pip:
- Acquire from https://github.com/pypa/get-pip
- Run `python get-pip.py`

### Virtualization
Note that enabled by step 1 in Package Mgmt is environmental virutalization
A common tactic is to use pip to maintain environmental packages:
`pip freeze > requirements.txt`
followed by
`pip install -r requirements.txt`
