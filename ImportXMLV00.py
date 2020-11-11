#XMLファイルを読み込むモジュール

import sys #sys関数のインポート(例外処理のため)
import my_functionV03, PurseXMLmoduleV03, MakeListV03,MakeJsonV00 #自作関数のインポート
import xml.etree.ElementTree as ET # xmlモジュールのインポート
import numpy as np #numpyパッケージのインポート
import os, tkinter, tkinter.filedialog, tkinter.messagebox # ファイル選択用モジュールのインポート

# xmlファイルの読み込み
FileName = my_functionV03.GetFileName() #ファイル名を取得
tree = ET.parse(FileName) # XMLを取得
root = tree.getroot() 

#xml記述のパース（別モジュールをコール）
a = PurseXMLmoduleV03.PurseXML(root)
TeamData_list=a[0]
Actor_list=a[1];Actor_array=np.array(Actor_list)
AC_list=a[2]
LO_list=a[3]
LOid_array=a[4]
Line_list=a[5]
Arrow_list=a[6]

#excel出力用リストの生成（別モジュールをコール）
b = MakeListV03.MakeList(Actor_list,AC_list,LO_list,LOid_array,Line_list,Arrow_list)
ex_list=b[0]
ST2Num_list=b[1]
AT2Num_list=b[2]

#csv出力
c = my_functionV03.csvexport_list('TeamData_list',TeamData_list) #actorsのチームデータ
c = my_functionV03.csvexport_list('Actor_list',Actor_list) #actorsのアクタ
c = my_functionV03.csvexport_list('sample_writer_row',ex_list) #senario
c = my_functionV03.csvexport_list('ST2Num',ST2Num_list) #ID確認用
c = my_functionV03.csvexport_list('AT2Num',AT2Num_list) #ID確認用

#json出力
d = MakeJsonV00.SettingJson(TeamData_list) #setting.json
d = MakeJsonV00.ContactsJson(TeamData_list,Actor_list) #contacts.json
d = MakeJsonV00.ActionsJson(ex_list,Actor_list) #actions.json
d = MakeJsonV00.StatesJson(ex_list) #states.json
d = MakeJsonV00.RepliesJson(ex_list) #replies.json
d = MakeJsonV00.PointsJson(ex_list) #points.json