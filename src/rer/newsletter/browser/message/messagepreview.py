# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from rer.newsletter.behaviors.ships import IShippable
from rer.newsletter.content.channel import Channel
from datetime import datetime


class MessagePreview(BrowserView):
    """ view for message preview """

    def getMessageStyle(self):
        for obj in self.context.aq_chain:
            if isinstance(obj, Channel):
                return obj.css_style

    def getChannel(self):
        channel = None
        for obj in self.context.aq_chain:
            if isinstance(obj, Channel):
                channel = obj
                break
        return channel

    def getMessageHeader(self):
        return self.getChannel().header if self.getChannel().header else u''

    def getMessageFooter(self):
        return self.getChannel().footer if self.getChannel().footer else u''

    def getMessageContent(self):
        channel = self.getChannel()
        if channel:
            return f"""
                <tr>
                    <td align="left">
                        <div class="divider"></div>
                        <div class="newsletterTitle">
                        <h1>{self.context.title}</h1>
                        <h4 class="newsletterDate">{
                            datetime.today().strftime('Newsletter %d %B %Y')
                        }</h4>
                    </div>

                    </td>
                </tr>
                <tr>
                    <td align="left">
                     {IShippable(self.context).message_content}
                    </td>
                </tr>
            """

    def getMessagePreview(self):
        channel = None
        for obj in self.context.aq_chain:
            if isinstance(obj, Channel):
                channel = obj
                break
        if channel:
            body = u''
            body = channel.header if channel.header else u''
            body += f"""

                <tr>
                    <td align="left">
                        <div class="gmail-blend-screen">
                        <div class="gmail-blend-difference">
                            <div class="divider"></div>
                        </div>
                        </div>
                        <div class="newsletterTitle">
                        <h1>{self.context.title}</h1>
                        <h4 class="newsletterDate">{
                            datetime.today().strftime('Newsletter %d %B %Y')
                        }</h4>
                    </div>

                    </td>
                </tr>
                <tr>
                    <td align="left">
                     {IShippable(self.context).message_content}
                    </td>
                </tr>

            """
            body += channel.footer if channel.footer else u''

        return body
