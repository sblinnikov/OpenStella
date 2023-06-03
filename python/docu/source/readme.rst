Instructions to generate a SPHINX documentation for PyStella
============================================================

Requirements:
------------

  - sphinx (Python autodocumentation generator)
  - numpydoc

HowTo:
------

Generate the documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^

Use the makefile to generate the html documentation:

make html

This generates the documentation, which is then located in build/html

If new modules are added to the packages, the following command should be
invoked inside the ../stella/ directory before the make command is issued:

sphinx-apidoc -f -o ../docu/source/ .

This updates the module list and the API part of the documentation

Extend the documentation
^^^^^^^^^^^^^^^^^^^^^^^^

All new modules should properly documented following the numpydoc style:

https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt

Additional documentation can be added by creating the simple text documents in
the reStructuredText format in the source folder of the docu directory and
adding them to a toctree in any existing .rst file.

http://sphinx-doc.org/rest.html
