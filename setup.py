from distutils.core import setup
from os import path

long_desc = open(path.join(path.dirname(__file__), "README.markdown"), "U").read()

setup(name="pyg2fa", version="1.1",
      url="https://github.com/thejeshgn/pyg2fa",
      author="Thejesh GN",
      author_email="i@thejeshgn.com",
      description="Google two factor Authentication for Python",
      long_description=long_desc,
      py_modules=["pyg2fa"])
