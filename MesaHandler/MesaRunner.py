# Runs MESA using the desired inlists
import os
import sys
import glob
import subprocess
import datetime
import numpy as np
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
        self.model_name = ''
        self.profile_name = ''

        self.convergence = False
        if(isinstance(self.inlist, list)):
            self.summary = np.zeros_like(self.inlist, dtype=bool)
        else:
            self.summary = False

    def run(self):
        """ Runs either a single inlist or a list of inlists. """
        if(isinstance(self.inlist, list)):
            for ind, item in self.inlist:
                self.last_inlist = item
                self.run_support(item)
                self.summary[ind] = self.convergence
                if not(self.convergence):
                    print('Aborting since previous inlist failed to run')
                    raise SystemExit()

            print('Finished running inlists', self.inlist)
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
        run_time = str(end_time - start_time)
        micro_index = run_time.find('.')

        if(os.path.isfile(self.model_name)):
            print(42 * '%')
            print('Evolving the star took: {} \
                   h:mm:ss'.format(run_time[:micro_index]))
            print(42 * '%')
            self.convergence = True
        else:
            print(42 * '%')
            print('Failed to run', inlist,
                  'after {} h:mm:ss'.format(run_time[:micro_index]))
            print(42 * '%')
            self.convergence = False

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
    def cleanup(keep_png=False, keep_logs=False, keep_photos=True):
        """ Cleans the photos, png and logs directories.

        Args:
            keep_png (bool): Store/delete the png directory.
            keep_logs (bool): Store/delete the logs directory.
            keep_photos (bool): Store/delete the photo directory.
        """
        if not(keep_png):
            dir_name = 'png'
            if(os.path.isdir(dir_name)):
                items = os.listdir(dir_name)
                for item in items:
                    if(item.endswith('.png')):
                        os.remove(os.path.join(dir_name, item))

        if not(keep_logs):
            dir_name = 'LOGS'
            if(os.path.isdir(dir_name)):
                items = os.listdir(dir_name)
                for item in items:
                    if(item.endswith('.data')):
                        os.remove(os.path.join(dir_name, item))

        if not(keep_photos):
            dir_name = 'photos'
            if(os.path.isdir(dir_name)):
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
