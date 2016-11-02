# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from plone import api
import random
from DateTime import DateTime
import time
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides
import csv
import logging


logger = logging.getLogger("ImportCSV")

class ImportCSV(BrowserView):
    """ Import Member
    """

    def __call__(self):
        context = self.context
        request = self.request
        catalog = context.portal_catalog
        portal = api.portal.get()
        alsoProvides(request, IDisableCSRFProtection)

        filepath = request.form.get('filepath')
        if not filepath:
            return

        folder = portal.get('data')
        if not folder:
            folder = api.content.create(
                type='Folder',
                container=portal,
                id='data',
                title='Data',
            )

        with open(filepath, "rb") as file:
            items = csv.DictReader(file)

            count = 0
            for item in items:
                id = '%s_%s' % (item.get('資料編號-文本ID'), item.get('資料編號-事件編碼'))
                title = safe_unicode(item.get('事件-事件敘述'))
                content = api.content.create(
                    type='Climate',
                    container=folder,
                    id=id,
                    title=title,
                )

                content.description = safe_unicode(item.get('事件-文本內容'))
                content.clrlby = safe_unicode(item.get('農曆起始時間-文本西元年'))
                content.clrlbm = safe_unicode(item.get('農曆起始時間-月'))
                content.clrlbd = safe_unicode(item.get('農曆起始時間-日'))
                content.clrlbt = safe_unicode(item.get('農曆起始時間-時-代碼'))
                content.clrlbs = safe_unicode(item.get('農曆起始時間-季節'))
                content.clrley = safe_unicode(item.get('農曆迄止時間-文本西元年'))
                content.clrlem = safe_unicode(item.get('農曆迄止時間-月'))
                content.clrled = safe_unicode(item.get('農曆迄止時間-日'))
                content.clrlet = safe_unicode(item.get('農曆迄止時間-時-代碼'))
                content.clrles = safe_unicode(item.get('農曆迄止時間-季節'))

                content.clrsby = safe_unicode(item.get('西曆起始時間-年'))
                content.clrsbm = safe_unicode(item.get('西曆起始時間-月'))
                content.clrsbd = safe_unicode(item.get('西曆起始時間-日'))
                content.clrsbt = safe_unicode(item.get('西曆起始時間-時-代碼'))
                content.clrsey = safe_unicode(item.get('西曆迄止時間-年'))
                content.clrsem = safe_unicode(item.get('西曆迄止時間-月'))
                content.clrsed = safe_unicode(item.get('西曆迄止時間-日'))
                content.clrset = safe_unicode(item.get('西曆迄止時間-時-代碼'))

                content.lctp = safe_unicode(item.get('空間-古地名'))
                content.lctf = safe_unicode(item.get('空間-今隸屬省級'))
                content.lcts = safe_unicode(item.get('空間-今隸屬縣市'))
                content.lcti = safe_unicode(item.get('空間-縣市ID'))

                content.lcte = float(item.get('空間-經度'))
                content.lctn = float(item.get('空間-緯度'))
                content.lcth = float(item.get('空間-高度'))

                content.hpng = item.get('事件編碼')

                content.tsrc = safe_unicode(item.get('文獻名稱'))
                content.novl = safe_unicode(item.get('冊'))
                content.nopg = safe_unicode(item.get('頁碼'))

                # coordinates for collective.geo
                #longitude = item.get('空間-經度')
                #latitude = item.get('空間-緯度')
                #geo = IWriteGeoreferenced(content)
                #geo.setGeoInterface('Point', (float(longitude), float(latitude)))

                content.reindexObject()
