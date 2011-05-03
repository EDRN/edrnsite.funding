# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Funding folder.'''

from edrnsite.funding.config import PROJECTNAME
from edrnsite.funding.interfaces import IFundingFolder
from Products.Archetypes import atapi
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from zope.interface import implements
from Products.ATContentTypes.content import folder

FundingFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    # No other fields
))
FundingFolderSchema['title'].storage = atapi.AnnotationStorage()
FundingFolderSchema['description'].storage = atapi.AnnotationStorage()

finalizeATCTSchema(FundingFolderSchema, folderish=True, moveDiscussion=False)

class FundingFolder(folder.ATFolder):
    '''Funding folder which contains funding opportunities.'''
    implements(IFundingFolder)
    portal_type               = 'Funding Folder'
    _at_rename_after_creation = True
    schema                    = FundingFolderSchema
    title                     = atapi.ATFieldProperty('title')
    description               = atapi.ATFieldProperty('description')

atapi.registerType(FundingFolder, PROJECTNAME)
