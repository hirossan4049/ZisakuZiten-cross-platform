from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.clock import Clock

# from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivymd.app import MDApp
import os
from kivymd.list import TwoLineListItem
from kivymd.snackbar import Snackbar

# from kivymd.list.OneLineListItem import OneLineListItem
# from kivymd.list.TwoLineListItem import TwoLineListItem
# Builder.load_file(os.getcwd()+'/kvfile.kv')
import requests
import json

Builder.load_file("kvfile.kv")


#ListAdapter
class MDCustomListItem(TwoLineListItem):
    text = StringProperty()
    secondary_text = StringProperty()
    def on_press(self):
        print(self.id)
    def _set_active(self, active, list):
        pass


        # self.ids.zlist.add_widget(MDCustomListItem(text="a"))

    # def show_snackber(self,position:int):
    #     print(position)
    #     Snackbar(text="This is a snackbar!").show()



class MainApp(MDApp):
    def __init__(self, **kwargs):
        # self.title = "KivyMD Examples - Bottom Navigation"
        super().__init__(**kwargs)



    def api_reload(self):
        self.get_json = requests.get("https://zisakuzitenapi2.herokuapp.com/api/groups/?format=json").json()
        print("===API RELOAD===")

    def build(self):
        self.root = Factory.MainWindow()
        self.api_set()
        # print(self.root.ids)

    def on_start(self):
        print("===START!===")

    def on_stop(self):
        print("===STOP!===")

    def refresh_callback(self, *args):
        def refresh_callback(interval):
            print("reload")
            self.api_set()
            self.root.ids.refresh_layout.refresh_done()
            self.tick=0
            print("done")
            # self.tick = 0
        Clock.schedule_once(refresh_callback, 1)
        # refresh_callback(0)


    def api_set(self):
        #zlistの初期化。
        self.root.ids.zlist.clear_widgets()
        self.get_json = requests.get("https://zisakuzitenapi2.herokuapp.com/api/groups/?format=json").json()
        ZtitleList = []
        GtitleList = []
        id_list = []
        for i in range(len(self.get_json)):
            title_list = [self.get_json[i]["ziten_updT_List"][a]["title"] for a in range(len(self.get_json[i]["ziten_updT_List"]))]
            ZtitleList.append(title_list)
            GtitleList.append(self.get_json[i]["title"])

            if not self.get_json[i]["ziten_updT_List"]:
                id_list.append(None)
            else:
                id_list.append(self.get_json[i]["ziten_updT_List"][0]["group"])

        gz_index = 0
        for Gtitle,Ztitle in zip(GtitleList,ZtitleList):
            if not Ztitle:
                Ztitle.append("Item is None")
            if len(Ztitle) >= 5:
                Ztitle = Ztitle[:5]
                Ziten.append("...")

            self.root.ids.zlist.add_widget(
                MDCustomListItem(
                    id=str(id_list[gz_index]),
                    # index=i,
                    text=Gtitle,
                    secondary_text=",".join(Ztitle),
                    ))
            gz_index += 1



if __name__ == "__main__":
    MainApp().run()






        # for i in range(10):
        #     self.ids.zlist.add_widget(
        #         MDCustomListItem(
        #             id=str(i),
        #             # index=i,
        #             text="Item :"+str(i),
        #             secondary_text="hello",
        #             ))

