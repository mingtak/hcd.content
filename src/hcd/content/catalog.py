# -*- coding: utf-8 -*-
from plone.indexer.decorator import indexer
from zope.interface import Interface
from Products.CMFPlone.utils import safe_unicode

from hcd.content.interfaces import IClimate


def hpng(obj):
    hpng = getattr(obj, 'hpng')
    if hpng:
        hpng = hpng.split(';')
    else:
        return None
    for i in range(len(hpng)):
        if int(hpng[i]) < 1:
            hpng[i] = hpng[i].strip()
            continue
    return hpng


@indexer(IClimate)
def ctgr1_indexer(obj):
    return [i[0:2] for i in hpng(obj)]


@indexer(IClimate)
def ctgr2_indexer(obj):
    return [i[0:4] for i in hpng(obj)]


@indexer(IClimate)
def degree_indexer(obj):
    return [i[7:8] for i in hpng(obj)]


@indexer(IClimate)
def lasting_indexer(obj):
    return [i[8:9] for i in hpng(obj)]


@indexer(IClimate)
def clrsby_indexer(obj):
    if obj.clrsby:
        return int(obj.clrsby)
