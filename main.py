__version__ = "0.1.0"

import json
import threading
import urllib.request
import urllib.error

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle


PINK = (1.0, 0.78, 0.87, 1)
BLUE = (0.78, 0.88, 1.0, 1)
CREAM = (1.0, 0.97, 0.91, 1)
DARK = (0.25, 0.20, 0.30, 1)


class SakuraApp(App):
    def build(self):
        self.title = "SakuraAI"
        self.api_key = ""

        root = BoxLayout(
            orientation="vertical",
            padding=dp(14),
            spacing=dp(10)
        )
        with root.canvas.before:
            Color(*CREAM)
            self.bg = RoundedRectangle(
                pos=root.pos, size=root.size, radius=[dp(18)]
            )
        root.bind(
            pos=lambda w, v: setattr(self.bg, "pos", v),
            size=lambda w, v: setattr(self.bg, "size", v)
        )

        title = Label(
            text="[b]🌸 SakuraAI 🌸[/b]",
            markup=True,
            color=DARK,
            font_size="28sp",
            size_hint_y=None,
            height=dp(55)
        )
        root.add_widget(title)

        subtitle = Label(
            text="Your cute little AI friend ✨",
            color=DARK,
            size_hint_y=None,
            height=dp(28)
        )
        root.add_widget(subtitle)

        self.key_box = TextInput(
            hint_text="Paste Gemini API key here",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=dp(48),
            background_color=(1, 1, 1, 1),
            foreground_color=DARK
        )
        root.add_widget(self.key_box)

        self.chat = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(10),
            padding=dp(8)
        )
        self.chat.bind(minimum_height=self.chat.setter("height"))

        scroll = ScrollView()
        scroll.add_widget(self.chat)
        root.add_widget(scroll)

        bottom = BoxLayout(
            size_hint_y=None,
            height=dp(52),
            spacing=dp(8)
        )
        self.message = TextInput(
            hint_text="Message SakuraAI...",
            multiline=False,
            background_color=(1, 1, 1, 1),
            foreground_color=DARK
        )
        self.message.bind(on_text_validate=self.send_message)

        send = Button(
            text="Send 🌸",
            size_hint_x=None,
            width=dp(100),
            background_normal="",
            background_color=(0.92, 0.55, 0.72, 1)
        )
        send.bind(on_press=self.send_message)

        bottom.add_widget(self.message)
        bottom.add_widget(send)
        root.add_widget(bottom)

        self.add_message("SakuraAI", "Hello! 🌸 I'm ready to chat.")
        return root

    def add_message(self, who, text):
        label = Label(
            text=f"{who}: {text}",
            color=DARK,
            size_hint_y=None,
            halign="left",
            valign="middle",
            text_size=(None, None)
        )
        label.bind(
            width=lambda w, width: setattr(
                w, "text_size", (width - dp(12), None)
            )
        )
        label.bind(
            texture_size=lambda w, size: setattr(
                w, "height", max(dp(42), size[1] + dp(16))
            )
        )
        self.chat.add_widget(label)

    def send_message(self, *args):
        question = self.message.text.strip()
        key = self.key_box.text.strip()

        if not question:
            return
        if not key:
            self.add_message("SakuraAI", "Please enter your Gemini API key first.")
            return

        self.api_key = key
        self.message.text = ""
        self.add_message("You", question)
        self.add_message("SakuraAI", "Thinking... 💗")

        threading.Thread(
            target=self.ask_gemini,
            args=(question,),
            daemon=True
        ).start()

    def ask_gemini(self, question):
        try:
            url = (
                "https://generativelanguage.googleapis.com/"
                "v1beta/models/gemini-3.5-flash-lite:generateContent"
            )
            body = {
                "contents": [{
                    "parts": [{"text": question}]
                }]
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "x-goog-api-key": self.api_key
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode("utf-8"))

            answer = result["candidates"][0]["content"]["parts"][0]["text"]
            Clock.schedule_once(
                lambda dt: self.add_message("SakuraAI", answer)
            )

        except Exception as error:
            Clock.schedule_once(
                lambda dt: self.add_message(
                    "SakuraAI", f"Sorry, something went wrong: {error}"
                )
            )


if __name__ == "__main__":
    SakuraApp().run()
