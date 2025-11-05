import tkinter as tk
import requests
from datetime import datetime

# Klasa obsługująca konwerter walut
class CurrencyConverter:
    def __init__(self):
        self.rates = {}  # Słownik przechowujący kursy walut
        self.update_rates()  # Aktualizacja kursów po utworzeniu instancji

    # Metoda aktualizująca kursy walut z API
    def update_rates(self):
        try:
            response = requests.get("https://api.exchangerate-api.com/v4/latest/PLN")
            data = response.json()
            self.rates = data["rates"]
        except Exception as e:
            # Obsługa wyjątku w przypadku niepowodzenia aktualizacji kursów
            self.error_label.config(text="Nie udało się zaktualizować kursów: " + str(e))

    # Metoda przeliczająca waluty
    def convert(self, amount, from_currency, to_currency):
        if from_currency == to_currency:
            return amount
        if not self.rates:
            self.error_label.config(text="Kursy nie są dostępne.")
            return None
        if from_currency not in self.rates or to_currency not in self.rates:
            self.error_label.config(text="Waluta nie jest obsługiwana.")
            return None

        from_rate = self.rates[from_currency]
        to_rate = self.rates[to_currency]

        converted_amount = amount * (to_rate / from_rate)
        self.result_label.config(text=f"{amount} {from_currency} jest równe {converted_amount:.2f} {to_currency}")

    # Metoda wyświetlająca aktualne kursy walut
    def display_rates(self):
        rates_str = "Kursy walut na dzień " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n"
        popular_currencies = ["PLN", "USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "SEK", "NZD", "MXN", "SGD",
                              "HKD", "NOK", "KRW", "TRY", "RUB", "INR", "BRL", "ZAR"]
        currency_names = {
            "PLN": "Polski Złoty",
            "USD": "Dolar Amerykański",
            "EUR": "Euro",
            "GBP": "Funt Brytyjski",
            "JPY": "Jen Japoński",
            "CAD": "Dolar Kanadyjski",
            "AUD": "Dolar Australijski",
            "CHF": "Frank Szwajcarski",
            "CNY": "Juan Chiński",
            "SEK": "Korona Szwedzka",
            "NZD": "Dolar Nowozelandzki",
            "MXN": "Peso Meksykańskie",
            "SGD": "Dolar Singapurski",
            "HKD": "Dolar Hongkoński",
            "NOK": "Korona Norweska",
            "KRW": "Won Południowokoreański",
            "TRY": "Lira Turecka",
            "RUB": "Rubel Rosyjski",
            "INR": "Rupia Indyjska",
            "BRL": "Real Brazylijski",
            "ZAR": "Rand Południowoafrykański"
        }
        for currency in popular_currencies:
            if currency in self.rates:
                rates_str += f"{currency} ({currency_names[currency]}): {self.rates[currency]:.2f}\n"
        self.result_label.config(text=rates_str)

# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.title("Konwerter Walut")

# Utworzenie instancji klasy CurrencyConverter
converter = CurrencyConverter()

# Etykiety i pola do wprowadzania danych
tk.Label(root, text="Kwota:").grid(row=0, column=0)
entry_amount = tk.Entry(root)
entry_amount.grid(row=0, column=1)

tk.Label(root, text="Z waluty:").grid(row=1, column=0)
entry_from_currency = tk.Entry(root)
entry_from_currency.grid(row=1, column=1)

tk.Label(root, text="Na walutę:").grid(row=2, column=0)
entry_to_currency = tk.Entry(root)
entry_to_currency.grid(row=2, column=1)

# Etykieta do wyświetlania błędów
converter.error_label = tk.Label(root, fg="red")
converter.error_label.grid(row=3, column=0, columnspan=2)

# Etykieta do wyświetlania wyniku konwersji
converter.result_label = tk.Label(root)
converter.result_label.grid(row=4, column=0, columnspan=2)

# Przyciski do przeliczania i wyświetlania kursów
convert_button = tk.Button(root, text="Przelicz", command=lambda: converter.convert(float(entry_amount.get()), entry_from_currency.get().upper(), entry_to_currency.get().upper()))
convert_button.grid(row=5, column=0, columnspan=2, pady=5)

display_button = tk.Button(root, text="Wyświetl Kursy", command=converter.display_rates)
display_button.grid(row=6, column=0, columnspan=2, pady=5)

# Uruchomienie głównej pętli programu
root.mainloop()