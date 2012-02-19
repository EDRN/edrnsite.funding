# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from plone.app.testing import PloneSandboxLayer, PLONE_FIXTURE, IntegrationTesting, FunctionalTesting
from plone.testing import z2

class EDRNSiteFunding(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)
    def setUpZope(self, app, configurationContext):
        import edrnsite.funding
        self.loadZCML(package=edrnsite.funding)
        z2.installProduct(app, 'edrnsite.funding')
    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'edrnsite.funding:default')
    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'edrnsite.funding')


EDRNSITE_FUNDING_FIXTURE = EDRNSiteFunding()
EDRNSITE_FUNDING_INTEGRATION_TESTING = IntegrationTesting(bases=(EDRNSITE_FUNDING_FIXTURE,), name='EDRNSiteFunding:Integration')
EDRNSITE_FUNDING_FUNCTIONAL_TESTING = FunctionalTesting(bases=(EDRNSITE_FUNDING_FIXTURE,), name='EDRNSiteFunding:Functional')
