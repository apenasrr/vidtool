=======
vidtool
=======


.. image:: https://img.shields.io/pypi/v/vidtool.svg
        :target: https://pypi.python.org/pypi/vidtool

.. image:: https://readthedocs.org/projects/vidtool/badge/?version=latest
        :target: https://vidtool.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


Smart optimization and join video files with minimum reencode process


* Free software: MIT license
* Documentation: https://vidtool.readthedocs.io.


Features
--------

* Homogenize resolutions and codecs from filling in spreadsheet
* Make turbo join, 400 times faster than common join
* Join can contain transition effect self-adapted for any video resolution
* Join process could respect:
    * Defined maximum sized per file, generating ordered video blocks, automatically split videos larger than the defined maximum size
    * Personal grouping criteria, like modules for video course
    * Transition effect auto adapted to the videos resolutions
* Works with video .mp4, .webm, .avi, .ts, .vob, .mov, .mkv, .wmv and more
* Require ffmpeg enabled on path system variables

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
