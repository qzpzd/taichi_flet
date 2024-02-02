from importlib import import_module
from turtle import onclick

import flet

try:
    from views import cense, immortality, lyra, main, mountain, rain, treasure, buddhist
    from views.treasure_dialogs import pdf2word
except:
    pass
from flet import Tabs, Tab, Page, Stack, ProgressBar, theme, alignment, animation, transform, Container, Image

from settings import navigation_tabs


class NavigationBar(Stack):
    def __init__(self, page: Page):
        self.page = page
        self.tabs = Tabs(expand=1)
        self.tabs_list = []
        for navigation in navigation_tabs:
            content = self.get_page(navigation[2])
            if not content:
                continue
            icon = navigation[0]
            text = navigation[1]
            self.tabs_list.append(Tab(content=content, icon=icon, text=text))
        self.tabs.tabs.extend(self.tabs_list)
        self.tabs.on_change = lambda e: self.tab_init_event(e.data)

        # 添加窗口最大化标识
        self.window_maximized_ = None
       
        # self.bg_src = '/imgs/bg.jpg'
        # self.bg = Container(
        #     content=Image(src=self.bg_src, fit="cover"),
        #     expand=True,
        # )
       
        title = flet.Row([flet.WindowDragArea(flet.IconButton(icon=flet.icons.ZOOM_OUT_MAP,tooltip= "拖动区域")),
        flet.IconButton(icon=flet.icons.REMOVE,on_click=lambda _: page.window_minimized(),tooltip= "最小化"),
        flet.IconButton(icon=flet.icons.CROP_SQUARE ,on_click=lambda _: self.window_maximized(),tooltip= "最大化",data=0),
        flet.IconButton(icon=flet.icons.CLOSE,on_click=lambda _: page.window_destroy(),tooltip= "退出")],
        alignment=flet.MainAxisAlignment.END,
        )
        super(NavigationBar, self).__init__(controls=[self.tabs, title],expand=True)

    #添加最大化按钮事件
    def window_maximized(self):
        if self.window_maximized_:
            self.window_maximized_ = False  # 切换为非最大化状态
        else:
            self.window_maximized_ = True  # 切换为最大化状态
        self.page._set_attr("windowMaximized", self.window_maximized_)  # 更新窗口最大化状态
        self.page.update()

    def tab_init_event(self, index):
        index = int(index)
        if hasattr(self.tabs_list[index].content, "init_event"):
            getattr(self.tabs_list[index].content, "init_event")()

    def get_page(self, module_name):
        try:
            module_file = import_module("views." + module_name)
            return module_file.ViewPage(self.page)
        except Exception as e:
            print("getpage", e)

    # def set_background_image(self, image_url):
    #     if self.view_page:
    #         self.view_page.set_bg(image_url)
    #         self.page.update()

def main(page: Page):
    # page.title = "太·极"
    # progress_bar = ProgressBar(visible=True)
    # page.splash = progress_bar
    # page.window_bgcolor = flet.colors.LIGHT_BLUE_200
    # page.bgcolor = flet.colors.LIGHT_BLUE_200
    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True
    # page.window_prevent_close = True
    # page.window_always_on_top = True
    page.window_maximizable = True
    page.window_movable = True
    # page.window_frameless = True
    # page.theme = theme.Theme(color_scheme_seed="daker")
    # page.padding = 0
    # page.update()

    t = NavigationBar(page)
    
    page.add(t)
    

flet.app(target=main, assets_dir="assets")
