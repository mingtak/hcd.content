# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from cStringIO import StringIO
import csv


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
        return catalog({'Type':'Climate', 'event':self.para, 'clrsYear':{'query':self.yearRange, 'range':'min:max'}})


    def downloadFile(self):
        self.request.response.setHeader('Content-Type', 'application/csv')
        self.request.response.setHeader('Content-Disposition', 'attachment; filename="results.csv"')

        output = StringIO()
        writer = csv.writer(output)
        for item in self.brain:
            writer.writerow([item.Title, item.Description, item.event])

        results = output.getvalue()
        output.close()
        return results


class ClimateListingView(BrowserView):

    template = ViewPageTemplateFile("template/climate_listing_view.pt")

    def __call__(self):
        if self.request.form.get('category-edit'):
            self.events = self.request.form.get('category-edit').split('\n')
        else:
            self.events = self.getEventList()
        return self.template()


    def getEventList(self):
        return api.portal.get_registry_record('hcd.content.browser.siteSetting.ISiteSetting.event')


class MapView(BrowserView):

    template = ViewPageTemplateFile("template/map-view.pt")

    def __call__(self):
        return self.template()
