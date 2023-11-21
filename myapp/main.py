import flet as ft

from Home import HomePage
from Dashboard import Dashboard
from Maintenance import FletCalendar
from Model import Model

shared_model = Model()

def main(page: ft.Page):
    page.window_width = 380
    page.window_height = 800
    page.window_min_height = 800
    page.window_min_width = 380
    page.scroll = ft.ScrollMode.HIDDEN
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0
    page.title = "My Application"


    home = HomePage(data=shared_model)

    dashboard = Dashboard()
    dashboard.visible = False
    
    maintenance = FletCalendar()
    maintenance.visible = False


    def changetab(navbar):
	# GET INDEX TAB
        my_index = navbar.control.selected_index
        dashboard.visible = True if my_index == 0 else False
        home.visible = True if my_index == 1 else False
        maintenance.visible = True if my_index == 2 else False
        page.update()
		 
    page.navigation_bar = ft.NavigationBar(
                            bgcolor = "red",
                            on_change = changetab,
                            selected_index = 1,
                            destinations = [
                                ft.NavigationDestination(icon = ft.icons.SPEED,
                                                        label = "Dashboard"),
                                ft.NavigationDestination(icon = ft.icons.HOME_OUTLINED,
                                                        selected_icon = ft.icons.HOME,
                                                        label = "Home"),
                                ft.NavigationDestination(icon = ft.icons.BUILD_OUTLINED, 
                                                        selected_icon = ft.icons.BUILD,
                                                        label = "Maintenance"),
                            ]
        )
    
    
    #print(model.get_parameter_dict())
    
    body = ft.Container(
        ft.Stack([
            home,
            dashboard,
            maintenance,
        ]),
    )
    
    page.add(body)
    page.update()
    

ft.app(target=main, assets_dir="assets")
#ft.app(target=main, view=ft.AppView.WEB_BROWSER, assets_dir="assets")