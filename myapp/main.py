import flet as ft
import datetime
import calendar
from calendar import HTMLCalendar
from dateutil import relativedelta

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

class FletCalendar(ft.UserControl):
    
    def __init__(self):
        super().__init__()
        
        self.get_current_date()
        self.set_theme()
        
        # Init the container control.
        self.calendar_container = ft.Container(width=355, 
                                               height=300,
                                                padding=ft.padding.all(2), 
                                                border=ft.border.all(2, self.border_color),
                                                border_radius=ft.border_radius.all(10),
                                                alignment=ft.alignment.bottom_center,)
        self.build() # Build the calendar.
        self.output = ft.Text() # Add output control.  
    
    def get_current_date(self):
        '''Get the initial current date'''
        today = datetime.datetime.today()
        self.current_month = today.month
        self.current_day   = today.day
        self.current_year  = today.year 
    
    def selected_date(self, e):
        '''User selected date'''
        self.output.value = e.control.data
        self.output.update()
        #return e.control.data
        
    def set_current_date(self):
        '''Set the calendar to the current date.'''
        today = datetime.datetime.today()
        self.current_month = today.month
        self.current_day   = today.day
        self.current_year  = today.year 
        self.build()
        self.calendar_container.update()
        
    def get_next(self, e):
        '''Move to the next month.'''
        current = datetime.date(self.current_year, self.current_month, self.current_day) 
        add_month = relativedelta.relativedelta(months=1)
        next_month = current + add_month
        
        self.current_year = next_month.year
        self.current_month = next_month.month
        self.current_day = next_month.day
        self.build()
        self.calendar_container.update()
    
    def get_prev(self, e):
        '''Move to the previous month.'''
        current = datetime.date(self.current_year, self.current_month, self.current_day) 
        add_month = relativedelta.relativedelta(months=1)
        next_month = current - add_month
        self.current_year = next_month.year
        self.current_month = next_month.month
        self.current_day = next_month.day
        self.build()
        self.calendar_container.update()
        
    def get_calendar(self):
        '''Get the calendar from the calendar module.'''
        cal = HTMLCalendar()
        return cal.monthdayscalendar(self.current_year, self.current_month)
    
    def set_theme(self, 
                  border_color=ft.colors.BLACK, 
                  text_color=ft.colors.BLACK, 
                  current_day_color=ft.colors.RED):
        self.border_color = border_color
        self.text_color = text_color
        self.current_day_color = current_day_color
    
    def build(self):
        '''Build the calendar for flet.'''
        current_calendar = self.get_calendar()
        
        str_date = '{0} {1}, {2}'.format(calendar.month_name[self.current_month], self.current_day, self.current_year)
        
        date_display = ft.Text(str_date, text_align='center', size=20, color=self.text_color)
        next_button = ft.Container( ft.Text('>', text_align='right', size=20, color=self.text_color), on_click=self.get_next )
        div = ft.Divider(height=1, thickness=2.0, color=self.border_color)
        prev_button = ft.Container( ft.Text('<', text_align='left', size=20, color=self.text_color), on_click=self.get_prev )
        
        calendar_column = ft.Column([ft.Row([prev_button, date_display, next_button], alignment=ft.MainAxisAlignment.SPACE_EVENLY, 
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER, height=40, expand=False), div], 
                                    spacing=2, width=355, height=330, alignment=ft.MainAxisAlignment.START, expand=False)
        # Loop weeks and add row.
        for week in current_calendar:
            week_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
            # Loop days and add days to row.
            for day in week:
                if day > 0:
                    is_current_day_font = ft.FontWeight.W_300
                    is_current_day_bg = ft.colors.TRANSPARENT
                    display_day = str(day)
                    if len(str(display_day)) == 1: display_day = '0%s' % display_day
                    if day == self.current_day: 
                        is_current_day_font = ft.FontWeight.BOLD
                        is_current_day_bg = self.current_day_color
                        
                    day_button = ft.Container(content=ft.Text(str(display_day), weight=is_current_day_font, color=self.text_color), 
                                              on_click=self.selected_date, data=(self.current_month, day, self.current_year), 
                                              width=40, height=40, ink=True, alignment=ft.alignment.center,
                                              border_radius=ft.border_radius.all(10),
                                              bgcolor=is_current_day_bg)
                else:
                    day_button = ft.Container(width=40, height=40, border_radius=ft.border_radius.all(10))
                    
                week_row.controls.append(day_button)
                
            # Add the weeks to the main column.
            calendar_column.controls.append(week_row)
        # Add column to our page container. 
        self.calendar_container.content = calendar_column
        return self.calendar_container

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
    dashboard = MainStackContainer()
    dashboard.visible = False
    maintenance = FletCalendar()
    maintenance.visible = False
    page.add(home,dashboard,maintenance)
    page.update()
    

#ft.app(target=main)
ft.app(target=main, view=ft.AppView.WEB_BROWSER)