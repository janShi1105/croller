from csv import writer
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import logging

from orator import DatabaseManager, Model
from orator.orm import belongs_to ,has_many

logger = logging.getLogger('orator.connection.queries')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    'It took %(elapsed_time)sms to execute the query  %(query)s'
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger.addHandler(handler)

config = {
    'mysql': {
        'driver': 'mysql',
        'host': 'localhost',
        'database': 'aozora_bunko',
        'user': 'root',
        'password': '',
        'prefix': '',
        'log_queries': True
    }
}

db = DatabaseManager(config)
Model.set_connection_resolver(db)

class MojidukaiType(Model):
    """文字遣い種別."""

    pass

class Work(Model):
    """作品."""

    URL_FORMAT = "https://www.aozora.gr.jp/cards/{writer_id:06d}/card{id}.html"

    @belongs_to
    def mojidukai_type(self):
        """この作品の文字遣い."""
        return MojidukaiType

    @belongs_to
    def writer(self):
        """この作品の作家."""
        return writer

    def build_url(self):
        """作品URLを構築する."""
        return self.URL_FORMAT.format(
            writer_id = self.writer_id,
            id = self.id
        )

class Writer(Model):
    """作家."""

    @has_many
    def works(self):
        """この作家の作品群."""
        return Work

def create_xml():
    """JSONを作る."""
    works = []
    writers = Writer.all()
    writers.load('works', 'works.mojidukai_type')
    for writer in writers:
        for work in writer.works:
            d = {}
            d['id'] = work.id
            d['title'] = work.title
            d['url'] = work.build_url()
            d['writer'] = {'id': writer.id, 'name': writer.name}
            d['mojidukai_type'] = {'id': work.mojidukai_type.id, 'name': work.mojidukai_type.name}

            works.append(d)
    return  json.dumps(works, ensure_ascii=False, indent=2)
 


if __name__ == "__main__":
    xml_str = create_xml()
    print(xml_str)
        
