import os
from tkinter import filedialog
from tkinter import ttk as tw
from ..filecabinet import FileCabinet
from ...LoomTypes import LoomFrame


class PageExport(LoomFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cabinet: FileCabinet = None
        self._placeholder = tw.Button(self, text="Save Images", command=self._on_save)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self._placeholder.grid(column=0, row=0)

    def _on_save(self):
        folder = filedialog.askdirectory()
        if not folder:  # User cancelled the dialog
            return

        extract_list = self.cabinet.extract_list
        for pdf_name, images in extract_list.items():
            for img in images:
                # Get the image data to determine the correct file extension
                image_data = img.extract_image()
                ext = image_data.get("ext", "png")  # Default to 'png' if not found

                # Construct a descriptive filename and save the image
                if img.prefix != "":
                    save_path = os.path.join(folder, f"{img.prefix}_{pdf_name}_p{img.page_index}_i{img.image_index}.{ext}")
                else:
                    save_path = os.path.join(folder, f"{pdf_name}_p{img.page_index}_i{img.image_index}.{ext}")
                img.save_to_file(save_path)

    @property
    def cabinet(self):
        return self._cabinet

    @cabinet.setter
    def cabinet(self, val):
        self._cabinet = val
