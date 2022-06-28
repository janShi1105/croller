from os import device_encoding
from lxml import etree

from feedgen.ext.base import BaseExtension

class BookBaseExtension(BaseExtension):

    BOOK_NS = "http://my-service.com/xmlns/book"

    def __init__(self):
        self.__writer = {}

    def extend_ns(self):
        return {'book': self.BOOK_NS}

    def _extend_xml(self, elm):
        if self.__writer:
            writer = etree.SubElement(
                elm, 
                '{%s}writer' % self.BOOK_NS,
                attrib={'id': self.__writer.get('id')}
            )
            writer.text =  self.__writer.get('name')
        return elm

    def  writer(self, name_and_id_dict=None):
        if name_and_id_dict is not None:
            name = name_and_id_dict.get('name')
            id_ = name_and_id_dict.get('id')
            if name and id_:
                self.__writer = {'name': name, 'id': id_}
            elif not name and not id_:
                self.__writer = {}
            else:
                raise ValueError('nameとidは両方セットしてください')
        return self.__writer

class BookFeedExtension(BookBaseExtension):

    def extend_rss(self, rss_feed):
        channel = rss_feed[0]
        self._extend_xml(channel)

class BookEntryExtension(BookBaseExtension):

    def extend_rss(self, entry):
        self._extend_xml(entry)
    