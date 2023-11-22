import flet as ft

class Dashboard(ft.UserControl):
    def __int__(self):
        super().__int__()

    def MakeList(self):
        self._parameters_list = ft.ListView(
            expand=True,
            spacing=1,
            padding=0,
            auto_scroll=False,  # change this for auto scrolling to last item
        )

        self._parameters_list.controls.append(
                ft.Container(
                    alignment=ft.alignment.center,
                    height=60,
                    bgcolor="white",
                    border_radius=8,
                    content=ft.Text(0),
                    border=ft.border.only(bottom=ft.border.BorderSide(1, "black"))
                )
            )

        for i in range(6):
            self._parameters_list.controls.append(
                ft.Container(
                    alignment=ft.alignment.center,
                    height=60,
                    bgcolor="white",
                    border_radius=8,
                    content=ft.Text(0),
                    border=ft.border.only(bottom=ft.border.BorderSide(0.1, "grey"))
                )
            )

    def Dashtitle(self):
        self._dashtitle = ft.Container(
            margin=ft.margin.only(top=10),
            padding=ft.padding.only(left=10,right=10),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        value="DASHBOARD",
                        size=26,
                        color=ft.colors.GREY_800,
                        weight="w600",
                    ),
                ],
            ),
        )

    def initialize_model(self):
        self._model = self.data

    def set_dashboard_value(self):
        parameter_dict = self._model.get_parameter_dict()
        maintenance_dict = self._model.get_Maintenance_dict()

        for parameter in parameter_dict:
            if parameter == 'engine_rpm':
                self._parameters_list.controls[1].content = self.create_text(parameter,maintenance_dict)
                self._parameters_list.controls[1].update()
            if parameter == 'lub_oil_pressure':
                self._parameters_list.controls[2].content = self.create_text(parameter,maintenance_dict)
                self._parameters_list.controls[2].update()
            if parameter == 'fuel_pressure':
                self._parameters_list.controls[3].content = self.create_text(parameter,maintenance_dict)
                self._parameters_list.controls[3].update()
            if parameter == 'coolant_pressure':
                self._parameters_list.controls[4].content = self.create_text(parameter,maintenance_dict)
                self._parameters_list.controls[4].update()
            if parameter == 'lub_oil_temp':
                self._parameters_list.controls[5].content = self.create_text(parameter,maintenance_dict)
                self._parameters_list.controls[5].update()
            if parameter == 'coolant_temp':
                self._parameters_list.controls[6].content = self.create_text(parameter,maintenance_dict)
                self._parameters_list.controls[6].update()
            if parameter == 'engine_condition':
                self._parameters_list.controls[0].content = self.create_text(parameter,maintenance_dict)
                self._parameters_list.controls[0].update()
    
    def create_text(self,parameter, maintenance_dict):
        if maintenance_dict[parameter] == 1 :
            status = "GOOD"
            color = ft.colors.GREEN
        elif maintenance_dict[parameter] == 0.5:
            status = "POOR"
            color = ft.colors.AMBER_600
        elif maintenance_dict[parameter] == 0:
            status = " BAD"
            color = ft.colors.DEEP_ORANGE_ACCENT_700

        required_text = ft.Row(
            controls=[
                ft.Text(value=" "),
            ],
        )
        
        if parameter == 'engine_rpm':
            required_text.controls.append(ft.Icon(name=ft.icons.SPEED,size=40))
            required_text.controls.append(ft.Text(
                value="  Engine Status",
                style=ft.TextThemeStyle.TITLE_SMALL,
            ))
            required_text.controls.append(ft.Text(value="                      ")) 
        elif parameter == 'lub_oil_pressure':
            required_text.controls.append(ft.Icon(name=ft.icons.OIL_BARREL,size=40))
            required_text.controls.append(ft.Text(
                    value="  Oil Pressure",
                    style=ft.TextThemeStyle.TITLE_SMALL,
            ))
            required_text.controls.append(ft.Text(value="                        "))
        elif parameter == 'fuel_pressure':
            required_text.controls.append(ft.Icon(name=ft.icons.DISC_FULL,size=40))
            required_text.controls.append(ft.Text(
                    value="  Fuel Pressure",
                    style=ft.TextThemeStyle.TITLE_SMALL,
            ))
            required_text.controls.append(ft.Text(value="                      "))
        elif parameter == 'coolant_pressure':
            required_text.controls.append(ft.Icon(name=ft.icons.WATER_DROP,size=40))
            required_text.controls.append(ft.Text(
                    value="  Coolant Pressure",
                    style=ft.TextThemeStyle.TITLE_SMALL,
            ))
            required_text.controls.append(ft.Text(value="                "))
        elif parameter == 'lub_oil_temp':
            required_text.controls.append(ft.Icon(name=ft.icons.HOT_TUB,size=40))
            required_text.controls.append(ft.Text(
                    value="  Oil Temperature",
                    style=ft.TextThemeStyle.TITLE_SMALL,
                ))
            required_text.controls.append(ft.Text(value="                 "))
        elif parameter == 'coolant_temp':
            required_text.controls.append(ft.Icon(name=ft.icons.THERMOSTAT,size=40))
            required_text.controls.append(ft.Text(
                    value="  Coolant Temperature",
                    style=ft.TextThemeStyle.TITLE_SMALL,
            ))
            required_text.controls.append(ft.Text(value="         "))
        elif parameter == 'engine_condition':
            required_text.controls.append(ft.Icon(name=ft.icons.DIRECTIONS_CAR,size=40))
            required_text.controls.append(ft.Text(
                    value="  Overall Status",
                    style=ft.TextThemeStyle.TITLE_SMALL,
            ))
            required_text.controls.append(ft.Text(value="                      "))
        #required_text.controls.append(ft.VerticalDivider(width=10, thickness=0))
        #required_text.controls.append(ft.Text(value="                      "))
        required_text.controls.append(ft.Text(
                value=status,
                style=ft.TextThemeStyle.TITLE_SMALL,
                color=color,
                text_align=ft.TextAlign.RIGHT
        ))
        
        return required_text





    def build(self):
        self.initialize_model()
        self.MakeList()
        self.Dashtitle()


        self._Dashboard = ft.Container(
            width=380,
            height=600,
            content=ft.Column(
                controls=[
                    self._dashtitle,
                    self._parameters_list
                ],
            ),
            margin=ft.margin.only(top=20,left=10,right=10)
        )

        return self._Dashboard
