
import os
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
from PIL import Image, ImageTk, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter

APP_TITLE = "ProtegerDNI v1.5"

BG = "#F3F6FA"
CARD = "#FFFFFF"
TEXT = "#16324F"
MUTED = "#6E7F92"
PRIMARY = "#1769E0"
PRIMARY_DARK = "#0F55B9"
BORDER = "#DCE5EF"
DANGER = "#C43D3D"
PREVIEW_BG = "#E9EEF5"


class MovableSelectionMixin:
    def setup_selection(self):
        self.selection = None
        self.drag_start = None
        self.drag_rect = None
        self.move_mode = False
        self.move_origin = None
        self.selection_origin = None
        self.display_scale = 1.0
        self.image_x = 0
        self.image_y = 0
        self.image_ref = None

    def inside_image(self, x, y):
        w = self.working_image.width * self.display_scale
        h = self.working_image.height * self.display_scale
        return (
            self.image_x <= x <= self.image_x + w and
            self.image_y <= y <= self.image_y + h
        )

    def inside_selection(self, x, y):
        if not self.selection:
            return False
        x1, y1, x2, y2 = self.selection
        dx1 = self.image_x + x1 * self.display_scale
        dy1 = self.image_y + y1 * self.display_scale
        dx2 = self.image_x + x2 * self.display_scale
        dy2 = self.image_y + y2 * self.display_scale
        return dx1 <= x <= dx2 and dy1 <= y <= dy2

    def press_selection(self, event):
        if not self.inside_image(event.x, event.y):
            return

        if self.inside_selection(event.x, event.y):
            self.move_mode = True
            self.move_origin = (event.x, event.y)
            self.selection_origin = self.selection
            self.canvas.config(cursor="fleur")
            return

        self.move_mode = False
        self.drag_start = (event.x, event.y)
        self.drag_rect = self.canvas.create_rectangle(
            event.x, event.y, event.x, event.y,
            outline="white", width=3
        )

    def drag_selection(self, event):
        if self.move_mode and self.selection_origin:
            ox, oy = self.move_origin
            dx = (event.x - ox) / self.display_scale
            dy = (event.y - oy) / self.display_scale

            x1, y1, x2, y2 = self.selection_origin
            w = x2 - x1
            h = y2 - y1

            nx1 = max(0, min(x1 + dx, self.working_image.width - w))
            ny1 = max(0, min(y1 + dy, self.working_image.height - h))

            self.selection = (
                int(nx1), int(ny1),
                int(nx1 + w), int(ny1 + h)
            )
            self.render()
            return

        if self.drag_rect is None or self.drag_start is None:
            return

        max_x = self.image_x + self.working_image.width * self.display_scale
        max_y = self.image_y + self.working_image.height * self.display_scale

        x = min(max(event.x, self.image_x), max_x)
        y = min(max(event.y, self.image_y), max_y)

        self.canvas.coords(
            self.drag_rect,
            self.drag_start[0], self.drag_start[1],
            x, y
        )

    def release_selection(self, event):
        if self.move_mode:
            self.move_mode = False
            self.move_origin = None
            self.selection_origin = None
            self.canvas.config(cursor="cross")
            self.render()
            return

        if self.drag_rect is None or self.drag_start is None:
            return

        max_x = self.image_x + self.working_image.width * self.display_scale
        max_y = self.image_y + self.working_image.height * self.display_scale

        x = min(max(event.x, self.image_x), max_x)
        y = min(max(event.y, self.image_y), max_y)

        x1d, x2d = sorted((self.drag_start[0], x))
        y1d, y2d = sorted((self.drag_start[1], y))

        if (x2d - x1d) >= 8 and (y2d - y1d) >= 8:
            self.selection = (
                max(0, int((x1d - self.image_x) / self.display_scale)),
                max(0, int((y1d - self.image_y) / self.display_scale)),
                min(self.working_image.width, int((x2d - self.image_x) / self.display_scale)),
                min(self.working_image.height, int((y2d - self.image_y) / self.display_scale))
            )

        self.drag_rect = None
        self.drag_start = None
        self.render()


class CropDialog(tk.Toplevel, MovableSelectionMixin):
    def __init__(self, parent, image, callback):
        super().__init__(parent)
        self.title("Recortar")
        self.geometry("980x700")
        self.minsize(820, 600)
        self.configure(bg=BG)

        self.original = image.copy().convert("RGB")
        self.working_image = image.copy().convert("RGB")
        self.callback = callback
        self.history = []
        self.setup_selection()

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build()
        self.after(150, self.render)

    def _btn(self, parent, text, command, primary=False):
        return tk.Button(
            parent, text=text, command=command,
            bg=PRIMARY if primary else CARD,
            fg="white" if primary else TEXT,
            activebackground=PRIMARY_DARK if primary else "#EAF0F6",
            activeforeground="white" if primary else TEXT,
            bd=0, padx=12, pady=7,
            font=("Segoe UI", 9, "bold" if primary else "normal"),
            cursor="hand2"
        )

    def _build(self):
        top = tk.Frame(self, bg=BG, padx=16, pady=10)
        top.grid(row=0, column=0, sticky="ew")

        tk.Label(
            top, text="Recortar imagen",
            bg=BG, fg=TEXT,
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w")

        tk.Label(
            top,
            text="1. Marcá el área a conservar.  2. Mové el recuadro si hace falta.  3. Aplicá el recorte.  4. Aceptá los cambios.",
            bg=BG, fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(2, 0))

        toolbar = tk.Frame(self, bg=BG, padx=16, pady=7)
        toolbar.grid(row=1, column=0, sticky="ew")

        tk.Label(
            toolbar,
            text="Marcá el área a conservar y ajustala con el mouse. Al aceptar se aplica el recorte.",
            bg=BG, fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(side="left")

        actions = tk.Frame(toolbar, bg=BG)
        actions.pack(side="right")

        self._btn(actions, "Restablecer", self.reset).pack(side="left", padx=3)
        self._btn(actions, "Cancelar", self.destroy).pack(side="left", padx=3)
        self._btn(actions, "Aceptar", self.accept, primary=True).pack(side="left", padx=3)

        self.status = tk.Label(
            self, text="Sin selección",
            bg=BG, fg=MUTED,
            font=("Segoe UI", 9),
            padx=16, pady=4
        )
        self.status.grid(row=3, column=0, sticky="w")

        self.canvas = tk.Canvas(
            self, bg="#202B3A",
            highlightthickness=0,
            cursor="cross"
        )
        self.canvas.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 8))

        self.canvas.bind("<ButtonPress-1>", self.press_selection)
        self.canvas.bind("<B1-Motion>", self.drag_selection)
        self.canvas.bind("<ButtonRelease-1>", self.release_selection)
        self.canvas.bind("<Configure>", lambda e: self.after_idle(self.render))


    def render(self):
        if not self.winfo_exists():
            return

        self.update_idletasks()
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        if cw < 50 or ch < 50:
            return

        iw, ih = self.working_image.size
        self.display_scale = max(0.05, min((cw - 30) / iw, (ch - 30) / ih))

        dw = max(1, int(iw * self.display_scale))
        dh = max(1, int(ih * self.display_scale))
        preview = self.working_image.resize((dw, dh), Image.Resampling.LANCZOS)

        self.image_ref = ImageTk.PhotoImage(preview, master=self)
        self.canvas.image_ref = self.image_ref

        self.canvas.delete("all")
        self.image_x = max(15, (cw - dw) // 2)
        self.image_y = max(15, (ch - dh) // 2)
        self.canvas.create_image(self.image_x, self.image_y, anchor="nw", image=self.image_ref)

        if self.selection:
            x1, y1, x2, y2 = self.selection
            dx1 = self.image_x + x1 * self.display_scale
            dy1 = self.image_y + y1 * self.display_scale
            dx2 = self.image_x + x2 * self.display_scale
            dy2 = self.image_y + y2 * self.display_scale

            self.canvas.create_rectangle(
                dx1, dy1, dx2, dy2,
                outline="white", width=3, dash=(8, 4)
            )

            r = 5
            for hx, hy in ((dx1,dy1),(dx2,dy1),(dx1,dy2),(dx2,dy2)):
                self.canvas.create_oval(
                    hx-r, hy-r, hx+r, hy+r,
                    fill="white", outline=TEXT
                )

        self.status.config(
            text=("Área seleccionada: podés moverla con el mouse"
                  if self.selection else
                  f"Recortes aplicados: {len(self.history)}")
        )

    def apply_crop(self):
        if not self.selection:
            messagebox.showwarning(
                "Sin selección",
                "Marcá primero el área que querés conservar."
            )
            return False

        x1, y1, x2, y2 = self.selection
        if x2 <= x1 or y2 <= y1:
            messagebox.showwarning("Recorte inválido", "La selección no es válida.")
            return False

        self.history.append(self.working_image.copy())
        self.working_image = self.working_image.crop((x1, y1, x2, y2)).copy()
        self.selection = None
        self.render()
        return True

    def cancel_selection(self):
        self.selection = None
        self.render()

    def undo(self):
        if not self.history:
            messagebox.showinfo("Sin cambios", "No hay recortes aplicados para deshacer.")
            return
        self.working_image = self.history.pop()
        self.selection = None
        self.render()

    def reset(self):
        self.working_image = self.original.copy()
        self.history = []
        self.selection = None
        self.render()

    def accept(self):
        if not self.selection:
            messagebox.showwarning(
                "Sin selección",
                "Marcá primero el área que querés conservar."
            )
            return

        x1, y1, x2, y2 = self.selection
        if x2 <= x1 or y2 <= y1:
            messagebox.showwarning("Recorte inválido", "La selección no es válida.")
            return

        result = self.working_image.crop((x1, y1, x2, y2)).copy()
        self.callback(result)
        self.destroy()


class RedactDialog(tk.Toplevel, MovableSelectionMixin):
    def __init__(self, parent, image, callback):
        super().__init__(parent)
        self.title("Tapar datos")
        self.geometry("980x700")
        self.minsize(820, 600)
        self.configure(bg=BG)

        self.original = image.copy().convert("RGB")
        self.working_image = image.copy().convert("RGB")
        self.callback = callback
        self.history = []
        self.setup_selection()

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build()
        self.after(150, self.render)

    def _btn(self, parent, text, command, primary=False):
        return tk.Button(
            parent, text=text, command=command,
            bg=PRIMARY if primary else CARD,
            fg="white" if primary else TEXT,
            activebackground=PRIMARY_DARK if primary else "#EAF0F6",
            activeforeground="white" if primary else TEXT,
            bd=0, padx=12, pady=7,
            font=("Segoe UI", 9, "bold" if primary else "normal"),
            cursor="hand2"
        )

    def _build(self):
        top = tk.Frame(self, bg=BG, padx=16, pady=10)
        top.grid(row=0, column=0, sticky="ew")

        tk.Label(
            top, text="Tapar datos",
            bg=BG, fg=TEXT,
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w")

        tk.Label(
            top,
            text="1. Marcá un dato.  2. Mové el recuadro si hace falta.  3. Aplicá el ocultamiento.  4. Repetí o aceptá.",
            bg=BG, fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(2, 0))

        toolbar = tk.Frame(self, bg=BG, padx=16, pady=7)
        toolbar.grid(row=1, column=0, sticky="ew")

        tk.Label(
            toolbar,
            text="Arrastrá sobre cada dato: al soltar el mouse se tapa automáticamente.",
            bg=BG, fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(side="left")

        actions = tk.Frame(toolbar, bg=BG)
        actions.pack(side="right")

        self._btn(actions, "Deshacer", self.undo).pack(side="left", padx=3)
        self._btn(actions, "Restablecer", self.reset).pack(side="left", padx=3)
        self._btn(actions, "Cancelar", self.destroy).pack(side="left", padx=3)
        self._btn(actions, "Aceptar", self.accept, primary=True).pack(side="left", padx=3)

        self.status = tk.Label(
            self, text="Sin selección",
            bg=BG, fg=MUTED,
            font=("Segoe UI", 9),
            padx=16, pady=4
        )
        self.status.grid(row=3, column=0, sticky="w")

        self.canvas = tk.Canvas(
            self, bg="#202B3A",
            highlightthickness=0,
            cursor="cross"
        )
        self.canvas.grid(row=2, column=0, sticky="nsew", padx=16, pady=(0, 8))

        self.canvas.bind("<ButtonPress-1>", self.press_selection)
        self.canvas.bind("<B1-Motion>", self.drag_selection)
        self.canvas.bind("<ButtonRelease-1>", self.release_selection)
        self.canvas.bind("<Configure>", lambda e: self.after_idle(self.render))


    def render(self):
        if not self.winfo_exists():
            return

        self.update_idletasks()
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        if cw < 50 or ch < 50:
            return

        iw, ih = self.working_image.size
        self.display_scale = max(0.05, min((cw - 30) / iw, (ch - 30) / ih))

        dw = max(1, int(iw * self.display_scale))
        dh = max(1, int(ih * self.display_scale))
        preview = self.working_image.resize((dw, dh), Image.Resampling.LANCZOS)

        self.image_ref = ImageTk.PhotoImage(preview, master=self)
        self.canvas.image_ref = self.image_ref

        self.canvas.delete("all")
        self.image_x = max(15, (cw - dw) // 2)
        self.image_y = max(15, (ch - dh) // 2)
        self.canvas.create_image(self.image_x, self.image_y, anchor="nw", image=self.image_ref)

        if self.selection:
            x1, y1, x2, y2 = self.selection
            dx1 = self.image_x + x1 * self.display_scale
            dy1 = self.image_y + y1 * self.display_scale
            dx2 = self.image_x + x2 * self.display_scale
            dy2 = self.image_y + y2 * self.display_scale

            self.canvas.create_rectangle(
                dx1, dy1, dx2, dy2,
                outline="white", width=3, dash=(8, 4)
            )

            r = 5
            for hx, hy in ((dx1,dy1),(dx2,dy1),(dx1,dy2),(dx2,dy2)):
                self.canvas.create_oval(
                    hx-r, hy-r, hx+r, hy+r,
                    fill="white", outline=TEXT
                )

        self.status.config(
            text=("Área seleccionada: podés moverla con el mouse"
                  if self.selection else
                  f"Datos tapados aplicados: {len(self.history)}")
        )

    def release_selection(self, event):
        if self.move_mode:
            self.move_mode = False
            self.move_origin = None
            self.selection_origin = None
            self.canvas.config(cursor="cross")
            self.render()
            return

        if self.drag_rect is None or self.drag_start is None:
            return

        max_x = self.image_x + self.working_image.width * self.display_scale
        max_y = self.image_y + self.working_image.height * self.display_scale

        x = min(max(event.x, self.image_x), max_x)
        y = min(max(event.y, self.image_y), max_y)

        x1d, x2d = sorted((self.drag_start[0], x))
        y1d, y2d = sorted((self.drag_start[1], y))

        if (x2d - x1d) >= 8 and (y2d - y1d) >= 8:
            selection = (
                max(0, int((x1d - self.image_x) / self.display_scale)),
                max(0, int((y1d - self.image_y) / self.display_scale)),
                min(self.working_image.width, int((x2d - self.image_x) / self.display_scale)),
                min(self.working_image.height, int((y2d - self.image_y) / self.display_scale))
            )

            # Apply immediately on mouse release.
            self.history.append(self.working_image.copy())
            new_image = self.working_image.copy().convert("RGB")
            draw = ImageDraw.Draw(new_image)
            draw.rectangle(selection, fill=(0, 0, 0))
            self.working_image = new_image

        self.drag_rect = None
        self.drag_start = None
        self.selection = None
        self.render()

    def apply_redaction(self):
        if not self.selection:
            messagebox.showwarning(
                "Sin selección",
                "Marcá primero el dato o zona que querés tapar."
            )
            return False

        x1, y1, x2, y2 = self.selection
        if x2 <= x1 or y2 <= y1:
            messagebox.showwarning("Selección inválida", "La selección no es válida.")
            return False

        # Save full previous working state to guarantee undo works.
        self.history.append(self.working_image.copy())

        new_image = self.working_image.copy().convert("RGB")
        draw = ImageDraw.Draw(new_image)
        draw.rectangle((x1, y1, x2, y2), fill=(0, 0, 0))
        self.working_image = new_image

        self.selection = None
        self.render()
        return True

    def cancel_selection(self):
        self.selection = None
        self.render()

    def undo(self):
        if not self.history:
            messagebox.showinfo(
                "Sin cambios",
                "No hay datos tapados para deshacer."
            )
            return

        self.working_image = self.history.pop()
        self.selection = None
        self.render()

    def reset(self):
        self.working_image = self.original.copy()
        self.history = []
        self.selection = None
        self.render()

    def accept(self):
        self.callback(self.working_image.copy())
        self.destroy()


class ProtegerDNIApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1180x800")
        self.root.minsize(1000, 720)
        self.root.configure(bg=BG)

        self.front_img = None
        self.back_img = None
        self.front_history = []
        self.back_history = []

        self.front_ref = None
        self.back_ref = None

        self.recipient = tk.StringVar()
        self.date = tk.StringVar(value=datetime.now().strftime("%d/%m/%Y"))
        self.password_enabled = tk.BooleanVar(value=False)
        self.password = tk.StringVar()

        self._preview_job = None

        self.build_ui()

        self.recipient.trace_add("write", lambda *args: self.schedule_live_preview())
        self.date.trace_add("write", lambda *args: self.schedule_live_preview())

    def btn(self, parent, text, command, primary=False, danger=False):
        bg = DANGER if danger else (PRIMARY if primary else "#EAF0F6")
        fg = "white" if primary or danger else TEXT
        return tk.Button(
            parent, text=text, command=command,
            bg=bg, fg=fg,
            bd=0, padx=11, pady=6,
            font=("Segoe UI", 9, "bold" if primary or danger else "normal"),
            cursor="hand2"
        )

    def card(self, parent):
        return tk.Frame(
            parent, bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )

    def step_header(self, parent, number, title):
        row = tk.Frame(parent, bg=CARD)
        row.pack(fill="x", padx=12, pady=(8, 3))

        tk.Label(
            row, text=number,
            bg=PRIMARY, fg="white",
            width=2,
            font=("Segoe UI", 9, "bold")
        ).pack(side="left")

        tk.Label(
            row, text=title,
            bg=CARD, fg=TEXT,
            font=("Segoe UI", 11, "bold")
        ).pack(side="left", padx=7)

    def build_ui(self):
        header = tk.Frame(self.root, bg=TEXT, height=58)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="ProtegerDNI",
            bg=TEXT, fg="white",
            font=("Segoe UI", 19, "bold")
        ).pack(side="left", padx=(20, 10), pady=11)

        tk.Label(
            header,
            text="Copias de identidad, bajo control.",
            bg=TEXT, fg="#D7E5F3",
            font=("Segoe UI", 10)
        ).pack(side="left")

        self.btn(header, "ⓘ Créditos", self.show_credits).pack(side="right", padx=18, pady=11)

        outer = tk.Frame(self.root, bg=BG)
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.content = tk.Frame(canvas, bg=BG, padx=14, pady=10)
        self.content_id = canvas.create_window((0,0), window=self.content, anchor="nw")

        self.content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfigure(self.content_id, width=e.width)
        )

        # STEP 1
        self.front_card = self.card(self.content)
        self.front_card.pack(fill="x", pady=(0, 7))
        self.step_header(self.front_card, "1", "Frente")

        row = tk.Frame(self.front_card, bg=CARD)
        row.pack(fill="x", padx=12, pady=(2, 10))

        controls = tk.Frame(row, bg=CARD, width=250)
        controls.pack(side="left", fill="y")
        controls.pack_propagate(False)

        self.front_name = tk.Label(
            controls,
            text="Sin archivo seleccionado",
            bg=CARD, fg=MUTED,
            font=("Segoe UI", 8),
            wraplength=230,
            justify="left"
        )
        self.front_name.pack(anchor="w", pady=(2, 7))

        self.btn(controls, "Cargar frente", self.load_front, primary=True).pack(fill="x", pady=3)
        self.btn(controls, "Recortar", lambda: self.open_crop("front")).pack(fill="x", pady=3)
        self.btn(controls, "Tapar datos", lambda: self.open_redact("front")).pack(fill="x", pady=3)
        self.btn(controls, "Deshacer último cambio", lambda: self.undo_side("front")).pack(fill="x", pady=3)

        preview_box = tk.Frame(row, bg=PREVIEW_BG, height=145)
        preview_box.pack(side="left", fill="both", expand=True, padx=(12,0))
        preview_box.pack_propagate(False)

        self.front_preview = tk.Label(
            preview_box,
            text="La vista previa del frente aparecerá aquí",
            bg=PREVIEW_BG, fg=MUTED,
            font=("Segoe UI", 9)
        )
        self.front_preview.pack(fill="both", expand=True)

        # STEP 2
        self.back_card = self.card(self.content)
        self.back_card.pack(fill="x", pady=7)
        self.step_header(self.back_card, "2", "Dorso")

        row = tk.Frame(self.back_card, bg=CARD)
        row.pack(fill="x", padx=12, pady=(2, 10))

        controls = tk.Frame(row, bg=CARD, width=250)
        controls.pack(side="left", fill="y")
        controls.pack_propagate(False)

        self.back_name = tk.Label(
            controls,
            text="Sin archivo seleccionado",
            bg=CARD, fg=MUTED,
            font=("Segoe UI", 8),
            wraplength=230,
            justify="left"
        )
        self.back_name.pack(anchor="w", pady=(2, 7))

        self.btn(controls, "Cargar dorso", self.load_back, primary=True).pack(fill="x", pady=3)
        self.btn(controls, "Recortar", lambda: self.open_crop("back")).pack(fill="x", pady=3)
        self.btn(controls, "Tapar datos", lambda: self.open_redact("back")).pack(fill="x", pady=3)
        self.btn(controls, "Deshacer último cambio", lambda: self.undo_side("back")).pack(fill="x", pady=3)

        preview_box = tk.Frame(row, bg=PREVIEW_BG, height=145)
        preview_box.pack(side="left", fill="both", expand=True, padx=(12,0))
        preview_box.pack_propagate(False)

        self.back_preview = tk.Label(
            preview_box,
            text="La vista previa del dorso aparecerá aquí",
            bg=PREVIEW_BG, fg=MUTED,
            font=("Segoe UI", 9)
        )
        self.back_preview.pack(fill="both", expand=True)

        # STEP 3 + STEP 4 side by side
        lower = tk.Frame(self.content, bg=BG)
        lower.pack(fill="x", pady=7)

        indiv = self.card(lower)
        indiv.pack(side="left", fill="both", expand=True, padx=(0,4))
        self.step_header(indiv, "3", "Individualización")

        form = tk.Frame(indiv, bg=CARD)
        form.pack(fill="x", padx=12, pady=(3, 8))

        tk.Label(
            form,
            text="Para ser presentado ante",
            bg=CARD, fg=TEXT,
            font=("Segoe UI", 8, "bold")
        ).grid(row=0, column=0, sticky="w")

        tk.Entry(
            form,
            textvariable=self.recipient,
            font=("Segoe UI", 10),
            bd=1, relief="solid"
        ).grid(row=1, column=0, sticky="ew", padx=(0,10), pady=(3,0))

        tk.Label(
            form,
            text="Fecha",
            bg=CARD, fg=TEXT,
            font=("Segoe UI", 8, "bold")
        ).grid(row=0, column=1, sticky="w")

        tk.Entry(
            form,
            textvariable=self.date,
            font=("Segoe UI", 10),
            width=14,
            bd=1, relief="solid"
        ).grid(row=1, column=1, sticky="w", pady=(3,0))

        form.columnconfigure(0, weight=1)

        tk.Label(
            indiv,
            text="La marca de agua se actualiza en vivo.",
            bg=CARD, fg=MUTED,
            font=("Segoe UI", 8)
        ).pack(anchor="w", padx=12, pady=(0,8))

        output = self.card(lower)
        output.pack(side="left", fill="both", expand=True, padx=(4,0))
        self.step_header(output, "4", "Generar")

        gen = tk.Frame(output, bg=CARD)
        gen.pack(fill="x", padx=12, pady=(4,8))

        self.btn(gen, "Generar PDF", self.generate_pdf, primary=True).pack(side="left")

        pw = tk.Frame(gen, bg=CARD)
        pw.pack(side="left", padx=10)

        tk.Checkbutton(
            pw,
            text="Proteger PDF con contraseña",
            variable=self.password_enabled,
            command=self.toggle_password,
            bg=CARD, fg=TEXT,
            selectcolor=CARD,
            font=("Segoe UI", 8)
        ).pack(anchor="w")

        self.password_entry = tk.Entry(
            pw,
            textvariable=self.password,
            show="•",
            state="disabled",
            width=18,
            font=("Segoe UI", 9),
            bd=1, relief="solid"
        )
        self.password_entry.pack(anchor="w", pady=(2,0))

        self.btn(gen, "Generar JPG", self.generate_jpg, primary=True).pack(side="left", padx=8)
        self.btn(gen, "Limpiar todo", self.clear_all, danger=True).pack(side="right")

        footer = tk.Frame(self.content, bg=BG)
        footer.pack(fill="x", pady=(2,8))

        self.status = tk.Label(
            footer,
            text="Listo",
            bg=BG, fg=MUTED,
            font=("Segoe UI", 8)
        )
        self.status.pack(side="left")

        tk.Label(
            footer,
            text="ProtegerDNI v1.5 · EEL CIBERSEGURIDAD",
            bg=BG, fg=MUTED,
            font=("Segoe UI", 8)
        ).pack(side="right")

    def show_credits(self):
        messagebox.showinfo(
            "Créditos",
            "ProtegerDNI\n\n"
            "Eduardo Ernesto Lecce\n"
            "EEL CIBERSEGURIDAD\n"
            "eelciberseguridad@gmail.com"
        )

    def toggle_password(self):
        self.password_entry.config(
            state="normal" if self.password_enabled.get() else "disabled"
        )
        if not self.password_enabled.get():
            self.password.set("")

    def load_image(self):
        path = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[
                ("Imágenes", "*.jpg *.jpeg *.png *.webp *.bmp"),
                ("Todos los archivos", "*.*")
            ]
        )
        if not path:
            return None, None

        try:
            with Image.open(path) as im:
                im.load()
                clean = im.convert("RGB").copy()
            return path, clean
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la imagen.\n\n{e}")
            return None, None

    def load_front(self):
        path, image = self.load_image()
        if image is None:
            return
        self.front_img = image
        self.front_history = []
        self.front_name.config(text=os.path.basename(path))
        self.update_live_previews()
        self.status.config(text="Frente cargado")

    def load_back(self):
        path, image = self.load_image()
        if image is None:
            return
        self.back_img = image
        self.back_history = []
        self.back_name.config(text=os.path.basename(path))
        self.update_live_previews()
        self.status.config(text="Dorso cargado")

    def open_crop(self, side):
        image = self.front_img if side == "front" else self.back_img
        if image is None:
            messagebox.showwarning(
                "Falta imagen",
                f"Primero cargá el {'frente' if side == 'front' else 'dorso'}."
            )
            return

        CropDialog(
            self.root,
            image,
            lambda result: self.accept_edit(side, result, "recorte")
        )

    def open_redact(self, side):
        image = self.front_img if side == "front" else self.back_img
        if image is None:
            messagebox.showwarning(
                "Falta imagen",
                f"Primero cargá el {'frente' if side == 'front' else 'dorso'}."
            )
            return

        RedactDialog(
            self.root,
            image,
            lambda result: self.accept_edit(side, result, "ocultamiento")
        )

    def accept_edit(self, side, image, action):
        if side == "front":
            if self.front_img is not None:
                self.front_history.append(self.front_img.copy())
                if len(self.front_history) > 20:
                    self.front_history.pop(0)
            self.front_img = image.copy()
        else:
            if self.back_img is not None:
                self.back_history.append(self.back_img.copy())
                if len(self.back_history) > 20:
                    self.back_history.pop(0)
            self.back_img = image.copy()

        self.update_live_previews()
        self.status.config(
            text=f"{'Frente' if side == 'front' else 'Dorso'} actualizado: {action}"
        )

    def undo_side(self, side):
        if side == "front":
            if not self.front_history:
                messagebox.showinfo("Sin cambios", "No hay cambios aceptados del frente para deshacer.")
                return
            self.front_img = self.front_history.pop()
            label = "Frente"
        else:
            if not self.back_history:
                messagebox.showinfo("Sin cambios", "No hay cambios aceptados del dorso para deshacer.")
                return
            self.back_img = self.back_history.pop()
            label = "Dorso"

        self.update_live_previews()
        self.status.config(text=f"{label}: último cambio deshecho")

    def watermark(self, image):
        recipient = self.recipient.get().strip()
        date_text = self.date.get().strip()

        if not recipient and not date_text:
            return image.copy()

        text_parts = []
        if recipient:
            text_parts.append(f"PARA SER PRESENTADO ANTE: {recipient}")
        if date_text:
            text_parts.append(date_text)

        text = "  ·  ".join(text_parts)

        base = image.copy().convert("RGBA")
        overlay = Image.new("RGBA", base.size, (255,255,255,0))
        draw = ImageDraw.Draw(overlay)

        font_size = max(18, int(base.width * 0.022))
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0,0), text, font=font)
        tw = bbox[2]-bbox[0]
        th = bbox[3]-bbox[1]

        pad = max(8, font_size // 3)
        stamp = Image.new("RGBA", (tw + pad*2, th + pad*2), (255,255,255,0))
        sd = ImageDraw.Draw(stamp)
        sd.text((pad+1, pad+1), text, font=font, fill=(255,255,255,55))
        sd.text((pad, pad), text, font=font, fill=(12,55,100,105))

        rotated = stamp.rotate(24, expand=True, resample=Image.Resampling.BICUBIC)
        x = (base.width - rotated.width) // 2
        y = (base.height - rotated.height) // 2

        overlay.alpha_composite(rotated, (x, y))
        return Image.alpha_composite(base, overlay).convert("RGB")

    def schedule_live_preview(self):
        if self._preview_job:
            try:
                self.root.after_cancel(self._preview_job)
            except:
                pass
        self._preview_job = self.root.after(120, self.update_live_previews)

    def update_live_previews(self):
        self._preview_job = None
        self.update_one_preview(self.front_img, self.front_preview, "front")
        self.update_one_preview(self.back_img, self.back_preview, "back")

    def update_one_preview(self, image, label, side):
        if image is None:
            label.config(
                image="",
                text=f"La vista previa del {'frente' if side == 'front' else 'dorso'} aparecerá aquí"
            )
            if side == "front":
                self.front_ref = None
            else:
                self.back_ref = None
            return

        preview = self.watermark(image)
        preview.thumbnail((760, 180), Image.Resampling.LANCZOS)

        ref = ImageTk.PhotoImage(preview, master=self.root)
        label.config(image=ref, text="")
        label.image = ref

        if side == "front":
            self.front_ref = ref
        else:
            self.back_ref = ref

    def get_output_images(self):
        if self.front_img is None or self.back_img is None:
            raise ValueError("Cargá frente y dorso.")

        if not self.recipient.get().strip():
            raise ValueError("Completá 'Para ser presentado ante'.")

        if not self.date.get().strip():
            raise ValueError("Completá la fecha.")

        return self.watermark(self.front_img), self.watermark(self.back_img)

    def generate_pdf(self):
        try:
            front, back = self.get_output_images()
        except ValueError as e:
            messagebox.showwarning("Faltan datos", str(e))
            return

        if self.password_enabled.get() and not self.password.get():
            messagebox.showwarning(
                "Contraseña",
                "Ingresá una contraseña o desactivá la protección."
            )
            return

        output = filedialog.asksaveasfilename(
            title="Guardar PDF",
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")]
        )
        if not output:
            return

        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
                temp_path = temp.name

            front.save(
                temp_path,
                "PDF",
                resolution=150.0,
                save_all=True,
                append_images=[back]
            )

            reader = PdfReader(temp_path)
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            writer.add_metadata({})

            if self.password_enabled.get():
                writer.encrypt(self.password.get())

            with open(output, "wb") as f:
                writer.write(f)

            messagebox.showinfo("PDF generado", "La copia protegida fue generada correctamente.")
            self.status.config(text="PDF generado correctamente")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF.\n\n{e}")
        finally:
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass

    def generate_jpg(self):
        try:
            front, back = self.get_output_images()
        except ValueError as e:
            messagebox.showwarning("Faltan datos", str(e))
            return

        front_path = filedialog.asksaveasfilename(
            title="Guardar JPG del frente",
            defaultextension=".jpg",
            initialfile="DNIProtegido_Frente.jpg",
            filetypes=[("Imagen JPG", "*.jpg *.jpeg")]
        )
        if not front_path:
            return

        back_path = filedialog.asksaveasfilename(
            title="Guardar JPG del dorso",
            defaultextension=".jpg",
            initialfile="DNIProtegido_Dorso.jpg",
            filetypes=[("Imagen JPG", "*.jpg *.jpeg")]
        )
        if not back_path:
            return

        front.save(front_path, "JPEG", quality=95, optimize=True)
        back.save(back_path, "JPEG", quality=95, optimize=True)

        messagebox.showinfo(
            "JPG generados",
            f"Se generaron:\n\n{front_path}\n{back_path}"
        )
        self.status.config(text="JPG generados correctamente")

    def safe_name(self, text):
        result = []
        for c in text:
            if c.isalnum() or c in "-_":
                result.append(c)
            elif c.isspace():
                result.append("_")
        return "".join(result)[:50] or "destinatario"

    def clear_all(self):
        self.front_img = None
        self.back_img = None
        self.front_history = []
        self.back_history = []

        self.front_name.config(text="Sin archivo seleccionado")
        self.back_name.config(text="Sin archivo seleccionado")

        self.recipient.set("")
        self.date.set(datetime.now().strftime("%d/%m/%Y"))

        self.password_enabled.set(False)
        self.password.set("")
        self.toggle_password()

        self.update_live_previews()
        self.status.config(text="Todo limpio")


if __name__ == "__main__":
    root = tk.Tk()
    ProtegerDNIApp(root)
    root.mainloop()
