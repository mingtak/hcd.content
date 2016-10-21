# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api


class GetClimate(BrowserView):

    template = ViewPageTemplateFile("template/get_climate.pt")

    def __call__(self):
        context = self.context
        request = self.request
        catalog = context.portal_catalog

        para = request.get('para')
        yearRange = request.form.get('yearRange')
        yearStart = int(yearRange.split(',')[0])
        yearEnd = int(yearRange.split(',')[1])
        yearRange = [yearStart, yearEnd]

        if not para or not yearRange:
            return '<div>No Result</div>'

        self.brain = catalog({'Type':'Climate', 'event':para, 'clrsYear':{'query':yearRange, 'range':'min:max'}})
        return self.template()


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
