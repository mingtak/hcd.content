# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from hcd.content.testing import HCD_CONTENT_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that hcd.content is properly installed."""

    layer = HCD_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if hcd.content is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'hcd.content'))

    def test_browserlayer(self):
        """Test that IHcdContentLayer is registered."""
        from hcd.content.interfaces import (
            IHcdContentLayer)
        from plone.browserlayer import utils
        self.assertIn(IHcdContentLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = HCD_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['hcd.content'])

    def test_product_uninstalled(self):
        """Test if hcd.content is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'hcd.content'))

    def test_browserlayer_removed(self):
        """Test that IHcdContentLayer is removed."""
        from hcd.content.interfaces import IHcdContentLayer
        from plone.browserlayer import utils
        self.assertNotIn(IHcdContentLayer, utils.registered_layers())
