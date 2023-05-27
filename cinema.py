import json

class Cinema:
    id_counter = 0
    sans={}
    def __init__(self,id : int,film_name: str,film_genre: str,film_play_time: str, film_age_category: int, capacity: int):
        Cinema.id_counter += 1
        self.id = Cinema.id_counter
        self.film_name = film_name
        self.film_genre = film_genre
        self.film_paly_time = film_play_time
        self.film_age_category = film_age_category
        self.capacity = capacity
        
 
    
    