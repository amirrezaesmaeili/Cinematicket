import json
import os
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

  
                
