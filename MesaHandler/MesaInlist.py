import os
from shutil import copyfile
from MesaHandler import MesaAccess


class MesaInlist:
    """ Changes the inlist settings of a file with a given name.

    Alternatively, it creates a list of all the inlists in the
    current directory, which can be used to iteratetively edit
    all inlists at once.

    Attributes:
        inlist_name (str): Inlist filename
        inlists (list):  List of all the inlists in the directory
        inlist (obj): The MesaAccess object that is used to manipulate
                      the inlists.

    To-do: Change this to work with setting 'extra_star_job_inlist1_name
    """
    def __init__(self):
        self.inlist_name = ''
        self.inlists = ([fname for fname in os.listdir()
                        if(fname.startswith('inlist') and
                        fname != 'inlist' and 'pgstar' not in fname)])

    def prepare_edit(self, inlist_name='inlist'):
        """ Creates the MesaAccess object that can be used to edit an inlist.

        Args:
        inlist_name (str): Filename of the inlist to be edited
        """
        self.inlist_name = inlist_name
        if(os.path.isfile('inlist')):
            os.remove('inlist')
        copyfile(self.inlist_name, 'inlist')
        self.inlist = MesaAccess()

    def finish_edit(self):
        """ Finalizes the editing process by replacing the original file """
        os.replace('inlist', self.inlist_name)

    @staticmethod
    def get_X(self, Z):
        """ Calculates the hydrogen fraction given
            a heavy-element fraction Z and assuming protosolar
            composition.

        Args:
            Z (float): Heavy-element mass fraction

        Returns:
            X (float): Hydrogen mass fraction

        """
        yproto = 0.275  # protosolar helium abundance
        xproto = 0.705  # protosolar hydrogen abundance
        eta = yproto / xproto

        X = (1 - Z) / (1 + eta)
        return X

    @staticmethod
    def get_Y(self, Z):
        """ Calculates the helium fraction given
            a heavy-element fraction Z and assuming protosolar
            composition.

        Args:
            Z (float): Heavy-element mass fraction

        Returns:
            Y (float): Helium mass fraction
        """
        X = self.get_X(Z)
        return (round(1 - Z - X, 3))
