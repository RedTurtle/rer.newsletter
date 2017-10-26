from zope.interface import implements
from rer.newsletter import logger
from rer.newsletter.utility.newsletter import INewsletterUtility
from rer.newsletter.utility.newsletter import OK, ALREADY_SUBSCRIBED, INVALID_NEWSLETTER, INVALID_EMAIL, INEXISTENT_EMAIL, MAIL_NOT_PRESENT
import json
import re

# api
from plone import api

# annotations
from persistent.list import PersistentList
from persistent.dict import PersistentDict
from zope.annotation.interfaces import IAnnotations

# for calculate email uuid
from zope.component import getUtility
from plone.uuid.interfaces import IUUIDGenerator

# datetime
from datetime import datetime, timedelta

KEY = "rer.newsletter.subscribers"


def mailValidation(mail):
    # valido la mail
    match = re.match(
        '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
        mail
    )
    if match is None:
        return False
    return True


def isCreationDateExpired(creation_date):
    # settare una data di scadenza di configurazione
    if (datetime.today() - datetime.strptime(creation_date, '%d/%m/%Y %H:%M:%S')) < timedelta(days=2):
        return True
    return False


class BaseHandler(object):
    implements(INewsletterUtility)
    """ utility class to send newsletter email with mailer of plone """

    # metodo privato
    def _api(self, newsletter):
        """ return Newsletter and initialize annotations """

        # controllo che il contesto sia la newsletter
        nl = api.content.find(
            portal_type='Newsletter',
            id_newsletter=newsletter
        )

        if not nl:
            # newsletter non prensete
            return None

        # controllo l'annotations della newsletter
        annotations = IAnnotations(nl[0].getObject())
        if KEY not in annotations.keys():
            # inizializzo l'annotations
            annotations[KEY] = PersistentList([PersistentDict()])
        self.annotations = annotations[KEY]

        return nl[0].getObject()

    def importUsersList(self, usersList, newsletter):
        logger.info("DEBUG: import userslist %s in %s", usersList, newsletter)
        nl = self._api(newsletter)
        if not nl:
            return INVALID_NEWSLETTER

        # controllo che tutte le mail siano valide
        # come mi devo comportare se ci sono mail che non sono valide ?
        for user in usersList:
            if not mailValidation(user):
                return INVALID_EMAIL

        # calculate new uuid for email
        generator = getUtility(IUUIDGenerator)
        uuid = generator()

        for user in usersList:
            if user not in self.annotations:
                self.annotations.append({
                    'email': user,
                    'is_active': True,
                    'token': uuid,
                    'creation_date': datetime.today().strftime('%d/%m/%Y %H:%M:%S'),
                })

        # catch exception
        return OK

    def exportUsersList(self, newsletter):
        logger.info("DEBUG: export users of newsletter: %s", newsletter)
        response = []
        nl = self._api(newsletter)
        if not nl:
            return INVALID_NEWSLETTER

        c = 0
        for user in self.annotations:
            element = {}
            element['id'] = c
            element['email'] = user['email']
            element['is_active'] = user['is_active']
            element['creation_date'] = user['creation_date']
            response.append(element)
            c += 1

        return json.dumps(response), OK

    def deleteUser(self, newsletter, mail):
        logger.info("DEBUG: delete user %s from newsletter %s", mail, newsletter)
        nl = self._api(newsletter)
        if not nl:
            return INVALID_NEWSLETTER

        try:
            element_id = None
            count = 0
            for user in self.annotations:
                if user['email'] == mail:
                    element_id = count
                    break
                count += 1

            # elimino persona dalla newsletter
            if element_id is not None:
                self.annotations.pop(element_id)
            else:
                raise ValueError
        except ValueError:
            return MAIL_NOT_PRESENT

        return OK

    def deleteUserList(self, usersList, newsletter):
        # manca il modo di far capire se una mail non e presente nella lista
        logger.info("DEBUG: delete userslist %s from %s", usersList, newsletter)
        nl = self._api(newsletter)
        if not nl:
            return INVALID_NEWSLETTER

        for user in usersList:
            try:
                element_id = None
                count = 0
                for u in self.annotations:
                    if u['email'] == user:
                        element_id = count
                        break
                    count += 1

                if element_id is not None:
                    self.annotations.pop(element_id)

            except ValueError:
                # to handle
                pass

        return OK

    def emptyNewsletterUsersList(self, newsletter):
        logger.info("DEBUG: emptyNewsletterUsersList %s", newsletter)
        nl = self._api(newsletter)
        if not nl:
            return INVALID_NEWSLETTER

        del self.annotations[:]

        return OK

    def unsubscribe(self, newsletter, mail):
        logger.info("DEBUG: unsubscribe %s %s", newsletter, mail)
        nl = self._api(newsletter)
        if not nl:
            return INVALID_NEWSLETTER

        try:
            element_id = None
            count = 0
            for user in self.annotations:
                if user['email'] == mail:
                    element_id = count
                    break
                count += 1

            # elimino persona dalla newsletter
            if element_id is not None:
                self.annotations.pop(element_id)
            else:
                raise ValueError

        except ValueError:
            return INEXISTENT_EMAIL

        return OK

    def addUser(self, newsletter, mail):
        logger.info("DEBUG: add user: %s %s", newsletter, mail)
        nl = self._api(newsletter)

        if not nl:
            return INVALID_NEWSLETTER

        if not mailValidation(mail):
            return INVALID_EMAIL

        # calculate new uuid for email
        generator = getUtility(IUUIDGenerator)
        uuid = generator()

        # controllo che la mail non sia gia presente e attiva nel db
        for user in self.annotations:
            if (mail == user['email'] and user['is_active']) or (mail == user['email'] and not user['is_active'] and isCreationDateExpired(user['creation_date'])):
                return ALREADY_SUBSCRIBED
        else:
            self.annotations.append({
                'email': mail,
                'is_active': True,
                'token': uuid,
                'creation_date': datetime.today().strftime('%d/%m/%Y %H:%M:%S')
            })

        return OK

    def subscribe(self, newsletter, mail, name=None):
        logger.info("DEBUG: subscribe %s %s", newsletter, mail)
        nl = self._api(newsletter)

        if not nl:
            return INVALID_NEWSLETTER

        if not mailValidation(mail):
            return INVALID_EMAIL

        # calculate new uuid for email
        generator = getUtility(IUUIDGenerator)
        uuid = generator()

        for user in self.annotations:
            if (mail == user['email'] and user['is_active']) or (mail == user['email'] and not user['is_active'] and isCreationDateExpired(user['creation_date'])):
                return ALREADY_SUBSCRIBED
        else:
            self.annotations.append({
                'email': mail,
                'is_active': False,
                'token': uuid,
                'creation_date': datetime.today().strftime('%d/%m/%Y %H:%M:%S')
            })

        return OK

    def sendMessage(self, newsletter, message):
        logger.info("DEBUG: sendMessage %s %s", newsletter, message)
        nl = self._api(newsletter)
        if not nl:
            return INVALID_NEWSLETTER

        return OK
