import json
import os
import flet as ft
from utils import snack_bar, DESKTOP
from views.treasure_dialogs.base import BaseDialog
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    icons,
)

class Dialog(BaseDialog):
    def __init__(self):
        self.close_btn = ft.IconButton(
            icon=ft.icons.CLOSE_OUTLINED, on_click=self.close_dlg
        )
        self.choose_file_dialog_image = None
        self.choose_file_dialog_label = None
        self.image_folder_data = Text() # 存储图像文件夹的数据
        self.label_folder_data = Text() # 存储标签文件夹的数据
        self.choose_file_btn_image = ft.ElevatedButton(
            "请选择图像文件夹", on_click=self.open_image_dialog, width=300
        )
        self.choose_file_btn_label = ft.ElevatedButton(
            "请选择标签文件夹", on_click=self.open_label_dialog, width=300
        )
        self.prefix_input = ft.TextField(label="前缀：")
        self.rename_btn = ft.FilledButton(
            text="Go", on_click=self.rename_files
        )
        self.hint = ft.Text(
            "· 目前仅支持label为txt格式，image为jpg格式\n"
            "· 直接在源文件上修改，如果需要源文件，请提前复制源文件\n"
        )
        self.content = ft.Column([
            self.choose_file_btn_image,
            self.image_folder_data,
            self.choose_file_btn_label,
            self.label_folder_data,
            self.prefix_input,
            self.rename_btn,
            self.hint,
            
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        super(Dialog, self).__init__(
            title=ft.Text("重命名文件"),
            content=self.content,
            actions=[self.close_btn],
            actions_alignment="center",
        )

    def open_image_dialog(self, e):
        self.choose_file_dialog_image = ft.FilePicker(on_result=self.get_image_result)
        self.page.overlay.append(self.choose_file_dialog_image)
        self.page.update()
        self.choose_file_dialog_image.get_directory_path(dialog_title="选择图像文件夹")


    def open_label_dialog(self, e):
        self.choose_file_dialog_label = ft.FilePicker(on_result=self.get_label_result)
        self.page.overlay.append(self.choose_file_dialog_label)
        self.page.update()
        self.choose_file_dialog_label.get_directory_path(dialog_title="选择标签文件夹")


    # Open directory dialog
    def get_image_result(self, e: FilePickerResultEvent):
        self.image_folder_data.value = e.path if e.path else "Cancelled!"
        self.image_folder_data.update()

     # Open directory dialog
    def get_label_result(self, e: FilePickerResultEvent):
        self.label_folder_data.value = e.path if e.path else "Cancelled!"
        self.label_folder_data.update()



    def rename_files(self, e):
        prefix = self.prefix_input.value  # 获取用户输入的前缀
        if not prefix:
            snack_bar(self.page, "请输入前缀")
            return

        # 获取图像和标签文件夹的路径
        if (
            not self.image_folder_data
            or not self.label_folder_data
        ):
            snack_bar(self.page, "请选择图像和标签文件夹")
            return


        images_folder = self.image_folder_data.value
        labels_folder = self.label_folder_data.value

        # self.page.splash.visible = True
        self.page.update()

        # 遍历 labels 文件夹中的所有 txt 文件
        for filename in os.listdir(labels_folder):
            if filename.endswith('.txt'):
                # 构建源文件和目标文件的路径
                src_txt_path = os.path.join(labels_folder, filename)
                dst_txt_path = os.path.join(labels_folder, f'{prefix}_{filename}')

                # 添加前缀到标签文件
                os.rename(src_txt_path, dst_txt_path)

                # 找到对应的图像文件
                image_filename = os.path.splitext(filename)[0] + '.jpg'
                src_image_path = os.path.join(images_folder, image_filename)
                dst_image_path = os.path.join(images_folder, f'{prefix}_{image_filename}')

                # 添加前缀到图像文件
                os.rename(src_image_path, dst_image_path)

        # self.page.splash.visible = False
        self.page.update()
        snack_bar(self.page, "重命名完成!")
