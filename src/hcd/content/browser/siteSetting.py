# -*- coding: utf-8 -*-
from hcd.content import _
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from plone.z3cform import layout
from z3c.form import form
from plone.directives import form as Form
from zope import schema


class ISiteSetting(Form.Schema):

    event = schema.Text(
        title=_(u"Event Code and Description"),
        description=_(u"Support Json format"),
        required=False,
    )


class SiteSettingControlPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = ISiteSetting


SiteSettingControlPanelView = layout.wrap_form(SiteSettingControlPanelForm, ControlPanelFormWrapper)
SiteSettingControlPanelView.label = _(u"Site Setting")

