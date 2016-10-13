from zope.interface import implementer
from plone.dexterity.content import Item

from hcd.content.interfaces import IClimate


@implementer(IClimate)
class Climate(Item):
    """Item Subclass for Climate
    """

