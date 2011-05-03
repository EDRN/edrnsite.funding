# encoding: utf-8
# Copyright 2008 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
Testing base code.
'''

from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

# Traditional Products we have to load manually for test cases:
# (none at this time)

@onsetup
def setupedrnsitefunding():
    '''Set up additional products required.'''
    fiveconfigure.debug_mode = True
    import edrnsite.funding
    zcml.load_config('configure.zcml', edrnsite.funding)
    fiveconfigure.debug_mode = False
    ztc.installPackage('edrnsite.funding')

setupedrnsitefunding()
ptc.setupPloneSite(products=['edrnsite.funding'])

class BaseTestCase(ptc.PloneTestCase):
    '''Base for tests in this package.'''
    pass
    

class FunctionalBaseTestCase(ptc.FunctionalTestCase):
    '''Base class for functional (doc-)tests.'''
    pass
    

