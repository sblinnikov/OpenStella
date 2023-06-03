# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
#  File Name : dep.py
#
#  Purpose : Provides Reading and Processing tools for Stella *.dep files
#
#  Creation Date : 25-11-2015
#
#  Last Modified : Wed 24 Aug 2016 15:58:36 CEST
#
#  Created By : U.M.Noebauer
#
# _._._._._._._._._._._._._._._._._._._._._.
"""This modules provides a simple reader to parse *.dep files produced by
Stella. These files primarily store the total gamma deposition during the
calculation.

Notes
----

The deposition files only store information about the amount of
gamma-deposition. If this is to be linked to actual times, the corresponding
*.flx file has to be read as well. See :py:mod:`~stella.flx`.
"""
import struct
import numpy as np
import astropy.units as units
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class dep_record_reader(object):
    """Read a single fortran record of the dep file.

    The information about the gamma deposition is stored in chunks. Each data
    block contains ~900 entries and is written out as fortran record. This
    class parses exactly one such record.

    Notes:
    -----
    The following file record format is expected:
    - i4, Nrecord: record length in byte
    - i4, Lsave: number of entries in the block
    - Lsave x f8, Depos: gamma-deposition
    - i4, Nrecord: record length in byte

    The reader is based upon the node ``_stinfodepos`` in [1]_

    .. [1] stella/strc/stradio.trf

    Parameters
    ---------
    fstream : file stream object
        reference to the dep file object (must have been open in the read
        binary mode)

    Attributes
    ----------
    Nrec : int
        record size in byte
    Lsave : int
        number of data points in record
    Depos : astropy.units.Quantity array
        gamma deposition (array length = Lsave)

    """
    def __init__(self, fstream):

        self.fstream = fstream

        self.read_record()

    def read_record(self):
        """Parse record

        """

        self.Nrec = struct.unpack("i", self.fstream.read(4))[0]
        self.Lsave = struct.unpack("i", self.fstream.read(4))[0]
        self.Depos = (np.array(struct.unpack("{:d}d".format(self.Lsave),
                                             self.fstream.read(self.Lsave * 8)))
                      * 1e50 * units.erg / units.s)

        try:
            assert(self.Nrec == struct.unpack("i", self.fstream.read(4))[0])
        except AssertionError:
            logger.exception("Mismatch in record length at start and end stamps")
            raise IOError
        logger.info("Record with Lsave={:d} successfully read".format(self.Lsave))

class dep_reader(object):
    """Parse a complete *.dep file produced by Stella

    All records contained in the *.dep file are read and stored.

    Parameters
    ----------
    fname : str
        name of *.dep file

    Attributes
    ----------
    fstream : file object
        reference to file object holding the dep file
    records : list of dep_record_reader
        list holding the different records (stored in dep_record_reader
        objects)
    Depos : numpy array
        deposition array, holding the information of all records

    """
    def __init__(self, fname):

        self.fname = fname
        self.fstream = open(fname, "rb")

        self.records = []
        self.read_dep_file()
        self.prep_easy_access()

    def read_dep_file(self):
        """Read the *.dep files by successively parsing the records

        Notes
        -----
        The awkward while loop construction catches empty records, which are
        often at the end of Stella binary files.

        """

        while 1:
            fpos = self.fstream.tell()
            buffer = self.fstream.read(4)
            if buffer == "":
                #EOF
                logger.info("EOF triggered")
                break
            else:
                if struct.unpack("i", buffer)[0] == 4:
                    #last record with Lsave = 0
                    logging.info("Last empty, record found: stopping")
                    break
                else:
                    self.fstream.seek(fpos)
            self.records.append(dep_record_reader(self.fstream))
            logging.info("Now at stream position {:d}".format(self.fstream.tell()))

        self.fstream.close()

    def prep_easy_access(self):
        """Prepares deposition array containing the information of all arrays

        """

        self.Depos = np.empty(0)

        for rec in self.records:
            self.Depos = np.append(self.Depos, rec.Depos.value)

        self.Depos = self.Depos * rec.Depos.unit

