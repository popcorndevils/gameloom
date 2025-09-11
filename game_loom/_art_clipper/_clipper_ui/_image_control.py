import io
from tkinter import ttk as tw
from PIL import Image, ImageTk
from ..filecabinet import ImageObj
from ...LoomTypes._loomframe import LoomFrame


class ImageControl(LoomFrame):
    def __init__(self, img: ImageObj, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.MAX_WIDTH = 400
        self.MAX_HEIGHT = 400
        self._img = img

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self._frm_prefix = tw.Frame(self)
        self._lbl_image = tw.Label(self, justify="center", anchor="center", cursor="hand2", padding=5)
        self._lbl_prefix = tw.Label(self._frm_prefix, justify="center", anchor="center", padding=5, text="Prefix")
        self._etr_prefix = tw.Entry(self._frm_prefix, textvariable=img.prefix_var)
        self._chk_extract = tw.Checkbutton(self, text="Extract", variable=img.selected_var)

        self._frm_prefix.columnconfigure(0, weight=1)
        self._frm_prefix.rowconfigure(0, weight=1)

        self._lbl_image.grid(column=0, row=0, sticky="nsew")
        self._frm_prefix.grid(column=0, row=1, sticky="s")
        self._lbl_prefix.grid(column=0, row=0)
        self._etr_prefix.grid(column=1, row=0)
        self._chk_extract.grid(column=0, row=2, sticky="s")

        # set image
        self.image_data = img.extract_image()

        self.bind("<Configure>", self._resize_image)
        self._lbl_image.bind("<Enter>", self._on_enter)
        self._lbl_image.bind("<Leave>", self._on_leave)
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
        # 1. Get original image dimensions
        ori_w, ori_h = img.size
        if ori_w <= 0 or ori_h <= 0:
            return img.resize((1, 1), Image.LANCZOS)

        # 2. Get available space from the widget's current size, with padding
        padding = 10
        box_w = self.winfo_width() - padding
        box_h = self.winfo_height() - padding

        # If the widget is not yet drawn, its size is 1x1. Return a placeholder.
        if box_w <= 1 or box_h <= 1:
            return img.resize((1, 1), Image.LANCZOS)

        # 3. Apply constraints to find the target box size for the image
        # Constraint A: The box cannot be larger than our predefined maximums.
        target_w = min(box_w, self.MAX_WIDTH)
        target_h = min(box_h, self.MAX_HEIGHT)

        # Constraint B: Enforce a max aspect ratio for the display box itself.
        # This prevents a tall, thin image from creating an overly tall cell.
        max_display_ratio = 1.5
        if target_h > target_w * max_display_ratio:
            target_h = int(target_w * max_display_ratio)

        # 4. Calculate new image size, maintaining aspect ratio, to fit the target box
        ratio_diff = min(target_w / ori_w, target_h / ori_h)
        new_width = max(int(ori_w * ratio_diff), 1)
        new_height = max(int(ori_h * ratio_diff), 1)

        return img.resize((new_width, new_height), Image.LANCZOS)

    def _resize_image(self, event):
        if self.original_image:
            if self.winfo_width() > 1 and self.winfo_height() > 1:
                self.tk_image = ImageTk.PhotoImage(self._fit_frame(self.original_image))

    def _handle_label_click(self, _):
        self._img.is_selected = not self._img.is_selected

    def _on_enter(self, event):
        """Changes the border to indicate the widget is interactive."""
        self._lbl_image.config(relief="groove", borderwidth=2)

    def _on_leave(self, event):
        """Resets the border when the mouse leaves."""
        self._lbl_image.config(relief="flat", borderwidth=0)
