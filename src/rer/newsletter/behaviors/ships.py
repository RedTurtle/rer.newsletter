# -*- coding: utf-8 -*-
from zope.interface import alsoProvides
from zope.interface import Interface
from zope.component import adapter
from plone.app.contenttypes.content import Collection
from rer.newsletter.content.message import Message
from plone import api


class IShippableMarker(Interface):
    pass


class IShippable(Interface):
    """Marker interface for ships object"""


alsoProvides(IShippable)


@adapter(IShippableMarker)
class Shippable(object):

    def __init__(self, context):
        self.context = context

    @property
    def message_content(self):
        if isinstance(self.context, Collection):
            return api.content.get_view(
                name='collection_sending_view',
                context=self.context,
                request=self.context.REQUEST
            )()
        elif isinstance(self.context, Message):
            return self.context.text.output if self.context.text else u''
