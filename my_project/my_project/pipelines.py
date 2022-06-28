from dataclasses import dataclass
from hashlib import sha256
from pyexpat import model
from bs4 import Tag

from orator import DatabaseManager, Model
from orator.orm import belongs_to_many

from my_project.settings import ORATOR_CONFIG


db = DatabaseManager(ORATOR_CONFIG)
Model.set_connection_resolver(db)

class Quote(Model):

    @belongs_to_many
    def tags(self):
        return Tag

class Tag(Model):

    @belongs_to_many
    def quote(self):
        return Quote

class DatabasePipeline(object):

    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(item)
        return item
    
    def close_spider(self,spider):
        for item in self.items:
            text_hash = sha256(
                item['text'].encode('utf8', 'ignore')
            ).hexdigest()
            exist_quote = Quote.where('text_hash', text_hash).get()
            if exist_quote:
                continue
            quote = Quote()
            quote.author = item['author']
            quote.text = item['text']
            quote.text_hash = text_hash
            quote.save()

            tags = []
            for tag_name in item['tags']:
                tag = Tag.where('name', tag_name).first()
                if not Tag:
                    tag = Tag()
                    tag.name = tag_name
                    tag.save()
                tags.append(tag)
                quote_tags = quote.tags()
                quote_tags.save(tag)