from tkinter import ttk as tw


class PDFBrowser(tw.Frame):
    def __init__(self, root):
        super().__init__(root, padding=5)
        self.root = root
        self.grid(column=0, row=0, sticky="nesw")

        # configure frame layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(1, minsize=5)

        # Placeholder
        self._button1 = tw.Button(
            self,
            text="TEST BUTTON 1",
            command=self._handle_click
        )

        self._button2 = tw.Button(
            self,
            text="TEST BUTTON 2",
            command=self._handle_click
        )

        self._button1.grid(column=0, row=0, sticky="nesw")
        self._button2.grid(column=0, row=2, sticky="nesw")

    def _handle_click(self):
        print("PDF_BROWSER")
