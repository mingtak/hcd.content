# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope import schema
from hcd.content import _


class IHcdContentLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IClimate(Interface):
    """Climate Type
    """
    title = schema.TextLine(
        title=_(u"Title"),
        required=False,
    )

    description = schema.Text(
        title=_(u"Description"),
        required=False,
    )

    clrl = schema.List(
        title=_(u"Lunar Calendar"),
        value_type = schema.TextLine(),
        required=False,
    )

    clrs = schema.List(
        title=_(u"Solar Calendar"),
        value_type = schema.TextLine(),
        required=False,
    )

    lctp = schema.TextLine(
        title=_(u"Location Past"),
        required=False,
    )

    lctn = schema.List(
        title=_(u"Location Now"),
        value_type=schema.TextLine(),
        required=False,
    )

    lcth = schema.Float(
        title=_(u"Location Height"),
        required=False,
    )

    event = schema.Text(
        title=_(u"Event Code"),
        required=False,
    )

    source = schema.List(
        title=_(u"Text Source"),
        value_type=schema.TextLine(),
        required=False,
    )
