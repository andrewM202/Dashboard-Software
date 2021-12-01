from dataclasses import dataclass
from news_sites.new_york_times.seed_db_newyorktimes import main as seed_nyt
from news_sites.zerohedge.seed_db_zerohedge import main as  seed_zerohedge
from news_sites.the_guardian.seed_db_the_guardian import main as seed_the_guardian

@dataclass
class Seed_DB():
    @staticmethod
    def new_york_times(month, year):
        print("Seeding The New York Times.\n")
        seed_nyt(month, year)

    @staticmethod
    def the_guardian(month, year):
        print("Seeding The Guardian.\n")
        seed_the_guardian()

    @staticmethod
    def zerohedge(month, year):
        print("Seeding Zerohedge.\n")
        seed_zerohedge()

def main():
    db = Seed_DB()
    col = None
    month = None
    year = None
    while col not in [1, 2, 3]:
        col = int(input("""
Which collection in DB do you want to seed?
1. The New York Times 
2. The Guardian 
3. Zerohedge

> """))

    while month not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        month = int(input("""
Which month do you want to seed?
1 = January,   2  = February, 3 = March,     4 = April,
5 = May,       6  = June,     7 = July,      8 = August,  
9 = September, 10 = October, 11 = November, 12 = December      

> """))

    while year is None:
        year = int(input("""
Which year do you want to seed?    

> """))

    if   col == 1: db.new_york_times(month, year)
    elif col == 2: db.the_guardian(month, year)
    elif col == 3: db.zerohedge(month, year)

if __name__ == "__main__":
    main()
