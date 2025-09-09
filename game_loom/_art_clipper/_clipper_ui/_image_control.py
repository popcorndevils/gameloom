import io
from tkinter import StringVar, BooleanVar
from tkinter import ttk as tw
from PIL import Image, ImageTk
from ...LoomTypes._loomframe import LoomFrame


class ImageControl(LoomFrame):
    def __init__(self, *args, max_height_container=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._max_height_container = max_height_container
        self._name_override = StringVar()
        self._extract_image = BooleanVar()

        # NEW: A variable to hold the ID of a scheduled 'after' job
        self._after_id = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self._lbl_image = tw.Label(self, justify="center", anchor="center", cursor="hand2")
        self._txt_name = tw.Entry(self, textvariable=self._name_override)
        self._chk_extract = tw.Checkbutton(self, text="Extract", variable=self._extract_image)

        self._lbl_image.grid(column=0, row=0, sticky="nsew")
        self._txt_name.grid(column=0, row=1, sticky="s")
        self._chk_extract.grid(column=0, row=2, sticky="s")

        self.bind("<Configure>", self._resize_image)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self._lbl_image.bind("<Button-1>", self._handle_label_click)

    @property
    def frame_size(self):
        return (self.winfo_width(), self.winfo_height())

    @property
    def image_data(self):
        return self._image_data

    @image_data.setter
    def image_data(self, data):
        self._image_data = data["image"]
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
        self._lbl_image.configure(image=self.tk_image)

    def _fit_frame(self, img: Image):
        fr_w, fr_h = self.frame_size
        fr_w, fr_h = fr_w - 10, fr_h - 10

        if fr_w <= 1 or fr_h <= 1:
            return img.resize((1, 1), Image.LANCZOS)

        # Enforce absolute maximum height from the container ---
        if self._max_height_container:
            max_h = self._max_height_container.winfo_height() / 2
            fr_h = min(fr_h, max_h)

        # Enforce relative aspect ratio (so a cell doesn't get too tall and skinny)
        max_display_ratio = 1.5
        if fr_h > fr_w * max_display_ratio:
            fr_h = int(fr_w * max_display_ratio)

        # The rest of the function proceeds as normal
        ori_w, ori_h = img.size
        if ori_w <= 0 or ori_h <= 0:
            return img.resize((1, 1), Image.LANCZOS)

        ratio_diff = min(fr_w / ori_w, fr_h / ori_h)
        new_width = max(int(ori_w * ratio_diff), 1)
        new_height = max(int(ori_h * ratio_diff), 1)

        return img.resize((new_width, new_height), Image.LANCZOS)

    def _resize_image(self, event):
        if self.original_image:
            if self.winfo_width() > 1 and self.winfo_height() > 1:
                self.tk_image = ImageTk.PhotoImage(self._fit_frame(self.original_image))

    def _handle_label_click(self, _):
        self._extract_image.set(not self._extract_image.get())

    def _on_enter(self, event):
        """Changes the border to indicate the widget is interactive."""
        self.config(relief="groove", borderwidth=2)

    def _on_leave(self, event):
        """Resets the border when the mouse leaves."""
        self.config(relief="flat", borderwidth=0)
