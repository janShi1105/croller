from csv import writer
import csv
import io
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
    """CSVを作る."""
    output = io.StringIO()
    csv_writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    header = ["id", "title", "url", "writer_id", "writer_name", "mojidukai_type_id","mojidukai_type_name"]
    csv_writer.writerow(header)

    writers = Writer.all()
    writers.load('works', 'works.mojidukai_type')
    for writer in writers:
        for work in writer.works:
            line = [
                work.id,
                work.title,
                work.build_url(),
                writer.id,
                writer.name,
                work.mojidukai_type.id,
                work.mojidukai_type.name
            ]
            csv_writer.writerow(line)
    return output.getvalue()
    

if __name__ == "__main__":
    xml_str = create_xml()
    print(xml_str)
        
