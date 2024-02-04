import flet as ft
import os
import sys
sys.path.append(os.getcwd())
from views.treasure_dialogs.pdf2word import Dialog as pdf2wordDialog
from views.treasure_dialogs.checkcovareas import Dialog as covAreaDialog
from views.treasure_dialogs.selectweather import Dialog as weatherDialog
from views.treasure_dialogs.rename_txt_image_name import Dialog as renamefilename

class ViewPage(ft.Stack):
    def __init__(self, page):
        self.grid = ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=150,
            child_aspect_ratio=1.0,
            spacing=10,
            run_spacing=10,
            padding=100,
        )
        self.pdf2word = ft.Stack(
            [
                ft.OutlinedButton(
                    "pdf转word",
                    icon=ft.icons.PICTURE_AS_PDF_OUTLINED,
                    width=200,
                    height=50,
                    on_click=self.open_pdf2word,
                )
            ]
        )
        self.cov_area = ft.Stack(
            [
                ft.OutlinedButton(
                    "高风险地区",
                    icon=ft.icons.PICTURE_AS_PDF_OUTLINED,
                    width=200,
                    height=50,
                    on_click=self.open_cov_area,
                )
            ]
        )

        self.weather_query = ft.Stack(
            [
                ft.OutlinedButton(
                    "天气预报",
                    icon=ft.icons.PICTURE_AS_PDF_OUTLINED,
                    width=200,
                    height=50,
                    on_click=self.open_weathervision,
                )
            ]
        )

        self.rename_file = ft.Stack(
            [
                ft.OutlinedButton(
                    "重命名文件",
                    icon=ft.icons.PICTURE_AS_PDF_OUTLINED,
                    width=200,
                    height=50,
                    on_click=self.open_renamefilename,
                )
            ]
        )

        self.grid.controls.extend([self.pdf2word, self.cov_area, self.weather_query, self.rename_file])
        super(ViewPage, self).__init__([self.grid])

    def open_pdf2word(self, e):
        self.page.dialog = pdf2wordDialog()
        self.page.update()
        self.page.dialog.open_dlg(None)

    def open_cov_area(self, e):
        self.page.dialog = covAreaDialog()
        self.page.update()
        self.page.dialog.open_dlg(None)

    def open_weathervision(self, e):
        self.page.dialog = weatherDialog()
        self.page.update()
        self.page.dialog.open_dlg(None)

    def open_renamefilename(self, e):
        self.page.dialog = renamefilename()
        self.page.update()
        self.page.dialog.open_dlg(None)

# def main(page: ft.Page):
#     page.title = "aaaa"
#     a = ViewPage(page)
#     page.add(a)


# ft.app(
#     target=main,
# )