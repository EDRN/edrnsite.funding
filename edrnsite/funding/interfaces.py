# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''EDRN funding opportunities: interfaces.
'''

from zope.interface import Interface
from zope import schema
from zope.container.constraints import contains
from edrnsite.funding import ProjectMessageFactory as _
from Products.ATContentTypes.interface import IATFolder

class IFundingFolder(IATFolder):
    '''Funding Folder.'''
    contains('edrnsite.funding.interfaces.IFundingOpportunity')
    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Descriptive name of this folder.'),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A short summary of this folder.'),
        required=False,
    )

class IFundingOpportunity(IATFolder):
    '''Funding Opportunity.'''
    contains('edrnsite.funding.interfaces.IAnnouncement')
    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Title of the opportunity.'),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A short summary of the opportunity.'),
        required=False,
    )
    opportunityType = schema.TextLine(
        title=_(u'Opportunity Type'),
        description=_(u'The kind of opportunity being made available'),
        required=True,
    )
    reissuable = schema.Bool(
        title=_(u'Reissuable'),
        description=_(u'True if this funding opportunity may be reissued, false otherwise.'),
        required=False,
    )
    def getClosingDate():
        '''Get when this opportunity closes based on its announcements, if any.'''
    

class IAnnouncement(Interface):
    '''Announcement.'''
    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Title of the announcement.'),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A short summary of the announcement.'),
        required=False,
    )
    announcementLink = schema.TextLine(
        title=_(u'Announcement Link'),
        description=_(u'A hyperlink URL to the actual official announcement.'),
        required=True,
    )
    idNum = schema.TextLine(
        title=_(u'ID Number'),
        description=_(u'Official identification number of the announcement.'),
        required=True,
    )
    releaseDate = schema.Datetime(
        title=_(u'Release Date'),
        description=_(u'Date when this announcement was released.'),
        required=True,
    )
    closingDate = schema.Datetime(
        title=_(u'Closing Date'),
        description=_(u'Date when applications close.'),
        required=True,
    )
    loiDates = schema.Text(
        title=_(u'Letters-of-Intent Dates'),
        description=_(u'Dates when letters-of-intent for this announcement are due, in the ISO format YYYY-MM-DD, one per line.'),
        required=False,
    )
    appReceiptDates = schema.Text(
        title=_(u'Application Receipt Dates'),
        description=_(u'Dates when applications must be received, in the ISO format YYYY-MM-DD, one per line.'),
        required=False,
    )

