import sys,os
import xml.etree.ElementTree as ET # xmlモジュールのインポート
import numpy as np #numpyパッケージのインポート
import os, tkinter, tkinter.filedialog, tkinter.messagebox # ファイル選択用モジュールのインポート

#XMLファイル名を取得する関数
def PurseXML(root):
    #レイヤのidを取得
    lay_ct=0
    for mxCell in root.iter('mxCell'):
        if lay_ct==2:
            break
        elif mxCell.get('value')=='Actor': #アクタレイヤのidを取得
            #ActLayerID=mxCell.get('id')　未使用
            lay_ct=lay_ct+1
            continue
        elif mxCell.get('value')=='Scenario': #シナリオレイヤのidを取得
            #ScnLayerID=mxCell.get('id') 未使用
            lay_ct=lay_ct+1

    #チーム情報の取得（親スイムレーン）
    TeamData_list=[['id','ShapeType','label','TeamAddress','TeamName','DataDir']]
    for Ob in root.iter('object'):
        if Ob.get('ShapeType')=='TeamData': #チームデータ（親スイムレーン）のidを取得
            ActParentID=Ob.get('id')
            TeamData_list.append([Ob.get('id'),Ob.get('ShapeType'),Ob.get('label'),Ob.get('TeamAddress')\
                ,Ob.get('TeamName'),Ob.get('DataDir')])
            break

    #アクター情報の取得（子スイムレーン）
    Actor_list=[['id','ShapeType','Mode','label','Role','Account']]
    for Ob in root.iter('object'):
        i=Ob.attrib
        j=i.get('ShapeType')
        if j=='Actor': #アクター（子スイムレーン）の取得
            for mxCell in Ob.iter('mxCell'):
                k=mxCell.attrib
                if 'swimlane' in k.get('style')==False:  #アクターがスイムレーンでなければエラー
                    tkinter.messagebox.showinfo('design error','The actor '+Ob.get('id')+' is not a swimlane.')
                    print(Ob.get('id')+' is an incorrect actor.')
                    sys.exit(1)
                elif mxCell.get('parent')!=ActParentID: #親スイムレーン上になければエラーを返す
                    tkinter.messagebox.showinfo('design error','The actor '+Ob.get('id')+' is an incorrect swimlane.')
                    print(Ob.get('id')+' is an incorrect swimlane.')
                    sys.exit(1)
            Actor_list.append([Ob.get('id'),Ob.get('ShapeType'),Ob.get('Mode'),Ob.get('label')\
                ,Ob.get('Role'),Ob.get('Account')])
    
    #アクションカードのデータをリストに格納
    AC_list=[['0id','1label','2parent','3CardNo','4ShapeType','5Mode','6Name','7Message','8Description','9AddStateList'\
        ,'10AddStateNameList','11AddStateTo','12RemoveStateList','13TrigerCondition','14TrigerTimer'\
            '15Delay','16From','17To','18Cc','19AttachmentList','20AttachmentNameList','21RolesList','22DisplayCondition']]
    acct=0;a=[]
    ACid_array=np.array([])
    for j in root.iter('object'):
        if j.get('A_ShapeType')=='ActionCard':
            acct+=1
            for mxCell in j.iter('mxCell'):
                k=mxCell.attrib.get('parent') #parentのidを取得
                for y,row in enumerate(Actor_list):
                    try:
                        pos=(y,row.index(k))
                        break
                    except ValueError:
                        pass
                k=Actor_list[pos[0]][3] #parentのアクターを取得
                if pos[0]==0:
                    tkinter.messagebox.showinfo('design error',Ob.get('id')+' card is not on an user swimlane.')
                    print(Ob.get('id')+' card is not on an user swimlane.')
                    sys.exit(1)

            a.append(j.get('id'));a.append(j.get('label'));a.append(k)
            a.append(str(acct));a.append(j.get('A_ShapeType'));a.append(j.get('B_Mode'))
            a.append(j.get('C_Name'));a.append(j.get('D_Message'));a.append(j.get('E_Description'))
            a.append(j.get('F_AddStateList'));a.append(j.get('G_AddStateNameList'))
            a.append(j.get('H_AddStateTo'));a.append(j.get('I_RemoveStateList'))
            a.append(j.get('J_TrigerCondition'));a.append(j.get('K_TrigerTimer'))
            a.append(j.get('L_Delay'));a.append(j.get('M_From'))
            a.append(j.get('N_To'));a.append(j.get('O_Cc')),a.append(j.get('P_AttachmentList'))
            a.append(j.get('Q_AttachmentNameList'));a.append(j.get('R_RolesList'))
            a.append(j.get('S_DisplayCondition'))
            AC_list.append(a)
            ACid_array= np.append( ACid_array, j.get('id'))
            a=[]

    #論理演算子
    LO_list=[['id','operation','foward']]
    LOid_array=np.array(['LOid_array'])
    for mxCell in root.iter('mxCell'):
        i=mxCell.attrib
        j=i.get('style')
        if j!=None:
            dict={}
            while j!='':
                j1=j.find('=') ;j2=j[0:j1];j3=j.find(';')
                if j1<j3:dict[j2]=j[j1+1:j3]
                else:
                    j4=j[0:j3];dict[j4]=''#value=''
                j=j[j3+1:]
            a=[]

            if dict.get('shape')!=None:
                if dict.get('shape')=='mxgraph.electrical.logic_gates.logic_gate':#論理演算子なら
                    a.append(i.get('id')) 
                    a.append(dict.get('operation').upper()) #演算子のid/種類'and'とか'or'とか
                    LO_list.append(a)
                    LOid_array= np.append( LOid_array, i.get('id'))
                    continue
                elif dict.get('shape')=='mxgraph.electrical.logic_gates.buffer2':#NOTなら
                    a.append(i.get('id')) 
                    a.append('NOT') #演算子のid/種類'and'とか'or'とか
                    LO_list.append(a)
                    LOid_array= np.append( LOid_array, i.get('id')) 
                    continue  

    #Line、Arrowの取得
    Line_list=[['id','source','target']]
    Arrow_list=[['id','source','target']]
    LineTar_array=np.array(['LineTar_array'])
    a=[]
    for mxCell in root.iter('mxCell'):
        i=mxCell.attrib;j=i.get('style')
        if j!=None:
            dict={}
            while j!='':
                j1=j.find('=') ;j2=j[0:j1];j3=j.find(';')
                if j1<j3:dict[j2]=j[j1+1:j3]
                else:
                    j4=j[0:j3];dict[j4]=''#value=''
                j=j[j3+1:]
            if dict.get('edgeStyle') ==None:
                continue
            elif dict.get('edgeStyle')=='orthogonalEdgeStyle' and dict.get('shape')==None:#Lineなら
                index11=np.where(ACid_array==mxCell.get('target'))
                index12=np.where(LOid_array==mxCell.get('target'))
                index21=np.where(ACid_array==mxCell.get('source'))
                index22=np.where(LOid_array==mxCell.get('source'))
                if index11==False or index12==False:#ラインのターゲットがアクションカードまたは論理演算子でなければエラー
                    tkinter.messagebox.showinfo('Design Error','Line '+Ob.get('id')+' does not have the correct target.')
                    print('Line '+Ob.get('id')+' does not have the correct target.')
                    sys.exit(1)
                elif index21==False or index22==False:#ラインのソースがアクションカードまたは論理演算子でなければエラー
                    tkinter.messagebox.showinfo('Design Error','Line '+Ob.get('id')+' does not have the correct source.')
                    print('Line '+Ob.get('id')+' does not have the correct source.')
                    sys.exit(1)
                else:
                    a.append(mxCell.get('id'));a.append(mxCell.get('source'));a.append(mxCell.get('target'))
                    Line_list.append(a);a=[]
                    LineTar_array= np.append(LineTar_array, mxCell.get('target'))
                continue
            elif dict.get('edgeStyle')=='orthogonalEdgeStyle' and dict.get('shape')=='flexArrow':#Arrowなら
                index1=np.where(ACid_array==mxCell.get('target'))
                index2=np.where(ACid_array==mxCell.get('source'))
                if index1==False:#アローのターゲットがアクションカードでなければエラー
                    tkinter.messagebox.showinfo('design error','Arrow '+Ob.get('id')+' does not have the correct target.')
                    print('Arrow '+Ob.get('id')+' does not have the correct target.')
                    sys.exit(1)
                elif index2==False:#アローのソースがアクションカードでなければエラー
                    tkinter.messagebox.showinfo('design error','Arrow '+Ob.get('id')+' does not have the correct source.')
                    print('Arrow '+Ob.get('id')+' does not have the correct source.')
                    sys.exit(1)
                else:
                    a.append(mxCell.get('id'));a.append(mxCell.get('source'));a.append(mxCell.get('target'))
                    Arrow_list.append(a);a=[]
                continue
            else:pass

    #------------------------------------------------------------------------
    #論理演算子の接続関係を整理
    mae='';ct=0
    for i in LO_list[1:]: #LO_listに入力情報を追加
        ct+=1
        k1=np.where(LineTar_array == i[0])#演算子の入力となるLineのインデックスを取得 1,5
        for j in range(len(k1[0])):
            #print(Line_list[k1[0][j]][1])
            k2=np.where(LOid_array == Line_list[k1[0][j]][1])#このラインのsourceに演算子があるか？
            if k2[0]>=1:
                mae= mae + 'LO_'+ str(k2[0][0]) +','#前が演算子なら、LO_前の演算子のインデックス
            else:mae= mae + 'ST_'+Line_list[k1[0][j]][1] +','#前がアクションカードなら、ST_カードのid   
        LO_list[ct].append(mae)
        mae=''

    ct=0;skip_list=[]
    for i in LO_list[1:]: #LO_listに演算式を追加
        ct+=1
        k1='LO_' in LO_list[ct][2]
        if k1==False:
                k2=LO_list[ct][2]
                k2=k2[:-1]
                LO_list[ct].append(LO_list[ct][1]+'('+k2+')')#演算子の前がアクションカードのみなら演算式を入力
                continue
        else:
                LO_list[ct].append('skip')#演算子の前に演算子がある場合、入力をスキップ
                skip_list.append(ct)
    skip_list2=[]
    ct=len(skip_list)
    while ct>0:
        for i in range(len(skip_list)): #スキップした要素を入力
            k1=str(LO_list[skip_list[i]][2])
            index1 = k1.find('LO_')
            while index1>=0:
                index1 = k1.find('LO_')
                index21 = k1.find(',',index1)
                if index1<index21:
                    index11=index1+3
                    k2=k1[index11:index21]
                    k2=int(k2)
                index1 = k1.find('LO_',index11)
                k3=LO_list[k2][3]
                if k3!='skip':
                    kk1=k1.replace('LO_'+str(k2),k3)
                    k1=kk1
                else:pass
            LO_list[skip_list[i]][2]=k1
            if k1.find('LO_')==-1:
                LO_list[skip_list[i]][3]=LO_list[skip_list[i]][1]+'('+k1[:-1]+')'
                ct-=1
            else:skip_list2.append(skip_list[i])
        skip_list=skip_list2;skip_list2=[]

    return TeamData_list,Actor_list,AC_list,LO_list,LOid_array,Line_list,Arrow_list