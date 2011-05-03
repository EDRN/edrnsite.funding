# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
EDRN funding opportunities: test the setup of this package.
'''

import unittest
from edrnsite.funding.tests.base import BaseTestCase
from Products.CMFCore.utils import getToolByName

class TestSetup(BaseTestCase):
    '''Unit tests the setup of this package.'''
    def testCatalogIndexes(self):
        '''Check if indexes are properly installed'''
        catalog = getToolByName(self.portal, 'portal_catalog')
        indexes = catalog.indexes()
        for i in ('closingDate',):
            self.failUnless(i in indexes)
    def testCatalogMetadata(self):
        '''Check if indexed metadata are properly installed'''
        catalog = getToolByName(self.portal, 'portal_catalog')
        metadata = catalog.schema()
        for i in ('closingDate',):
            self.failUnless(i in metadata)
    

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
    
