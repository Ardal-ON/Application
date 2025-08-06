import flet as ft

from gui.Home import HomePage
from gui.Dashboard import Dashboard
from gui.Maintenance import Maintenance
from gui.Model import Model

shared_model = Model()


def main(page: ft.Page):
    page.window_width = 380
    page.window_height = 840
    page.window_min_height = 840
    page.window_min_width = 380
    page.scroll = ft.ScrollMode.HIDDEN
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0
    page.title = "My Application"

    home = HomePage(data=shared_model)

    dashboard = Dashboard(data=shared_model)
    dashboard.visible = False

    maintenance = Maintenance(data=shared_model)
    maintenance.visible = False

    def changetab(navbar):
        # GET INDEX TAB
        my_index = navbar.control.selected_index
        if my_index == 0:
            dashboard.set_dashboard_value()
            dashboard.visible = True
        else:
            dashboard.visible = False
        home.visible = True if my_index == 1 else False
        if my_index == 2:
            maintenance.set_suggestion_box()
            maintenance.visible = True
        else:
            maintenance.visible = False
        page.update()

    page.navigation_bar = ft.NavigationBar(
        bgcolor="red",
        on_change=changetab,
        selected_index=1,
        destinations=[
            ft.NavigationDestination(icon=ft.icons.SPEED, label="Dashboard"),
            ft.NavigationDestination(
                icon=ft.icons.HOME_OUTLINED, selected_icon=ft.icons.HOME, label="Home"
            ),
            ft.NavigationDestination(
                icon=ft.icons.BUILD_OUTLINED,
                selected_icon=ft.icons.BUILD,
                label="Maintenance",
            ),
        ],
    )

    body = ft.Container(
        ft.Stack(
            [
                home,
                dashboard,
                maintenance,
            ]
        ),
    )

    page.add(body)
    page.update()


ft.app(target=main)
