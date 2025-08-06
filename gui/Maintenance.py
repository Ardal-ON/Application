import flet as ft
import datetime
import calendar
from calendar import HTMLCalendar
from dateutil import relativedelta


class Maintenance(ft.UserControl):
    def __int__(self):
        super().__int__()

    def init_calendar_container(self):
        self.calendar_container = ft.Container(
            width=355,
            height=300,
            margin=ft.margin.only(top=20),
            padding=ft.padding.all(2),
            border=ft.border.all(2, self.border_color),
            border_radius=ft.border_radius.all(10),
            alignment=ft.alignment.bottom_center,
        )

    def init_suggestion_container(self):
        self.suggestion_container = ft.Container(
            width=355,
            height=30,
            padding=ft.padding.all(2),
            border=ft.border.all(2, self.border_color),
            border_radius=ft.border_radius.all(10),
            content=ft.Row(
                [self.suggestion_box],
            ),
        )

    def calendar_column(self):
        current_calendar = self.get_calendar()
        today = datetime.datetime.today()

        if self.current_month == today.month and self.current_year == today.year:
            str_date = "{0} {1}, {2}".format(
                calendar.month_name[self.current_month],
                self.current_day,
                self.current_year,
            )
        else:
            str_date = "{0}, {1}".format(
                calendar.month_name[self.current_month], self.current_year
            )

        date_display = ft.Text(
            value=str_date,
            text_align="center",
            size=20,
            color=self.text_color,
        )

        next_button = ft.Container(
            ft.Text(
                value=">",
                text_align="right",
                size=20,
                color=self.text_color,
            ),
            on_click=self.get_next,
        )

        div = ft.Divider(height=1, thickness=2.0, color=self.border_color)

        prev_button = ft.Container(
            ft.Text(
                value="<",
                text_align="left",
                size=20,
                color=self.text_color,
            ),
            on_click=self.get_prev,
        )

        calendar_column = ft.Column(
            controls=[
                ft.Row(
                    controls=[prev_button, date_display, next_button],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    height=40,
                    expand=False,
                ),
                ft.Row(
                    controls=[
                        ft.Text(
                            value="  Mo         Tu        We       Th         Fr         Sa         Su"
                        )
                    ]
                ),
                div,
            ],
            spacing=2,
            width=355,
            height=280,
            alignment=ft.MainAxisAlignment.START,
            expand=False,
        )

        for week in current_calendar:
            week_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
            for day in week:
                if day > 0:
                    is_current_day_font = ft.FontWeight.W_300
                    is_current_day_bg = ft.colors.TRANSPARENT
                    display_day = "{0:0=2d}".format(day)

                    if (
                        day == today.day
                        and self.current_month == today.month
                        and self.current_year == today.year
                    ):
                        is_current_day_font = ft.FontWeight.BOLD
                        is_current_day_bg = self.current_day_color

                    if self._model.get_repair_date_status():
                        rd = self._model.get_repair_day()
                        if (
                            day == rd.day
                            and self.current_month == rd.month
                            and self.current_year == rd.year
                        ):
                            is_current_day_font = ft.FontWeight.BOLD
                            is_current_day_bg = ft.colors.GREEN

                    day_button = ft.Container(
                        content=ft.Text(
                            value=display_day,
                            weight=is_current_day_font,
                            color=self.text_color,
                        ),
                        width=40,
                        height=40,
                        alignment=ft.alignment.center,
                        border_radius=ft.border_radius.all(10),
                        bgcolor=is_current_day_bg,
                    )

                else:
                    day_button = ft.Container(
                        width=40,
                        height=40,
                        border_radius=ft.border_radius.all(10),
                    )

                week_row.controls.append(day_button)

            calendar_column.controls.append(week_row)

        self.calendar_container.content = calendar_column

    def button_container(self):
        self.buttons_container = ft.Container(
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        text="Accept",
                        bgcolor=ft.colors.GREEN,
                        color=ft.colors.WHITE,
                        on_click=self.accept_repair_date,
                    ),
                    ft.ElevatedButton(
                        text="Decline",
                        bgcolor=ft.colors.GREY,
                        color=ft.colors.WHITE,
                        on_click=self.decline_repair_date,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            width=360,
        )

    def initialize_model(self):
        self._model = self.data

    def set_suggestion_box(self):
        self.suggestion_box = ft.Row(
            controls=[
                ft.Text(
                    value="No Repair Needed",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        repair_date = self._model.get_repair_day()
        print("maintenance: ", repair_date)
        if repair_date:
            self.suggestion_box.controls = []
            part_list = self._model.get_maintenance_req_part()
            self.suggestion_box.controls.append(
                ft.Text(
                    value="\n".join(part_list),
                    size=14,
                    weight=ft.FontWeight.BOLD,
                )
            )
            self.suggestion_box.controls.append(
                ft.Text(
                    value=", ".join(
                        [
                            str(repair_date.day),
                            str(calendar.month_name[repair_date.month]),
                            str(repair_date.year),
                        ]
                    ),
                    size=14,
                    weight=ft.FontWeight.BOLD,
                )
            )
            if self._model.get_repair_date_status():
                self.suggestion_box.controls[-1].color = ft.colors.GREEN
            self.suggestion_box.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
            self.suggestion_container.content = self.suggestion_box
            self.suggestion_container.height = 25 * len(part_list)
            self.suggestion_container.update()

    def accept_repair_date(self, e):
        self._model.set_repair_date()
        self.calendar_column()
        self.suggestion_box.controls[-1].color = ft.colors.GREEN
        self.suggestion_container.update()
        self.calendar_container.update()

    def decline_repair_date(self, e):
        self._model.find_repair_date()
        self.set_suggestion_box()
        self.suggestion_container.update()

    def get_current_date(self):
        today = datetime.datetime.today()
        self.current_month = today.month
        self.current_day = today.day
        self.current_year = today.year

    def get_next(self, e):
        current = datetime.date(self.current_year, self.current_month, self.current_day)
        rel_month = relativedelta.relativedelta(months=1)
        next_month = current + rel_month
        self.current_year = next_month.year
        self.current_month = next_month.month
        self.current_day = next_month.day
        self.calendar_column()
        self.calendar_container.update()

    def get_prev(self, e):
        current = datetime.date(self.current_year, self.current_month, self.current_day)
        rel_month = relativedelta.relativedelta(months=1)
        prev_month = current - rel_month
        self.current_year = prev_month.year
        self.current_month = prev_month.month
        self.current_day = prev_month.day
        self.calendar_column()
        self.calendar_container.update()

    def get_calendar(self):
        cal = HTMLCalendar()
        return cal.monthdayscalendar(self.current_year, self.current_month)

    def set_theme(
        self,
        border_color=ft.colors.BLACK,
        text_color=ft.colors.BLACK,
        current_day_color=ft.colors.RED,
    ):
        self.border_color = border_color
        self.text_color = text_color
        self.current_day_color = current_day_color

    def build(self):
        self.initialize_model()
        self.get_current_date()
        self.set_theme()
        self.init_calendar_container()
        self.set_suggestion_box()
        self.init_suggestion_container()
        self.calendar_column()
        self.button_container()

        self.Maintenance = ft.Column(
            [
                self.calendar_container,
                self.suggestion_container,
                self.buttons_container,
            ],
            alignment=ft.alignment.center,
            spacing=15,
        )

        return self.Maintenance
