Title: Setting up python for macOS
Date: 2017-01-16 23:36
Category: Python
Tags: atom, python, macOS
Authors: Longwen Ou
Summary: An introduction to my python setup

[Atom](https://atom.io/) is a cross-platform text editor developed by [GitHub](https://github.com/). It is highly comtomizable with support for plug-ins. In this post we'll talk about setting up Atom for Python, Latex and web development.

## Atom settings
My atom settings looks like this:

<img src='/images/atom_theme.jpg' width=70%/>

I use [atom-material-ui](https://atom.io/themes/atom-material-ui) UI theme and the corresponding syntax theme [atom-material-syntax](https://atom.io/themes/atom-material-syntax). I also installed [file-icons](https://atom.io/packages/file-icons) to assign beautiful file extension icons and colors.

## Set up Atom for Python Programming

There are a number of packages for python programming.

* [autocomplete-python](https://atom.io/packages/autocomplete-python): provides autocompletion for Python packages, variables, methods, and functions.

* [linter](https://atom.io/packages/linter): a base linter provider. It provides a top-level API to other packages to visualize errors and other kind-of messages, easily.

* [linter-flake8](https://atom.io/packages/linter-flake8): a flake8 provider for linter. It requires installation of [flake8](https://pypi.python.org/pypi/flake8) python package.

* [linter-pep8](https://atom.io/packages/linter-pep8): provides an interface to pep8. It requires installation of [pep8](https://pypi.python.org/pypi/pep8) python package.

* [python-tools](https://atom.io/packages/python-tools): provides handy tools for developing Python code. It bring feature such as Goto Definition, Select String Contents, etc.

Now you'are ready to have some fun developing Python code with atom. Congrats :-)


Python is a popular programming language. Python comes with macOS. However, it is not recommended
to use the system python for development.

## Installing python on macOS
There are two ways of installing python on macOS. The first way is to install python from source.  
