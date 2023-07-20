=========
Changelog
=========

2.0.0a3 (unreleased)
--------------------

- Adapt management buttons for Plone 6
  [pnicolli]


2.0.0a2 (2023-03-16)
--------------------

- Updated subheader template
  [pnicolli]


2.0.0a1 (2023-03-14)
--------------------

- added restapi services for Volto usage
- fixed results for unsubscribe service
- italian translation
- remove CSRFProtection when call services
- fix email validation when mailinglist are imported
- using preview_image instead of lead image in newsletter shippable collection
- Remove subtitle (h4) in nl template and preview

1.2.0 (2023-01-25)
------------------

- Remove recaptha usage in the channel subscribe form, will be used honeypot instead.
  [foxtrot-dfm1]


1.1.2 (2022-05-12)
------------------

- Improve error handling messages in massive user import.
  [cekk]


1.1.1 (2021-11-11)
------------------

- Fix encoding in unsubscribe.py.
  [cekk]


1.1.0 (2021-06-10)
------------------

- Use mail validator from portal_registration.
  [cekk]


1.0.7 (2021-01-28)
------------------

- Fix logic in delete expired users view.
  [cekk]


1.0.6 (2020-12-18)
------------------

- Handle "running" state in status table for long queues.
  [cekk]


1.0.5 (2020-11-25)
------------------

- Fix upgrade step.
  [cekk]

1.0.4 (2020-11-12)
------------------

- Fix encoding for the channel title.
  [daniele]


1.0.3 (2020-11-06)
------------------

- Handle mail not found in subscribe form.
  [cekk]


1.0.2 (2020-08-18)
------------------

- Styles for newsletter subscription modal
- Fix cancel button moving when in error state
  [nzambello]


1.0.1 (2020-07-27)
------------------

- Remove direct dependency to collective.taskqueue.
  [cekk]

1.0.0 (2020-07-21)
------------------

- Heavy refactoring to support different send methods from adapters.
  [cekk]


0.4.0 (2020-04-21)
------------------

- Fixed subscribers import in Python3.
  [daniele]
- Fixed RichText behavior name in types definition.
  [daniele]
- Fix initializedModal.js to correctly support tiles loading
  [nzambello]

0.3.0 (2020-03-07)
------------------

- Python 3 compatibility.
  [cekk]


0.2.0 (2019-04-01)
------------------

- Fix initializedModal.js to support new functionality in tilesmanagement: anonymous always load a static version of tiles list.
  [cekk]


0.1.12 (2019-01-30)
-------------------

- Added shippable collection.
- Fixed template for shippable collection.
- Fixed search object for channel history view.
  [eikichi18]

- a11y: added role attribute for portalMessage
  [nzambello]


0.1.11 (2018-09-27)
-------------------

- Fix ascii encode problem on site name.
  [eikichi18]


0.1.10 (2018-09-27)
-------------------

- Added number of removed user on delete_expired_users view.
- Removed layer for delete_expired_users view.
- Fixed view for delete expired users.
  [eikichi18]


0.1.9 (2018-09-20)
------------------

- Fixed modal timeout
  [eikichi18]


0.1.8 (2018-07-19)
------------------

- Added Redis for asynchronous task
- Fixed label of close button on subscription modal
- Added Translatation
- Fixed the way in which it takes the title of the site
- Added content rules for user subscription and unsubscription
  [eikichi18]


0.1.7 (2018-06-19)
------------------

- Fixed buildout
  [eikichi18]


0.1.6 (2018-06-19)
------------------

- Fixed some minor label
  [eikichi18]


0.1.5 (2018-05-25)
------------------

- fixed default profile in upgrade step
  [eikichi18]


0.1.4 (2018-05-23)
------------------

- upgrade step to fix bundle for initializedModal.js
  [eikichi18]


0.1.3 (2018-05-23)
------------------

- Fixed accessibility problem on subscribe/unsubscribe modal for IE.
  [eikichi18]


0.1.2 (2018-03-15)
------------------

- Fixed accessibility and style for subscribe/unsubscribe modal.
  [eikichi18]


0.1.1 (2018-03-02)
------------------

- Fixed doc.
  [eikichi18]


0.1.0 (2018-03-02)
------------------

- Initial release.
  [eikichi18]
