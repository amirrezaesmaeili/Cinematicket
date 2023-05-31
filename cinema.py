import json
import datetime
from users import User
import logging

logger = logging.getLogger("CinemaLogger")
logger.setLevel(level=logging.INFO)
file_handler = logging.FileHandler("cinematicket.log")
pattern = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(pattern)
logger.addHandler(file_handler)

class MyException(Exception):
    pass

class Cinema:
    id_counter = 0
    sans={}
    def __init__(self,film_name: str,film_genre: str,film_play_time: str, film_age_category: int, capacity: int,ticket_price: float):
        Cinema.id_counter += 1
        self.id = Cinema.id_counter
        self.film_name = film_name
        self.film_genre = film_genre
        self.film_play_time = film_play_time
        self.film_age_category = film_age_category
        self.capacity = capacity
        self.ticket_price = ticket_price
        
    def save_sans_to_file(self):
        with open("Cinema_sans.json","w",encoding="utf_8") as file:
            sans_data = {
                "id" : self.id,
                "film_name": self.film_name,
                "film_genre": self.film_genre,
                "film_play_time": self.film_paly_time,
                "film_age_category": self.film_age_category,
                "capacity": self.capacity,
                "ticket_price":self.ticket_price,
            }
            Cinema.sans[self.film_name] = sans_data
            json.dump(Cinema.sans,file,indent=4)
            logger.info("save_sans_to_file;  Cinema sans saved to the file.")
            
    @classmethod
    def load_sans_from_file(cls):
        try:
            with open("Cinema_sans.json","r",encoding="utf_8") as file:
                Cinema.sans = json.load(file)
                logger.info("load_sans_from_file/ try;  Cinema sans loaded from the file.")
                
        except FileNotFoundError:
            Cinema.sans = {}
            logger.info("load_sans_from_file/ except;  empty Cinema sans dictionary created.") 
            
    @classmethod
    def create_sans(cls,film_name: str,film_genre: str,film_play_time: str, film_age_category: int, capacity: int,ticket_price: float):
        try:
                cinema_sans = cls(film_name,film_genre,film_play_time,film_age_category,capacity)
                cinema_sans.save_sans_to_file()
                logger.info("create_sans/ try; Sans created successfully.")
                return f"\n>>>>  Sans created successfully. <<<<\n"
        except ValueError as Err:
            logger.error("create_sans/ except; return value error")
            return str(Err)

    @classmethod
    def get_all_sans(cls):
        cls.load_sans_from_file()
        logger.info("get_all_sans;  called load_sans_from_file function.")
        return list(cls.sans.values())            

    def can_reserve_sans(self, film_play_time: str, capacity: int) -> bool:
        """
        Check if the user can reserve a session.
        """
        film_play_time = datetime.datetime.strptime(film_play_time, "%H:%M").time()
        film_formatted_time = film_play_time.strftime("%H:%M")
        current_time = datetime.datetime.now()
        current_formatted_time = current_time.strftime("%H:%M")
        if film_formatted_time < current_formatted_time:
            logger.error("can_reserve_sans/ if film;  raied my exception error: Session time has passed.")
            raise MyException("Session time has passed.")
        if capacity is not None and capacity <= 0:
            logger.error("can_reserve_sans/ if capacity;  raied my exception error: Theater capacity is full.")
            raise MyException("Theater capacity is full.")
        if self.film_age_category > User.user_age():
            logger.error("can_reserve_sans/ if self;  raied my exception error: You are not allowed to reserve or watch this film.")
            raise MyException("You are not allowed to reserve or watch this film.")
        logger.error("can_reserve_sans; returned True.")
        return True