from lxml.etree import parse
from grab.spider import Spider
from settings import DB_URI, DB_NAME, SPIDER_CONFIG


class BaseSpider(Spider):
    data_science_blogs_list = 'var/data-science.opml'

    @classmethod
    def parse_blogs_list(cls):
        opml = parse(cls.data_science_blogs_list)
        for outline in opml.findall("//outline/outline"):
            blog = {
                'title': outline.get('title'),
                'rss': outline.get('xmlUrl'),
                'html': outline.get('htmlUrl'),
            }
            yield blog

    @classmethod
    def get_instance(cls, use_proxy=False,
                     use_cache=False, **kwargs):
        """ Create and setup spider instance instance.
        """

        bot = cls(**SPIDER_CONFIG)

        if use_proxy:
            # yes, grab provides feature to easily use proxies
            # (and even auto change them for requests) out of the box
            bot.load_proxylist('var/proxylist.txt', 'text_file', 'http',
                               auto_change=True)
        if use_cache:
            # it would be inefficiently to download pages from web each run
            # during development. So there is ability to use various
            # caching backends. For this project i use mongodb
            # to store scraped data and requests cache.

            # mongodb uri could contain auth parameters (usr/pwd)
            # in case if you're using remote mongodb instance
            # or cloud like mongolab
            host = DB_URI.format('')  # leave database param empty

            bot.setup_cache(
                backend='mongo',
                database=DB_NAME,
                use_compression=True, host=host)

        # default grab object configuration
        bot.setup_grab(timeout=20, connect_timeout=20)

        # setup additional class parameters
        for key, value in kwargs.items():
            setattr(bot, key, value)

        return bot
