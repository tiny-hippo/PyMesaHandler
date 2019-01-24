# PyMesaHandler
PyMesaHandler is a python interface that interacts with MESA by means of manipulating inlists and running the star executable.

This fork is a continuation of the original work found [here](https://github.com/muma7490/PyMesaHandler), 
with (hopefully) useful bugfixes and new features.

## New features
- **Access and update several inlists at once**: The new MesaInlist class allows the user to access and edit an arbitrary amount of inlists at once. This is useful when a parameter should be changed for all the intermediate steps of a model.
- **Python-to-Fortran conversion**: This should be more robust now. In particular, it can now handle the proper conversion of scientifically formatted numbers.

- **Run models with the new MesaRunner class**: MesaRunner has several methods that are useful for running MESA, including evolving models with desired inlists, easy restarting, as well as handling of log files
