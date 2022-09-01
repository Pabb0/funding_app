from kivymd.app import MDApp
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from funding_rates import get_current_funding_rates
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
import plyer


class FundingApp(MDApp):
    def build(self):
        # Clock used as callback for notifcations
        Clock.schedule_interval(self.retrieve_data_callback, 60) # Arg = number of seconds

        self.theme_cls.primary_palette = "BlueGray"

        screen = MDScreen()
        box = MDBoxLayout(orientation='vertical')
        screen.add_widget(box)

        top_bar = MDTopAppBar(
            title='Funding rates overview',
        )
        box.add_widget(top_bar)

        self.data_tables = MDDataTable(
            background_color_header=self.theme_cls.primary_color,
            pos_hint={"center_y": 0.5, "center_x": 0.5},
            size_hint=(0.9, 0.6),
            use_pagination=False,
            rows_num=300,
            column_data=[
                ("Trading pair", dp(30)),
                ("Funding rate", dp(30)),
            ]
        )

        # Fill data table
        self.data = get_current_funding_rates()
        for symbol, funding in sorted(self.data.items(),
                                      key=lambda x: abs(x[1]['current_rate']),
                                      reverse=True):
            self.data_tables.add_row((symbol, funding['current_rate']))

        box.add_widget(self.data_tables)

        return screen

    def send_notification(self, symbol, rate):
        plyer.notification.notify(title='Possible profit', message=f"The pair {symbol} has a funding rate of {rate}.")

    def retrieve_data_callback(self, dt):
        self.data = get_current_funding_rates()
        self.data_tables = MDDataTable(
            background_color_header=self.theme_cls.primary_color,
            pos_hint={"center_y": 0.5, "center_x": 0.5},
            size_hint=(0.9, 0.6),
            use_pagination=False,
            rows_num=300,
            column_data=[
                ("Trading pair", dp(30)),
                ("Funding rate", dp(30)),
            ]
        )

        for i, (symbol, funding) in enumerate(sorted(self.data.items(),
                                                key=lambda x: abs(x[1]['current_rate']),
                                                reverse=True)):

            if funding['current_rate'] > 0.05:
                self.send_notification(symbol, funding['current_rate'])
            self.data_tables.add_row((symbol, funding['current_rate']))


if __name__ == '__main__':
    FundingApp().run()
