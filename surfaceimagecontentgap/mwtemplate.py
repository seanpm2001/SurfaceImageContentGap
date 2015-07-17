# -*- coding: utf-8 -*-

"""Search for articles with a given template."""

import logging


import mwclient

LOGGER_NAME = 'sicglog'
LOG = logging.getLogger(LOGGER_NAME)


class ArticleWithTemplate(object):

    """Search article with a given template."""

    def __init__(self, site, templatename):
        """Constructor."""
        self.site = site
        self.templatename = templatename
        if 'Template:' not in templatename:
            self.templatename = 'Template:' + templatename

    def listarticles(self):
        """List of articles containing a given template."""
        result = []
        has_continue = True
        eicontinue = None
        while has_continue:
            LOG.info("Searching for article with template...size %d %s",
                     len(result),
                     eicontinue)
            api_result = self.queryapi(eicontinue)
            result += self.parse_result(api_result)
            if 'query-continue' in api_result:
                has_continue = True
                eicontinue = self.parse_eicontinue(api_result)
            else:
                has_continue = False
        return result

    def queryapi(self, eicontinue):
        """Send the query to wikipedia."""
        if eicontinue is None:
            return self.site.api('query',
                                 list='embeddedin', rawcontinue='',
                                 eilimit='max',
                                 eititle=self.templatename)
        else:
            return self.site.api('query', eicontinue=eicontinue,
                                 list='embeddedin', rawcontinue='',
                                 eilimit='max',
                                 eititle=self.templatename)

    @staticmethod
    def parse_eicontinue(api_result):
        """The eicontinue of the api_result."""
        return api_result['query-continue']['embeddedin']['eicontinue']

    def parse_result(self, api_result):
        """Returns list of articles from result of api."""
        if 'query' in api_result:
            if 'embeddedin' in api_result['query']:
                return [mwclient.page.Page(self.site, a['title'])
                        for a in api_result['query']['embeddedin']
                        ]
            else:
                []
        else:
            []
