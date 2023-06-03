Prf Module - Reading and Processing Stella-prf files
====================================================

During a Stella, a <run_name.prf> binary file is typically produced, storing
detailed information for a number of snapshots. The frequency of dumps to the
prf file is controlled by the `NOUT` parameter in the `.dat` strad/run
configuration file. In the prf binary file, in particular, detailed information
about the radiation field is stored.

The main class of the prf module is the prf_reader class, which parses a
prf-binary file.

Prf_reader and prf_snapshot_reader classes
------------------------------------------

To read a Stella prf-binary file, create an instance of the
:class:`~stella.prf.prf_reader`. Some information, such as number of frequency
bins  (obtained from the .inc files which were used in the Stella compilation
process) must be provided by the keyword arguments during the initialisation
(consult :class:`~stella.prf.prf_reader`). If wrong values are provided, the
reading process will fail. 

The reading procedure is called already during the initialisation process. It
stores each snapshot it encounters in a separate
:class:`~stella.prf.prf_snapshot_reader` object. These snapshots may then be
accessed via the snapshots attribute of the prf_reader.::

    import stella.prf as prf

    prfdat = prf.prf_reader("model.prf")

    #access the first snapshot and read its time
    prfdat.snapshots[0].t

Consult :class:`~stella.prf.prf_snapshot_reader` for an overview of the
quantities stored in a snapshot object. Their nomenclature is adopted from
Stella, in particular from stradio.trf. For some of the most important
quantities, easy access methods are provided (see next section)

Easy Access of Physical quantities
----------------------------------

Once the prf file has been parsed, accessing some important physical quantities
is wrapped via :class:`~stella.prf.prf_quantity` instances:

For example, after parsing, the prf_reader will have prf_quantity instances to
easily access the mean intensity and the flux of the radiation field::

    import stella.prf as prf

    prfdat = prf.prf_reader("model.prf")

    # access the mean intensity of the first snapshot
    prfdat.J.acess(0)

    # access the mean intensity of the snapshot which is closest to t = 2d
    prfdat.J.time(2)

    # access the mean intenisty of the snapshot with Nstep closest to cycle = 2700
    prfdat.J.cycle(2700)

As shown in the above example, three different modes of accessing the data are
provided, either by the index of the snapshot, using the timestamp or the cycle
number of the snapshot.

The following quantities may be accessed in a similar fashion
  - radiation field mean intensity: prfdat.J; returns a 2D-numpy.array
  - radiation field flux: prfdat.H; returns a 2D-numpy.array
