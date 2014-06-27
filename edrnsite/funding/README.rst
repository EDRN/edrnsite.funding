This package provides Plone content objects for for the announcement and
managing of EDRN funding opportunities.


Installation
============

Add "edrnsite.funding" to the buildout.


Content Types
=============

The content types introduced in this package include the following:

FundingFolder
    A folder to contain funding opportunities.
FundingOpportunity
    An source of moolah. Can be announced zero or more times.
Announcement
    An announcement of a source of moolah.  Has various deadlines for
    application.

The remainder of this document demonstrates the content types using a series
of functional tests.


Tests
=====

First we have to set up some things and login to the site::

    >>> app = layer['app']
    >>> from plone.testing.z2 import Browser
    >>> from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD
    >>> browser = Browser(app)
    >>> browser.handleErrors = False
    >>> browser.addHeader('Authorization', 'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD))
    >>> portal = layer['portal']    
    >>> portalURL = portal.absolute_url()

Now we can check out the new types introduced in this package.


Addable Content
---------------

Here we'll exercise some of the content objects available in this project and
demonstrate their properties and constraints.


FundingFolder
~~~~~~~~~~~~~

A funding folder can be created anywhere in the portal.  Here we'll add one to
the root::

    >>> browser.open(portalURL)
    >>> l = browser.getLink(id='funding-folder')
    >>> l.url.endswith('createObject?type_name=Funding+Folder')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = u'My Funding Folder'
    >>> browser.getControl(name='description').value = u'This folder is just for functional tests.'
    >>> browser.getControl(name='form.button.save').click()
    >>> 'my-funding-folder' in portal.objectIds()
    True
    >>> f = portal['my-funding-folder']
    >>> f.title
    'My Funding Folder'
    >>> f.description
    'This folder is just for functional tests.'


FundingOpportunity
~~~~~~~~~~~~~~~~~~

A funding opportunity describes Program Announcements and other sources of
moolah. They may be added only to FundingFolders, as shown below::

    >>> browser.open(portalURL)
    >>> l = browser.getLink(id='funding-opportunity')
    Traceback (most recent call last):
    ...
    LinkNotFoundError
    >>> browser.open(portalURL + '/my-funding-folder')
    >>> l = browser.getLink(id='funding-opportunity')
    >>> l.url.endswith('createObject?type_name=Funding+Opportunity')
    True

Funding opportunities have very few attributes. Here, we create one::

    >>> l.click()
    >>> browser.getControl(name='title').value = u'Project: Death'
    >>> browser.getControl(name='description').value = u'An opportunity to murder cancer.'
    >>> browser.getControl('Notice').selected = True
    >>> browser.getControl('Reissuable').selected = True
    >>> browser.getControl(name='form.button.save').click()
    >>> 'project-death' in f.objectIds()
    True
    >>> p = f['project-death']
    >>> p.title
    'Project: Death'
    >>> p.description
    'An opportunity to murder cancer.'
    >>> p.opportunityType
    'Notice'
    >>> p.reissuable
    True


Announcement
~~~~~~~~~~~~
    
Funding opportunities don't announce themselves.  That's the job of
Announcements.  Announcements may be created only within FundingOpportunity
objects::

    >>> browser.open(portalURL)
    >>> l = browser.getLink(id='announcement')
    Traceback (most recent call last):
    ...
    LinkNotFoundError
    >>> browser.open(portalURL + '/my-funding-folder')
    >>> l = browser.getLink(id='announcement')
    Traceback (most recent call last):
    ...
    LinkNotFoundError
    >>> browser.open(portalURL + '/my-funding-folder/project-death')
    >>> l = browser.getLink(id='announcement')
    >>> l.url.endswith('createObject?type_name=Announcement')
    True

An Announcement captures a number of attributes, much having to do with
various deadline dates.

    >>> l.click()
    >>> browser.getControl(name='title').value = 'Announcement of Death'
    >>> browser.getControl(name='description').value = 'The very first announcement of Project: Death.'
    >>> browser.getControl(name='announcementLink').value = u'http://google.com/'
    >>> browser.getControl(name='idNum').value = 'D-12345'
    >>> browser.getControl(name='releaseDate_year').displayValue = ['2012']
    >>> browser.getControl(name='releaseDate_month').value = ['02']
    >>> browser.getControl(name='releaseDate_day').value = ['22']
    >>> browser.getControl(name='closingDate_year').displayValue = ['2012']
    >>> browser.getControl(name='closingDate_month').value = ['05']
    >>> browser.getControl(name='closingDate_day').value = ['26']
    >>> browser.getControl(name='loiDates:lines').value = '2000-03-12\n2000-03-15'
    >>> browser.getControl(name='appReceiptDates:lines').value = '2000-04-15\n2000-04-22'
    >>> browser.getControl(name='form.button.save').click()
    >>> 'announcement-of-death' in p.objectIds()
    True
    >>> a = p['announcement-of-death']
    >>> a.title
    'Announcement of Death'
    >>> a.description
    'The very first announcement of Project: Death.'
    >>> a.announcementLink
    'http://google.com/'
    >>> a.idNum
    'D-12345'
    >>> a.releaseDate.year, a.releaseDate.month, a.releaseDate.day
    (2012, 2, 22)
    >>> a.closingDate.year, a.closingDate.month, a.closingDate.day
    (2012, 5, 26)
    >>> a.loiDates
    ('2000-03-12', '2000-03-15')
    >>> a.appReceiptDates
    ('2000-04-15', '2000-04-22')
    
Announcements have custom validation for the letter-of-intent and application
receipt dates.  They must be ISO style YYYY-MM-DD entries separated by
newlines.  Let's see if that works::

    >>> browser.open(portalURL + '/my-funding-folder/project-death')
    >>> browser.getLink(id='announcement').click()
    >>> browser.getControl(name='title').value = 'Invalid Announcement'
    >>> browser.getControl(name='announcementLink').value = u'http://google.com/'
    >>> browser.getControl(name='idNum').value = u'D-Invalid'
    >>> browser.getControl(name='releaseDate_year').displayValue = ['2012']
    >>> browser.getControl(name='releaseDate_month').value = ['02']
    >>> browser.getControl(name='releaseDate_day').value = ['22']
    >>> browser.getControl(name='closingDate_year').displayValue = ['2012']
    >>> browser.getControl(name='closingDate_month').value = ['05']
    >>> browser.getControl(name='closingDate_day').value = ['26']
    >>> browser.getControl(name='loiDates:lines').value = 'February 4th, 1996\nThe Ides of March, 2000'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.contents
    '...You must enter dates in the YYYY-MM-DD format, one per line...'


Funding Views
-------------

Funding Folders by default have a user-friendly view that enables browsers to
find interesting opportunities to apply for.  This hides the structure of
Funding Folder → Funding Opportunity → Announcement from end users.

Funding folders display their opportunities in two sections:  current and
prior.  Current opportunities are those that have an announcement whose
closing date is in today or in the future, while prior are those with
announcement closing dates in the past.

To see if this works, we'll start with an empty funding folder::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='funding-folder').click()
    >>> browser.getControl(name='title').value = 'Testing Funding Views'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/testing-funding-views')

Both the current and prior sections should say none available::

    >>> browser.contents
    '...Current Opportunities...no opportunities available...Prior Opportunities...no prior opportunities...'
    
Now we'll add opportunity.  By default, an opportunity with no announcements
is optimistically current::

    >>> browser.getLink(id='funding-opportunity').click()
    >>> browser.getControl(name='title').value = 'Alpha'
    >>> browser.getControl('Request for Application').selected = True
    >>> browser.getControl(name='form.button.save').click()
    
Does it appear on the folder?

    >>> browser.open(portalURL + '/testing-funding-views')
    >>> browser.contents
    '...Current Opportunities...Alpha...Prior Opportunities...no prior opportunities...'
    
Now, we'll add an announcement that places the Alpha opportunity into the past::

    >>> from datetime import datetime, timedelta
    >>> yesterday = datetime.now() - timedelta(1)
    >>> browser.open(portalURL + '/testing-funding-views/alpha')
    >>> browser.getLink(id='announcement').click()
    >>> browser.getControl(name='title').value = 'Alpha Announcement'
    >>> browser.getControl(name='announcementLink').value = 'http://google.com/'
    >>> browser.getControl(name='idNum').value = 'LIFE-is-POINTLESS'
    >>> browser.getControl(name='releaseDate_year').displayValue = ['2008']
    >>> browser.getControl(name='releaseDate_month').value = ['01']
    >>> browser.getControl(name='releaseDate_day').value = ['01']
    >>> browser.getControl(name='closingDate_year').displayValue = [str(yesterday.year)]
    >>> browser.getControl(name='closingDate_month').value = ['%02d' % yesterday.month]
    >>> browser.getControl(name='closingDate_day').value = ['%02d' % yesterday.day]
    >>> browser.getControl(name='form.button.save').click()

Returning to the folder should show this opportunity in the prior section::

    >>> browser.open(portalURL + '/testing-funding-views')
    >>> browser.contents
    '...Current Opportunities...no opportunities available...Prior Opportunities...Alpha...'

Similarly, placing an announcement into the future should pop the opportunity
back up to the current section.  We'll add a new announcement to do just
that::

    >>> tomorrow = datetime.now() + timedelta(2)
    >>> browser.open(portalURL + '/testing-funding-views/alpha')
    >>> browser.getLink(id='announcement').click()
    >>> browser.getControl(name='title').value = 'Alpha Announcement'
    >>> browser.getControl(name='announcementLink').value = 'http://google.com/'
    >>> browser.getControl(name='idNum').value = 'LIFE-is-POINTLESS'
    >>> browser.getControl(name='releaseDate_year').displayValue = ['2008']
    >>> browser.getControl(name='releaseDate_month').value = ['01']
    >>> browser.getControl(name='releaseDate_day').value = ['01']
    >>> browser.getControl(name='closingDate_year').displayValue = [str(tomorrow.year)]
    >>> browser.getControl(name='closingDate_month').value = ['%02d' % tomorrow.month]
    >>> browser.getControl(name='closingDate_day').value = ['%02d' % tomorrow.day]
    >>> browser.getControl(name='form.button.save').click()

And there it is::

    >>> browser.open(portalURL + '/testing-funding-views')
    >>> browser.contents
    '...Current Opportunities...Alpha...Prior Opportunities...no prior opportunities...'

Later announcements always have priority over earlier announcements; i.e., the
closing date is the farthest date out of all the announcements for an
opportunity.

Can opportunities appear in both sections?  Certainly.  We have "Alpha"
already as a current, so let's create a new opportunity called "Beta" and give
it an announcement in the past::

    >>> browser.getLink(id='funding-opportunity').click()
    >>> browser.getControl(name='title').value = 'Beta'
    >>> browser.getControl('Request for Application').selected = True
    >>> browser.getControl(name='form.button.save').click()
    >>> yesterday = datetime.now() - timedelta(1)
    >>> browser.open(portalURL + '/testing-funding-views/beta')
    >>> browser.getLink(id='announcement').click()
    >>> browser.getControl(name='title').value = 'Beta Announcement'
    >>> browser.getControl(name='announcementLink').value = 'http://google.com/'
    >>> browser.getControl(name='idNum').value = 'Suicide-is-an-option'
    >>> browser.getControl(name='releaseDate_year').displayValue = ['2008']
    >>> browser.getControl(name='releaseDate_month').value = ['01']
    >>> browser.getControl(name='releaseDate_day').value = ['01']
    >>> browser.getControl(name='closingDate_year').displayValue = [str(yesterday.year)]
    >>> browser.getControl(name='closingDate_month').value = ['%02d' % yesterday.month]
    >>> browser.getControl(name='closingDate_day').value = ['%02d' % yesterday.day]
    >>> browser.getControl(name='form.button.save').click()
    
Now the funding folder has both sections filled::

    >>> browser.open(portalURL + '/testing-funding-views')
    >>> browser.contents
    '...Current Opportunities...Alpha...Prior Opportunities...Beta...'
