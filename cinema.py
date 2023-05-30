import json
import datetime
from users import User


class MyException(Exception):
    pass

class Cinema:
    id_counter = 0
    sans={}
    def __init__(self,film_name: str,film_genre: str,film_play_time: str, film_age_category: int, capacity: int):
        Cinema.id_counter += 1
        self.id = Cinema.id_counter
        self.film_name = film_name
        self.film_genre = film_genre
        self.film_paly_time = film_play_time
        self.film_age_category = film_age_category
        self.capacity = capacity
        
    def save_sans_to_file(self):
        with open("Cinema_sans.json","w",encoding="utf_8") as file:
            sans_data = {
                "id" : self.id,
                "film_name": self.film_name,
                "film_genre": self.film_genre,
                "film_play_time": self.film_paly_time,
                "film_age_category": self.film_age_category,
                "capacity": self.capacity
            }
            Cinema.sans[self.film_name] = sans_data
            json.dump(Cinema.sans,file,indent=4)
            
    @classmethod
    def load_sans_from_file(cls):
        try:
            with open("Cinema_sans.json","r",encoding="utf_8") as file:
                Cinema.sans = json.load(file)
                
        except FileNotFoundError:
            Cinema.sans = {}   
            
    @classmethod
    def create_sans(cls,film_name: str,film_genre: str,film_play_time: str, film_age_category: int, capacity: int):
        try:
            cinema_sans = cls(film_name,film_genre,film_play_time,film_age_category,capacity)
            cinema_sans.save_sans_to_file()
            return "\n>>>>  Sans created successfully. <<<<\n"
        except ValueError as Err:
            return str(Err)

    @classmethod
    def get_all_sans(cls):
        cls.load_sans_from_file()
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
            raise MyException("Session time has passed.")
        if capacity is not None and capacity <= 0:
            raise MyException("Theater capacity is full.")
        if self.film_age_category > user_age_category:
            raise MyException("You are not allowed to reserve or watch this film.")
        return True