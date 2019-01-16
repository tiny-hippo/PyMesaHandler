import os
from shutil import copyfile
from MesaHandler import MesaAccess


class MesaInlist(object):
    """ Changes the inlist settings of a file with a given name.

    Alternatively, it creates a list of all the inlists in the
    current directory, which can be used to iteratetively edit
    all inslists at once.

    Attributes:
        inlist_name (str): Inlist filename
        inlists (list):  List of all the inlists in the directory
        inlist (obj): The MesaAccess that is used to manipulate the inlists.
    """
    def __init__(self):
        self.inlist_name = ''
        self.inlists = ([fname for fname in os.listdir()
                        if(fname.startswith('inlist') and
                        fname != 'inlist' and 'pgstar' not in fname)])

    def prepare_edit(self, inlist_name='inlist'):
        """ Creates the MesaAcess object that can be used to edit an inlist.

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
