import os
import tempfile

import pywal
import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        file1 = self.request.files.get("file1")[0]
        infile = tempfile.NamedTemporaryFile("w+b")
        infile.write(file1['body'])

        path = pywal.image.get(infile.name)
        colors = pywal.colors.get(path)
        exp_type = self.get_argument("export")
        out = tempfile.NamedTemporaryFile("w+")
        pywal.export.color(colors, exp_type, out.name)
        infile.seek(0)
        colors["special"].pop("cursor")
        self.render("result.html", colors=colors, out=out.read(), out_name=self._get_export_type(exp_type),
                    wallpaper=infile.read())

    @staticmethod
    def _get_export_type(export_type):
        """Convert template type to the right filename."""
        return {
            "css": "colors.css",
            "dwm": "colors-wal-dwm.h",
            "st": "colors-wal-st.h",
            "tabbed": "colors-wal-tabbed.h",
            "gtk2": "colors-gtk2.rc",
            "json": "colors.json",
            "konsole": "colors-konsole.colorscheme",
            "plain": "colors",
            "putty": "colors-putty.reg",
            "rofi": "colors-rofi.Xresources",
            "scss": "colors.scss",
            "shell": "colors.sh",
            "sway": "colors-sway",
            "tty": "colors-tty.sh",
            "xresources": "colors.Xresources",
            "yaml": "colors.yml",
        }.get(export_type, export_type)


def main():
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/upload", UploadHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True,
    )
    app.listen(os.environ.get("PORT", 8080))
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
