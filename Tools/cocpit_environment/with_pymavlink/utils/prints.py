import sys
from time import sleep
from colorama import init, Fore, Style


def cool_print():
        print("""
╔════════════════════════╗
║   Welcome to Drone Gym ║
╚════════════════════════╝
* by moshe braunshtein ! *
            """)
        sleep(2)

def reminder_print():
        print("""
        set parameters values in "sitl parameters list":
            - angle_max
            - sim_rate 
            - msg mavlink rate
            - vehicle parameters
        """)

def report_to_file(episode_N, angle_of_attack,total_penalty,steps,time):    
    filename = "/ardupilot/Tools/cocpit_environment/with_pymavlink/saved_data/reports/output.txt"
    with open(filename, "a") as file:
        sys.stdout = file  # Redirect standard output to the file
        print(f"""
    ╔════════════════════════╗
    ║   report {episode_N}         ║
    ╚════════════════════════╝
                """)
        print("{:15} {:<20} {:<15} {:<15} {:<15}".format("Episode","Angle of Attack", "Total penalty", "Steps","time"))
        print("="*60)
        print("{:<15} {:<20} {:<15} {:<15} {:<15} ".format(episode_N, angle_of_attack, total_penalty, steps, time))
        sys.stdout = sys.__stdout__  # Reset standard output to the console

        print(f"""{Fore.GREEN}
    ╔════════════════════════╗
    ║   episode {episode_N} reported to file       ║
    ╚════════════════════════╝
                {Style.RESET_ALL}""")