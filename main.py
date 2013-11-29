import json
import os

from dogpile.cache import make_region
from gdata.service import RequestError
from gspreadsheet import GSpreadsheet
from tornado.options import define, options, parse_command_line
import tornado.ioloop
import tornado.web

NOT_FOUND = False

# `heroku addons:add redistogo:nano`
redis_url = os.environ.get('REDISTOGO_URL')
if redis_url:
    region = make_region().configure(
        'dogpile.cache.redis',
        expiration_time=3600,  # one hour
        arguments={
            'url': redis_url,
        },
    )
else:
    region = make_region().configure(
        'dogpile.cache.memory',
        expiration_time=300,  # five minutes
    )


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        import markdown
        with open('README.md') as f:
            self.write(markdown.markdown(f.read()))


class RobotsHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'text/plain')
        self.write('User-agent: *\nDisallow: /')


class SpreadsheetHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self, key):
        gid = self.get_argument('gid', 0)
        cache_key = u'{}#{}'.format(key, gid)
        # TODO add cache invalidation
        output = region.get(cache_key)
        if output == NOT_FOUND:
            raise tornado.web.HTTPError(404, u'Spreadsheet Not Found (cached)')

        if not output:
            try:
                worksheet = int(gid) + 1
                sheet = GSpreadsheet(key=key, worksheet=worksheet)
            except RequestError:
                region.set(cache_key, NOT_FOUND)
                raise tornado.web.HTTPError(404, u'Spreadsheet Not Found')
            except ValueError:
                # TODO show invalid gid help message?
                region.set(cache_key, NOT_FOUND)
                raise tornado.web.HTTPError(404,
                        u'Spreadsheet/Worksheet Not Found')
            output = json.dumps(list((x.copy() for x in sheet)))

        region.set(cache_key, output)
        callback = self.get_argument('callback', None)
        if callback:
            # return jsonp version
            output = '{0}({1})'.format(callback, output)
            self.set_header("Content-Type", "application/javascript")
        else:
            self.set_header("Content-Type", "application/json")
        self.write(output)


if __name__ == "__main__":
    define("port", default=5000, help="run on the given port")
    define("debug", default=False, help="enable debug mode")
    parse_command_line()

    application = tornado.web.Application([
            (r'/([\-\w]+)/?', SpreadsheetHandler),
            (r'/robots.txt', RobotsHandler),
            (r'/', IndexHandler),
        ],
        debug=options.debug,
        gzip=True,
    )

    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
