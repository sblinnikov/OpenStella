Eve Module - Reading and Processing Stelle eve files
====================================================

Prior to any Stella calculation, a set of files describing the initial model
have to be generated. This is commonly performed with the Stella eve tools. The
eve.py module provides a reader for the most important file generated in this
process, namely the <run_name.rho> file.

Everho_reader class
-------------------

To read a Stella-Eve '.rho' file, create an instance of the
:class:`~stella.eve.everho_reader` class. Upon creation, the rho file will be
parsed. The different quantities may then be accesses through the class
attributes. The following example illustrates this:::

    import stella.eve as eve

    model = eve.eve_rhoreader("model.rho")

    #access the logarithmic density of the model
    model.lg_rho


To get an overview of the different attributes storing the physical quantities
of the rho file, use the print_att_info method. It will print out a list of
available attributes:::

    model.print_att_info()

