import flet as ft
import time


class HomePage(ft.UserControl):
    def __int__(self):
        super().__int__()

    def Greeting(self):
        self._greeting = ft.Container(
            content=ft.Text(
                "Hello, Ardalan!",
                size=25,
                font_family="RobotoSlab",
                weight=ft.FontWeight.W_800,
                color=ft.colors.RED_600,
            ),
            alignment=ft.alignment.center,
            margin=ft.margin.only(top=10),
            padding=-10,
        )

    def Card(self):
        self._card = ft.Container(
            ft.Column(
                [
                    ft.Container(
                        ft.Text(
                            "Ford Focus 2018",
                            color=ft.colors.BLACK,
                            size=24,
                            weight="W800",
                        ),
                        # margin=ft.margin.only(left=10,top=10)
                    ),
                    ft.Container(
                        ft.Text(
                            "Ardalan's Car",
                            color=ft.colors.BLACK,
                            size=14,
                            weight="w600",
                        ),
                        # margin=ft.margin.only(left=10)
                    ),
                    ft.Container(
                        ft.Text(
                            "CA#7RSV070",
                            color=ft.colors.BLACK,
                            size=13,
                            weight="w500",
                        ),
                        # margin=ft.margin.only(left=10)
                    ),
                    ft.Container(
                        ft.Image(src="Car.png", fit=ft.ImageFit.FIT_HEIGHT),
                        width=360,
                        height=80,
                        alignment=ft.alignment.Alignment(0.95, 0.75),
                        margin=ft.margin.only(top=-15),
                    ),
                ],
                spacing=0,
            ),
            width=360,
            height=160,
            # margin=ft.margin.only(top=20),
            padding=10,
            bgcolor=ft.colors.GREEN_300,
            border_radius=12,
        )

    def ParameterList(self):
        self._parameterlist = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(
                        "Engine Health Parameters",
                        text_align=ft.TextAlign.CENTER,
                        weight="w600",
                        size=20,
                    ),
                    alignment=ft.alignment.center,
                    padding=-5,
                ),
                ft.TextField(
                    label="Engine RPM",
                    suffix_text="80...1450  RPM",
                    keyboard_type=ft.KeyboardType.NUMBER,
                    prefix_icon=ft.icons.SPEED,
                ),
                ft.TextField(
                    label="Lub oil pressure",
                    suffix_text="0.2...6.4  Pa",
                    keyboard_type=ft.KeyboardType.NUMBER,
                    prefix_icon=ft.icons.OIL_BARREL,
                ),
                ft.TextField(
                    label="Fuel pressure",
                    suffix_text="0.6...12.0  Pa",
                    keyboard_type=ft.KeyboardType.NUMBER,
                    prefix_icon=ft.icons.DISC_FULL,
                ),
                ft.TextField(
                    label="Coolant pressure",
                    suffix_text="0.0...4.8  Pa",
                    keyboard_type=ft.KeyboardType.NUMBER,
                    prefix_icon=ft.icons.WATER_DROP,
                ),
                ft.TextField(
                    label="Lub oil temperature",
                    suffix_text="72.2...81.6  °C",
                    keyboard_type=ft.KeyboardType.NUMBER,
                    prefix_icon=ft.icons.HOT_TUB,
                ),
                ft.TextField(
                    label="Coolant temperature",
                    suffix_text="61.6...95.9  °C",
                    keyboard_type=ft.KeyboardType.NUMBER,
                    prefix_icon=ft.icons.THERMOSTAT,
                ),
            ],
            alignment=ft.alignment.center,
        )

    def Buttons(self):
        self._buttons = ft.Container(
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        text="Random Parameters",
                        icon=ft.icons.CASINO,
                        bgcolor=ft.colors.BLUE,
                        color=ft.colors.WHITE,
                        on_click=self.randomize_parameters,
                    ),
                    ft.ElevatedButton(
                        text="Prediction",
                        icon=ft.icons.CALCULATE,
                        bgcolor=ft.colors.GREEN,
                        color=ft.colors.WHITE,
                        on_click=self.predict,
                    ),
                ],
            ),
            alignment=ft.alignment.center,
            width=360,
        )

    def initialize_model(self):
        self._model = self.data

    def randomize_parameters(self, e):
        self._model.random_initialization()

        parameter_dict = self._model.get_parameter_dict()

        for parameter in parameter_dict:
            if parameter == "engine_rpm":
                self._parameterlist.controls[1].value = str(parameter_dict[parameter])
            if parameter == "lub_oil_pressure":
                self._parameterlist.controls[2].value = str(parameter_dict[parameter])
            if parameter == "fuel_pressure":
                self._parameterlist.controls[3].value = str(parameter_dict[parameter])
            if parameter == "coolant_pressure":
                self._parameterlist.controls[4].value = str(parameter_dict[parameter])
            if parameter == "lub_oil_temp":
                self._parameterlist.controls[5].value = str(parameter_dict[parameter])
            if parameter == "coolant_temp":
                self._parameterlist.controls[6].value = str(parameter_dict[parameter])

        for i in range(1, 7):
            self._parameterlist.controls[i].update()

        # print(self._model.get_parameter_dict())

    def predict(self, e):
        for parameter in self._model._parameter_dict:
            if parameter == "engine_rpm":
                self._model.set_parameter_dict(
                    parameter, float(self._parameterlist.controls[1].value)
                )
            if parameter == "lub_oil_pressure":
                self._model.set_parameter_dict(
                    parameter, float(self._parameterlist.controls[2].value)
                )
            if parameter == "fuel_pressure":
                self._model.set_parameter_dict(
                    parameter, float(self._parameterlist.controls[3].value)
                )
            if parameter == "coolant_pressure":
                self._model.set_parameter_dict(
                    parameter, float(self._parameterlist.controls[4].value)
                )
            if parameter == "lub_oil_temp":
                self._model.set_parameter_dict(
                    parameter, float(self._parameterlist.controls[5].value)
                )
            if parameter == "coolant_temp":
                self._model.set_parameter_dict(
                    parameter, float(self._parameterlist.controls[6].value)
                )

        self._model.predict()

        self._buttons.content.controls[1].text = "    Done    "
        self._buttons.content.controls[1].update()

        time.sleep(0.6)

        self._buttons.content.controls[1].text = "Prediction"
        self._buttons.content.controls[1].update()

        # print(self._model.get_parameter_dict())

    def build(self):
        self.initialize_model()
        self.Greeting()
        self.Card()
        self.ParameterList()
        self.Buttons()

        self._Homepage = ft.Container(
            margin=ft.margin.only(top=20, left=10, right=10),
            width=360,
            height=740,
            content=ft.Column(
                [
                    self._greeting,
                    self._card,
                    self._parameterlist,
                    self._buttons,
                ]
            ),
        )

        return self._Homepage
