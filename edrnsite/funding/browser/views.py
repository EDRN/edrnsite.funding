# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
EDRN Site Funding: views for content types.
'''

from Acquisition import aq_inner
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from edrnsite.funding.interfaces import IAnnouncement, IFundingOpportunity
import datetime, pytz

class BaseView(BrowserView):
    def formatDate(self, date):
        return u'%4d-%02d-%02d' % (date.year, date.month, date.day)


class AnnouncementView(BaseView):
    '''Default view for an Announcement.'''
    __call__ = ViewPageTemplateFile('templates/announcement.pt')
    


class FundingFolderView(BaseView):
    '''Default view for Funding Folder.'''
    __call__ = ViewPageTemplateFile('templates/fundingfolder.pt')

    def getOpportunities(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(
            path=dict(query='/'.join(context.getPhysicalPath()), depth=1),
            object_provides=IFundingOpportunity.__identifier__,
        )
        opportunities = [i.getObject() for i in results]
        opportunities.sort(lambda a, b: cmp(a.getClosingDate(), b.getClosingDate()))
        now, index = datetime.datetime.now(pytz.utc), 0
        for i in opportunities:
            if i.getClosingDate() >= now:
                break
            index += 1
        return opportunities[:index], opportunities[index:]

    def getCurrentOpportunities(self):
        return self.getOpportunities()[1]
    
    def getPriorOpportunities(self):
        return self.getOpportunities()[0]
    
    def getAnnouncementsForOpportunity(self, opportunity):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(
            object_provides=IAnnouncement.__identifier__,
            path=dict(query='/'.join(opportunity.getPhysicalPath()), depth=1),
            sort_on='closingDate',
        )
        return [i.getObject() for i in results]
    
    def sortVariousDates(self, announcements):
        loiDates, ardDates = [], []
        for i in announcements:
            if i.loiDates:
                loiDates.append(dict(idNum=i.idNum, dates=i.loiDates))
            if i.appReceiptDates:
                ardDates.append(dict(idNum=i.idNum, dates=i.appReceiptDates))
        return dict(loiDates=loiDates, ardDates=ardDates)
    

class FundingOpportunityView(BaseView):
    '''Default view for Funding Opportunity.'''
    __call__ = ViewPageTemplateFile('templates/fundingopportunity.pt')
    @memoize
    def getAnnouncements(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(
            object_provides=IAnnouncement.__identifier__,
            path=dict(query='/'.join(context.getPhysicalPath()), depth=1),
            sort_on='closingDate',
        )
        return [dict(title=i.Title, description=i.Description, closingDate=i.closingDate, url=i.getURL()) for i in results]
    

