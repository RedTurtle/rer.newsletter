# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from plone import api
from plone.restapi.deserializer import json_body
from plone.protect.authenticator import createToken
from plone.restapi.services import Service
from rer.newsletter import _
from rer.newsletter import logger
from rer.newsletter.adapter.subscriptions import IChannelSubscriptions
from rer.newsletter.utils import compose_sender, get_site_title, SUBSCRIBED, UNHANDLED
from six import PY2
from zope.component import getMultiAdapter


class NewsletterSubscribe(Service):

    def getData(self, data):
        errors = {}
        if not data.get("email", None):
            errors['email'] = u"invalid_email"
        if not data.get("g-recaptcha-response", None):
            errors['g-recaptcha-response'] = u"invalid_captcha"
        return {
            "email": data.get("email", None),
            'g-recaptcha-response': data.get('g-recaptcha-response', None),
        }, errors

    def handleSubscribe(self, postData):
        status = UNHANDLED
        data, errors = self.getData(postData)
        import pdb; pdb.set_trace()
        # recaptcha
        captcha = getMultiAdapter(
            (aq_inner(self.context), self.request), name="captcha"
        )
        if errors:
           return data, errors

        self.request['g-recaptcha-response'] = data['g-recaptcha-response']
        # come funziona/ come testarlo?
        if not captcha.verify():
            errors = u"message_wrong_captcha"

            return data, errors

        email = data.get("email", "").lower()

        if self.context.is_subscribable:
            channel = getMultiAdapter(
                (self.context, self.request), IChannelSubscriptions
            )
            status, secret = channel.subscribe(email)

        if status == SUBSCRIBED:

            # creo il token CSRF
            token = createToken()

            # mando mail di conferma
            url = self.context.absolute_url()
            url += "/confirm-subscription?secret=" + secret
            url += "&_authenticator=" + token
            url += "&action=subscribe"

            mail_template = self.context.restrictedTraverse(
                "@@activeuser_template"
            )

            parameters = {
                "title": self.context.title,
                "header": self.context.header,
                "footer": self.context.footer,
                "style": self.context.css_style,
                "activationUrl": url,
                "portal_name": get_site_title(),
            }

            mail_text = mail_template(**parameters)

            portal = api.portal.get()
            mail_text = portal.portal_transforms.convertTo(
                "text/mail", mail_text
            )
            sender = compose_sender(channel=self.context)

            channel_title = self.context.title
            if PY2:
                channel_title = self.context.title.encode("utf-8")

            mailHost = api.portal.get_tool(name="MailHost")
            mailHost.send(
                mail_text.getData(),
                mto=email,
                mfrom=sender,
                subject="Conferma la tua iscrizione alla Newsletter {channel}"
                " del portale {site}".format(
                    channel=channel_title, site=get_site_title()
                ),
                charset="utf-8",
                msg_type="text/html",
                immediate=True,
            )
            return data, errors

        else:
            if status == 2:
                logger.exception("user already subscribed")
                errors = u"user_already_subscribed"
                return data, errors
            else:
                logger.exception("unhandled error subscribe user")
                errors = u"Problems...{0}".format(status)
                return data, errors

    def reply(self):
        data = json_body(self.request)
        _data, errors = self.handleSubscribe(data)

        return {
            "@id": self.request.get("URL"),
            "errors": errors if errors else None,
            'status': u"user_subscribe_success" if not errors else 'error',
        }
