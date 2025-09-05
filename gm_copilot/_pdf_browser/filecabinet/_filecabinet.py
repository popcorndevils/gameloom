import logging
import fitz


class FileCabinet:
    def __init__(self, files = None):
        logging.info("FileCabinet loaded.")
        self._files = []

        if files is not None:
            if isinstance(files, list):
                self._files += files
            else:
                self._files.append(files)
            logging.info(f"{len(self._files)} files have been loaded.")

    def add(self, files):
        if isinstance(files, list):
            for f in files:
                _pdf = fitz.open(f)
                logging.info(f"PDF {str(_pdf)} loaded.")
                self._files.append(_pdf)
        else:
            _pdf = fitz.open(files)
            self._files.append(_pdf)
