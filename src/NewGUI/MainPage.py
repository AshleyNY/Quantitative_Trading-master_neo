import customtkinter as ctk
from src.NewGUI.HomePage import NewHomePage
from src.NewGUI.DailyPage import NewDailyPage

from src.NewGUI.TickPage import NewTickPage


class MainPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master,**kwargs)
        self.grid(row=0, column=1, sticky='nsew')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.home_page = NewHomePage(self)

        self.tick_page = NewTickPage(self)

        self.daily_page = NewDailyPage(self)
        self.current_page = None
        self.show_page('HomePage')

    def show_page(self, page_name):
        new_page = None
        if page_name == 'HomePage':
            new_page = self.home_page
        elif page_name == 'TickPage':
            new_page = self.tick_page
        elif page_name == 'DailyPage':
            new_page = self.daily_page
        
        if new_page == self.current_page:
            return

        if new_page:
            new_page.grid(row=0, column=0, sticky="nswe")
            new_page.update_idletasks()

        if self.current_page and self.current_page != new_page:
            self.current_page.grid_forget()

        self.current_page = new_page

        if new_page:
            new_page.focus_set()


