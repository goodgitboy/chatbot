from __future__ import annotations

"""Simple Tkinter overlay showing current Hangul/English input mode.

This script listens for the Hangul toggle key while the window is focused
and updates the label to show whether the user is typing in Korean or
English. It cannot read the system IME state, so it keeps an internal
state that flips whenever one of the toggle keys is pressed inside the
window.
"""

import argparse
import tkinter as tk
from tkinter import ttk


class HangulEnglishIndicator:
    """Display the current Hangul/English key state.

    The indicator tracks an internal boolean that toggles whenever the
    Hangul key (or common alternatives) is pressed while the window has
    focus. Because the script does not query the OS IME state, the user
    can also toggle by clicking the on-screen button to keep the display
    in sync.
    """

    def __init__(
        self,
        *,
        start_korean: bool = False,
        geometry: str | None = None,
        topmost: bool = False,
    ) -> None:
        self.is_korean = start_korean

        self.root = tk.Tk()
        self.root.title("한/영 표시기")
        if geometry:
            self.root.geometry(geometry)
        else:
            self.root.geometry("320x180")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", topmost)

        self.content = ttk.Frame(self.root, padding=20)
        self.content.pack(fill=tk.BOTH, expand=True)

        self.status_label = ttk.Label(
            self.content,
            text=self._status_text(),
            anchor=tk.CENTER,
            font=("Noto Sans", 20, "bold"),
        )
        self.status_label.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.toggle_button = ttk.Button(
            self.content,
            text="상태 직접 변경 (한/영 키와 동일)",
            command=self._toggle_state,
        )
        self.toggle_button.pack(fill=tk.X)

        info_text = (
            "창이 포커스된 상태에서 한/영 키, Hangul/Hangul_Mode 키 또는 "
            "Shift+Space를 누르면 상태가 바뀝니다."
        )
        ttk.Label(
            self.content,
            text=info_text,
            wraplength=280,
            justify=tk.CENTER,
            style="Info.TLabel",
        ).pack(fill=tk.X, pady=(10, 0))

        # Bind common key events that users press to toggle IME in Korea.
        for keysym in ("Hangul", "Hangul_Mode", "Hangul_Hanja"):
            self.root.bind(f"<KeyPress-{keysym}>", self._on_toggle_key)

        # Some keyboards use Shift+Space as an alternative toggle.
        self.root.bind("<Shift-KeyPress-space>", self._on_toggle_key)

        # Close the window quickly with Escape.
        self.root.bind("<Escape>", lambda _event: self.root.destroy())

    def _status_text(self) -> str:
        return "현재 입력: 한국어" if self.is_korean else "현재 입력: 영어"

    def _set_label_colors(self) -> None:
        # Update background to make state visually obvious.
        bg = "#cce5ff" if not self.is_korean else "#ffe6cc"
        fg = "#004085" if not self.is_korean else "#8a3b00"
        self.root.configure(bg=bg)
        self.content.configure(style="Bg.TFrame")
        style = ttk.Style()
        style.configure("Bg.TFrame", background=bg)
        style.configure("Status.TLabel", background=bg, foreground=fg)
        style.configure("Info.TLabel", background=bg)
        self.status_label.configure(style="Status.TLabel")

    def _toggle_state(self, event=None) -> None:  # noqa: ANN001
        self.is_korean = not self.is_korean
        self.status_label.config(text=self._status_text())
        self._set_label_colors()

    def _on_toggle_key(self, event) -> None:  # noqa: ANN001
        self._toggle_state()

    def run(self) -> None:
        # Initialize colors once the window exists.
        self._set_label_colors()
        self.root.mainloop()


def main() -> None:
    parser = argparse.ArgumentParser(description="Display current Hangul/English toggle state.")
    parser.add_argument("--start-korean", action="store_true", help="Start with Korean state active.")
    parser.add_argument("--geometry", help="Custom geometry string (e.g. 320x180+100+100).", default=None)
    parser.add_argument("--topmost", action="store_true", help="Keep the window always on top.")
    args = parser.parse_args()

    indicator = HangulEnglishIndicator(
        start_korean=args.start_korean,
        geometry=args.geometry,
        topmost=args.topmost,
    )
    indicator.run()


if __name__ == "__main__":
    main()
