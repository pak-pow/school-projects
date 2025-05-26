import pandas as pd # Gumamit po tayo ng import para magamit ang panda sa pagbasa at pagparse ng CSV FILE

""" Dito po gumawa po tayo ng function para ma-load natin ang CSV file na may collumn na 'Name' at 'Birthday' (YYYY-MM-DD) """
def load_birthdays(file_name: str) -> pd.DataFrame:
    return pd.read_csv(file_name, parse_dates=['Birthday']) # Binabasa na po ang CSV at kino-convert ang 'Birthday' column sa datetime format natin

""" Hinahanap ang unang pares na may parehong MM-DD. IMPORTANTE: Pigeonhole logic—may 365 na buckets (MM-DD), kaya kung >365 entries, siguradong may duplicate. """
def find_first_birthday_collision(df: pd.DataFrame) -> tuple[str, str, str]:

    seen: dict[str, str] = {} # Gumawa po tayo ng dictionary para ma-i-track natin ang mga naunang pangalan kada MM-DD

    for _, row in df.iterrows(): # Chinecheck po natin yung bawat line or row sa ating data frame

        name = row['Name'] # Kinokolekto po natin dito yung mga names
        mm_dd = row['Birthday'].strftime('%m-%d') # Kinuha po natin ang petsa bilang MM-DD string na magsisilbing bucket key

        """ IMPORTANTE: dito sa condition na ito ay kung ang MM-DD key ay nasa seen na pwede natin masabi na naganap na ang collision """
        if mm_dd in seen:
            return seen[mm_dd], name, mm_dd # Ibabalik po ang unang pangalan, kasalukuyang pangalan, at ang MM-DD

        seen[mm_dd] = name # Ireregister na po ang bagong MM-DD at pangalan sa dictionary

    # Kapag po walang nakita na duplication (posibleng only kung ≤365 entries)
    raise ValueError("There is no 2 person that has the same birthday. Therefore there is no collision.")

"""IMPORTANTE: User input"""
def prompt_file_name() -> str:

    while True: # Isa po to sa mga loop na hanggang walang input ang user o walang tamang input ang user, deretso parin ang program sa pag andar

        """ Humihhingi po ang system ng input nang user at sa gamit ng strip tinatanggal nya lahat ng white spaces """
        file_name = input("Enter the CSV file name (e.g., birthdays.csv): ").strip()

        try:
            with open(file_name, 'r'): # Sa gamit po ng Open() binubuksan po nya yung said csv file
                return file_name # Kapag po na kuha na yung file ibabalik napo sya as code na para mabasa nung python
        except FileNotFoundError: # Eto po ay kapag hindi po nakita yung file mag tutuloy parin (running) yung file po
            print("File not found. Please try again.")  # Magsesend po ng error message at uulit po ulet sa una

"""IMPORTANTE: Main function po nung program or parang interfaced narin po"""
def main():
    print("=== Birthday Collision Detector ===") # Header po para sa user
    file_name = prompt_file_name() # Kunin po ang filename mula sa user
    df = load_birthdays(file_name) # I-load po ang CSV data gamit ang pandas

    try:
        first, second, day = find_first_birthday_collision(df) # Dito po ay hanapin ang unang collision at kunin ang dalawang pangalan at ang araw
        print(f"Collision detected: '{first}' and '{second}' share the birthday {day}.") # I-print po ang resulta kung may natagpuang collision

    except ValueError as e: # Huhuliin po kung wala pong collision (≤365 entries)
        print(str(e)) # I-print naman po ang error message

if __name__ == "__main__": # Titingnan po kung ang script ang direktang pina-run
    main() # Sini-Simulan po ang programa sa pamamagitan ng pagtawag sa main()
