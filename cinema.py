import json
import datetime
import logging
from users import User

logger = logging.getLogger("CinemaLogger")
logger.setLevel(level=logging.INFO)
file_handler = logging.FileHandler("cinematicket.log")
pattern = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(pattern)
logger.addHandler(file_handler)


class MyException(Exception):
    pass


class Subscription:
    BRONZE = "bronze"
    SILVER = "silver"
    GOLDEN = "golden"


class subs:
    subscriptions = {
        Subscription.BRONZE: {
            "name": "Bronze",
            "description": "It is a simple and default basic service that exists for every user at the beginning and does not have special privileges."
        },
        Subscription.SILVER: {
            "name": "Silver",
            "description": "This service returns 20% of the amount of each transaction to his wallet for up to 3 future purchases."
        },
        Subscription.GOLDEN: {
            "name": "Golden",
            "description": "This service gives 50% of the amount plus a free energy drink for the next month."
        }
    }

    def __init__(self, subscription_type: str = Subscription.BRONZE):
        self.subscription_type = subscription_type
        self.wallet = 0.0

    def subscribe(self, subscription_type: str):
        """
        Subscribe the user to a new subscription type.

        Args:
            subscription_type : The new subscription type.

        Raises:
            MyException: If the subscription type is invalid.

        """
        if subscription_type not in subs.subscriptions:
            raise MyException("Invalid subscription type.")

        self.subscription_type = subscription_type
        logger.info(f"User {self} subscribed to {subscription_type} subscription.")

    def get_subscription_name(self) -> str:
        """Return the name of the user's current subscription."""
        return subs.subscriptions[self.subscription_type]["name"]

    def get_subscription_description(self) -> str:
        """Return the description of the user's current subscription."""
        return subs.subscriptions[self.subscription_type]["description"]

    def add_to_wallet(self, amount: float):
        """
        Add an amount to the user's wallet.

        Args:
            The amount to add to the wallet.

        """
        self.wallet += amount

    def get_discounted_price(self, ticket_price: float) -> float:
        """
        Calculate the discounted price based on the user's subscription.

        Args:
            ticket_price : The original ticket price.

        Returns:
            The discounted price.

        """
        if self.subscription_type == Subscription.SILVER:
            discount_amount = ticket_price * 0.2
            self.add_to_wallet(discount_amount)
            logger.info(f"User {self} received {discount_amount} discount to the wallet.")
            return ticket_price - discount_amount
        elif self.subscription_type == Subscription.GOLDEN:
            discount_amount = ticket_price * 0.5
            self.add_to_wallet(discount_amount)
            logger.info(f"User {self} received {discount_amount} discount to the wallet.")
            return 0.0
        else:
            return ticket_price

    def make_purchase(self, ticket_price: float):
        """
        Make a purchase with the user's wallet.

        Args:
            The ticket price.

        """
        discounted_price = self.get_discounted_price(ticket_price)
        if discounted_price > 0.0:
            logger.info(f"User {self} made a purchase of {discounted_price}.")


class Cinema:
    id_counter = 0
    sans = {}

    def __init__(self, film_name: str, film_genre: str, film_play_time: str, film_age_category: int, capacity: int, ticket_price: float):
        Cinema.id_counter += 1
        self.id = Cinema.id_counter
        self.film_name = film_name
        self.film_genre = film_genre
        self.film_play_time = film_play_time
        self.film_age_category = film_age_category
        self.capacity = capacity
        self.ticket_price = ticket_price

    def save_sans_to_file(self):
        """
        Save the cinema session to a JSON file.
        """
        with open("Cinema_sans.json", "w", encoding="utf_8") as file:
            sans_data = {
                "id": self.id,
                "film_name": self.film_name,
                "film_genre": self.film_genre,
                "film_play_time": self.film_play_time,
                "film_age_category": self.film_age_category,
                "capacity": self.capacity,
                "ticket_price": self.ticket_price,
            }
            Cinema.sans[self.film_name] = sans_data
            json.dump(Cinema.sans, file, indent=4)
            logger.info("save_sans_to_file; Cinema sans saved to the file.")

    @classmethod
    def load_sans_from_file(cls):
        """
        Load the cinema sessions from the JSON file.
        """
        try:
            with open("Cinema_sans.json", "r", encoding="utf_8") as file:
                Cinema.sans = json.load(file)
                logger.info("load_sans_from_file/ try; Cinema sans loaded from the file.")

        except FileNotFoundError:
            Cinema.sans = {}
            logger.info("load_sans_from_file/ except; empty Cinema sans dictionary created.")

    @classmethod
    def create_sans(cls, film_name: str, film_genre: str, film_play_time: str, film_age_category: int, capacity: int, ticket_price: float):
        """
        Create a new cinema session.

        Args:
            film_name : The name of the film.
            film_genre : The genre of the film.
            film_play_time : The play time of the film.
            film_age_category : The age category of the film.
            capacity : The capacity of the cinema.
            ticket_price : The ticket price.


        """
        try:
            cinema_sans = cls(film_name, film_genre, film_play_time, film_age_category, capacity, ticket_price)
            cinema_sans.save_sans_to_file()
            logger.info("create_sans/ try; Sans created successfully.")
            return "\n>>>> Sans created successfully. <<<<\n"
        except ValueError as Err:
            logger.error("create_sans/ except; return value error")
            return str(Err)

    @classmethod
    def get_all_sans(cls):
        """
        Get all cinema sessions.

        Returns:
            A list of cinema sessions.

        """
        cls.load_sans_from_file()
        logger.info("get_all_sans; called load_sans_from_file function.")
        return list(cls.sans.values())

    def can_reserve_sans(self, film_play_time: str, capacity: int) -> bool:
        """
        Check if the user can reserve a session.

        Args:
            film_play_time : The play time of the film.
            capacity : The remaining capacity of the cinema.

        Returns:
            True if the user can reserve a session, False otherwise.

        Raises:
            MyException: If the session time has passed, the theater is full, or the user is not allowed to watch the film.

        """
        film_play_time = datetime.datetime.strptime(film_play_time, "%H:%M").time()
        film_formatted_time = film_play_time.strftime("%H:%M")
        current_time = datetime.datetime.now()
        current_formatted_time = current_time.strftime("%H:%M")
        if film_formatted_time < current_formatted_time:
            logger.error("can_reserve_sans/ if film; raised MyException: Session time has passed.")
            raise MyException("Session time has passed.")
        if capacity is not None and capacity <= 0:
            logger.error("can_reserve_sans/ if capacity; raised MyException: Theater capacity is full.")
            raise MyException("Theater capacity is full.")
        if self.film_age_category > User.user_age():
            logger.error("can_reserve_sans/ if self; raised MyException: You are not allowed to reserve or watch this film.")
            raise MyException("You are not allowed to reserve or watch this film.")
        logger.error("can_reserve_sans; returned True.")
        return True
