# -*- coding: utf-8 -*-
from hcd.content import _
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from plone.z3cform import layout
from z3c.form import form
from plone.directives import form as Form
from zope import schema


class ISiteSetting(Form.Schema):

    event = schema.List(
        title=_(u"Event Code and Description"),
        description=_(u"Please use ':' to split event code and description"),
        value_type=schema.TextLine(),
        required=False,
    )


class SiteSettingControlPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = ISiteSetting


SiteSettingControlPanelView = layout.wrap_form(SiteSettingControlPanelForm, ControlPanelFormWrapper)
SiteSettingControlPanelView.label = _(u"Site Setting")

