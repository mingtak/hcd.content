# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from plone import api
import random
from DateTime import DateTime
import time
from Products.CMFPlone.utils import safe_unicode
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides
import csv
import logging
from collective.geo.geographer.interfaces import IWriteGeoreferenced


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
                title='data',
            )

        with open(filepath, "rb") as file:
            items = csv.DictReader(file)

            count = 0
            for item in items:
                id = '%s_%s' % (item.get('資料編號-文本ID'), item.get('資料編號-事件編碼'))
                title = item.get('事件-事件敘述')
                content = api.content.create(
                    type='Climate',
                    container=folder,
                    id=id,
                    title=title,
                )

                content.description = item.get('事件-文本內容')
                content.clrl = []
                content.clrl.append(item.get('農曆起始時間-文本西元年'))
                content.clrl.append(item.get('農曆起始時間-月'))
                content.clrl.append(item.get('農曆起始時間-日'))
                content.clrl.append(item.get('農曆起始時間-時-代碼'))
                content.clrl.append(item.get('農曆起始時間-季節'))
                content.clrl.append(item.get('農曆迄止時間-文本西元年'))
                content.clrl.append(item.get('農曆迄止時間-月'))
                content.clrl.append(item.get('農曆迄止時間-日'))
                content.clrl.append(item.get('農曆迄止時間-時-代碼'))
                content.clrl.append(item.get('農曆迄止時間-季節'))

                content.clrs = []
                content.clrs.append(item.get('西曆起始時間-年'))
                content.clrs.append(item.get('西曆起始時間-月'))
                content.clrs.append(item.get('西曆起始時間-日'))
                content.clrs.append(item.get('西曆起始時間-時-代碼'))
                content.clrs.append(item.get('西曆迄止時間-年'))
                content.clrs.append(item.get('西曆迄止時間-月'))
                content.clrs.append(item.get('西曆迄止時間-日'))
                content.clrs.append(item.get('西曆迄止時間-時-代碼'))

                content.lctp = item.get('空間-古地名')
                content.lctn = []
                content.lctn.append(item.get('空間-今隸屬省級'))
                content.lctn.append(item.get('空間-今隸屬縣市'))

                content.lcth = float(item.get('空間-高度'))

                content.event = item.get('事件編碼')

                content.source = []
                content.source.append(item.get('文獻名稱'))
                content.source.append(item.get('冊'))
                content.source.append(item.get('頁碼'))

                # coordinates for collective.geo
                longitude = item.get('空間-經度')
                latitude = item.get('空間-緯度')
                geo = IWriteGeoreferenced(content)
                geo.setGeoInterface('Point', (float(longitude), float(latitude)))

                content.reindexObject()
