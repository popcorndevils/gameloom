import io
import logging
from tkinter import ttk as tw
from PIL import Image, ImageTk
from ...LoomTypes._loomframe import LoomFrame


class ImageControl(LoomFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._image_data = None
        self._original_image = None
        self._tk_image = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self._fr_image = tw.Frame(self)

        self._fr_image.rowconfigure(0, weight=1)
        self._fr_image.columnconfigure(0, weight=1, minsize=100)
        self._fr_image.rowconfigure(0, weight=1, minsize=100)
        self._fr_image.grid(column=0, row=0, sticky="nsew")

        self._image_display = tw.Label(self._fr_image, text="HELLO THERE")
        self._image_display.grid(column=0, row=0, sticky="nsew")

        self._fr_image.bind("<Configure>", self._resize_image)

    @property
    def frame_size(self):
        return (self._fr_image.winfo_width(), self._fr_image.winfo_height())

    @property
    def image_data(self):
        return self._image_data

    @image_data.setter
    def image_data(self, data):
        self._image_data = data["image"]
        logging.info(f"image data {type(self.image_data)} loaded")
        self.original_image = Image.open(io.BytesIO(self.image_data))

    @property
    def original_image(self):
        return self._original_image

    @original_image.setter
    def original_image(self, image: Image):
        self._original_image = image
        _fit_img = self._fit_frame(self.original_image)
        self.tk_image = ImageTk.PhotoImage(_fit_img)

    @property
    def tk_image(self):
        return self._tk_image

    @tk_image.setter
    def tk_image(self, image: ImageTk.PhotoImage):
        self._tk_image = image
        self._image_display.configure(image=self.tk_image)

    def _fit_frame(self, img: Image):
        fr_w, fr_h = self.frame_size
        ori_w, ori_h = img.size
        ratio_diff = min(fr_w / ori_w, fr_h / ori_h)
        new_width = int(ori_w * ratio_diff)
        new_height = int(ori_h * ratio_diff)

        return img.resize((new_width, new_height), Image.LANCZOS)

    def _resize_image(self, _):
        if self.original_image:
            self.tk_image = ImageTk.PhotoImage(self._fit_frame(self.original_image))
