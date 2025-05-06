'''This application will store and display the relevant :class:`~projects.models.Project` objects and associated data.

Current Functionality
=====================

* Displays and summarizes current and previous lab projects.
* There is a comment threads at each project served by Disqus.
* Projects will also link to the people working on that project (see the :mod:`personnel` app).
* Projects will also link to publications (see the :mod:`papers` app).
* Shows up in the website's sitemap.
* Projects show up in the lab projects RSS feeds.
* There is an API estabished which serves :class:`~projects.models.Project` information in json or xml format.  See :mod:`projects.api` for details.

Longer Term Goals
=================

* Another idea is to have hidden discussions of projects, or projects which are not publicly displayed and require a login.
* Projects appear on personnel and paper detail pages.
* It is possible to tweet, like (through facebook) or +1 (through google plus) a project, though the functionality of these are not yet refined.
* Potentially convert to a facebook app with custom actions and objects.
* Markup with opengraph tags and incorporate twitter cards.
* Projects are marked up with microdata markup from http://schema.org.  
'''