import os
import django
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myecom.settings")
django.setup()

# Import Product directly from your app
from myecom.models import Product   # ✅ adjust to your actual app name

class ActionShowProducts(Action):
    def name(self) -> str:
        return "action_show_products"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):
        products = Product.objects.all()[:5]
        names = [p.name for p in products]

        if names:
            dispatcher.utter_message(text=f"Here are some products: {', '.join(names)}")
        else:
            dispatcher.utter_message(text="No products found in the database.")

        return []

