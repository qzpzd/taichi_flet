from inspect import stack
from turtle import width
from typing import Optional

from flet import (
    Container,
    Row,
    Text,
    Image,
    ListView,
    colors,
    Stack,
    border,
    TextField,
    FloatingActionButton,
    Column,
    Card,
    IconButton,
    icons,
    Audio,
    audio,
    Slider,
    PopupMenuButton,
    PopupMenuItem,
    Page,
)
import sys
import os
sys.path.append(os.getcwd())

from methods.getmusics import DataSong
from methods.getmusics import HIFINI
from utils import snack_bar, ms_to_time, handle_redirect, download_url_content, DESKTOP

import flet

class Song(Row):
    """
    每首歌的展示条
    """

    def __init__(self, song: DataSong, select_callback, parent: 'ViewPage'):
        self.parent = parent
        self.song: DataSong = song
        self.select_callback = select_callback
        self.photo = Image(
            src=song.photo_url,
            width=40,
            height=40,
            border_radius=10,
            fit="cover",
        )
        self.music = Text(
            song.music_name,
            width=100,
            height=20,
            no_wrap=True,
            weight="bold",
            tooltip=song.music_name,
        )
        self.singer = Text(
            song.singer_name,
            width=80,
            height=20,
            no_wrap=True,
            weight="bold",
            tooltip=song.singer_name,
        )
        self.addbutton = flet.IconButton(
            icon=flet.icons.ADD_CIRCLE,
            on_click=self.parent.add_song_to_my_playlist,
            tooltip= "我的歌单")
        self.singer_button = Row([self.singer, self.addbutton], spacing=1)  
        self.photo_music = Row([self.photo, self.music],spacing=1)
        self.container = Container(
            content=Row([ self.photo_music,self.singer_button], spacing=50),
            on_click=self.on_click,
            bgcolor=colors.BLUE_GREY_300,
            padding=5,
            opacity=0.6,
            animate=300,
            border_radius=10,
            border=border.all(width=1),
        )

        self.delete_button = flet.IconButton(
            icon=flet.icons.DELETE,
            tooltip="删除歌曲",
            on_click=self.parent.delete_song_from_my_playlist,
        )

        self.container.content = Row(
            [self.photo_music, self.singer_button, self.delete_button],
            spacing=50,
        )

        super(Song, self).__init__(
            controls=[self.container],
            alignment="start",
            scroll=None,
            wrap=True,
        )
        self.__selected = False

    @property
    def selected(self):
        return self.__selected

    @selected.setter
    def selected(self, value: bool):
        self.__selected = value
        if value is True:
            self.container.bgcolor = colors.BLUE_GREY_700
            self.container.opacity = 1
            self.update()
            self.select_callback(self)
        else:
            self.container.bgcolor = colors.BLUE_GREY_300
            self.container.opacity = 0.7
            self.update()

    def on_click(self, e):
        self.selected = True

    def un_select(self):
        self.selected = False

    # def add_song_to_my_playlist(self, e):
    #     if self.song not in self.parent.my_playlist_songs:
    #         self.parent.my_playlist_songs.append(self.song)
    #         song_with_delete = Song(
    #             song=self.song,
    #             select_callback=self.select_callback,
    #             delete_callback=self.delete_song_from_my_playlist,
    #         )
    #         self.parent.my_playlist_list.set_musics(song_with_delete)

    # def delete_song_from_my_playlist(self, e):
    #     self.parent.my_playlist_songs.remove(self.song)
    #     self.parent.my_playlist_list.remove_music(self)


class PlayAudio(Audio):
    def __init__(self, song: DataSong, *args, **kwargs):
        self.song = song
        self.during: Optional[int] = None
        super(PlayAudio, self).__init__(*args, **kwargs)

    def update_during(self, during):
        # 将总时长记录下来，就不需要每次重新获取了
        self.during = during


class SearchCompoment(Row):
    """
    搜索音乐的组件
    """

    def __init__(self, parent: "ViewPage"):
        self.parent=parent
        self.music_api = HIFINI
        self.search_callback = self.parent.search_callback
        self.search_input = TextField(
            label="请输入歌曲名称或歌手名称",
            width=300,
            height=40,
            on_submit=self.search,
        )
        self.submit_btn = FloatingActionButton(
            "搜索", on_click=self.search, height=40, width=80, autofocus=True
        )
        self.button1 = flet.FilledButton(
            text="上一页", on_click=self.prev_page_click)
        self.button2 = flet.FilledButton(
            text="下一页", on_click=self.next_page_click)
        super(SearchCompoment, self).__init__(
            controls=[self.search_input, self.submit_btn,
                      self.button1, self.button2],
            alignment="center",
            vertical_alignment="center",
        )

    def search(self, e):
        self.search_callback(self.search_input.value)

        # 上一页按钮点击事件
    def prev_page_click(self, e):
        if hasattr(self.parent, 'current_page'):
            MusicList(self.parent.select_callback).list.controls.clear()
            self.parent.current_page -= 1
            self.search_callback(self.search_input.value)

    # 下一页按钮点击事件
    def next_page_click(self, e):
        if hasattr(self.parent, 'current_page'):
            MusicList(self.parent.select_callback).list.controls.clear()
            self.parent.current_page += 1
            print(len(self.parent.current_page_songs))
            if len(self.parent.current_page_songs) < 9:
                self.parent.current_page = 0
                self.parent.next_page += 1
                print(self.parent.next_page)
            self.search_callback(self.search_input.value)


class MusicList(Column):
    """
    展示查询音乐列表的区域
    """

    def __init__(self, select_callback):
        self.select_callback = select_callback
        self.list = flet.GridView(expand=1,
            runs_count=1,
            max_extent=350,
            child_aspect_ratio=5,
            spacing=2,
            run_spacing=5,
            padding=100,)
        super(MusicList, self).__init__(
            controls=[self.list], 
            # alignment="center", vertical_alignment="center"
            expand=True
        )

    def set_musics(self, data: DataSong, first=False):
        if first:
            self.list.controls.clear()
        self.list.controls.append(Song(data, self.middle_select_callback, parent=ViewPage))
        # self.update()

    def next_music(self):
        c = self.list.controls
        for i in range(len(c) - 1):
            if c[i].selected:
                c[i + 1].on_click(None)
                return
        c[0].on_click(None)

    def middle_select_callback(self, song: Song):
        for _song in self.list.controls:
            if _song.selected:
                if _song != song:
                    _song.un_select()
        self.select_callback(song)

    def remove_music(self, song):
        # Remove the song from the "我的歌单" tab
        self.list.controls.remove(song)
# from dataclasses import dataclass, field
# from typing import List
# @dataclass
# class DataSong:
#     photo_url: str  # 图片链接
#     big_photo_url: str  # 大图链接
#     music_name: str  # 歌曲名称
#     singer_name: str  # 歌手名称
#     music_url: Optional[str] = field(default=None)  # 音乐链接
# class MusicList(Column):
#     """
#     展示查询音乐列表的区域
#     """

#     def __init__(self, select_callback):
#         self.select_callback = select_callback
#         self.page = 1  # 当前页数
#         self.songs_per_page = 10  # 每页显示的歌曲数量
#         self.song_data = []  # 存储所有音乐数据
#         self.current_index = 0  # 当前索引位置
#         self.list = flet.GridView(
#             expand=1,
#             runs_count=1,
#             max_extent=350,
#             child_aspect_ratio=5,
#             spacing=2,
#             run_spacing=5,
#             padding=100,
#         )
#         # self.prev_button = flet.FilledButton("上一页", on_click=self.prev_page)
#         # self.next_button = flet.FilledButton("下一页", on_click=self.next_page)
#         # self.page_label = flet.Text("页数: 1")
#         super(MusicList, self).__init__(
#             controls=[self.list, self.prev_button, self.page_label, self.next_button],
#             expand=True,
#         )

#     def set_musics(self, data: List[DataSong], first=False):
#         if first:
#             self.song_data = data  # 第一次设置音乐数据时，保存全部数据
#             self.page = 1  # 重置页数
#             self.current_index = 0  # 重置当前索引位置
#             self.update_page_controls()
#         else:
#             self.song_data.extend(data)  # 添加更多音乐数据

#     def next_music(self):
#         c = self.list.controls
#         for i in range(len(c) - 1):
#             if c[i].selected:
#                 c[i + 1].on_click(None)
#                 return
#         c[0].on_click(None)

#     def update_page_controls(self):
#         start_idx = self.current_index
#         end_idx = start_idx + self.songs_per_page
#         current_page_songs = self.song_data[start_idx:end_idx]

#         self.list.controls.clear()
#         for song_data in current_page_songs:
#             self.list.controls.append(Song(song_data, self.middle_select_callback))
#         self.page_label.text = f"页数: {self.page}"
#         self.update()

#     def prev_page(self, button):
#         if self.page > 1:
#             self.page -= 1
#             self.current_index -= self.songs_per_page
#             self.update_page_controls()

#     def next_page(self, button):
#         max_pages = (len(self.song_data) - 1) // self.songs_per_page + 1
#         if self.page < max_pages:
#             self.page += 1
#             self.current_index += self.songs_per_page
#             self.update_page_controls()

#     def middle_select_callback(self, song: Song):
#         for _song in self.list.controls:
#             if _song.selected:
#                 if _song != song:
#                     _song.un_select()
#         self.select_callback(song)

class AudioInfo(Row):
    """
    展示播放时的图片，名称和歌手名称
    """

    def __init__(self):
        self.audio_photo = Card(
            width=100,
            height=100,
            elevation=10,
        )
        self.audio_name = Text("", size=18)
        self.audio_singer = Text("", size=14)
        self.name_singer = Column( 
            controls=[self.audio_name, self.audio_singer],
            alignment="start",
            horizontal_alignment="start",)
        self.column = Row(
            controls=[self.audio_photo, self.name_singer],
            alignment="start",
            # vertical_alignment="stretch"
        )
        super(AudioInfo, self).__init__(
            controls=[self.column],
            width=200,
            height=100,
            # vertical_alignment="stretch",
            alignment="start",
        )

    def set_info(self, song: DataSong):
        self.audio_photo.content = Image(song.big_photo_url, fit="cover")
        self.audio_name.value = song.music_name
        self.audio_singer.value = song.singer_name
        self.update()


class AudioBar(Row):
    """
    播放进度条和控制按钮
    """

    def __init__(self, root: 'ViewPage'):
        self.root = root
        self.song: Optional[DataSong] = None
        self.playing_audio: Optional[PlayAudio] = None
        self.is_sliding = False
        self.curr_time = Text("00:00")
        self.control_bar = Slider(
            on_change_start=self.on_change_start,
            on_change=self.on_change,
            on_change_end=self.on_change_end,
            on_focus=lambda e: print("on focus", e.data),
            disabled=False,
        )
        self.total_time = Text("00:00")
        self.popup_menu = PopupMenuButton(
            items=[PopupMenuItem(text="下载歌曲", on_click=self.download_music)]
        )
        self.play_btn = IconButton(
            icon=icons.PLAY_CIRCLE,
            selected_icon=icons.PAUSE_CIRCLE,
            on_click=self.toggle_play,
            icon_size=30,
        )
        self.play_type_btn = IconButton(
            icon=icons.PLAYLIST_PLAY_ROUNDED,
            selected_icon=icons.REPLAY_CIRCLE_FILLED_ROUNDED,
            on_click=self.toggle_play_type,
            icon_size=30,
        )
        self.row1 = Row(
            controls=[
                self.curr_time,
                self.control_bar,
                self.total_time,
                self.popup_menu,
            ]
        )
        self.row2 = Row(controls=[self.play_btn, self.play_type_btn])
        super(AudioBar, self).__init__(
            controls=[Column([self.row2, self.row1],horizontal_alignment="center")],
            alignment="end",
            # vertical_alignment="center",
        )

    def play(self, song: Optional[DataSong] = None):
        if song is None:
            if self.song is not None:
                self.playing_audio.play()
                self.play_btn.selected = True
                self.update()
                return
            else:
                return
        if self.song and self.song.music_url == song.music_url:
            self.playing_audio.play()
        else:
            self.song = song
            if self.playing_audio in self.page.overlay:
                self.page.overlay.remove(self.playing_audio)
            # 双重保险
            for i in self.page.overlay[:]:
                if isinstance(i, PlayAudio):
                    self.page.overlay.remove(i)

            self.playing_audio = PlayAudio(
                song=song,
                src=handle_redirect(song.music_url),
                autoplay=False,
                volume=100,
                balance=0,
                release_mode=audio.ReleaseMode.STOP,
                on_loaded=self.loaded,
                on_duration_changed=self.during_changed,
                on_position_changed=self.position_changed,
                on_state_changed=self.state_changed,
                on_seek_complete=self.seek_complete,
            )

            self.page.overlay.append(self.playing_audio)
            self.page.update()
            self.playing_audio.play()

    def resume(self):
        self.playing_audio.resume()
        self.play_btn.selected = False
        self.update()

    def pause(self):
        self.playing_audio.pause()
        self.play_btn.selected = True
        self.update()

    def next_music(self, e=None):
        self.root.right_widget.music_list.next_music()

    def release(self):
        self.playing_audio.release()
        self.play_btn.selected = False
        self.update()

    def loaded(self, e):
        # print("on loaded", e.data)
        pass

    def during_changed(self, e):
        # 歌曲总时长发生了改变
        during = int(e.data)
        self.playing_audio.update_during(during)
        self.total_time.value = ms_to_time(during)
        self.update()

    def position_changed(self, e):
        during = float(e.data)
        self.curr_time.value = ms_to_time(during)
        percent = (
            during / self.playing_audio.during
            if self.playing_audio.during
            else self.playing_audio.get_duration()
        )
        if not self.is_sliding:
            self.control_bar.value = percent
            # if during == self.playing_audio.during != 0:
            #         print(during)
            #         print(self.playing_audio.during)
            #         self.next_music(None)

        self.update()

    def state_changed(self, e):
        status = e.data
        if status == "playing":
            self.play_btn.selected = True
        else:
            if status == "completed":
                if self.play_type_btn.selected:
                    self.playing_audio.play()
                else:
                    self.next_music(None)
            self.play_btn.selected = False
        self.update()

    def seek_complete(self, e):
        pass

    def toggle_play(self, e):
        if e.control.selected:
            self.pause()
        else:
            self.resume()

    def toggle_play_type(self, e):
        self.play_type_btn.selected = not e.control.selected
        self.update()

    def on_change_start(self, e):
        self.is_sliding = True

    def on_change(self, e):
        target_during = float(e.data) * self.playing_audio.during
        self.playing_audio.seek(int(target_during))
        self.update()

    def on_change_end(self, e):
        self.is_sliding = False

    def download_music(self, e):
        if self.song is None:
            return
        music_name = self.song.music_name
        music_singer = self.song.singer_name
        name = music_name + "_" + music_singer + ".mp3"
        url = self.song.music_url
        resp = download_url_content(url)
        with open(DESKTOP + "/" + name, "wb") as f:
            f.write(resp.content)
        snack_bar(self.page, f"{name} 已保存至桌面")


class RightSearchSection(Column):
    """右侧区域"""

    def __init__(self, parent: "ViewPage"):
        self.parent = parent
        self.music_list = MusicList(self.parent.select_callback)
        self.search_content = SearchCompoment(self.parent)
        super(RightSearchSection, self).__init__(
            controls=[self.search_content, self.music_list],
            # alignment="center",
            # horizontal_alignment="center",
            expand=True,
        )
class RightSearchSection(Column):
    """右侧区域"""

    def __init__(self, parent: "ViewPage"):
        self.parent = parent
        self.music_list = MusicList(self.parent.select_callback)
        self.search_content = SearchCompoment(self.parent)
        super(RightSearchSection, self).__init__(
            controls=[self.search_content, self.music_list],
            # alignment="center",
            # horizontal_alignment="center",
            expand=True,
        )

class LeftPlaySection(Column):
    """左侧区域"""

    def __init__(self, parent):
        self.parent = parent
        self.playing_song: Optional[PlayAudio] = None
        self.audio_info = AudioInfo()
        self.audio_bar = AudioBar(self.parent)
        self.row =  Container(content=Row(
            controls=[self.audio_info, self.audio_bar],
            alignment="center",
            vertical_alignment="center",
            
        ),bgcolor=colors.BLUE_GREY_300,
        )
        super(LeftPlaySection, self).__init__(
            controls=[self.row],
            # expand=True,
        )

    def play_music(self, song: Song):
        self.audio_info.set_info(song.song)
        self.audio_bar.play(song.song)


class ViewPage(Stack):
    def __init__(self, page, song: DataSong):
        self.song = song
        self.my_playlist_songs = []
        self.my_playlist_list = MusicList(self.select_callback) 
        self.music_api = HIFINI
        self.left_widget = LeftPlaySection(self)
        self.right_widget = RightSearchSection(self)
        self.row = Column(
            controls=[self.right_widget, self.left_widget],
            # alignment="center",
            # vertical_alignment="center",
            expand=True,
        )
        t = flet.Tabs(
        selected_index=1,
        animation_duration=300,
        tabs=[
            flet.Tab(
                text="精选歌单",
                content=flet.Container(
                    content=self.row , alignment=flet.alignment.center
                ),
            ),
            flet.Tab(
                text="我的歌单",
                content=flet.Container(
                    content=Row(self.my_playlist_songs) , alignment=flet.alignment.center
                ),
            ),
        ],
        expand=1,
    )
        super(ViewPage, self).__init__(controls=[t], expand=True)
        self.page = page

    def init_event(self):
        if not self.right_widget.music_list.list.controls:
            self.right_widget.search_content.search(None)

    def select_callback(self, song: Song):
        self.left_widget.play_music(song)

    def search_callback(self, target):
        flag = False
        self.next_page = 2
        search_results = self.music_api.search_musics(target,self.next_page)
        if not search_results:
            snack_bar(self.page, "没有找到相关音乐。")
            return

        # 初始化或获取当前页数
        if not hasattr(self, 'current_page'):
            self.current_page = 0
        # 定义每页显示的元素数量
        per_page = 9
        # 计算总页数
        total_pages = (len(search_results) + per_page - 1) // per_page
        # 确保当前页数在合法范围内
        self.current_page = max(0, min(self.current_page, total_pages - 1))
        # 计算当前页的起始和结束索引
        start_idx = self.current_page * per_page
        end_idx = start_idx + per_page
        # 获取当前页的音乐列表
        self.current_page_songs = search_results[start_idx:end_idx]


        if not self.current_page_songs:
            snack_bar(self.page, "没有更多音乐了。")
            return

        for song in self.current_page_songs:
            if isinstance(song, tuple):
                snack_bar(self.page, f"音乐api出错: {song[1]}")
                return
            else:
                if not flag:
                    self.right_widget.music_list.set_musics(song, first=True)
                    flag = True
                else:
                    self.right_widget.music_list.set_musics(song)
            # print(song)

        self.update()

    def add_song_to_my_playlist(self):
        if self.song not in self.my_playlist_songs:
            self.my_playlist_songs.append(self.song)
            song_with_delete = Song(
                song=self.song,
                select_callback=self.select_callback,
                delete_callback=self.delete_song_from_my_playlist,
            )
            self.my_playlist_list.set_musics(song_with_delete)

    def delete_song_from_my_playlist(self):
        self.my_playlist_songs.remove(self.song)
        self.my_playlist_list.remove_music(self)

        
def main(page: Page):
    # page.vertical_alignment = "center"
    # page.horizontal_alignment = "center"

    page.add(ViewPage(page,DataSong))


flet.app(target=main)