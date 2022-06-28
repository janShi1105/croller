from multiprocessing import connection
import feedparser
import MySQLdb


# start db
connection = MySQLdb.connect(
    user="scrapingman",
    passwd="myPassword-1",
    host="localhost",
    db="scrapingdata",
    charset="utf8"
)

#create cursor
cursor = connection.cursor()

#delete tables
cursor.execute('drop table if exists books')

# create table
cursor.execute('create  table books (title text, url text)')

# Get FeedparserDictObject
rss = feedparser.parse("https://www.shoeisha.co.jp/rss/index.xml")

# Get RSS version
print(rss.version)

# Output the title of feed and the date contents published 
print(rss['feed']['title'])
print(rss['feed']['published'])

# Output the title of entries and link
for content in rss["entries"]:
    cursor.execute('insert into books values(%s, %s)', (content["title"], content['link']))

# Commit
connection.commit()

# Close
connection.close()