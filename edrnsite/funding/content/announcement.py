# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Announcement of a funding opportunity.'''

from edrnsite.funding.config import PROJECTNAME
from edrnsite.funding.interfaces import IAnnouncement
from Products.Archetypes import atapi
from Products.Archetypes.interfaces import IObjectPostValidation
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from zope.interface import implements
from zope.component import adapts
from Products.ATContentTypes.content import schemata, base
from edrnsite.funding import ProjectMessageFactory as _
from DateTime import DateTime
import re
_dateRegex = re.compile(r'^[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}$')

AnnouncementSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
    atapi.StringField(
        'announcementLink',
        required=True,
        storage=atapi.AnnotationStorage(),
        validators=('isURL',),
        default='http://',
        widget=atapi.StringWidget(
            label=_(u'Announcement Link'),
            description=_(u'A hyperlink URL to the actual official announcement.'),
        ),
    ),
    atapi.StringField(
        'idNum',
        required=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'ID Number'),
            description=_(u'Official identification number of the announcement.'),
        ),
    ),
    atapi.DateTimeField(
        'releaseDate',
        required=True,
        storage=atapi.AnnotationStorage(),
        default_method='getCurrentDate',
        widget=atapi.CalendarWidget(
            label=_(u'Release Date'),
            description=_(u'Date when this announcement was released.'),
            show_hm=False,
        ),
    ),
    atapi.DateTimeField(
        'closingDate',
        required=True,
        storage=atapi.AnnotationStorage(),
        default_method='getCurrentDate',
        widget=atapi.CalendarWidget(
            label=_(u'Closing Date'),
            description=_(u'Date when applications close.'),
            show_hm=False,
        ),
    ),
    atapi.LinesField(
        'loiDates',
        required=False,
        storage=atapi.AnnotationStorage(),
        widget=atapi.LinesWidget(
            label=_(u'Letters-of-Intent Dates'),
            description=_(u'Dates when letters-of-intent for this announcement are due, in the ISO format YYYY-MM-DD,' \
                + ' one per line.'),
        ),
    ),
    atapi.LinesField(
        'appReceiptDates',
        required=False,
        storage=atapi.AnnotationStorage(),
        widget=atapi.LinesWidget(
            label=_(u'Application Receipt Dates'),
            description=_(u'Dates when applications must be received, in the ISO format YYYY-MM-DD, one per line.'),
        ),
    ),
))
AnnouncementSchema['title'].storage = atapi.AnnotationStorage()
AnnouncementSchema['description'].storage = atapi.AnnotationStorage()

finalizeATCTSchema(AnnouncementSchema, folderish=False, moveDiscussion=False)

class Announcement(base.ATCTContent):
    '''Funding Opportunity.'''
    implements(IAnnouncement)
    portal_type               = 'Announcement'
    _at_rename_after_creation = True
    schema                    = AnnouncementSchema
    title                     = atapi.ATFieldProperty('title')
    description               = atapi.ATFieldProperty('description')
    announcementLink          = atapi.ATFieldProperty('announcementLink')
    idNum                     = atapi.ATFieldProperty('idNum')
    releaseDate               = atapi.ATDateTimeFieldProperty('releaseDate')
    closingDate               = atapi.ATDateTimeFieldProperty('closingDate')
    loiDates                  = atapi.ATFieldProperty('loiDates')
    appReceiptDates           = atapi.ATFieldProperty('appReceiptDates')
    def getCurrentDate(self):
        return DateTime()

atapi.registerType(Announcement, PROJECTNAME)

class MultipleDateValidator(object):
    implements(IObjectPostValidation)
    adapts(IAnnouncement)
    def __init__(self, context):
        self.context = context
    def __call__(self, request):
        for fieldName in ('loiDates', 'appReceiptDates'):
            value = request.form.get(fieldName, request.get(fieldName, None))
            if value is not None:
                for line in value:
                    line = line.strip()
                    if not _dateRegex.match(line):
                        return {fieldName: _(u'You must enter dates in the YYYY-MM-DD format, one per line.')}
        return None
    

