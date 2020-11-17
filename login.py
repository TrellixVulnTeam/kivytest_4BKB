from kivy.uix.screenmanager import Screen

from kivymd.app import MDApp
# from kivymd.uix.button import MDRectangleFlatButton
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.button import Button
# from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.core.audio import SoundLoader

from os import listdir, path

Builder.load_string('''
<MusicPlayer>:
    canvas.before:
        Color:
            rgba: 0, .5, .1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    TextInput:
        id: direct
        pos: 0,root.top-35
        size: root.width-200,35
        hint_text: 'Enter File Location or Leave Empty to Browse'
    Button:
        id: searchBtn
        text: 'Browse'
        size: 200,35
        background_color: 0,.5,1,1
        pos: root.width-200, root.top-35
        on_release: root.getSongs()

    ScrollView:
        size_hint: None, None
        size: root.width, root.height-135
        pos: 0, 100
        GridLayout:
            id: scroll
            cols: 2
            spacing: 10
            size_hint_y: None
            row_force_default: True
            row_default_height: 40

    GridLayout:
        rows: 1
        pos: 0, 50
        size: root.width, 50
        Button:
            text: 'Preview'
            background_color: 0,.5,1,1
        Button:
            text: 'Play'
            background_color: 0,.5,1,1
        Button:
            text: 'Next'
            background_color: 0,0,1,1
    Button:
        id: nowplay
        text: 'Playing'
        pos: 0,0
        size: root.width, 50
        background_color: 0,0,1,1

    Label:
        id: status
        text: ''
        center: root.center

<ChooseFile>:

    canvas.before:
        Color:
            rgba: 0, 0, .4, 1
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        FileChooserIconView:
            id: filechooser

        BoxLayout:
            size_hint_y: None
            height: 30
            Button:
                text: "Cancel"
                background_color: 0,.5,1,1
                on_release: root.cancel()

            Button:
                text: "Select Folder"
                background_color: 0,.5,1,1
                on_release: root.select(filechooser.path)


''')


class ChooseFile(FloatLayout):
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)


class MusicPlayer(Widget):
    directory = ''  # location of songs folder
    nowPlaying = ''  # Song that is currently playing

    def getpath(self):
        try:
            f = open("sav.dat", "r")
            self.ids.direct.text = str(f.readline())
            f.close()
            self.ids.searchBtn.text = "Browser"
            self.getSongs()
        except:
            self.ids.direct.text = ''

    def savepath(self, path)\
             :
        f = open("sav.dat", "w")
        f.write(path)
        f.close()

    def dismiss_popup(self):
        self._popup.dismiss()

    def fileSelect(self):
        content = ChooseFile(select=self.select,
                             cancel=self.dismiss_popup)

        self._popup = Popup(title="Select Folder", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def select(self, path):
        self.directory = path
        self.ids.direct.text = self.directory
        self.ids.searchBtn.text = "Browser"
        self.savepath(self.directory)
        self.getSongs()
        self.dismiss_popup()

    def getSongs(self):

        songs = []  # List to hold songs from music directory
        self.directory = self.ids.direct.text  # Directory entered by the user

        if self.directory == '':
            self.fileSelect()

        # To make sure that the directory ends with a '/'
        if not self.directory.endswith('/'):
            self.directory += '/'

        # Check if directory exists
        if not path.exists(self.directory):
            self.ids.status.text = 'Folder Not Found'
            self.ids.status.color = (1, 0, 0, 1)

        else:

            self.ids.status.text = ''

            self.ids.scroll.bind(minimum_height=self.ids.scroll.setter('height'))

            # get mp3 files from directory
            for fil in listdir(self.directory):
                if fil.endswith('.mp3'):
                    songs.append(fil)

            # If there are no mp3 files in the chosen directory
            if songs == [] and self.directory != '':
                self.ids.status.text = 'No Music Found'
                self.ids.status.color = (1, 0, 0, 1)

            songs.sort()

            for song in songs:

                def playSong(bt):
                    try:
                        self.nowPlaying.stop()
                    except:
                        pass
                    finally:
                        self.nowPlaying = SoundLoader.load(self.directory + bt.text + '.mp3')
                        self.nowPlaying.play()
                        self.ids.nowplay.text = bt.text

                btn = Button(text=song[:-4], on_press=playSong)
                icon = Button(size_hint_x=None, width=50, background_down="icon.png", background_normal="icon.png")

                # Color Buttons Alternatively
                if songs.index(song) % 2 == 0:
                    btn.background_color = (0, 0, 1, 1)
                else:
                    btn.background_color = (0, 0, 2, 1)

                self.ids.scroll.add_widget(icon)  # Add icon to layout
                self.ids.scroll.add_widget(btn)  # Add btn to layout


class MusicApp(MDApp):

    def build(self):
        music = MusicPlayer()
        music.getpath()
        return music

    def on_pause(self):
        return True

    def on_resume(self):
        pass


MusicApp().run()
