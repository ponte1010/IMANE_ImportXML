import my_functionV03 #自作関数のインポート
import sys

#setting.jsonの作成
def SettingJson(TeamData_list):
  #TeamAddress="samplerM32.com";TeamName="SampleConpanyrM32" #モジュール動作テスト用
  TeamAddress=TeamData_list[1][3];TeamName=TeamData_list[1][4]
  setting_dict={
    "teams":[
      {"id":TeamAddress,"name":TeamName}
    ],
    "phases":[
      {"phase":1,"description":"phase1","timelimit":1200,"endstate":[]}
    ]
  }
  #setting.jsonの出力
  my_functionV03.JsonExport('setting.json',setting_dict)
  return print("setting.json export was succeeded.")

#contacts.jsonの作成
def ContactsJson(TeamData_list,Actor_list):
  #TeamAddress="samplerM32.com";TeamName="SampleConpanyrM32" #モジュール動作テスト用
  TeamAddress=TeamData_list[1][3];Recipients=[]
  for i in range(3,len(Actor_list)):
    Recipients.append(Actor_list[i][3])
  contacts_dict={};contacts_list=[]
  for i in range(2,len(Actor_list)):
    AcName=Actor_list[i][3];Role=Actor_list[i][4];RoleName=Actor_list[i][4];Email=AcName+'@'+TeamAddress;Team=TeamAddress;Desc=Actor_list[i][5]
    if Actor_list[i][2]=='Auto':
      bool1=True
    elif Actor_list[i][2]=='Manual':
      bool1=False
    System=[bool1]
    k={"name":AcName,"role":Role,"rolename":RoleName,"email":Email,"team":Team,"desc":Desc,"recipients":Recipients,"system":System}
    contacts_list.append(k)
    contacts_dict={"contacts":contacts_list}
  #ファシリテータ
  ActName="facilitator";Role="facilitator";RoleName="facilitator";Email=ActName+'@'+TeamAddress;Team=TeamAddress
  bool1=False;System=[bool1];Recipients=["all"];Isadmin=True
  k={"name":ActName,"role":Role,"rolename":RoleName,"email":Email,"team":Team,"system":System,"recipients":Recipients,"isadmin":Isadmin}
  contacts_list.append(k)
  contacts_dict={"contacts":contacts_list}
  #contacts.jsonの出力
  my_functionV03.JsonExport('contacts.json',contacts_dict)
  return print("contacts.json export was succeeded.")

def ActionsJson(ex_list,Actor_list):
  actions_dict={};actions_list=[]

  #idの採番
  for i in range(1,len(ex_list)):
    ACactive=int(ex_list[i][0])
    if ACactive==0: #0で終了
      sys.exit(1)
    elif ACactive>0: #正で読み取り
      #if ex_list[i][2]=="Timer": #systemの場合は、actions.json不要だったわ
      #  ACNo=int(ex_list[i][1])
      #  if ACNo<10:ACid="s000"+str(ACNo)
      #  elif ACNo<100:ACid="s00"+str(ACNo)
      #  elif ACNo<1000:ACid="s0"+str(ACNo)
      #  elif ACNo<10000:ACid="s"+str(ACNo)
      #  else: sys.exit(1) #カードは制限枚数越え
      #else: #Auto,Manualの場合
      ACNo=int(ex_list[i][1])
      if ACNo<10:ACid="A0000"+str(ACNo)
      elif ACNo<100:ACid="A000"+str(ACNo)
      elif ACNo<1000:ACid="A00"+str(ACNo)
      elif ACNo<10000:ACid="A0"+str(ACNo)
      elif ACNo<100000:ACid="A"+str(ACNo)
      else: sys.exit(1) #カードは制限枚数越え

      ACMode=ex_list[i][2] #Mode別にアクションカードを読み取り
      #if ACMode=='Timer': #Timerなら
      #  ACName=ex_list[i][3];ACMessage=ex_list[i][4];ACDesc=ex_list[i][5];ACTo=ex_list[i][14]
      #  ACAttachments=[];ACRoles=[];ACSC=[];bool1=True
      #  k={"name":ACName,"type":"notification","id":ACid,"roles":"all"}
      #  if ACTo!="":k["assignTo"]=ACTo
      #  if ACDesc!="":k["desc"]=ACDesc
      #  k["hidden"]=bool1
      #  actions_list.append(k)

      if ACMode=='Manual': #Manualなら
        ACName=ex_list[i][3];ACMessage=ex_list[i][4];ACDesc=ex_list[i][5]
        ACAttachments=[];ACRoles=[];ACSC=[]
        ACAttachments.append(ex_list[i][16]);ACRoles.append(ex_list[i][18]);ACSC.append(ex_list[i][19])
        k={"type":"action","name":ACName}
        if ACMessage!="":k["message"]=ACMessage
        if ACDesc!="":k["desc"]=ACDesc
        if ACAttachments[0]!="":k["attachments"]=ACAttachments
        if ACRoles[0]!="":k["roles"]=ACRoles
        if ACSC[0]!="":k["statecondition"]=ACSC               
        k["id"]=ACid
        actions_list.append(k)

      elif ACMode=='Auto': #Autoなら
        ACName=ex_list[i][3];ACMessage=ex_list[i][4];ACDesc=ex_list[i][5]
        ACDelay=int(ex_list[i][12]);ACFrom=ex_list[i][13];ACTo=ex_list[i][14];ACCc=ex_list[i][15]
        ACSSC=[];ACRSC=[];ACAttachments=[]
        ACAttachments.append(ex_list[i][16]);ACRSC.append(ex_list[i][9]);ACSSC.append(ex_list[i][10])
        k={"type":"auto","name":ACName}
        if ACMessage!="":k["message"]=ACMessage
        if ACDesc!="":k["desc"]=ACDesc
        if ACRSC[0]!="":k["removestatecondition"]=ACRSC
        if ACSSC[0]!="":k["systemstatecondition"]=ACSSC
        if ACDelay!="":k["delay"]=ACDelay
        if ACFrom!="":k["from"]=ACFrom
        if ACTo!="":k["to"]=ACTo
        if ACCc!="":k["cc"]=ACCc
        if ACAttachments[0]!="":k["attachments"]=ACAttachments
        k["id"]=ACid
        actions_list.append(k)

  #自動入力
  ACRoles=["all"]
  #通知
  bool1=True
  k={"name":"通知","type":"notification","id":"s0000","roles": ACRoles,"assignTo":ACRoles,"description":"システムからの通知メッセージです。","hidden":bool1}
  actions_list.append(k)
  #相談
  k={"name":"相談","type":"talk","id":"i0001","roles":ACRoles,"assignTo":ACRoles,"description":"任意のコミュニケーションに使用します。"}
  actions_list.append(k)
  #報告・連絡
  k={"name":"報告・連絡","type":"action","id":"i0009","attach":bool1,"roles":ACRoles,"description":"他ロールへのインシデント情報の共有・展開"}
  actions_list.append(k)
  actions_dict={"actions":actions_list}
  #actions.jsonの出力
  my_functionV03.JsonExport('actions.json',actions_dict)
  return print("actions.json export was succeeded.")

def StatesJson(ex_list):
  states_list=[]
  for i in range(1,len(ex_list)):
    SAddstateList=ex_list[i][6];SName=ex_list[i][3];SAttachmentList=ex_list[i][16];SAttachmentNameList=ex_list[i][17]
    #State
    if SAddstateList!="":
      k={}
      k["id"]=SAddstateList
      k["name"]=SName
      k["type"]=1
      states_list.append(k)
    #Attachment
    if SAttachmentList!="":
      k={}
      k["id"]=SAttachmentList
      k["name"]=SAttachmentNameList
      k["type"]=1
      states_list.append(k)
  #自動入力
  k={}
  k["id"]="1009999"
  k["type"]=3
  k["name"]="対応外"
  states_list.append(k)
  #states.jsonの出力
  my_functionV03.JsonExport('states.json',states_list)
  return print("states.json export was succeeded.")

#replies.jsonの生成
def RepliesJson(ex_list):
  replies_dict={};states_list=[];states_dict={};reply_list=[];message_list=[]
  #reply_list
  for i in range(1,len(ex_list)):
    k={}
    ACactive=int(ex_list[i][0])
    if ACactive==0: #0で終了
      sys.exit(1)
    elif ACactive>0: #正で読み取り
      if ex_list[i][2]=="Timer": #systemの場合
        #id採番しなくてもよかったわ
        #ACNo=int(ex_list[i][1])
        #if ACNo<10:ACid="s000"+str(ACNo)
        #elif ACNo<100:ACid="s00"+str(ACNo)
        #lif ACNo<1000:ACid="s0"+str(ACNo)
        #elif ACNo<10000:ACid="s"+str(ACNo)
        #else: sys.exit(1) #カードは制限枚数越え
        #reply要素の生成
        k["actionid"]="s0000"
        if ex_list[i][3]!="":k["name"]=ex_list[i][3]
        if ex_list[i][4]!="":k["message"]=ex_list[i][4]
        if ex_list[i][5]!="":k["desc"]=ex_list[i][5]
        if ex_list[i][6]!="":k["addstate"]=[ex_list[i][6]]
        if ex_list[i][12]!="":k["delay"]=int(ex_list[i][12])
        if ex_list[i][13]!="":k["from"]=ex_list[i][13]
        if ex_list[i][14]!="":k["to"]=ex_list[i][14]
        if ex_list[i][15]!="":k["cc"]=ex_list[i][15]
        if ex_list[i][16]!="":k["state"]=ex_list[i][16]
        if ex_list[i][11]!="":k["elapsed"]=int(ex_list[i][11])
      else: #Auto,Manualの場合
        #id採番
        ACNo=int(ex_list[i][1])
        if ACNo<10:ACid="A0000"+str(ACNo)
        elif ACNo<100:ACid="A000"+str(ACNo)
        elif ACNo<1000:ACid="A00"+str(ACNo)
        elif ACNo<10000:ACid="A0"+str(ACNo)
        elif ACNo<100000:ACid="A"+str(ACNo)
        else: sys.exit(1) #カードは制限枚数越え
        #reply要素の生成
        k["type"]="hidden"
        if ex_list[i][6]!="":k["addstate"]=[ex_list[i][6]]
        if ex_list[i][14]!="":k["to"]=ex_list[i][14]
        if ex_list[i][3]!="":k["name"]=ex_list[i][3]
        if ex_list[i][4]!="":k["message"]=ex_list[i][4]
        if ex_list[i][5]!="":k["desc"]=ex_list[i][5]
        k["actionid"]=ACid
      reply_list.append(k)#要素をリストに追加
  #自動入力
  bool1=True
  k={"actionid":"i0001","to":"all","name":"相談"};reply_list.append(k)
  k={"actionid":"all","to": "all","name": "こちらの対応範囲外です。別のところにお問い合わせ下さい。","delay":5,"abort": bool1,"type":"notfound"};reply_list.append(k)
  k={"actionid":"all","to": "all","name":"自動応答２","type":"null","delay": 0,"abort":bool1};reply_list.append(k)
  #message_list
  k={"actionid":"8000","text":"8000のテキスト"};message_list.append(k)
  #states_dictの作成
  states_dict={"phase":"1"}
  states_dict["reply"]=reply_list
  states_dict["message"]=message_list
  #replies_dictの作成
  states_list=[states_dict]
  replies_dict["states"]=states_list
  #actions.jsonの出力
  my_functionV03.JsonExport('replies.json',replies_dict)
  return print("replies.json export was succeeded.")

#pointss.jsonの生成 ->未作成
def PointsJson(ex_list):
  points_dict={}
  points_dict["pointcard"]=[]
  #points.jsonの出力
  my_functionV03.JsonExport('points.json',points_dict)
  return print("points.json export was succeeded.")
