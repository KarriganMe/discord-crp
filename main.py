from textual.app import App, ComposeResult
from textual.widgets import Input, Button, Static, Header, Footer
from textual.containers import Container
from pypresence import ActivityType, AioClient
import asyncio


class DiscordRCP:
    def __init__(self):
        self.client = None
        self.connected = False
        self.update_task = None

    async def connect(self, CID):
        try:
            self.client = AioClient(CID)
            await self.client.start()
            self.connected = True
            self.update_task = asyncio.create_task(self._update_loop())
            return "Connected successfully!"
        except Exception as e:
            return f"Connection error: {e}"

    async def _update_loop(self):
        """Background task to maintain presence"""
        while self.connected:
            try:
                await self.client.set_activity(
                    activity_type=ActivityType.WATCHING,
                    name="Discord Custom Rich Presence",
                    state="by karrigan.me",
                    details="Download from our Website",
                    large_text="karrigan.me",
                    small_text="karrigan.me",
                    large_image="https://karrigan.me/wp-content/uploads/2025/09/cropped-logo-1-100x100.png",
                )
                await asyncio.sleep(15)
            except Exception as e:
                print(e)

    async def update_presence(self, name, state, details, large_txt, small_txt, large_img, small_img):
        """Update presence with custom values"""
        if self.connected and self.client:
            if not any([name, state, details, large_txt, small_txt, large_img, small_img]):
                # default presence
                await self.client.set_activity(
                    activity_type=ActivityType.WATCHING,
                    name="Discord Custom Rich Presence",
                    state="by karrigan.me",
                    details="Download from our Website",
                    large_text="karrigan.me",
                    small_text="karrigan.me",
                    large_image="https://karrigan.me/wp-content/uploads/2025/09/cropped-logo-1-100x100.png",
                )
            else:
                await self.client.set_activity(
                    name=name or None,
                    state=state or None,
                    details=details or None,
                    large_text=large_txt or None,
                    small_text=small_txt or None,
                    large_image=large_img or None,
                    small_image=small_img or None,
                )

class DiscordRPCApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    Container {
        width: 60%;
        height: auto;
        border: solid green;
        padding: 1;
    }
    #status {
        width: 100%;
        height: 3;
        content-align: center middle;
        margin: 1 0;
    }
    .buttons {
        width: 100%;
        height: auto;
        layout: horizontal;
    }
    Button {
        width: 1fr;
        margin: 0 1;
    }
    """

    def __init__(self):
        super().__init__()
        self.drpc = DiscordRCP()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Bot Client ID", id="cid")

        yield Button("Connect", id="rpc_btn")
        yield Button("Update CRP", id="update_btn")

        yield Input(placeholder="Name", id="def_name")
        yield Input(placeholder="State", id="def_state")
        yield Input(placeholder="Details", id="def_details")
        yield Input(placeholder="Large Text", id="def_large_txt")
        yield Input(placeholder="Small Text", id="def_small_txt")
        yield Input(placeholder="Large Image URL", id="def_large_img")
        yield Input(placeholder="Small Image URL", id="def_small_img")

        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "rpc_btn":
            if event.button.label == "Connect":
                cid = "1410296139089051648"
                #cid = self.query_one("#cid", Input).value
                if cid == "" or None:
                    self.notify("CID needed", severity="warning")
                elif not cid.isnumeric():
                    self.notify("Wrong CID", severity="error")
                else:
                    cid = int(cid)
                    if await self.connect_rpc(cid) == 1:
                        event.button.label = "Exit"
                    else:
                        self.notify("error", severity="warning")

            elif event.button.label == "Exit":
                self.exit()

        elif event.button.id == "update_btn":
            # Get values from input fields
            name = self.query_one("#def_name", Input).value
            state = self.query_one("#def_state", Input).value
            details = self.query_one("#def_details", Input).value
            large_txt = self.query_one("#def_large_txt", Input).value
            small_txt = self.query_one("#def_small_txt", Input).value
            large_img = self.query_one("#def_large_img", Input).value
            small_img = self.query_one("#def_small_img", Input).value

            await self.drpc.update_presence(
                name, state, details, large_txt, small_txt, large_img, small_img
            )

    async def connect_rpc(self, CID) -> int:
        result = await self.drpc.connect(CID)
        return 1 if "successfully" in result else 0


if __name__ == "__main__":
    app = DiscordRPCApp()
    app.run()