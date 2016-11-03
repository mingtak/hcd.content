# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from cStringIO import StringIO
import csv
import json


class GetClimate(BrowserView):

    template = ViewPageTemplateFile("template/get_climate.pt")

    def __call__(self):
        context = self.context
        request = self.request
#        catalog = context.portal_catalog

        self.para = request.get('para')
        self.yearRange = request.form.get('yearRange')
        self.yearStart = int(self.yearRange.split(',')[0])
        self.yearEnd = int(self.yearRange.split(',')[1])
        self.yearRange = [self.yearStart, self.yearEnd]

        if not self.para or not self.yearRange:
            return '<div>No Result</div>'

        self.brain = self.getBrain()

        if request.form.get('download'):
            return self.downloadFile()
            
        return self.template()


    def getBrain(self):
        catalog = self.context.portal_catalog
        # TODO: 目前只能以主類別搜尋，與次類別的交聯集尚未完成
        return catalog({'Type':'Climate', 'ctgr1':self.para, 'clrsby':{'query':self.yearRange, 'range':'min:max'}})


    def downloadFile(self):
        self.request.response.setHeader('Content-Type', 'application/csv')
        self.request.response.setHeader('Content-Disposition', 'attachment; filename="results.csv"')

        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['事件-事件敘述', '事件-文本內容', '事件編碼', '文獻名稱', '冊', '頁碼'])
        for item in self.brain:
            itemObj = item.getObject()
            # TODO: 要寫入那些值，這裏是sample，正確的內容要再確認
            writer.writerow([itemObj.title.encode('utf-8'),
                             itemObj.description.encode('utf-8'),
                             itemObj.hpng.encode('utf-8'),
                             itemObj.tsrc.encode('utf-8'),
                             itemObj.novl.encode('utf-8'),
                             itemObj.nopg.encode('utf-8'),])

        results = output.getvalue()
        output.close()
        return results


class ClimateListingView(BrowserView):

    template = ViewPageTemplateFile("template/climate_listing_view.pt")

    def __call__(self):
        if self.request.form.get('category-edit'):
            self.ctgr = json.loads(self.request.form.get('category-edit'))
        else:
            self.ctgr = self.getCtgr()
        return self.template()


    def getCtgr(self):
        return json.loads(api.portal.get_registry_record('hcd.content.browser.siteSetting.ISiteSetting.event'))


    def getCtgr_text(self):
        return api.portal.get_registry_record('hcd.content.browser.siteSetting.ISiteSetting.event')


class MapView(BrowserView):

    template = ViewPageTemplateFile("template/map-view.pt")

    def __call__(self):
        return self.template()
