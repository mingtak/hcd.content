# -*- coding: utf-8 -*-
from plone.app.testing import TEST_USER_ID
from zope.component import queryUtility
from zope.component import createObject
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from plone import api

from hcd.content.testing import HCD_CONTENT_INTEGRATION_TESTING  # noqa
from hcd.content.interfaces import IClimate

import unittest2 as unittest


class ClimateIntegrationTest(unittest.TestCase):

    layer = HCD_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Climate')
        schema = fti.lookupSchema()
        self.assertEqual(IClimate, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Climate')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Climate')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IClimate.providedBy(obj))

    def test_adding(self):
        self.portal.invokeFactory('Climate', 'Climate')
        self.assertTrue(
            IClimate.providedBy(self.portal['Climate'])
        )
