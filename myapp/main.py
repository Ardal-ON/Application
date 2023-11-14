import flet as ft

class AnimatedCard(ft.UserControl):
    def __int__(self):
        super().__int__()

    def build(self):
        self._icon_container_ = ft.Container(
            width=120,
            height=35,
            bgcolor=ft.colors.BLUE_800,
            border_radius=25,
            animate_opacity=200,
            offset=ft.transform.Offset(0, 0.25),
            animate_offset=ft.animation.Animation(duration=900, curve="ease"),
            visible=False,
            content=ft.Row(
                alignment="center",
                vertical_alignment="center",
                controls=[
                    ft.Text(
                        "More Info",
                        size=12,
                        weight="w600",
                    ),
                ],
            ),
        )

        self._container = ft.Container(
            #width=280,
            #height=380,
            bgcolor=ft.colors.WHITE,
            border_radius=12,
            #on_hover=lambda e: self.AnimatedCardHover(e),
            animate=ft.animation.Animation(600, "ease"),
            border=ft.border.all(2, ft.colors.WHITE24),
            content=ft.Column(
                alignment="center",
                horizontal_alignment="start",
                spacing=0,
                controls=[
                    ft.Container(
                        padding=20,
                        alignment=ft.alignment.bottom_center,
                        content=ft.Text(
                            "Card Title",
                            color=ft.colors.BLACK,
                            size=28,
                            weight="w800",
                        ),
                    ),
                    ft.Container(
                        padding=20,
                        alignment=ft.alignment.top_center,
                        content=ft.Text(
                            "Insert card details here...",
                            color=ft.colors.BLACK,
                            size=14,
                            weight="w500",
                        ),
                    ),
                ],
            ),
        )

        self.__card = ft.Card(
            elevation=0,
            content=ft.Container(
                content=ft.Column(
                    spacing=0,
                    horizontal_alignment="center",
                    controls=[
                        self._container,
                    ],
                ),
            ),
        )

        self._card = ft.Column(
            horizontal_alignment="start",
            spacing=0,
            controls=[
                self.__card,
                self._icon_container_,
            ],
        )

        self._main = self._card

        return self._main


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

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
 
    home = AnimatedCard()
    dashboard = ft.Text("Dashboard",size=30,visible=False)
    maintenance = ft.Text("Maintenance",size=30,visible=False)
    
    page.add(home,dashboard,maintenance)

 
ft.app(target=main)
#ft.app(target=main, view=ft.AppView.WEB_BROWSER)