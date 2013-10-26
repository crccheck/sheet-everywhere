import json

from gdata.service import RequestError
from gspreadsheet import GSpreadsheet
from tornado.options import define, options, parse_command_line
import tornado.ioloop
import tornado.web


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # TODO write templates/index.html
        self.write("Hello, world!")


class RobotsHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'text/plain')
        self.write('User-agent: *\nDisallow: /')


class SpreadsheetHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self, key):
        try:
            sheet = GSpreadsheet(key=key)
        except RequestError:
            raise tornado.web.HTTPError(404, u'Spreadsheet Not Found')
        output = json.dumps(list((x.copy() for x in sheet)))
        callback = self.get_argument('callback', None)
        if callback:
            # return jsonp version
            output = '{0}({1})'.format(callback, output)
            self.set_header("Content-Type", "application/javascript")
        else:
            self.set_header("Content-Type", "application/json")
        self.write(output)


application = tornado.web.Application([
        (r'/(\w+)/?', SpreadsheetHandler),
        (r'/robots.txt', RobotsHandler),
        (r'/', IndexHandler),
    ],
    # debug=True,
    gzip=True,
)


if __name__ == "__main__":
    define("port", default=5000, help="run on the given port")
    parse_command_line()
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
