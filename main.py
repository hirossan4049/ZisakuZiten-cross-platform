from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.clock import Clock
from kivymd.toast.kivytoast.kivytoast import toast

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
import datetime
Builder.load_file("kvfile.kv")
import time

#ListAdapter
class MDCustomListItem(TwoLineListItem):
    text = StringProperty()
    secondary_text = StringProperty()
    def on_press(self):
        print(self.id)
    def _set_active(self, active, list):
        pass








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

    # def show_snackber(self,comment):
    #     Snackbar(text=comment).show()

    def on_start(self):
        print("===START!===")

    def on_stop(self):
        print("===STOP!===")

    def gz_post(self):
        #get
        gtitle = self.root.ids.pgtitle.text
        ztitle1 = self.root.ids.pztitle1.text
        zcontent1 = self.root.ids.pzcontent1.text
        ztitle2 = self.root.ids.pztitle2.text
        zcontent2 = self.root.ids.pzcontent2.text

        print(gtitle,ztitle1,zcontent1)

        if not all([gtitle,ztitle1,zcontent1]):
            Snackbar(text="gtitle or ztitle,zcontent is None").show()
        else:

            time.sleep(3)
            z1list = [ztitle1,zcontent1]
            z2list = [ztitle2,zcontent2]
            ziten_updT_List = [z1list,z2list]
            self.api_post(gtitle,ziten_updT_List)
            self.root.ids.pgtitle.text = ""
            self.root.ids.pztitle1.text = ""
            self.root.ids.pzcontent1.text = ""
            self.root.ids.pztitle2.text = ""
            self.root.ids.pzcontent2.text = ""

        self.root.ids.scr_mngr.current = 'fields'





    def refresh_callback(self, *args):
        def refresh_callback(interval):
            print("reload")
            self.api_set()
            self.root.ids.refresh_layout.refresh_done()
            # self.tick=5
            print("done")
            # self.tick = 0
        Clock.schedule_once(refresh_callback, 1)


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

        #新しい順
        ZtitleList = list(reversed(ZtitleList))
        GtitleList = list(reversed(GtitleList))
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


    def api_post(self,gtitle,ziten_updT_List):
        print(ziten_updT_List)
        group_postUrl = "https://zisakuzitenapi2.herokuapp.com/api/groups/?format=json"
        ziten_postUrl = "https://zisakuzitenapi2.herokuapp.com/api/ziten/"
        headers = {"pragma": "no-cache", 'content-type': 'application/json'}
        # 2019-12-14 04:04:45.899541 => 2019-12-14 04:04:45
        now = str(datetime.datetime.now()).split(".")[0]
        gjson = {
            "title": gtitle,
            "updateTime": now
        }
        # 2019-12-14 13:03:52
        r_post = requests.post(group_postUrl, headers=headers, json=gjson)
        posted_id = r_post.json()["id"]
        for i in ziten_updT_List:
            if not i:
                pass
            else:
                zjson = {
                    "title": i[0],
                    "content": i[1],
                    "updateTime": now,
                    "group": posted_id
                }
                r_post = requests.post(ziten_postUrl, headers=headers, json=zjson)
                print(r_post.json())
        print("api_post done!")



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

