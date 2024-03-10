from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Select, Label, Input, Button
from textual import on
from textual.screen import Screen
from textual_pandas import DataFrameTable
import os
from pathlib import Path


from datahandler import main

clg_list = []
def get_clg():
    for clg in os.listdir("clg"):
        if clg.startswith("NIT"):
            clg_list.append(Path(clg).stem)


class DataScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]


    def compose(self) -> ComposeResult:
        yield Header()
        yield DataFrameTable()
        yield Footer()

    def on_mount(self):
        table = self.query_one(DataFrameTable)
        table.add_df(main(rank, homenit).sort_values(by=['Closing']))


class JoserApp(App):
    homenit = None
    CSS_PATH = "main.tcss"
    BINDINGS = [("q", "app.exit()", "Quit")] #! work agalla

    SCREENS = {"data":DataScreen()}

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Select home state NIT:")
        yield Select.from_values(clg_list)
        yield Input(placeholder="Enter rank", type="integer")
        yield Button("Submit")
        yield Footer()

    def on_button_pressed(self, event) -> None:
        self.push_screen('data')


    @on(Select.Changed)
    def select_changed(self, event) -> None:
        global homenit
        homenit = str(event.value)

    @on(Input.Changed)
    def input_submitted(self, event) -> None:
        global rank
        try:
            rank = int(event.value)
        except ValueError:
            pass

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

if __name__ == '__main__':
    get_clg()
    app = JoserApp()
    app.run()