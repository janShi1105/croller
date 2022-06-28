from csv import writer
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
    """XMLを作る."""
    elm_root = ET.Element("catalog")
    writers  = Writer.all()
    writers.load("works", "works.mojidukai_type")
    for writer in writers:
        for work in writer.works:
            elm_work = ET.SubElement(elm_root, "work", id=str(work.id))
            ET.SubElement(elm_work, "writer", id=str(writer.id)).text = writer.name
            ET.SubElement(elm_work, "title").text = work.title
            ET.SubElement(elm_work, "mojidukai_type", id=str(work.mojidukai_type.id)).text = work.mojidukai_type.name
            ET.SubElement(elm_work, "url").text  = work.build_url()
    with minidom.parseString(ET.tostring(elm_root, 'utf-8')) as dom:
        return dom.toprettyxml(indent="  ")


if __name__ == "__main__":
    xml_str = create_xml()
    print(xml_str)
        
