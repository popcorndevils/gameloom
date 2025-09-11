import io
import pathlib
import logging
import pymupdf
from tkinter import StringVar, BooleanVar


class ImageObj:
    def __init__(self, page, img_i: int, img_ref: int, select_img: bool):
        self._page = page
        self._img_index = img_i
        self._img_ref = img_ref
        self._selected = BooleanVar()
        self._prefix = StringVar()

    @property
    def page(self):
        return self._page

    @property
    def page_index(self):
        return self._page.index

    @property
    def image_index(self):
        return self._img_index

    @property
    def image_ref(self):
        return self._img_ref

    @property
    def is_selected(self):
        return self._is_selected

    @is_selected.setter
    def is_selected(self, val: bool):
        self._is_selected = val

    @property
    def file(self):
        return self.page.file

    @property
    def prefix(self):
        return self._prefix.get()

    @prefix.setter
    def prefix(self, val: str):
        self._prefix.set(val)

    @property
    def is_selected(self):
        return self.selected_var.get()

    @is_selected.setter
    def is_selected(self, val: bool):
        self.selected_var.set(val)

    @property
    def prefix_var(self):
        return self._prefix

    @property
    def selected_var(self):
        return self._selected

    def extract_image(self):
        return self.file.extract_image(self.image_ref)

    def save_to_file(self, path: str):
        """Extracts the image data and saves it to the given path.
        Args:
            path (str): The full path (including filename) to save the image to.
        """
        with open(path, "wb") as f:
            f.write(self.extract_image()["image"])


class PageObj:
    def __init__(self, file, page_i: int, page: pymupdf.Page):
        self._file = file
        self._index = page_i
        self._page = page
        self._page_imgs = {
            im_i: ImageObj(self, im_i, img[0], False)
            for im_i, img in enumerate(page.get_images(full=True))
        }

    @property
    def index(self):
        return self._index

    @property
    def images(self):
        return self._page_imgs

    @property
    def file(self):
        return self._file

    def __iter__(self):
        return iter(self._page_imgs.values())

    def __getitem__(self, key):
        return self._page_imgs[key]


class PDFObj:
    def __init__(self, file: pymupdf.Document):
        self._file = file
        self._pages = {
            pg_num: PageObj(self, pg_num, file[pg_num]) for pg_num in range(file.page_count)
        }
        self._images_by_ref = {}

        for _pg in self:
            for _im in _pg:
                self._images_by_ref[_im.image_ref] = _im

    @property
    def page_count(self):
        return self._file.page_count

    @property
    def file(self):
        return self._file

    def extract_image(self, xref):
        return self._file.extract_image(xref)

    def get_image_by_ref(self, ref):
        return self._images_by_ref[ref]

    def __getitem__(self, key):
        return self._pages[key]

    def __iter__(self):
        return iter(self._pages.values())


class FileCabinet:
    def __init__(self):
        logging.info("FileCabinet loaded.")
        self._files = {}

    def add(self, file: str):
        if not isinstance(file, io.TextIOWrapper):
            raise ValueError("Unexpected value")

        try:
            _pdf = pymupdf.open(file)
            _fname = pathlib.Path(file.name).stem
            self._files[_fname] = PDFObj(_pdf)
            logging.info(f"File {_fname} loaded.  Document is {_pdf.page_count} pages.")
        except Exception as e:
            logging.error(f"Unable to load file {str(file)}.  {e}")

    @property
    def file_names(self):
        return [k for k in self._files]

    @property
    def extract_list(self):
        _output = {}
        for k, v in self._files.items():
            _output[k] = []
            for _p in v:
                _im_list = [_i for _i in _p if _i.is_selected]
                for _i in _im_list:
                    _output[k].append(_i)
        return _output

    def __getitem__(self, key):
        return self._files[key]
