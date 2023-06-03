# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
#  File Name : elements.py
#
#  Purpose : utility classes and functions to handle abundances
#
#  Creation Date : 04-12-2015
#
#  Last Modified : Fri 04 Dec 2015 11:55:17 CET
#
#  Created By : U.M.Noebauer
#
# _._._._._._._._._._._._._._._._._._._._._.
"""Provides a utility class to identify atomic numbers with standard element
labels and vice-versa.

Notes
-----
The original lists and dictionaries have been compiled by P.V.F.Edelmann for
flame_plot.py
"""


class elements_helper(object):
    """Simple class providing dictionaries to identify atomic numbers with
    element labels

    Parameters
    ----------
        None

    Attributes
    ----------
    elements : dict
        dictionary with element labels as keys and corresponding atomic numbers
        as values
    inv_elements : dict
        dictionary with atomic numbers as keys and corresponding element labels
        as values

    """
    def __init__(self):
        self._elements = {'neut': 0, 'h': 1, 'he': 2, 'li': 3, 'be': 4, 'b': 5,
                          'c': 6, 'n': 7, 'o': 8, 'f': 9, 'ne': 10, 'na': 11,
                          'mg': 12, 'al': 13, 'si': 14, 'p': 15, 's': 16,
                          'cl': 17, 'ar': 18, 'k': 19, 'ca': 20, 'sc': 21,
                          'ti': 22, 'v': 23, 'cr': 24, 'mn': 25, 'fe': 26,
                          'co': 27, 'ni': 28, 'cu': 29, 'zn': 30, 'ga': 31,
                          'ge': 32, 'as': 33, 'se': 34, 'br': 35, 'kr': 36,
                          'rb': 37, 'sr': 38, 'y': 39,  'zr': 40, 'nb': 41,
                          'mo': 42, 'tc': 43, 'ru': 44, 'rh': 45, 'pd': 46,
                          'ag': 47, 'cd': 48,
                          }

        self._inv_elements = None
        self.lower()    # set self.elements

    @property
    def inv_elements(self):
        if self._inv_elements is None:
            self._inv_elements = dict([(v, k)
                                       for k, v in self.elements.items()])
        return self._inv_elements

    def capitalize(self):
        """Capitalizes all element labels"""

        self._inv_elements = None

        self.elements = {}

        for key, value in self._elements.items():
            self.elements[key.capitalize()] = value

    def lower(self):
        """Lowers all element labels"""

        self._inv_elements = None
        self.elements = self._elements.copy()
