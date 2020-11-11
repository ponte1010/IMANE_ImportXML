import sys,os
import numpy as np #numpyパッケージのインポート
import my_functionV03 #自作関数のインポート
import os, tkinter, tkinter.filedialog, tkinter.messagebox # ファイル選択用モジュールのインポート

def MakeList(Actor_list,AC_list,LO_list,LOid_array,Line_list,Arrow_list): #excel出力用リストの生成
    Actor_array=np.array(Actor_list)

    ex_list=[['0Active','1CardNo','2Mode','3Name','4Message','5Description','6AddState-List'\
        ,'7AddState-Name-List','8AddState-To','9RemoveState-List','10TrigerCondition','11TrigerTimer'\
            ,'12Delay','13From','14To','15O_Cc','16Attachment-List','17Attachment-Name-List','18Roles-List','19DisplayCondition']]
    ST2Num_list=[];ST2Num_list2=[];STNum=''
    AT2Num_list=[];AT2Num_list2=[];ATNum=''
    acct=len(AC_list)-1
    for i in range(1,acct+1):
        label=AC_list[i][1].replace('<br>','')
        ex_list2=['1'] #0Active

        ex_list2.append(AC_list[i][3]) #1CardNo
        
        k='' #2Mode
        if AC_list[i][5]!='':
            k=AC_list[i][5]
        else:
            for j in range(1,len(Actor_list)):
                if Actor_list[j][3]==AC_list[i][2]: #Actor_listのidがカードの親のidなら
                    k=Actor_list[j][2] #親のアクタのModeを取得
        ex_list2.append(k) 
        
        if AC_list[i][6] !='':ex_list2.append(AC_list[i][6]) #3Name、dataが空ならラベルをNameとする
        else:ex_list2.append(label)
        
        if AC_list[i][7] !='':ex_list2.append(AC_list[i][7]) #4Message、dataが空ならラベルをMessageとする
        else:ex_list2.append(label)
        
        ex_list2.append(AC_list[i][8]) #5description

        k='ST_' + AC_list[i][0] #6AddState-List 'ST_id'
        ex_list2.append(k) 
        #ST_に対応する数値記述を作成する
        k3=np.where(Actor_array==AC_list[i][2]) #ActorNoを取得する
        k31=k3[0]
        k32=str(k31[0])
        k32.strip('[')
        k32.strip(']')
        k32=int(k32)
        if k32<=0:
            tkinter.messagebox.showinfo('Design Error','The actor of the ActionCard '+AC_list[i][0]+' is not obtained.')
            sys.exit(1)
        elif k32<=9:
            k32='0'+str(k32)
        else:k32=str(k32)
        ST2Num_list2.append(k)
        if i<=9:
            i2='000'+str(i)
        elif i<=99:
            i2='00'+str(i)
        elif i<=999:
            i2='0'+str(i)
        elif i<=9999:
            i2=str(i)
        else:
            tkinter.messagebox.showinfo('Design Error','The amount of the ActionCards is over 9999.')
            sys.exit(1)
        STNum='10'+k32+i2
        ST2Num_list2.append(STNum)
        ST2Num_list.append(ST2Num_list2)
        ST2Num_list2=[]

        if AC_list[i][10] !='':ex_list2.append(AC_list[i][10]) #7AddState-Name-List 手動入力優先
        else:ex_list2.append(label) 
        if AC_list[i][11]!='':#8AddState-To 手動入力のみ！
            k=AC_list[i][11] 
        else:k='system'

        ex_list2.append(k)
        k=''#9RemoveState-list
        if AC_list[i][12]!='':#手動入力優先
            k=AC_list[i][12] 
        else:
            tar=''
            for j in range(len(Arrow_list)):
                if Arrow_list[j][1]==AC_list[i][0]: #sourceになっている（=arrowの出力がある）
                    tar=Arrow_list[j][2] #ターゲットのカードのidを取得
                    k='ST_' + tar + ','
        ex_list2.append(k[:-1])

        k='' #10TriggerCondition
        if AC_list[i][13]!='':#手動入力優先
            k=AC_list[i][13] 
        else:
            for j in range(len(Line_list)):
                if Line_list[j][2]==AC_list[i][0]: #targetになっている（=lineの出力がある）
                    k1=np.where(LOid_array==Line_list[j][1])
                    if k1[0]!=False: #ラインの入力は演算子
                        k=LO_list[k1[0][0]][3]
                    else:#ラインの入力はカード
                        k='ST_'+Line_list[j][1] #sourceのカードのstateを取得
            if k=='': #targetになっていなければ（=lineの入力がない）空
                k=''
        ex_list2.append(k)
        
        if ex_list2[2]=='Timer': #11TriggerTimer
            if AC_list[i][14] !='':ex_list2.append(AC_list[i][14])
            else:ex_list2.append('0')
        else:ex_list2.append('')

        if AC_list[i][15] !='':ex_list2.append(AC_list[i][15]) #12delay
        else:ex_list2.append('0')

        ex_list2.append(AC_list[i][2]) #13from 親アクタ

        k='' #14to
        if AC_list[i][17]!='':#14to 手動入力のみ！
            k=AC_list[i][17] 
        else:k='system'
        ex_list2.append(k)
        
        ex_list2.append(AC_list[i][18]) #15cc　手動入力のみ

        k='AT_' + AC_list[i][0] #16Attachment-List 自動生成'AT_id'
        ex_list2.append(k)
        AT2Num_list2.append(k)
        if i<=9:
            i2='000'+str(i)
        elif i<=99:
            i2='00'+str(i)
        elif i<=999:
            i2='0'+str(i)
        elif i<=9999:
            i2=str(i)
        else:
            tkinter.messagebox.showinfo('design error','The number of the ActionCards is over 9999.')
            sys.exit(1)
        ATNum='20'+k32+i2
        AT2Num_list2.append(ATNum)
        AT2Num_list.append(AT2Num_list2)
        AT2Num_list2=[]

        if AC_list[i][20] !='':ex_list2.append(AC_list[i][20]) #17Attachment-Name-List 手動入力優先
        else:ex_list2.append(label) 

        #18Roles-list
        if ex_list2[2]=='Manual':#Mode='Manual'時のみ入力 *今はexcel出力なのでOFF
            if AC_list[i][21] !='':ex_list2.append(AC_list[i][21])#手動入力優先
            else:ex_list2.append(AC_list[i][2]) #親アクタを自動入力
        else:ex_list2.append('')

        k='' #19DisplayCondition
        if ex_list2[2]=='Manual':#Mode='Manual'時のみ入力 *今はexcel出力なのでOFF
            if AC_list[i][22]!='':#手動入力優先
                k=AC_list[i][22] 
            else:
                k=ex_list2[10].replace('ST_','AT_')
        else:pass
        ex_list2.append(k)

        #ex_list2をex_listの行として追加する
        ex_list.append(ex_list2)
    
    #ST_,AT_表記の変換
    c = my_functionV03.altvalue(ex_list,ST2Num_list,6) #addstate-list
    ex_list=c
    c = my_functionV03.altvalue(ex_list,ST2Num_list,9) #removestate-list
    ex_list=c
    c = my_functionV03.altvalue(ex_list,ST2Num_list,10) #TriggerCondition
    ex_list=c
    c = my_functionV03.altvalue(ex_list,AT2Num_list,16) #attachment-list
    ex_list=c
    c = my_functionV03.altvalue(ex_list,AT2Num_list,19) #DisplayCondition
    ex_list=c

    return ex_list,ST2Num_list,AT2Num_list