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
    hpngList = hpng(obj)
    if hpngList:
        return [i[0:2] for i in hpngList]

@indexer(IClimate)
def ctgr2_indexer(obj):
    hpngList = hpng(obj)
    if hpngList:
        return [i[0:4] for i in hpngList]


@indexer(IClimate)
def degree_indexer(obj):
    hpngList = hpng(obj)
    if hpngList:
        return ['%s%s' % (i[0:2], i[7]) for i in hpngList] + ['%s%s' % (i[0:4], i[7]) for i in hpngList]


@indexer(IClimate)
def lasting_indexer(obj):
    hpngList = hpng(obj)
    if hpngList:
        return ['%s%s' % (i[0:2], i[8]) for i in hpngList] + ['%s%s' % (i[0:4], i[8]) for i in hpngList]

@indexer(IClimate)
def long_lat_indexer(obj):
    return [obj.lcte,obj.lctn]
    
@indexer(IClimate)
def clrsby_indexer(obj):
    if obj.clrsby:
        return int(obj.clrsby)


@indexer(IClimate)
def bsym_indexer(obj):
    if obj.clrsby and obj.clrsbm:
        try:
            if int(obj.clrsbm) < 10:
                return int('%s0%s' % (obj.clrsby, obj.clrsbm))
            else:
                return int('%s%s' % (obj.clrsby, obj.clrsbm))
        except:pass
