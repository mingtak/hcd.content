# -*- coding: utf-8 -*-
from plone.indexer.decorator import indexer
from zope.interface import Interface
from Products.CMFPlone.utils import safe_unicode

from hcd.content.interfaces import IClimate


@indexer(IClimate)
def event_indexer(obj):
    event = getattr(obj, 'event')

#    import pdb; pdb.set_trace()

    if event:
        event = event.split(';')
    else:
        return

    for i in range(len(event)):
        if int(event[i]) < 1:
            event[i] = event[i].strip()
            continue
        event[i] = event[i].strip()[0:2]
    return event
