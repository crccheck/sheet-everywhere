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


class SpreadsheetHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self, key):
        try:
            sheet = GSpreadsheet(key=key)
        except RequestError:
            raise tornado.web.HTTPError(404, u'Spreadsheet Not Found')
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(list((x.copy() for x in sheet))))


application = tornado.web.Application([
    (r'/(\w+)/?', SpreadsheetHandler),
    (r'/', IndexHandler),
], debug=True)


if __name__ == "__main__":
    define("port", default=5000, help="run on the given port")
    parse_command_line()
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
