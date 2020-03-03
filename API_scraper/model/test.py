from get_id import Params
import cProfile




p = Params()



data = p.league_season()

def print_all(det):
    for i in det.items():
        print(i)



cProfile.run("print_all(data)", filename='first_iteration.cprof' )

