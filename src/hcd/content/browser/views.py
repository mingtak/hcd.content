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
        # TODO: index 名稱有改過， 'event' 要再改名稱, 要再查看'hpng'的index對應值
        # TODO: 目前只能以主類別搜尋，與次類別的交聯集尚未完成
        ctgr1 = []
        ctgr2 = []
        for para in self.para:
            if len(para) == 2:
                ctgr1.append(para)
            elif len(para) == 4:
                ctgr2.append(para)
        return catalog({'Type':'Climate', 'ctgr2':ctgr2, 'clrsby':{'query':self.yearRange, 'range':'min:max'}})


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
        context = self.context
        portal = api.portal.get()

        if self.request.form.get('custom'):
            if api.user.is_anonymous():
                request.response.redirect(context.absolute_url())
                return
            jsonString = portal['members'][api.user.get_current().id].customCategories
            self.ctgr = json.loads(jsonString)
        else:
            self.ctgr = self.getCtgr()
        return self.template()


    def getCtgr(self):
        return json.loads(api.portal.get_registry_record('hcd.content.browser.siteSetting.ISiteSetting.event'))


    def getCtgr_text(self):
        return api.portal.get_registry_record('hcd.content.browser.siteSetting.ISiteSetting.event')


class ProfileView(BrowserView):

    template = ViewPageTemplateFile("template/profile_view.pt")

    def __call__(self):
        context = self.context
        request = self.request

        resourceJson = json.loads(api.portal.get_registry_record('hcd.content.browser.siteSetting.ISiteSetting.event'))

        if request.form.get('submit'):
            newJson = {}
            for item in request.form.items():
                if newJson.get(item[1]):
                    newJson[item[1]].append(item[0])
                elif ':' not in item[0]:
                    continue
                else:
                    newJson[item[1]] = [item[0]]

            pool = {}
            for group in resourceJson.values():
                for item in group.items():
                    pool[item[0]] = item[1]

            resultJson = {}
            groupCount = 1
            for items in newJson.items():
                resultJson['group_%s:%s' % (groupCount, items[0])] = {}
                for item in items[1]:
                    resultJson['group_%s:%s' % (groupCount, items[0])][item] = pool[item.decode('utf-8')]
                groupCount += 1

            context.customCategories = json.dumps(resultJson)
            request.response.redirect(context.absolute_url())
            return

        return self.template()


class MapView(BrowserView):

    template = ViewPageTemplateFile("template/map-view.pt")

    def __call__(self):
        return self.template()
