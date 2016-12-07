from zope.interface import implementer
from plone.dexterity.content import Item

from hcd.content.interfaces import IClimate
from hcd.content.interfaces import IProfile


@implementer(IClimate)
class Climate(Item):
    """Item Subclass for Climate
    """

@implementer(IProfile)
class Profile(Item):
    """Item Subclass for Profile
    """
