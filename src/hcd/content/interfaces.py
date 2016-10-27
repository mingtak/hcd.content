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

    clrlby = schema.TextLine(
        title=_(u"Lunar Calendar: Begin Year"),
        required=False,
    )

    clrlbs = schema.TextLine(
        title=_(u"Lunar Calendar: Begin Season"),
        required=False,
    )

    clrlbm = schema.TextLine(
        title=_(u"Lunar Calendar: Begin Month"),
        required=False,
    )

    clrlbd = schema.TextLine(
        title=_(u"Lunar Calendar: Begin Date"),
        required=False,
    )

    clrlbt = schema.TextLine(
        title=_(u"Lunar Calendar: Begin Time"),
        required=False,
    )

    clrley = schema.TextLine(
        title=_(u"Lunar Calendar: End Year"),
        required=False,
    )

    clrles = schema.TextLine(
        title=_(u"Lunar Calendar: End Season"),
        required=False,
    )

    clrlem = schema.TextLine(
        title=_(u"Lunar Calendar: End Month"),
        required=False,
    )

    clrled = schema.TextLine(
        title=_(u"Lunar Calendar: End Date"),
        required=False,
    )

    clrlet = schema.TextLine(
        title=_(u"Lunar Calendar: End Time"),
        required=False,
    )

    clrsby = schema.TextLine(
        title=_(u"Solar Calendar: Begin Year"),
        required=False,
    )

    clrsbs = schema.TextLine(
        title=_(u"Solar Calendar: Begin Season"),
        required=False,
    )

    clrsbm = schema.TextLine(
        title=_(u"Solar Calendar: Begin Month"),
        required=False,
    )

    clrsbd = schema.TextLine(
        title=_(u"Solar Calendar: Begin Date"),
        required=False,
    )

    clrsbt = schema.TextLine(
        title=_(u"Solar Calendar: Begin Time"),
        required=False,
    )

    clrsey = schema.TextLine(
        title=_(u"Solar Calendar: End Year"),
        required=False,
    )

    clrses = schema.TextLine(
        title=_(u"Solar Calendar: End Season"),
        required=False,
    )

    clrsem = schema.TextLine(
        title=_(u"Solar Calendar: End Month"),
        required=False,
    )

    clrsed = schema.TextLine(
        title=_(u"Solar Calendar: End Date"),
        required=False,
    )

    clrset = schema.TextLine(
        title=_(u"Solar Calendar: End Time"),
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

    lcte = schema.Float(
        title=_(u"Location Lon"),
        required=False,
    )

    lctn = schema.Float(
        title=_(u"Location Lat"),
        required=False,
    )

    lcth = schema.Float(
        title=_(u"Location Height"),
        required=False,
    )

    hpng = schema.Text(
        title=_(u"Event List"),
        required=False,
    )

    tsrc = schema.TextLine(
        title=_(u"Text Source"),
        required=False,
    )

    novl = schema.TextLine(
        title=_(u"Volume No."),
        required=False,
    )

    nopg = schema.TextLine(
        title=_(u"Page No."),
        required=False,
    )
