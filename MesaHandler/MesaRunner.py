# Runs MESA using the desired inlists
import os
import sys
import glob
import subprocess
import datetime
from shutil import copy2, move
from distutils.dir_util import copy_tree
from MesaHandler import MesaAccess


class MesaRunner:
    """ Runs MESA using the desired inlist.

    It is also capable of various other useful manipulations.

    Attributes:
        inlist (str): Name of the inlist used in the run.
        last_inlist (str): Name of the last inlist to run.
        pgstar (bool): Enable/disable pgstar.
        pause (bool): Enable/disable waiting for user input at the end.
        check (bool): Checks whether the model successfully finished.
        model_name (str): Output model name.
        profile_name (str): Output profile name.
    """

    def __init__(self, inlist, pgstar=True, pause=True):
        """ __init__ method

        Args:
            inlist (str): Name of the inlist used in the run
            pgstar (bool): Enable/disable pgstar.
            pause (bool): Enable/disable waiting for user input at the end.
        """
        self.inlist = inlist
        self.last_inlist = inlist
        self.pause = pause
        self.pgstar = pgstar
        self.check = False
        self.model_name = ''
        self.profile_name = ''

    def run(self):
        """ Runs either a single inlist or a list of inlists. """
        if(isinstance(self.inlist, list)):
            for item in self.inlist:
                self.last_inlist = item
                self.run_support(item)
                if not(self.check):
                    print('Aborting since previous inlist failed to run')
                    raise SystemExit()

            print('Finished running all inlists')
        else:
            self.run_support(self.inlist)

    def run_support(self, inlist):
        """ Helper function for running MESA.

        args:
            inlist (str): Inlist to be run.
        """
        self.remove_file('inlist')
        self.remove_file('restart_photo')
        copy2(inlist, 'inlist')
        ma = MesaAccess()
        self.model_name = ma['save_model_filename']
        self.profile_name = ma['filename_for_profile_when_terminate']

        if(self.pause):
            ma['pause_before_terminate'] = True
        else:
            ma['pause_before_terminate'] = False

        if(self.pgstar):
            ma['pgstar_flag'] = True
        else:
            ma['pgstar_flag'] = False

        self.remove_file(self.model_name)
        start_time = datetime.datetime.now()
        if(os.path.isfile('star')):
            print('Running', inlist)
            subprocess.call('./star')
        else:
            print('You need to build star first!')
            sys.exit()
        end_time = datetime.datetime.now()
        run_time = end_time - start_time

        if(os.path.isfile(self.model_name)):
            print(42 * '%')
            print('Evolving the star took:', run_time)
            print(42 * '%')
            self.check = True
        else:
            print(42 * '%')
            print('Failed to run', self.inlist)
            print(42 * '%')
            self.check = False

    def restart(self, photo):
        """ Restarts the run from the given photo.

        Args:
            photo (str): Photo to run from in the photos directory.
        """
        if not(os.path.isfile('inlist')):
            copy2(self.last_inlist, 'inlist')

        photo_path = os.path.join('photos', photo)
        if(os.path.isfile(photo_path)):
            subprocess.call(['./re', photo])
        else:
            print(photo_path, 'not found')

    def restart_latest(self):
        """ Restarts the run from the latest photo. """
        old_path = os.getcwd()
        new_path = os.path.expanduser('photos')
        os.chdir(new_path)
        latest_file = max(glob.iglob('*'), key=os.path.getctime)
        os.chdir(old_path)

        if not(os.path.isfile('inlist')):
            copy2(self.last_inlist, 'inlist')

        if(latest_file):
            print('Restarting with photo', latest_file)
            subprocess.call(['./re', latest_file])
        else:
            print('No photo found.')

    def copy_logs(self, dir_name):
        """ Save the current logs and profile.

        Args:
            dir_name (str): Destination to copy the logs to.
        """
        if not(self.profile_name):
            ma = MesaAccess()
            self.profile_name = ma['filename_for_profile_when_terminate']

        dst = os.path.join(dir_name, self.profile_name)
        copy_tree('LOGS', dir_name)
        if(os.path.isfile(self.profile_name)):
            move(self.profile_name, dst)

    @staticmethod
    def make():
        """ Builds the star executable. """
        print('Building star')
        subprocess.call('./mk')

    @staticmethod
    def clean_logs():
        """ Cleans the photos, png and logs directories. """
        dir_name = 'png'
        items = os.listdir(dir_name)
        for item in items:
            if(item.endswith('.png')):
                os.remove(os.path.join(dir_name, item))

        dir_name = 'LOGS'
        items = os.listdir(dir_name)
        for item in items:
            if(item.endswith('.data')):
                os.remove(os.path.join(dir_name, item))

        dir_name = 'photos'
        items = os.listdir(dir_name)
        for item in items:
            os.remove(os.path.join(dir_name, item))

    @staticmethod
    def remove_file(file_name):
        """ Safely removes a file.

        Args:
            file_name (str): File to delete.
        """
        if(os.path.isfile(file_name)):
            os.remove(file_name)
