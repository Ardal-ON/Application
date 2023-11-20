import flet as ft


class MainStackContainer(ft.UserControl):
    def __init__(self):
        super().__init__()


    def build(self):
        return ft.Container(
            width=360,
            height=600,
            bgcolor="white",
            border_radius=32,
            padding=ft.padding.only(top=25, left=5, right=5, bottom=25),
            content=ft.Stack(
                expand=True,  # expand the stack control to fill the parent container
                controls=[
                    # we'll add the other classes here...
                    # this was the first page,
                    MainPage(),
                    # sidebar here...
                    #MenuPage(self.ShowMenu),
                ],
            ),
        )


# The bottom stack should be the main page (the page that will show first)
class MainPage(ft.UserControl):
    def __init__(self):
        super().__init__()

    # now we need a dummy list using ListView...
    def MakeList(self):
        dummy_list = ft.ListView(
            expand=True,
            spacing=10,
            padding=20,
            auto_scroll=False,  # change this for auto scrolling to last item
        )

        for i in range(6):
            dummy_list.controls.append(
                ft.Container(
                    alignment=ft.alignment.center,
                    padding=8,
                    height=40,
                    bgcolor="white",
                    border_radius=8,
                    content=ft.Text(i),
                    visible=True,
                    animate=ft.animation.Animation(200, "decelerate"),
                )
            )

        return dummy_list

    # we can create a small method that helps filter odd and even numbers..
    def FilterList(self, e):
        # the checkbox return true if it's clicked, so...
        if e.data == "true":  # meaning it's been clicked
            # EVEN FILTER
            if e.control.label == "Even":  # if the box clicked has the label X
                # here we loop through the listView...
                for item in self.controls[0].content.controls[3].controls[:]:
                    # now we do some math to filter the evens
                    if (
                        item.content.value % 2 == 0
                    ):  # if the remainder is 0 (even numebr)
                        item.height = 0
                        item.update()
            # ODD FILTER
            if e.control.label == "Odd":  # if the box clicked has the label X
                # here we loop through the listView...
                for item in self.controls[0].content.controls[3].controls[:]:
                    # now we do some math to filter the evens
                    if (
                        item.content.value % 2 != 0  # if there is a remainder
                    ):  # if the remainder is 0 (even numebr)
                        item.height = 0
                        item.update()

        else:  # meaning it's been unclicked
            # EVEN FILTER
            if e.control.label == "Even":  # if the box clicked has the label X
                # here we loop through the listView...
                for item in self.controls[0].content.controls[3].controls[:]:
                    # now we do some math to filter the evens
                    if (
                        item.content.value % 2 == 0
                    ):  # if the remainder is 0 (even numebr)
                        item.height = 40
                        item.update()
            # ODD FILTER
            if e.control.label == "Odd":  # if the box clicked has the label X
                # here we loop through the listView...
                for item in self.controls[0].content.controls[3].controls[:]:
                    # now we do some math to filter the evens
                    if (
                        item.content.value % 2 != 0  # if there is a remainder
                    ):  # if the remainder is 0 (even numebr)
                        item.height = 40
                        item.update()

    # let's create a top bar with two checkboxes for fitlering
    def FilterBoxes(self):
        return ft.Container(
            bgcolor="white",
            border_radius=8,
            content=ft.Row(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        spacing=0,
                        controls=[
                            ft.Checkbox(
                                label="Odd",
                                fill_color="red",
                                on_change=lambda e: self.FilterList(e),
                            )
                        ],
                    ),
                    ft.Row(
                        spacing=0,
                        controls=[
                            ft.Checkbox(
                                label="Even",
                                fill_color="blue",
                                on_change=lambda e: self.FilterList(e),
                            )
                        ],
                    ),
                ],
            ),
        )

    def build(self):
        return ft.Container(
            expand=True,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,  # clip the content to prevent overflow
            opacity=1,
            animate_opacity=300,  # opacity is to create a blurred effect
            #on_click=self.function2,  # add later...
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Row(
                                expand=3,
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(
                                        "Filter Your Data",
                                        size=15,
                                        color="black",
                                        weight="bold",
                                    )
                                ],
                            ),
                        ]
                    ),
                    ft.Container(
                        padding=ft.padding.only(left=15, right=15),
                        opacity=0.85,
                        content=ft.Divider(height=5, color="black"),
                    ),
                    # add the components here ...
                    self.FilterBoxes(),
                    self.MakeList(),
                ]
            ),
        )