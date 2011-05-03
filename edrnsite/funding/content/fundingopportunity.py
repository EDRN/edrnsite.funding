# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Funding opportunity.'''

from edrnsite.funding.config import PROJECTNAME
from edrnsite.funding.interfaces import IFundingOpportunity, IAnnouncement
from Products.Archetypes import atapi
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from zope.interface import implements, directlyProvides
from Products.ATContentTypes.content import folder
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName
from edrnsite.funding import ProjectMessageFactory as _
import datetime, pytz
_farFuture = datetime.datetime(datetime.MAXYEAR, 12, 31, tzinfo=pytz.utc)

_opportunityTypes = (
    (_(u'Request for Application'), u'RFA'),
    (_(u'Program Announcement'), u'PA'),
    (_(u'Notice'), u'Notice'),
)

FundingOpportunitySchema = folder.ATFolderSchema.copy() + atapi.Schema((
    atapi.StringField(
        'opportunityType',
        required=True,
        enforceVocabulary=True,
        vocabulary_display_path_bound=-1,
        vocabulary_factory=u'edrnsite.funding.OpportunityTypeVocabulary',
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            label=_(u'Opportunity Type'),
            description=_(u'The kind of opportunity being made available'),
        ),
    ),
    atapi.BooleanField(
        'reissuable',
        required=False,
        storage=atapi.AnnotationStorage(),
        widget=atapi.BooleanWidget(
            label=_(u'Reissuable'),
            description=_(u'True if this funding opportunity may be reissued, false otherwise.'),
        ),
    ),
))
FundingOpportunitySchema['title'].storage = atapi.AnnotationStorage()
FundingOpportunitySchema['description'].storage = atapi.AnnotationStorage()

finalizeATCTSchema(FundingOpportunitySchema, folderish=True, moveDiscussion=False)

class FundingOpportunity(folder.ATFolder):
    '''Funding Opportunity.'''
    implements(IFundingOpportunity)
    portal_type               = 'Funding Opportunity'
    _at_rename_after_creation = True
    schema                    = FundingOpportunitySchema
    title                     = atapi.ATFieldProperty('title')
    description               = atapi.ATFieldProperty('description')
    opportunityType           = atapi.ATFieldProperty('opportunityType')
    reissuable                = atapi.ATFieldProperty('reissuable')
    def getClosingDate(self):
        try:
            catalog = getToolByName(self, 'portal_catalog')
            results = catalog(
                object_provides=IAnnouncement.__identifier__,
                path=dict(query='/'.join(self.getPhysicalPath()), depth=1),
                sort_limit=1,
                sort_on='closingDate',
                sort_order='reverse'
            )[:1]
            if len(results) == 0:
                return _farFuture
            return results[0].closingDate
        except AttributeError:
            return _farFuture

atapi.registerType(FundingOpportunity, PROJECTNAME)

def OpportunityTypeVocabulary(context):
    '''Vocabualry factory for types of funding opportunities.'''
    return SimpleVocabulary.fromItems(_opportunityTypes)
    
directlyProvides(OpportunityTypeVocabulary, IVocabularyFactory)