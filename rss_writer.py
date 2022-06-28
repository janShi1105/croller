import xml.etree.ElementTree as ET
from xml.dom import minidom

NAMESPACES = {'book': 'http://my-service.com/xmlns/book'}


def create_rss():
    for ns_name, ns_uri in NAMESPACES.items():
        ET.register_namespace(ns_name,  ns_uri)

    elm_rss = ET.Element(
        "rss",
        attrib={
            'version': "2.0",
            'xmlns:book': NAMESPACES['book']
        },
    )

    elm_channel = ET.SubElement(elm_rss, 'channel')

    channel_sources = {
        'title': "芥川龍之介の新着作品",
        'link': "http://www.aozora.gr.jp/index_pages/person879.html",
        'description': "青空文庫に追加された芥川龍之介の新着作品のフィード",
    }
    children_of_channel = []
    for tag, text in channel_sources.items():
        child_elm_of_channel = ET.Element(tag)
        child_elm_of_channel.text = text
        children_of_channel.append(child_elm_of_channel)

    elm_channel.extend(children_of_channel)

    elm_item = ET.SubElement(elm_channel, 'item')

    elm_item_title = ET.SubElement(elm_item, 'title')
    elm_item_title.text = "羅生門"

    elm_item_link = ET.SubElement(elm_item, 'link')
    elm_item_link.text = "https://www.aozora.gr.jp/cards/000879/card128.html"

    elm_item_description = ET.SubElement(elm_item, 'description')
    elm_item_description.text \
        = ('<a href="http://www.aozora.gr.jp/index_pages/person879.html">芥川龍之介</a>の5作目の短編小説'
        "次の作品『今昔物語集』巻二十九「...」に題材を取り、人間のエゴイズムについて作者自身の解釈を加えたものである")

    elm_item_writer = ET.SubElement(elm_item, 'book:writer', id='879')
    elm_item_writer.text = "芥川　龍之介"

    xml = ET.tostring(elm_rss, 'utf-8')

    with minidom.parseString(xml) as dom:
        return dom.toprettyxml(indent="  ")

if __name__ == '__main__':
    rss_str = create_rss()
    print(rss_str)

    