import os
import tempfile
from collections import OrderedDict

import pywal
import tornado.ioloop
import tornado.web

import ui_methods


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        file1 = self.request.files.get("file1")[0]
        infile = tempfile.NamedTemporaryFile("w+b")
        infile.write(file1['body'])

        path = pywal.image.get(infile.name)
        backend = self.get_argument("backend")
        light = True if self.get_argument("light") == "True" else False
        colors = pywal.colors.get(path, light=light, backend=backend)
        exp_type = self.get_argument("export")
        out = tempfile.NamedTemporaryFile("w+")
        pywal.export.color(colors, exp_type, out.name)
        infile.seek(0)

        order = [
            ("bg", "background"), ("fg", "foreground"), ("0", "color0"), ("8", "color8"), ("1", "color1"),
            ("9", "color9"), ("2", "color2"), ("10", "color10"), ("3", "color3"), ("11", "color11"),
            ("4", "color4"), ("12", "color12"), ("5", "color5"), ("13", "color13"), ("6", "color6"),
            ("14", "color14"), ("7", "color7"), ("15", "color15")
        ]
        flatten_colors = {
            **colors["special"],
            **colors["colors"]
        }
        colors = OrderedDict()
        for label, k in order:
            colors[label] = flatten_colors[k]

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
            "json": "colors.json",
            "konsole": "colors-konsole.colorscheme",
            "plain": "colors",
            "putty": "colors-putty.reg",
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
        ui_methods=ui_methods,
        debug=True,
    )
    app.listen(os.environ.get("PORT", 8080))
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
