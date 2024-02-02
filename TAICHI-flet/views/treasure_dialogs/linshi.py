# import flet


# window = flet.Window("Custom Title Bar Example", width=800, height=600)

# # 创建一个自定义标题栏面板
# title_bar = flet.Panel(width=window.width, height=40)
# title_bar.background_color = "gray"  # 设置标题栏的背景颜色

# # 创建最小化按钮
# minimize_button = flet.IconButton(text="_", width=30, height=30)
# minimize_button.x = window.width - 90  # 调整按钮的位置
# minimize_button.y = 5  # 调整按钮的位置

# # 创建放大/缩小按钮
# maximize_button = flet.Button(text="[]", width=30, height=30)
# maximize_button.x = window.width - 60  # 调整按钮的位置
# maximize_button.y = 5  # 调整按钮的位置

# # 创建退出按钮
# exit_button = flet.Button(text="X", width=30, height=30)
# exit_button.x = window.width - 30  # 调整按钮的位置
# exit_button.y = 5  # 调整按钮的位置

# # 添加按钮到标题栏
# title_bar.add(minimize_button)
# title_bar.add(maximize_button)
# title_bar.add(exit_button)

# # 添加标题栏到窗口
# window.add(title_bar)

# # 创建一个内容面板
# content_panel = flet.Panel(width=window.width, height=window.height - title_bar.height)
# content_panel.background_color = "white"  # 设置内容面板的背景颜色

# # 添加内容到内容面板
# label = flet.Label("Custom Title Bar Example", font_size=24)
# content_panel.add(label)

# # 添加内容面板到窗口
# window.add(content_panel)

# # 设置窗口可拖动
# window.draggable = True

# # 设置退出按钮的点击事件
# def exit_button_click(event):
#     flet.

# exit_button.on_click = exit_button_click

# # 运行应用程序
# flet.app(target=main, assets_dir="assets")

# import flet as ft

# def main(page: ft.Page):
#     page.window_title_bar_hidden = True
#     page.window_title_bar_buttons_hidden = True

#     # page.window_minimizable = True
#     # page.window_maximizable = True
#     page.window_bgcolor = ft.colors.TRANSPARENT
#     page.bgcolor = ft.colors.TRANSPARENT
#     page.window_frameless = True

#     page.add(
#         ft.Row(
#             [   ft.WindowDragArea(ft.Container(ft.IconButton(ft.icons.ZOOM_OUT_MAP_ROUNDED))),
#                 ft.IconButton(ft.icons.MINOR_CRASH_ROUNDED, on_click=lambda _: page.window_minimizable),
#                 ft.IconButton(ft.icons.MAXIMIZE_SHARP, on_click=lambda _: page.window_full_screen),
#                 ft.IconButton(ft.icons.CLOSE, on_click=lambda _: page.window_close())
#             ]
#         )
#     )
 
# ft.app(target=main)

# import tkinter as tk

# def minimize_window():
#     root.iconify()  # 最小化窗口

# # 创建主窗口
# root = tk.Tk()
# root.title("最小化按钮示例")

# # 创建最小化按钮
# minimize_button = tk.Button(root, text="最小化", command=minimize_window)
# minimize_button.pack()

# root.mainloop()

# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton, QTabWidget, QToolButton, QTabBar
# from io import StringIO

# class CodeEditor(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#         # 为每个编辑页面保存默认代码
#         self.default_codes = {
#             "Main Page": "print('Hello from Main Page')",
#             "Editor Page 1": "print('Default Code for Editor Page 1')",
#             "Editor Page 2": "print('Default Code for Editor Page 2')"
#         }
#     def initUI(self):
#         self.central_widget = QWidget()
#         self.setCentralWidget(self.central_widget)

#         self.tab_widget = QTabWidget()
#         self.central_layout = QVBoxLayout()
#         self.central_layout.addWidget(self.tab_widget)
#         self.central_widget.setLayout(self.central_layout)

#         self.add_main_page()

#     def add_main_page(self):
#         main_page = QWidget()
#         main_layout = QVBoxLayout()

#         edit_button = QPushButton("Edit Code")
#         edit_button.clicked.connect(self.show_editor_page)

#         main_layout.addWidget(edit_button)
#         main_page.setLayout(main_layout)

#         self.tab_widget.addTab(main_page, "Main Page")

#     def show_editor_page(self):
#         editor_tab = QWidget()
#         editor_layout = QVBoxLayout()

#         editor = QTextEdit()
#         run_button = QPushButton("Run Code")
#         restore_button = QPushButton("Restore Code")
#         output = QTextEdit()
#         output.setReadOnly(True)

#         # 获取默认代码，如果没有默认代码则使用空字符串
#         print('self.tab_widget.currentIndex():',self.tab_widget.currentIndex())
#         default_code = self.default_codes.get(self.tab_widget.currentIndex(),'')
#         print('default_code:',default_code)
#         editor.setPlainText(default_code)

#         editor_layout.addWidget(editor)
#         editor_layout.addWidget(run_button)
#         editor_layout.addWidget(restore_button)
#         editor_layout.addWidget(output)

#         editor_tab.setLayout(editor_layout)
#         self.tab_widget.addTab(editor_tab, "Editor Page")

#          # 创建自定义的关闭按钮
#         close_button = QToolButton()
#         close_button.setText("x")
#         close_button.clicked.connect(lambda: self.close_editor_page(editor_tab))

#         # 在选项卡中设置关闭按钮
#         self.tab_widget.tabBar().setTabButton(self.tab_widget.count() - 1, QTabBar.RightSide, close_button)

#         run_button.clicked.connect(lambda: self.run_code(editor, output))
#         restore_button.clicked.connect(lambda: self.restore_code(editor, output))

#     def run_code(self, editor, output):
#         code = editor.toPlainText()
#         try:
#             local_vars = {}
#             exec(code, globals(), local_vars)
#             if 'result' in local_vars:
#                 result = str(local_vars['result'])
#                 output.setPlainText("Output:\n" + result)
#             else:
#                 original_stdout = sys.stdout  # 保存原始标准输出
#                 sys.stdout = open('output.txt', 'w')  # 重定向标准输出到文件
#                 exec(code)
#                 sys.stdout.close()  # 关闭文件以确保刷新输出
#                 sys.stdout = original_stdout  # 恢复原始标准输出

#                 with open('output.txt', 'r') as file:
#                     output_text = file.read()

#                 output.setPlainText("Output:\n" + output_text)
#                 # output.setPlainText("Output: No result")
#         except Exception as e:
#             output.setPlainText("Error:\n" + str(e))

#     def restore_code(self, editor,output):

#         # 获取当前编辑页面的默认代码
#         default_code = self.default_codes.get(self.tab_widget.currentIndex()-1, "")

#         editor.setPlainText(default_code)
#         output.clear()
    
#     def close_editor_page(self, editor_tab):
#         index = self.tab_widget.indexOf(editor_tab)
#         self.tab_widget.removeTab(index)
#         editor_tab.close()

#     def update_tabbar(self, index):
#         # 更新关闭按钮的位置
#         self.tab_widget.tabBar().setTabButton(index, QTabBar.RightSide, None)
#         for i in range(self.tab_widget.count()):
#             if i != index:
#                 close_button = QToolButton()
#                 close_button.setText("x")
#                 close_button.clicked.connect(lambda _, i=i: self.close_editor_page(self.tab_widget.widget(i)))
#                 self.tab_widget.tabBar().setTabButton(i, QTabBar.RightSide, close_button)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = CodeEditor()
#     window.show()
#     sys.exit(app.exec_())



import sys
from turtle import window_height
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, \
                            QPushButton, QTabWidget, QTabBar, QToolButton, QHBoxLayout, QGridLayout,\
                            QSizePolicy, QDesktopWidget

class CodeEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.tab_widget.currentChanged.connect(self.update_tabbar)

        # 创建一个字典以存储不同按钮对应的默认代码
        self.default_codes = {
            "button1": "print('Default Code for Button 1')",
            "button2": "print('Default Code for Button 2')",
            "button3": "print('Default Code for Button 3')",
            "button4": "print('Default Code for Button 4')",
            "button5": "print('Default Code for Button 5')",
            "button6": "print('Default Code for Button 6')",
            "button7": "print('Default Code for Button 7')",
            "button8": "print('Default Code for Button 8')",
            "button9": "print('Default Code for Button 9')",
            "button10": "print('Default Code for Button 10')",
            "button11": "print('Default Code for Button 11')",
            "button12": "print('Default Code for Button 12')",
            "button13": "print('Default Code for Button 13')",
            "button14": "print('Default Code for Button 14')",
            "button15": "print('Default Code for Button 15')",
            "button16": "print('Default Code for Button 16')",
            "button17": "print('Default Code for Button 17')",
            "button18": "print('Default Code for Button 18')",
            "button19": "print('Default Code for Button 19')",
            "button20": "print('Default Code for Button 20')",
            "button21": "print('Default Code for Button 21')",
        }

    def initUI(self):
        self.setWindowTitle('Python 文件处理')
        self.centerWindow()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.tab_widget = QTabWidget()
        self.central_layout = QVBoxLayout()
        self.central_layout.addWidget(self.tab_widget)
        self.central_widget.setLayout(self.central_layout)

        # 添加一个编辑页面
        self.add_main_page("首页")
        

    def add_button(self, button_name):
        edit_button = QPushButton(f"Edit {button_name}")
        edit_button.clicked.connect(lambda _, name=button_name: self.show_editor_page(name))

        return edit_button

    def centerWindow(self):
        # 获取桌面的大小
        desktop = QDesktopWidget()
        screen_rect = desktop.availableGeometry()

        # 设置应用窗口的大小为桌面大小的一部分（例如，宽度为2/3，高度为2/3）
        global window_width
        window_width = screen_rect.width() * 2 // 3
        window_height = screen_rect.height() * 2 // 3

        self.setGeometry(0, 0, window_width, window_height)  # 设置窗口的位置和大小    
    def add_main_page(self, main_page_name):
        main_page = QWidget()
        main_layout = QVBoxLayout()

         # 创建一个网格布局用于放置按钮
        button_layout = QGridLayout()

        button_name_list = ['button1','button2','button3','button4','button5','button6','button7',
        'button8','button9','button10','button4','button5','button6','button7',
        'button1','button2','button3','button4','button5','button6','button7']
        row, col = 0, 0  # 初始化行和列
        for button_name in button_name_list:

            edit_button = self.add_button(button_name)
            edit_button.setFixedSize(150, 30)  # 设置按钮的固定大小       
            edit_button.setStyleSheet("background-color: dark; border: 2px solid blue; border-radius: 10px; color: white;")
            # edit_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)# 设置按钮的大小策略，使其相对于窗口自适应
            button_layout.addWidget(edit_button, row, col, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            
            col += 1  # 水平排列，列增加
            if col > 5:  # 两列后换行
                col = 0
                row += 1
        # 设置按钮之间的水平和垂直间隔
        button_layout.setHorizontalSpacing(10)  # 设置水平间隔
        button_layout.setVerticalSpacing(10)  # 设置垂直间隔

        # 设置布局的内边距
        button_layout.setContentsMargins(10, 10, 10, 10)

        # 将按钮布局添加到一个父 QWidget 上
        button_container = QWidget()
        # button_container.setFixedWidth(window_width)
        button_container.setLayout(button_layout)

        main_layout.addWidget(button_container)
        main_page.setLayout(main_layout)
        main_page.setStyleSheet("background-image: url('assets/imgs/bg.jpg'); background-repeat: no-repeat;background-size: contain;")


        self.tab_widget.addTab(main_page, main_page_name)

        

    def show_editor_page(self, button_name):
        editor_tab = QWidget()
        editor_layout = QVBoxLayout()

        editor = QTextEdit()
        editor.setStyleSheet("background-color: lightyellow;")
        editor.setPlainText(self.default_codes.get(button_name, ""))
        run_button = QPushButton("Run Code")
        restore_button = QPushButton("Restore Code")
        output = QTextEdit()
        output.setStyleSheet("background-color: lightblue;")
        output.setReadOnly(True)

        editor_layout.addWidget(editor)
        editor_layout.addWidget(run_button)
        editor_layout.addWidget(restore_button)
        editor_layout.addWidget(output)

        editor_tab.setLayout(editor_layout)
        self.tab_widget.addTab(editor_tab, f"Editor for {button_name}")

        # 创建自定义的关闭按钮
        close_button = QToolButton()
        close_button.setText("x")
        close_button.clicked.connect(lambda: self.close_editor_page(editor_tab))

        # 在选项卡中设置关闭按钮
        self.tab_widget.tabBar().setTabButton(self.tab_widget.count() - 1, QTabBar.RightSide, close_button)

        run_button.clicked.connect(lambda: self.run_code(editor, output))
        restore_button.clicked.connect(lambda: self.restore_code(editor, output, button_name))

    def run_code(self, editor, output):
        code = editor.toPlainText()
        try:
            local_vars = {}
            exec(code, globals(), local_vars)
            if 'result' in local_vars:
                result = str(local_vars['result'])
                output.setPlainText("Output:\n" + result)
            else:
                original_stdout = sys.stdout  # 保存原始标准输出
                sys.stdout = open('output.txt', 'w')  # 重定向标准输出到文件
                exec(code)
                sys.stdout.close()  # 关闭文件以确保刷新输出
                sys.stdout = original_stdout  # 恢复原始标准输出

                with open('output.txt', 'r') as file:
                    output_text = file.read()

                output.setPlainText("Output:\n" + output_text)
                # output.setPlainText("Output: No result")
        except Exception as e:
            output.setPlainText("Error:\n" + str(e))

    def restore_code(self, editor, output, button_name):
        # print(self.tab_widget.currentIndex())
        default_code = self.default_codes.get(button_name, "")
        editor.setPlainText(default_code)
        output.clear()

    def close_editor_page(self, editor_tab):
        index = self.tab_widget.indexOf(editor_tab)
        self.tab_widget.removeTab(index)
        editor_tab.close()

    def update_tabbar(self, index):
        # 更新关闭按钮的位置
        self.tab_widget.tabBar().setTabButton(index, QTabBar.RightSide, None)
        for i in range(self.tab_widget.count()):
            if i != index:
                close_button = QToolButton()
                close_button.setText("x")
                close_button.clicked.connect(lambda _, i=i: self.close_editor_page(self.tab_widget.widget(i)))
                self.tab_widget.tabBar().setTabButton(i, QTabBar.RightSide, close_button)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CodeEditor()
    window.show()
    sys.exit(app.exec_())
