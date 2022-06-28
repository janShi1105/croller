from feedgen.feed import FeedGenerator

from feedgen_ext import BookEntryExtension, BookFeedExtension

def create_feed():

    fg = FeedGenerator()

    fg.register_extension(
        'book',
        extension_class_feed=BookFeedExtension,
        extension_class_entry=BookEntryExtension,
    )

    fg.title("芥川龍之介の新着作品")
    fg.link(href="http://aozora.gr.jp/index_pages/person879.html")
    fg.description("青空文庫に...")

    fe = fg.add_entry()

    fe.title("羅生門")
    fe.link(href="http://www.aozora.gr.jp/cards/000879/card128.html")
    fe.description('<a href="http://www.aozora.gr.jp/index_pages/person879.html">芥川</a>の5作目の短編小説')
    fe.book.writer({'name':"芥川龍之介", 'id': "879"})

    return fg.rss_str(pretty=True)

if __name__ == '__main__':
    rss_str = create_feed()
    print(rss_str.decode())