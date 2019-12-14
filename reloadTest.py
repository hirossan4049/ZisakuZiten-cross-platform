from kivy.lang import Builder
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.icon_definitions import md_icons
from kivymd.uix.list import ILeftBodyTouch, OneLineIconListItem

Builder.load_string(
    """
<ItemForList>
    text: root.text

    IconLeftSampleWidget:
        icon: root.icon


<Example@FloatLayout>

    BoxLayout:
        orientation: "vertical"

        MDToolbar:
            title: app.title
            md_bg_color: app.theme_cls.primary_color
            background_palette: "Primary"
            elevation: 10
            left_action_items: [["menu", lambda x: x]]

        MDScrollViewRefreshLayout:
            id: refresh_layout
            refresh_callback: app.refresh_callback
            root_layout: root

            GridLayout:
                id: box
                size_hint_y: None
                height: self.minimum_height
                cols: 1
"""
)


class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass


class ItemForList(OneLineIconListItem):
    icon = StringProperty()


class MainApp(MDApp):
    x = NumericProperty(0)
    y = NumericProperty(15)

    def __init__(self, **kwargs):
        self.title = "KivyMD Examples - Refresh Layout"
        super().__init__(**kwargs)

    def build(self):
        self.root = Factory.Example()
        self.set_list()

    def set_list(self):
        names_icons_list = list(md_icons.keys())[self.x : self.y]
        for name_icon in names_icons_list:
            self.root.ids.box.add_widget(ItemForList(icon=name_icon, text=name_icon))

    def refresh_callback(self, *args):
        """A method that updates the state of your application
        while the spinner remains on the screen."""

        def refresh_callback(interval):
            self.root.ids.box.clear_widgets()
            if self.x == 0:
                self.x, self.y = 15, 30
            else:
                self.x, self.y = 0, 15
            self.set_list()
            self.root.ids.refresh_layout.refresh_done()
            self.tick = 0

        Clock.schedule_once(refresh_callback, 1)


if __name__ == "__main__":
    MainApp().run()
