import flet as ft

class HomePage(ft.UserControl):
    def __int__(self):
        self._Homepage = None
        self._greeting = None
        self._card = None
        self._parameterlist = None
        self._buttons = None
        super().__int__()

    def Greeting(self):
        self._greeting =  ft.Container(
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
            ft.Column([
                ft.Container(
                    ft.Text(
                        "Ford Focus 2018",
                        color=ft.colors.BLACK,
                        size=24,
                        weight="W800",
                    ),
                    #margin=ft.margin.only(left=10,top=10)
                ),
                ft.Container(
                    ft.Text(
                        "Ardalan's Car",
                        color=ft.colors.BLACK,
                        size=14,
                        weight="w600",
                    ),
                    #margin=ft.margin.only(left=10)
                ),
                ft.Container(
                    ft.Text(
                        "CA#7RSV070",
                        color=ft.colors.BLACK,
                        size=13,
                        weight="w500",
                    ),
                    #margin=ft.margin.only(left=10)
                ),
                ft.Container(
                    ft.Image(src='Car.png',fit=ft.ImageFit.FIT_HEIGHT),
                    width=360,
                    height=80,
                    alignment= ft.alignment.Alignment(0.95,0.75),
                    margin=ft.margin.only(top=-15)
                ),
            ],spacing=0),
            width=360,
            height=160,
            #margin=ft.margin.only(top=20),
            padding=10,
            bgcolor=ft.colors.GREEN_300,
            border_radius=12,
        )
    
    def ParameterList(self):


        self._parameterlist = ft.Column(
            controls=[
                ft.Container(
                    content= ft.Text(
                                "Engine Healt Parameters",
                                text_align=ft.TextAlign.CENTER,
                                weight="w600",
                                size=20,),
                    alignment=ft.alignment.center,
                    padding=-5,
                ),
                ft.TextField(
                    label="Engine RPM",
                    suffix_text="RPM",
                    keyboard_type=ft.KeyboardType.NUMBER,
                    prefix_icon=ft.icons.SPEED),
                ft.TextField(
                    label="Lub oil pressure",
                    suffix_text="Pa",
                    keyboard_type=ft.KeyboardType.NUMBER,
                    prefix_icon=ft.icons.OIL_BARREL),
                ft.TextField(
                    label="Fuel pressure",
                    suffix_text="Pa",
                    keyboard_type=ft.KeyboardType.NUMBER,
                    prefix_icon=ft.icons.DISC_FULL),
                ft.TextField(
                    label="Coolant pressure",
                    suffix_text="Pa",
                    keyboard_type=ft.KeyboardType.NUMBER,
                    prefix_icon=ft.icons.WATER_DROP),
                ft.TextField(
                    label="Lub oil temperature",
                    suffix_text="°C",
                    keyboard_type=ft.KeyboardType.NUMBER,
                    prefix_icon=ft.icons.HOT_TUB),
                ft.TextField(
                    label="Coolant temperature",
                    suffix_text="°C",
                    keyboard_type=ft.KeyboardType.NUMBER,
                    prefix_icon=ft.icons.THERMOSTAT)
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
                        #on_click=Randomize Parameters,
                    ),
                    ft.ElevatedButton(
                        text="Predictions",
                        icon=ft.icons.CALCULATE,
                        bgcolor=ft.colors.GREEN,
                        color=ft.colors.WHITE,
                        #on_click=Prediction,
                    ),
                ],
            ),
            alignment=ft.alignment.center,
            width=360,
        )

    def build(self):
        self.Greeting()
        self.Card()
        self.ParameterList()
        self.Buttons()
        
        self._Homepage = ft.Container(
                        width=360,
                        height=740,
                        content=ft.Column(
                            [self._greeting,
                             self._card,
                             self._parameterlist,
                             self._buttons,]
                        )
                        )

        return self._Homepage
