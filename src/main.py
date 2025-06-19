import customtkinter
import customtkinter as ctk
from PIL import Image
from src.NewGUI.MainPage import MainPage


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title('神秘股市')
        self.app_width = int(self.winfo_screenwidth()/1.4)
        self.app_height = int(self.winfo_screenheight()/1.4)
        self.geometry(f'{self.app_width}x{self.app_height}')
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=11)
        self.grid_rowconfigure(0, weight=1)
        ctk.set_appearance_mode('dark')

    def change_appearance_mode(self):
        if ctk.get_appearance_mode() == 'Dark':
            ctk.set_appearance_mode('light')
        else:
            ctk.set_appearance_mode('dark')


class MenuBar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid(row=0, column=0, sticky='nsew')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure((1,2,3), weight=4)
        self.grid_rowconfigure(4, weight=12)
        self.grid_rowconfigure(5, weight=1)
        self.grid_propagate(False)
        self.home_icon = ctk.CTkImage(light_image=Image.open('NewGUI/icon_light/mine.png'), dark_image=Image.open(
            'NewGUI/icon_dark/mine.png'), size=(40, 40))
        self.title_icon = ctk.CTkImage(light_image=Image.open('NewGUI/icon_light/iconL.png'), dark_image=Image.open(
            'NewGUI/icon_dark/icon.png'), size=(80, 80))
        self.daily_icon = ctk.CTkImage(light_image=Image.open('NewGUI/icon_light/daily.png'), dark_image=Image.open(
            'NewGUI/icon_dark/daily.png'), size=(40, 40))
        self.tick_icon = ctk.CTkImage(light_image=Image.open('NewGUI/icon_light/tick.png'), dark_image=Image.open(
            'NewGUI/icon_dark/tick.png'), size=(40, 40))
        self.setting_icon = ctk.CTkImage(light_image=Image.open('NewGUI/icon_light/setting.png'), dark_image=Image.open(
            'NewGUI/icon_dark/setting.png'), size=(40, 40))

        self.title = ctk.CTkLabel(self, image=self.title_icon,text='神秘股市', text_color=('#3999F9','#FCFAFA'),font=('微软雅黑', 35, 'bold'),compound='left')
        self.title.grid(row=0, column=0,padx = 20,pady = (30,0), sticky='new')

        self.home_button = ctk.CTkButton(self, image=self.home_icon, fg_color='transparent',text='我们的项目', hover_color='grey',text_color=('black','#FCFAFA'),font=('微软雅黑', 15, 'bold'),
                                     command=lambda:main_page.show_page('HomePage'),corner_radius=0)
        self.home_button.grid(row=1, column=0,padx = 0, pady = 5, sticky='nsew')

        self.daily_button = ctk.CTkButton(self, image=self.daily_icon,text='日K回测', fg_color='transparent',hover_color='grey',text_color=('black','#FCFAFA'),font=('微软雅黑', 15, 'bold'),
                                     command=lambda:main_page.show_page('DailyPage'),corner_radius=0)
        self.daily_button.grid(row=2, column=0,padx = 0, pady = 5, sticky='nsew')

        self.tick_button = ctk.CTkButton(self, image=self.tick_icon,text='分时回测', fg_color='transparent',hover_color='grey',text_color=('black','#FCFAFA'),font=('微软雅黑', 15, 'bold'),
                                     command=lambda:main_page.show_page('TickPage'),corner_radius=0)
        self.tick_button.grid(row=3, column=0,padx = 0, pady = 5, sticky='nsew')


        self.setting_button = ctk.CTkButton(self, image=self.setting_icon, text='深浅切换', text_color=('black', '#FCFAFA'), font=('微软雅黑', 15, 'bold'),
                                            command=master.change_appearance_mode)
        self.setting_button.grid(row=5, column=0, padx = 25, pady = (0, 25), sticky='nsew')


app = App()
main_page = MainPage(app)
menu_bar = MenuBar(app)

app.mainloop()