#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from distutils.core import setup, Extension
import numpy as np

setup(
      name = 'EELS',
      version = '1.0',
	    author = "Sindre R. Bilden",
	    author_email = "s.r.bilden@fys.uio.no",
	    description = ("A collection of functions for simulating EELS"),
    	packages=['EELS'],

      )


ext_modules = [ Extension('_spectrum', sources = ['./EELS/_spectrum/spectrum.c']) ]

setup(
      name = '_spectrum',
      version = '1.0',
	    author = "Sindre R. Bilden",
	    author_email = "s.r.bilden@fys.uio.no",
	    description = ("A C-extended code for calulationg EEL-spectra"),
      ext_modules = ext_modules
      )

