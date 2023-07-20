# -*- coding: utf-8 -*-
from plone import api
from plone.memoize import view
from Products.Five.browser import BrowserView


class PloneVersionView(BrowserView):
    """View to check Plone version"""

    @view.memoize
    def is_plone_6_or_above(self):
        version = api.env.plone_version()
        major = version.split(".")[0]
        return int(major) >= 6
