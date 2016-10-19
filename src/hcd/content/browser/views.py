# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api


class GetClimate(BrowserView):

    template = ViewPageTemplateFile("template/get_climate.pt")

    def __call__(self):
        context = self.context
        request = self.request

        para = request.get('para')
        if not para:
            return '<div></div>'

        self.brain = api.content.find(Type='Climate', event=para)
        return self.template()


class ClimateListingView(BrowserView):

    template = ViewPageTemplateFile("template/climate_listing_view.pt")

    def __call__(self):
        return self.template()


    def getEventList(self):
        return api.portal.get_registry_record('hcd.content.browser.siteSetting.ISiteSetting.event')


class MapView(BrowserView):

    template = ViewPageTemplateFile("template/map-view.pt")

    def __call__(self):
        return self.template()
