import os
import io
import logging
import pymupdf


class FileCabinet:
    def __init__(self):
        logging.info("FileCabinet loaded.")
        self._files = {}

    def add(self, file: str):
        if not isinstance(file, io.TextIOWrapper):
            raise ValueError("Unexpected value")

        try:
            _fname = os.path.basename(file.name)
            _pdf = pymupdf.open(file)
            self._files[_fname] = _pdf
            logging.info(f"File {_fname} loaded.  Document is {_pdf.page_count} pages.")
        except Exception as e:
            logging.error(f"Unable to load file {str(file)}.  {e}")

    @property
    def file_names(self):
        return [k for k in self._files]

    def __getitem__(self, key):
        return self._files[key]
