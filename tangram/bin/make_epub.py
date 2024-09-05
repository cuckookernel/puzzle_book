import datetime as dt
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from ebooklib import epub
from ebooklib.epub import EpubBook, EpubHtml
from tangram.bin.common import PZLS_PATH, SOLS_PATH
from tangram.bin.download_renamer import downloads_to_solution_dir
from tangram.bin.solution_to_puzzle import make_puzzles_from_solutions

# define css style
STYLE = """
@namespace epub "http://www.idpf.org/2007/ops";
body {
    font-family: Cambria, Liberation Serif, Bitstream Vera Serif, Georgia, Times, Times New Roman, serif;
}
h2 {
     text-align: left;
     text-transform: uppercase;
     font-weight: 200;
}
ol {
        list-style-type: none;
}
ol > li:first-child {
        margin-top: 0.3em;
}
nav[epub|type~='toc'] > ol > li > ol  {
    list-style-type:square;
}
nav[epub|type~='toc'] > ol > li > ol > li {
        margin-top: 0.3em;
}
"""
# %%


def _main():
    # %%
    runfile("./tangram/bin/make_epub.py")
    downloads_to_solution_dir()
    make_puzzles_from_solutions()
    # %%
    pzl_ch_to_files = chapter_to_files(base_path=PZLS_PATH)
    sol_ch_to_files = chapter_to_files(base_path=SOLS_PATH)

    maker = BookMaker(lang="es")
    maker.make(pzl_ch_to_files, sol_ch_to_files)

    maker.final_render()
    # %%


TRNSL = {
    "es": {
        "abstract": "abstractos",
        "airplanes": "aviones",
        "aquatic-beasts": "animales acuáticos",
        "artifacts": "artefactos",
        "birds": "aves",
        "buildings": "construcciones",
        "cats": "gatos",
        "convex": "convexos",
        "geometric": "geométricos",
        "land-animals": "animales terrestres",
        "letters": "letras",
        "people": "personas",
        "plants": "plantas",
        "ships": "barcos",
        "tools": "herramientas",
        "toys": "juguetes",
        "tangram universe": "universo tangram",
        "solutions": "soluciones",
        "symbols": "símbolos",
        "puzzles": "acertijos",
        "wbg-transformed": "otros",
        "see solution": "Ver solucion",
    },
    "de": {
        "abstract": "Abstrakt",
        "airplanes": "Flugzeuge",
        "aquatic-beasts": "Wassertiere",
        "artifacts": "Geräte",
        "birds": "V“ogel",
        "buildings": "Gebäude",
        "people": "Leute",
        "ships": "Schiffe",
        "tools": "herramientas",
        "toys": "Spielzeuge",
        "puzzles": "Rätsel",
        "solutions": "Lösungen",
        "tangram universe": "Tangram Universum",
    },
}


class BookMaker:
    def __init__(self, lang):
        self.translator = TRNSL[lang]

        book = epub.EpubBook()

        book.set_identifier('asdasd12312')
        book.set_title( self.title('tangram universe') )
        book.set_language('es')

        book.add_author('Teo Restrepo')

        self.book: EpubBook = book
        self.spine = []

    def make(self, pzl_ch_to_files, sol_ch_to_files):

        self.make_puzzles_page()
        pzl_chs = []
        for ch_name, files in pzl_ch_to_files.items():
            ch_front_pg = self._make_chapter_front(ch_name, 'puzzles')
            pzl_chs.append(ch_front_pg)
            ch_pgs = [ self.make_single_page(ch_name, idx, pzl_img_path, prefix='puzzles')
                       for idx, pzl_img_path in enumerate(files) ]
            # pzl_chs.append( (epub.Section(self.title(ch_name)), ch_pgs) )

        self.make_solutions_page()
        sol_chs = []
        for ch_name, files in sol_ch_to_files.items():
            ch_front_pg = self._make_chapter_front(ch_name, 'solutions')
            sol_chs.append(ch_front_pg)

            ch_pgs = [ self.make_single_page(ch_name, idx, sol_img_path, prefix='solutions')
                       for idx, sol_img_path in enumerate(files) ]

            # sol_chs.append( (epub.Section(self.title(ch_name)), ch_pgs) )

        self.book.toc = (
            # epub.Link(puzzles_pg.file_name, puzzles_pg.title, puzzles_pg.id),
            (epub.Section(self.translator['puzzles'].title()),
             tuple(pzl_chs)),
            (epub.Section(self.translator['solutions'].title()),
             tuple(sol_chs)),
        )

    def title(self, a_str: str, caps: bool = True):
        translated = self.translator[a_str]
        return translated.title() if caps else translated

    def add_item(self, item):
        self.book.add_item(item)
        self.spine.append(item)

    def make_puzzles_page(self ):
        pg = epub.EpubHtml(title='Acertijos', file_name='puzzles.xhtml', lang='es')
        pg.content = '<h1>Acertijos</h1>'
        self.add_item(pg)

        return pg
    # %%

    def _make_chapter_front(self, name: str, suffix: str):
        pg = epub.EpubHtml(title=self.translator[name].title(),
                           file_name=f'{name}-{suffix}.xhtml', lang='es')
        pg.content = f'<h1>{self.title(name)}</h1>'
        self.add_item(pg)

        return pg

    def make_solutions_page(self):
        pg = epub.EpubHtml(title=self.translator['solutions'],
                           file_name='solutions.xhtml', lang='es')
        pg.content = f'<h1>{self.title("solutions")}</h1>'

        self.add_item(pg)

        return pg

    def make_single_page(self, ch_name: str, idx: int, img_path: Path, prefix: str) -> EpubHtml:
        name = f"{self.title(ch_name)} - {idx}"

        assert img_path.suffix.endswith('png'), f"{img_path} is not PNG!"

        # filename inside epub package:
        epub_file_name = f"{prefix}/{ch_name}/{img_path.name}"
        img_content = img_path.open('rb').read()
        img = epub.EpubItem(file_name=epub_file_name, media_type="image/png", content=img_content)
        self.book.add_item(img)

        pg = epub.EpubHtml(title=name, file_name=f'{img_path.stem}.xhtml', lang='es')

        if prefix == "puzzles":
            puzzle_stem = img_path.stem
            sol_stem = puzzle_stem.replace('.puzzle', '')
            # print(f'sol_file_name = {sol_stem}.xhtml')
            pg.content = f"""<p><img src="{epub_file_name}" /></p>
                         <p><a epub:type="noteref" href="{sol_stem}.xhtml">
                                {self.title('see solution')}
                            </a>
                        </p>"""
        else:
            pg.content = f'<img src="{epub_file_name}" />'

        self.add_item(pg)

        return pg


    def final_render(self):
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())

        # add css file
        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css",
                                content=STYLE)
        self.book.add_item(nav_css)

        self.book.spine = ['nav'] + self.spine

        tstamp = dt.datetime.now().strftime("%H%M%S")

        output_file = f'universo-tangram-{tstamp}.epub'
        print(f"Producing: {output_file}")
        epub.write_epub(output_file, self.book, {})


def chapter_to_files(base_path: Path) -> Dict[str, List[Path]]:

    ignored_cnt = 0

    chapter_to_files = defaultdict(list)
    for item in base_path.glob('*'):
        if item.is_dir():
            chapter_to_files[item.name] = list(item.glob('*'))
            print(item.name, len(chapter_to_files[item.name]))
        else:
            ignored_cnt += 1

    print(f'Ignored cnt: {ignored_cnt}')

    return chapter_to_files
