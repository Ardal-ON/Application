import flet as ft
import datetime
import calendar
from calendar import HTMLCalendar
from dateutil import relativedelta

class FletCalendar(ft.UserControl):

    def __init__(self):
        super().__init__()

        self.get_current_date()
        self.set_theme()
        self.maintenance_index()
        self.maintenance_date()

        # Init the container control.
        self.calendar_container = ft.Container(width=355,
                                               height=300,
                                               padding=ft.padding.all(2),
                                               border=ft.border.all(2, self.border_color),
                                               border_radius=ft.border_radius.all(10),
                                               alignment=ft.alignment.bottom_center,)

        self.suggestion_container = ft.Container(width=355,
                                               height=30,
                                               padding=ft.padding.all(2),
                                               border=ft.border.all(2, self.border_color),
                                               border_radius=ft.border_radius.all(10),
                                               alignment=ft.alignment.bottom_center,
                                               content=ft.Row(
                                                   [self._maintenance_index,
                                                    self._maintenance_date
                                                    ]))
        self.build()  # Build the calendar.
        self.output = ft.Text()  # Add output control.

    def maintenance_index(self):
        self._maintenance_index =  ft.Container(
            content=ft.Text(
                        value=self.get_maintenance_index(),
                        size=15,
                        color=ft.colors.BLACK,
            ),
            alignment=ft.alignment.top_left,
            #margin=ft.margin.only(top=10),
            #padding=-10,
        )

    def maintenance_date(self):
        self._maintenance_date =  ft.Container(
            content=ft.Text(
                        value=self.get_maintenance_date(),
                        size=15,
                        weight=ft.FontWeight.W_800,
                        color=ft.colors.BLACK,
            ),
            alignment=ft.alignment.top_right,
            #margin=ft.margin.only(top=10),
            #padding=-10,
        )
    def get_maintenance_index(self):
        name = "Coolant System"
        return name

    def get_maintenance_date(self):
        name = "                              24 Nov 2023"
        return name

    def get_current_date(self):
        '''Get the initial current date'''
        today = datetime.datetime.today()
        self.current_month = today.month
        self.current_day = today.day
        self.current_year = today.year

    def selected_date(self, e):
        '''User selected date'''
        self.output.value = e.control.data
        self.output.update()
        # return e.control.data

    def set_current_date(self):
        '''Set the calendar to the current date.'''
        today = datetime.datetime.today()
        self.current_month = today.month
        self.current_day = today.day
        self.current_year = today.year
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
        next_button = ft.Container(ft.Text('>', text_align='right', size=20, color=self.text_color),
                                   on_click=self.get_next)
        div = ft.Divider(height=1, thickness=2.0, color=self.border_color)
        prev_button = ft.Container(ft.Text('<', text_align='left', size=20, color=self.text_color),
                                   on_click=self.get_prev)


        calendar_column = ft.Column(
            [ft.Row([prev_button, date_display, next_button], alignment=ft.MainAxisAlignment.SPACE_EVENLY,
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
                    if len(display_day) == 1: display_day = '0%s' % display_day

                    # 获取今天的日期
                    today = datetime.datetime.today()
                    # 检查年、月、日是否与今天相匹配
                    if day == today.day and self.current_month == today.month and self.current_year == today.year:
                        is_current_day_font = ft.FontWeight.BOLD
                        is_current_day_bg = self.current_day_color

                    day_button = ft.Container(
                        content=ft.Text(display_day, weight=is_current_day_font, color=self.text_color),
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

        buttons_container = ft.Container(
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        text="Accept",
                        bgcolor=ft.colors.GREEN,
                        color=ft.colors.WHITE,
                    ),
                    ft.ElevatedButton(
                        text="Decline",
                        bgcolor=ft.colors.GREY,
                        color=ft.colors.WHITE,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            width=360,
        )

        self.final_layout = ft.Column(
            [
                self.calendar_container,
                self.suggestion_container,
                buttons_container  # Add the buttons container here
            ],
            alignment=ft.alignment.center,
            spacing=15
        )

        return self.final_layout





