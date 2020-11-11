#自作関数モジュール
import sys,os
import csv
#import importXMLV03 #親pyファイル名def CSVExport():
iDir = os.path.abspath(os.path.dirname(sys.argv[0]))

#XMLファイル名を取得する関数
def GetFileName():
    # tkinterモジュールのインポート
    import tkinter, tkinter.filedialog, tkinter.messagebox
    # ファイル選択ダイアログの表示
    root = tkinter.Tk()
    root.withdraw()
    fTyp = [("","*")]
    #iDir = os.path.abspath(os.path.dirname(__file__))
    tkinter.messagebox.showinfo('xmlファイルの選択','処理するxmlファイルを選択してください！')
    file = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
    fileformat=file[-4:]
    #print(fileformat)
    if fileformat != ".xml": 
        tkinter.messagebox.showinfo('ファイル形式エラー','xmlファイルを選択してください。')
        sys.exit()
    return file

#csvファイルを出力する関数
def csvexport_list(csvfilename,exlist):
    csvfilename=csvfilename+'.csv'
#    csvfile=os.path.join(os.path.abspath(os.path.dirname(__file__)),'csv',csvfilename)
    csvfile=os.path.join(iDir,'csv',csvfilename)
    with open(csvfile, 'w') as f:
        writer =csv.writer(f, lineterminator='\n')
        writer.writerows(exlist)
    return print("CSV export was succeeded.")

#ST_,AT_表記の変換
def altvalue(ex_list,ST2Num_list,lineNo):
    for i in range(len(ex_list)):
        for j in range(len(ST2Num_list)):
            k1=ST2Num_list[j][0] in ex_list[i][lineNo]
            if k1==True:
                TCstr=str(ex_list[i][lineNo])
                k2=TCstr.find(ST2Num_list[j][0]) #開始位置
                k31=TCstr.find(',',k2+1) #終了位置1
                k32=TCstr.find(')',k2+1) #終了位置2
                if k31<0 and k32<0: #文字列の最後尾
                    STstr=TCstr[k2:]
                elif k31>0 and k32<0: #,まで
                    STstr=TCstr[k2:k31]
                elif k31<0 and k32>0: #)まで
                    STstr=TCstr[k2:k32]
                elif k32>k31: #,まで
                    STstr=TCstr[k2:k31]
                elif k31>k32: #)まで
                    STstr=TCstr[k2:k32]
                if ST2Num_list[j][0]==STstr: #変数名が最後まで一致していれば
                    k5=TCstr.replace(ST2Num_list[j][0],ST2Num_list[j][1])
                    ex_list[i][lineNo]=k5
    return(ex_list)

#jsonファイルの出力
def JsonExport(jsonfilename,jsondict):
    jsonfile=os.path.join(iDir,'json',jsonfilename)
    import json,codecs
    with codecs.open(jsonfile,'w', 'utf-8') as f:
        dump = json.dumps(jsondict,indent=2,ensure_ascii=False)
        f.write(dump)
        return print("Json export was succeeded.")