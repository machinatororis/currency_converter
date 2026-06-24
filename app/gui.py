import requests
import customtkinter as ctk
from tkinter import messagebox

from app.api import convert_currency, get_currency_list
from app.config import API_KEY
from app.i18n import get_text


class CurrencyConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.language = "en"
        self.currencies = []

        self.title(self.t("app_title"))
        self.geometry("320x350")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        if not API_KEY:
            messagebox.showerror(self.t("error"), self.t("api_key_missing"))
            self.destroy()
            return

        try:
            self.currencies = get_currency_list(API_KEY)
        except requests.RequestException:
            messagebox.showerror(self.t("error"), self.t("currency_list_error"))
            self.currencies = []

        if self.currencies is None:
            messagebox.showerror(self.t("error"), self.t("currency_list_error"))
            self.currencies = []

        self.create_widgets()

    def t(self, key):
        return get_text(self.language, key)

    def create_widgets(self):
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.language_button = ctk.CTkButton(
            self.frame,
            text=self.t("language_button"),
            width=70,
            command=self.switch_language
        )
        self.language_button.pack(anchor="e", padx=5, pady=(10, 5))

        self.amount_label = ctk.CTkLabel(self.frame, text=self.t("amount"))
        self.amount_label.pack(anchor="w")

        self.amount_entry = ctk.CTkEntry(self.frame)
        self.amount_entry.pack(fill="x", padx=5, pady=2)

        self.base_currency_label = ctk.CTkLabel(
            self.frame,
            text=self.t("from_currency")
        )
        self.base_currency_label.pack(anchor="w")

        self.base_currency_var = ctk.StringVar(value="USD")
        self.base_currency_button = ctk.CTkButton(
            self.frame,
            textvariable=self.base_currency_var,
            command=lambda: self.open_currency_selector(self.base_currency_var)
        )
        self.base_currency_button.pack(fill="x", padx=5, pady=2)

        self.target_currency_label = ctk.CTkLabel(
            self.frame,
            text=self.t("to_currency")
        )
        self.target_currency_label.pack(anchor="w")

        self.target_currency_var = ctk.StringVar(value="EUR")
        self.target_currency_button = ctk.CTkButton(
            self.frame,
            textvariable=self.target_currency_var,
            command=lambda: self.open_currency_selector(self.target_currency_var)
        )
        self.target_currency_button.pack(fill="x", padx=5, pady=10)

        self.convert_button = ctk.CTkButton(
            self.frame,
            text=self.t("convert"),
            command=self.handle_convert
        )
        self.convert_button.pack(fill="x", padx=5, pady=5)

        self.result_label = ctk.CTkLabel(self.frame, text="", font=("Arial", 14))
        self.result_label.pack(anchor="w", padx=5, pady=5)

    def switch_language(self):
        if self.language == "en":
            self.language = "ru"
        else:
            self.language = "en"

        self.update_language()

    def update_language(self):
        self.title(self.t("app_title"))

        self.amount_label.configure(text=self.t("amount"))
        self.base_currency_label.configure(text=self.t("from_currency"))
        self.target_currency_label.configure(text=self.t("to_currency"))
        self.convert_button.configure(text=self.t("convert"))
        self.language_button.configure(text=self.t("language_button"))

    def open_currency_selector(self, currency_var):
        selector = ctk.CTkToplevel(self)
        selector.title(self.t("select_currency"))
        selector.geometry("200x300")

        scroll_frame = ctk.CTkScrollableFrame(selector)
        scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        for currency in self.currencies:
            button = ctk.CTkButton(
                scroll_frame,
                text=currency,
                command=lambda c=currency, window=selector: self.set_currency(
                    currency_var,
                    c,
                    window
                )
            )
            button.pack(fill="x", pady=2)

    def set_currency(self, currency_var, currency, window=None):
        currency_var.set(currency)

        if window:
            window.destroy()

    def handle_convert(self):
        base_currency = self.base_currency_var.get()
        target_currency = self.target_currency_var.get()
        amount_text = self.amount_entry.get().replace(",", ".")

        if not self.is_valid_amount(amount_text):
            messagebox.showerror(self.t("error"), self.t("invalid_amount"))
            return

        amount = float(amount_text)

        try:
            converted_amount = convert_currency(
                API_KEY,
                amount,
                base_currency,
                target_currency
            )
        except requests.RequestException:
            messagebox.showerror(self.t("error"), self.t("api_error"))
            return

        if converted_amount is None:
            messagebox.showerror(self.t("error"), self.t("api_error"))
            return

        self.result_label.configure(
            text=f"{amount} {base_currency} = {converted_amount:.2f} {target_currency}"
        )

    @staticmethod
    def is_valid_amount(amount_text):
        if not amount_text:
            return False

        try:
            amount = float(amount_text)
        except ValueError:
            return False

        return amount > 0