import os
import shutil
import customtkinter
from PIL import Image
from osu import Osu


FONT_TYPE = 15
APPDIR = os.getcwd()


class CursorFrame(customtkinter.CTkFrame):
    def __init__(self, *args, header_name="Cursor", **kwargs):
        super().__init__(*args, **kwargs)

        self.fonts = (FONT_TYPE, 15)
        self.header_name = header_name

        self.setup_form()


    def setup_form(self):
        # 行方向のマスのレイアウト設定
        self.grid_rowconfigure(1, weight=1)
        # 列方向のマスのレイアウト設定
        self.grid_columnconfigure(3, weight=1)

        # ラベルを表示
        self.label = customtkinter.CTkLabel(self, text=self.header_name, font=(FONT_TYPE, 11))
        self.label.grid(row=0, column=0, padx=20, sticky="w")

        self.create_file_list(f"{APPDIR}\\images\\cursor\\cursor (1).png")

        try:
            self.image = customtkinter.CTkImage(light_image=Image.open(fp=self.file_array[0]), size=[100, 100])
            self.label2 = customtkinter.CTkLabel(self, image=self.image, text="")
        except:
            self.label2 = customtkinter.CTkLabel(self, text="")
        self.label2.grid(row=1, column=1, padx=20, sticky="nsew")

        self.button_left = customtkinter.CTkButton(self, text="<", fg_color="#444", hover_color="#333", height=50, width=50, command=self.left_cursor)
        self.button_left.grid(row=1, column=0, padx=20)

        self.button_right = customtkinter.CTkButton(self, text=">", fg_color="#444", hover_color="#333", height=50, width=50, command=self.right_cursor)
        self.button_right.grid(row=1, column=2, padx=20)

        self.button_apply = customtkinter.CTkButton(self, text="⟲", width=50, height=28, command=self.apply_default)
        self.button_apply.grid(row=3, column=0, pady=(0, 10))

        self.button_apply = customtkinter.CTkButton(self, text="Apply", command=self.apply)
        self.button_apply.grid(row=3, column=1, pady=(0, 10))

        self.button_apply = customtkinter.CTkButton(self, text="@2x", fg_color="#444", hover_color="#333", command=self.apply2x)
        self.button_apply.grid(row=2, column=1, pady=(30, 10))

        self.button_delete2x = customtkinter.CTkButton(self, text="🗑", fg_color="#700", hover_color="#400", width=50, height=28, command=self.delete2x)
        self.button_delete2x.grid(row=3, column=2, pady=(0, 10))


    def apply_default(self):
        curr_skin = Osu.get_currskin(self)
        osu_dir = Osu.get_osudir(self)
        osu_dir = str(osu_dir).replace('osu!.exe', '')
        os.chdir(osu_dir)
        os.chdir(APPDIR)
        file_name = {'cursor.png',
                     'cursor@2x.png',
                     'cursortrail.png',
                     'cursortrail@2x.png',
                     } 
        for f in file_name:
            try:
                os.remove(f'{osu_dir}Skins\\{curr_skin}\\{f}')
            except:
                pass
            try:
                shutil.copy(f'./images/{curr_skin}/{f}', f'{osu_dir}Skins\\{curr_skin}\\{f}')
            except:
                pass


    def apply(self):
        osu_dir = Osu.get_osudir(self)
        osu_dir = str(osu_dir).replace('osu!.exe', '')
        os.chdir(osu_dir)
        os.chdir(APPDIR)
        curr_skin = Osu.get_currskin(self)
        file_name = ['cursor.png'
                    ]
        try:
            temp = self.cursor2x
            if temp == True:
                file_name.append('cursor@2x.png')
                self.cursor2x = False
        except:
            pass
        try:
            os.remove(f'{osu_dir}Skins\\{curr_skin}\\cursor@2x.png')
        except:
            pass
        for f in file_name:
            try:
                os.remove(f'{osu_dir}Skins\\{curr_skin}\\{f}')
            except:
                pass
            shutil.copy(f'{self.file_array[self.file_no]}', f'{osu_dir}Skins\\{curr_skin}\\{f}')
    

    def apply2x(self):
        self.cursor2x = True
    

    def delete2x(self):
        osu_dir = Osu.get_osudir(self)
        osu_dir = str(osu_dir).replace('osu!.exe', '')
        os.chdir(osu_dir)
        os.chdir(APPDIR)
        curr_skin = Osu.get_currskin(self)
        file_name = {'cursor.png',
                     'cursor@2x.png',
                    }
        for f in file_name:
            try:
                os.remove(f'{osu_dir}Skins\\{curr_skin}\\{f}')
            except:
                pass


    def left_cursor(self):
        self.change_cursor("Left")
    

    def right_cursor(self):
        self.change_cursor("Right")


    def change_cursor(self, flag):
        self.update_file_list(f'{APPDIR}\\images\\cursor\\')
        cnt = len(self.file_array)
        if cnt == 0:                                # 画像ファイル配列が空の時何もしない
            return
        if flag == "Right":                         # 右キーのとき 配列の次のファイル
            self.file_no += 1
            if cnt == self.file_no:                 # 配列上限オーバー時は0に戻る
                self.file_no = 0
        elif flag == "Left":                        # 左キーのとき 配列の一個前のファイル
            self.file_no -= 1
            if self.file_no == -1:                  # 一番最初より前のとき最後のファイルにする
                self.file_no = cnt - 1
        else:
            return                                  # その他のキーでは何もしない
        
        self.image = customtkinter.CTkImage(light_image=Image.open(fp=self.file_array[self.file_no]), size=[100, 100])
        self.label2.configure(image=self.image)

    
    def create_file_list(self, file_path):
        self.file_array = []
        self.file_no = 0
        tmp_arr = os.path.split(file_path)
        dir_name = tmp_arr[0]
        file_name = tmp_arr[1]
        n = 0
        for fname in os.listdir(dir_name):
            file_ext = os.path.splitext(fname)[1].lower()
            if file_ext == ".jpg" or file_ext == ".png" or file_ext == ".tif" or file_ext == ".jpeg" :
                self.file_array.append(os.path.join(dir_name ,fname))
                if file_name == fname:
                    self.file_no = n
                n += 1


    def update_file_list(self, file_path):
        self.file_array = []
        tmp_arr = os.path.split(file_path)
        dir_name = tmp_arr[0]
        for fname in os.listdir(dir_name):
            file_ext = os.path.splitext(fname)[1].lower()
            if file_ext == ".jpg" or file_ext == ".png" or file_ext == ".tif" or file_ext == ".jpeg" :
                self.file_array.append(os.path.join(dir_name ,fname))


    def save_skincursor(self):
        curr_skin = Osu.get_currskin(self)
        try:
            os.makedirs(f"./images/{curr_skin}")
        except:
            return
        osu_dir = Osu.get_osudir(self)
        osu_dir = str(osu_dir).replace('osu!.exe', '')
        os.chdir(osu_dir)
        os.chdir(APPDIR)
        file_name = {f'{osu_dir}Skins\\{curr_skin}\\cursor.png',
                        f'{osu_dir}Skins\\{curr_skin}\\cursor@2x.png',
                        f'{osu_dir}Skins\\{curr_skin}\\cursortrail.png', 
                        f'{osu_dir}Skins\\{curr_skin}\\cursortrail@2x.png'} 
        for f in file_name:
            try:
                shutil.copy(f, f'./images/{curr_skin}/')
            except:
                pass
        


class CursorTrailFrame(customtkinter.CTkFrame):
    def __init__(self, *args, header_name="Cursor Trail", **kwargs):
        super().__init__(*args, **kwargs)

        self.fonts = (FONT_TYPE, 15)
        self.header_name = header_name

        self.setup_form()


    def setup_form(self):
        # 行方向のマスのレイアウト設定
        self.grid_rowconfigure(1, weight=1)
        # 列方向のマスのレイアウト設定
        self.grid_columnconfigure(3, weight=1)

        # ラベルを表示
        self.label = customtkinter.CTkLabel(self, text=self.header_name, font=(FONT_TYPE, 11))
        self.label.grid(row=0, column=0, padx=20, sticky="w")

        self.create_file_list(f"{APPDIR}\\images\\cursortrail\\cursortrail (1).png")

        try:
            self.image = customtkinter.CTkImage(light_image=Image.open(fp=self.cursortrail_array[0]), size=[100, 100])
            self.label2 = customtkinter.CTkLabel(self, image=self.image, text="")
        except:
            self.label2 = customtkinter.CTkLabel(self, text="")
        self.label2.grid(row=1, column=1, padx=20, sticky="nsew")

        self.button_left = customtkinter.CTkButton(self, text="<", fg_color="#444", hover_color="#333", height=50, width=50, command=self.left_cursor)
        self.button_left.grid(row=1, column=0, padx=20)
        
        self.button_right = customtkinter.CTkButton(self, text=">", fg_color="#444", hover_color="#333", height=50, width=50, command=self.right_cursor)
        self.button_right.grid(row=1, column=2, padx=20)

        self.button_apply = customtkinter.CTkButton(self, text="Apply", command=self.apply)
        self.button_apply.grid(row=3, column=1, pady=(0, 10))

        self.button_apply = customtkinter.CTkButton(self, text="@2x", fg_color="#444", hover_color="#333", command=self.apply2x)
        self.button_apply.grid(row=2, column=1, pady=(30, 10))

        self.button_delete2x = customtkinter.CTkButton(self, text="🗑", fg_color="#700", hover_color="#400", width=50, height=28, command=self.delete2x)
        self.button_delete2x.grid(row=3, column=2, pady=(0, 10))


    def apply(self):
        osu_dir = Osu.get_osudir(self)
        osu_dir = str(osu_dir).replace('osu!.exe', '')
        os.chdir(osu_dir)
        os.chdir(APPDIR)
        curr_skin = Osu.get_currskin(self)
        file_name = ['cursortrail.png'
                    ]
        try:
            temp = self.cursortrail2x
            if temp == True:
                file_name.append('cursortrail@2x.png')
                self.cursortrail2x = False
        except:
            pass
        try:
            os.remove(f'{osu_dir}Skins\\{curr_skin}\\cursortrail@2x.png')
        except:
            pass
        for f in file_name:
            try:
                os.remove(f'{osu_dir}Skins\\{curr_skin}\\{f}')
            except:
                pass
            try:
                shutil.copy(f'{self.cursortrail_array[self.cursortrail_no]}', f'{osu_dir}Skins\\{curr_skin}\\{f}')
            except:
                pass


    
    def apply2x(self):
        self.cursortrail2x = True


    def delete2x(self):
        osu_dir = Osu.get_osudir(self)
        osu_dir = str(osu_dir).replace('osu!.exe', '')
        os.chdir(osu_dir)
        os.chdir(APPDIR)
        curr_skin = Osu.get_currskin(self)
        file_name = {'cursortrail.png',
                     'cursortrail@2x.png',
                    }
        for f in file_name:
            try:
                os.remove(f'{osu_dir}Skins\\{curr_skin}\\{f}')
            except:
                pass
    

    def left_cursor(self):
        self.change_cursor("Left")
    

    def right_cursor(self):
        self.change_cursor("Right")


    def change_cursor(self, flag):
        self.update_file_list(f'{APPDIR}\\images\\cursortrail\\')
        cnt = len(self.cursortrail_array)
        if cnt == 0:                                # 画像ファイル配列が空の時何もしない
            return
        if flag == "Right":                         # 右キーのとき 配列の次のファイル
            self.cursortrail_no += 1
            if cnt == self.cursortrail_no:          # 配列上限オーバー時は0に戻る
                self.cursortrail_no = 0
        elif flag == "Left":                        # 左キーのとき 配列の一個前のファイル
            self.cursortrail_no -= 1
            if self.cursortrail_no == -1:           # 一番最初より前のとき最後のファイルにする
                self.cursortrail_no = cnt - 1
        else:
            return                                  # その他のキーでは何もしない
        
        self.image = customtkinter.CTkImage(light_image=Image.open(fp=self.cursortrail_array[self.cursortrail_no]), size=[100, 100])
        self.label2.configure(image=self.image)  
        

    def create_file_list(self, file_path):
        self.cursortrail_array = []
        self.cursortrail_no = 0
        tmp_arr = os.path.split(file_path)
        dir_name = tmp_arr[0]
        file_name = tmp_arr[1]
        n = 0
        for fname in os.listdir(dir_name):
            file_ext = os.path.splitext(fname)[1].lower()
            if file_ext == ".jpg" or file_ext == ".png" or file_ext == ".tif" or file_ext == ".jpeg" :
                self.cursortrail_array.append(os.path.join(dir_name ,fname))
                if file_name == fname:
                    self.cursortrail_no = n
                    n += 1


    def update_file_list(self, file_path):
        self.cursortrail_array = []
        tmp_arr = os.path.split(file_path)
        dir_name = tmp_arr[0]
        for fname in os.listdir(dir_name):
            file_ext = os.path.splitext(fname)[1].lower()
            if file_ext == ".jpg" or file_ext == ".png" or file_ext == ".tif" or file_ext == ".jpeg" :
                self.cursortrail_array.append(os.path.join(dir_name ,fname))

