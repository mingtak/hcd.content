# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from cStringIO import StringIO
import csv
import json


# bsym: Begin Solar Year Month

class GetClimate(BrowserView):

    template = ViewPageTemplateFile("template/get_climate.pt")

    def getPara_from_queryString(self):
        context = self.context
        request = self.request
#        import pdb;pdb.set_trace()
        tmpDict = json.loads(request.form.get('queryString'))
        self.monthUnknow = tmpDict.get('monthUnknow')
#        if tmpDict.get('page'):
        self.prevDict = dict(tmpDict)
        self.prevDict['page'] -= 1
        self.prevDict = json.dumps(self.prevDict).replace('"', '%22').replace("'", "%27").replace(' ', '%20')
        self.nextDict = dict(tmpDict)
        self.nextDict['page'] += 1
        self.nextDict = json.dumps(self.nextDict).replace('"', '%22').replace("'", "%27").replace(' ', '%20')


        self.page = int(tmpDict.get('page', 0))
        self.queryString = json.dumps(tmpDict)

        self.para = tmpDict.get('para')
        self.yearRange = tmpDict.get('yearRange')
        self.yearStart = int(self.yearRange.split(',')[0])
        self.monthStart = int(self.yearRange.split(',')[1])
        self.yearEnd = int(self.yearRange.split(',')[2])
        self.monthEnd = int(self.yearRange.split(',')[3])

        self.yearRange = [self.yearStart, self.yearEnd]

        if int(self.monthStart) < 10:
            bsym_start = int('%s0%s' % (self.yearStart, self.monthStart))
        else:
            bsym_start = int('%s%s' % (self.yearStart, self.monthStart))

        if int(self.monthEnd) < 10:
            bsym_end = int('%s0%s' % (self.yearEnd, self.monthEnd))
        else:
            bsym_end = int('%s%s' % (self.yearEnd, self.monthEnd))

        self.bsym = [bsym_start, bsym_end]





    def getPara_from_Form(self):
        context = self.context
        request = self.request

#        import pdb; pdb.set_trace()
        self.page = int(request.get('page', 0))
        tmpDict = dict(request.form)
        tmpDict['page'] = self.page

        self.monthUnknow = tmpDict.get('monthUnknow')
#        if tmpDict.get('page'):
        self.prevDict = dict(tmpDict)
        self.prevDict['page'] -= 1
        self.prevDict = json.dumps(self.prevDict).replace('"', '%22').replace("'", "%27").replace(' ', '%20')
#        import pdb; pdb.set_trace()
        self.nextDict = dict(tmpDict)
        self.nextDict['page'] += 1
        self.nextDict = json.dumps(self.nextDict).replace('"', '%22').replace("'", "%27").replace(' ', '%20')


        self.queryString = json.dumps(tmpDict)

        self.para = request.get('para')
        self.yearRange = request.form.get('yearRange')
        self.yearStart = int(self.yearRange.split(',')[0])
        self.monthStart = int(self.yearRange.split(',')[1])
        self.yearEnd = int(self.yearRange.split(',')[2])
        self.monthEnd = int(self.yearRange.split(',')[3])

        self.yearRange = [self.yearStart, self.yearEnd]

        if int(self.monthStart) < 10:
            bsym_start = int('%s0%s' % (self.yearStart, self.monthStart))
        else:
            bsym_start = int('%s%s' % (self.yearStart, self.monthStart))

        if int(self.monthEnd) < 10:
            bsym_end = int('%s0%s' % (self.yearEnd, self.monthEnd))
        else:
            bsym_end = int('%s%s' % (self.yearEnd, self.monthEnd))

        self.bsym = [bsym_start, bsym_end]


    def __call__(self):
        context = self.context
        request = self.request

#        import pdb; pdb.set_trace()
        if request.form.get('queryString'):
            self.getPara_from_queryString()
        else:
            self.getPara_from_Form()

        if not self.para or not self.bsym:
            return '<div>No Result</div>'

        self.brain = self.getBrain()

        if request.form.get('download'):
            return self.downloadFile()

        return self.template()


    def getBrain(self):
        catalog = self.context.portal_catalog
        ctgr1 = []
        ctgr2 = []
        for para in self.para:
            if len(para) == 2:
                ctgr1.append(para)
            elif len(para) == 4:
                ctgr2.append(para)

#        import pdb; pdb.set_trace()
        if self.monthUnknow == 'true':
            queryDict = {'Type':'Climate', 'clrsby':{'query':self.yearRange, 'range':'min:max'}}
        else:
            queryDict = {'Type':'Climate', 'bsym':{'query':self.bsym, 'range':'min:max'}}
#        queryDict = {'Type':'Climate', 'clrsby':{'query':self.yearRange, 'range':'min:max'}}

# 改採只聯集不交集
#        if ctgr1:
#            queryDict['ctgr1'] = ctgr1

#        if ctgr2 and ctgr1:
#            for key in ctgr1:
#                for j in range(len(ctgr2)-1, -1, -1):
#                    if ctgr2[j].startswith(key):
#                        ctgr2.pop(j)
        if ctgr2:
            queryDict['ctgr2'] = ctgr2

        return catalog(queryDict)


    def downloadFile(self):
        self.request.response.setHeader('Content-Type', 'application/csv')
        self.request.response.setHeader('Content-Disposition', 'attachment; filename="results.csv"')

        output = StringIO()
        output.write(u'\uFEFF'.encode('utf-8'))
        writer = csv.writer(output)
        writer.writerow(['資料編號-文本ID', '資料編號-事件編碼', '事件-文本內容', '事件-事件敘述', '農曆起始時間-文本西元年', '農曆起始時間-季節', '農曆起始時間-月', '農曆起始時間-日', '農曆起始時間-時-代碼', '農曆迄止時間-文本西元年', '農曆迄止時間-季節', '農曆迄止時間-月', '農曆迄止時間-日', '農曆迄止時間-時-代碼', '西曆起始時間-年', '西曆起始時間-月', '西曆起始時間-日', '西曆起始時間-時-代碼', '西曆迄止時間-年', '西曆迄止時間-月', '西曆迄止時間-日', '西曆迄止時間-時-代碼', '空間-古地名', '空間-今隸屬省級', '空間-今隸屬縣市', '空間-經度', '空間-緯度', '空間-高度', '空間-縣市ID', '事件編碼', '文獻名稱', '冊', '頁碼'])
        for item in self.brain:
            itemObj = item.getObject()
            # TODO: 要寫入那些值，這裏是sample，正確的內容要再確認
            writer.writerow([itemObj.id[0:7].encode('utf-8'),
                             itemObj.id[8:].encode('utf-8'),
                             itemObj.description.encode('utf-8'),
                             itemObj.title.encode('utf-8'),
                             itemObj.clrlby.encode('utf-8'),
                             itemObj.clrlbs.encode('utf-8'),
                             itemObj.clrlbm.encode('utf-8'),
                             itemObj.clrlbd.encode('utf-8'),
                             itemObj.clrlbt.encode('utf-8'),
                             itemObj.clrley.encode('utf-8'),
                             itemObj.clrles.encode('utf-8'),
                             itemObj.clrlem.encode('utf-8'),
                             itemObj.clrled.encode('utf-8'),
                             itemObj.clrlet.encode('utf-8'),
                             itemObj.clrsby.encode('utf-8'),
                             itemObj.clrsbm.encode('utf-8'),
                             itemObj.clrsbd.encode('utf-8'),
                             itemObj.clrsbt.encode('utf-8'),
                             itemObj.clrsey.encode('utf-8'),
                             itemObj.clrsem.encode('utf-8'),
                             itemObj.clrsed.encode('utf-8'),
                             itemObj.clrset.encode('utf-8'),
                             itemObj.lctp.encode('utf-8'),
                             itemObj.lctf.encode('utf-8'),
                             itemObj.lcts.encode('utf-8'),
                             itemObj.lcti.encode('utf-8'),
                             str(itemObj.lcte),
                             str(itemObj.lctn),
                             str(itemObj.lcth),
                             itemObj.hpng.encode('utf-8'),
                             itemObj.tsrc.encode('utf-8'),
                             itemObj.novl.encode('utf-8'),
                             itemObj.nopg.encode('utf-8')])

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
