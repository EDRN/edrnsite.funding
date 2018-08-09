# encoding: utf-8
# Copyright 2009–2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''EDRN funding opportunities: test the setup of this package.
'''

import unittest
from edrnsite.funding.testing import EDRNSITE_FUNDING_INTEGRATION_TESTING
from Products.CMFCore.utils import getToolByName

class SetupTest(unittest.TestCase):
    '''Unit tests the setup of this package.'''
    layer = EDRNSITE_FUNDING_INTEGRATION_TESTING
    def setUp(self):
        super(SetupTest, self).setUp()
        self.portal = self.layer['portal']
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
    def testDiscussion(self):
        '''Ensure discussion is off (CA-1229)'''
        types = getToolByName(self.portal, 'portal_types')
        for typeName in ('Announcement', 'Funding Folder', 'Funding Opportunity'):
            self.failIf(types[typeName].allow_discussion, 'Type "%s" allows discussion, but should not' % typeName)



def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
