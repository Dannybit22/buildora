import customtkinter as ctk


class BaseForm(ctk.CTkFrame):
    def __init__(self, master, fields):
        super().__init__(master, fg_color="transparent")

        self.fields = fields
        self.inputs = {}

        self.create_form()

    def create_form(self):
        for index, field in enumerate(self.fields):
            label = ctk.CTkLabel(
                self,
                text=field["label"],
                font=("Arial", 12, "bold")
            )
            label.grid(row=index, column=0, padx=8, pady=6, sticky="w")

            if field["type"] == "entry":
                widget = ctk.CTkEntry(
                    self,
                    width=260,
                    placeholder_text=field.get("placeholder", "")
                )

            elif field["type"] == "option":
                widget = ctk.CTkOptionMenu(
                    self,
                    width=260,
                    values=field.get("values", [])
                )

            elif field["type"] == "textbox":
                widget = ctk.CTkTextbox(
                    self,
                    width=260,
                    height=70
                )

            else:
                widget = ctk.CTkEntry(self, width=260)

            widget.grid(row=index, column=1, padx=8, pady=6, sticky="w")
            self.inputs[field["name"]] = widget

    def get_data(self):
        data = {}

        for name, widget in self.inputs.items():
            if isinstance(widget, ctk.CTkTextbox):
                data[name] = widget.get("1.0", "end").strip()
            else:
                data[name] = widget.get().strip()

        return data

    def set_data(self, data):
        for name, value in data.items():
            widget = self.inputs.get(name)

            if not widget:
                continue

            value = "" if value is None else str(value)

            if isinstance(widget, ctk.CTkTextbox):
                widget.delete("1.0", "end")
                widget.insert("1.0", value)

            elif isinstance(widget, ctk.CTkOptionMenu):
                widget.set(value)

            else:
                widget.delete(0, "end")
                widget.insert(0, value)

    def clear(self):
        for field in self.fields:
            name = field["name"]
            widget = self.inputs.get(name)

            if not widget:
                continue

            if isinstance(widget, ctk.CTkTextbox):
                widget.delete("1.0", "end")

            elif isinstance(widget, ctk.CTkOptionMenu):
                values = field.get("values", [])
                if values:
                    widget.set(values[0])

            else:
                widget.delete(0, "end")