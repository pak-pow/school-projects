import csv
import os
import time
import datetime

class AttendanceSystem:
    FILE_NAME = "attendance.csv"
    HISTORY_EDIT = "edit_history.csv"
    HISTORY_DELETE = "delete_history.csv"

    def __init__(self):
        self.init_file()

    def init_file(self):
        if not os.path.exists(self.FILE_NAME):
            print("Creating file...")
            time.sleep(2)
            print("File has been created.\n")
            time.sleep(2)

            with open(self.FILE_NAME, 'w', newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["Name", "Time-in", "Time-out", "Duration"])
                writer.writeheader()
        else:
            print("File already exists\n")
            time.sleep(1)

        for history_file in [self.HISTORY_EDIT, self.HISTORY_DELETE]:
            if not os.path.exists(history_file):
                with open(history_file, 'w', newline="") as f:
                    if "edit" in history_file:
                        fieldnames = ["Timestamp", "Name", "Field Edited", "Old Value", "New Value"]
                    else:
                        fieldnames = ["Timestamp", "Name", "Deleted Record"]
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()

    def read_record(self):
        with open(self.FILE_NAME, 'r') as f:
            return list(csv.DictReader(f))

    def write_record(self, records):
        with open(self.FILE_NAME, 'w', newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["Name", "Time-in", "Time-out", "Duration"])
            writer.writeheader()
            writer.writerows(records)

    def log_edit_history(self, name, field, old_value, new_value):
        """Log the edit history to edit_history.csv."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.HISTORY_EDIT, 'a', newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["Timestamp", "Name", "Field Edited", "Old Value", "New Value"])
            writer.writerow({
                "Timestamp": timestamp,
                "Name": name,
                "Field Edited": field,
                "Old Value": old_value,
                "New Value": new_value
            })

    def log_delete_history(self, name, deleted_record):
        """Log the deletion history to delete_history.csv."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.HISTORY_DELETE, 'a', newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["Timestamp", "Name", "Deleted Record"])
            writer.writerow({
                "Timestamp": timestamp,
                "Name": name,
                "Deleted Record": str(deleted_record)
            })

    def add_record(self):
        get_name = input("Enter name: ").strip().title()
        time_now = datetime.datetime.now()
        now_str = time_now.strftime("%Y-%m-%d %H:%M:%S")
        records = self.read_record()
        found = None

        for record in records:
            if record["Name"] == get_name and record["Time-out"] == "":
                found = record
                break

        if found is not None:
            time_in = datetime.datetime.strptime(found["Time-in"], "%Y-%m-%d %H:%M:%S")
            duration = time_now - time_in
            hours = duration.seconds // 3600
            minutes = (duration.seconds % 3600) // 60

            found["Time-out"] = now_str
            found["Duration"] = f"{hours}h {minutes}m"

            print(f"Time-out recorded at {now_str} | Duration: {found['Duration']}\n")
            time.sleep(2)
        else:
            new_record = {"Name": get_name, "Time-in": now_str, "Time-out": "", "Duration": ""}
            records.append(new_record)
            print("Time-in recorded at", now_str + '\n')
            time.sleep(2)

        self.write_record(records)

    def list_record(self):
        records = self.read_record()
        print("Listing Records...")
        time.sleep(1)

        print("---------" * 6)
        print("Name | Time-in | Time-out | Duration")
        for record in records:
            print(f"{record['Name']}: {record['Time-in']} - {record['Time-out']} | {record['Duration']}")
        print("---------" * 6)
        time.sleep(2)

    def edit_record(self):
        get_name = input("Enter your name for editing: ").strip().title()
        records = self.read_record()
        user_record = [record for record in records if record['Name'] == get_name]

        if not user_record:
            print(f"No records for {get_name}\n")
            time.sleep(2)
            return

        for i, r in enumerate(user_record, 1):
            print(f"{i}: {r}")

        record_number = int(input("Enter a number to edit: "))
        record = user_record[record_number - 1]
        index = records.index(record)

        print("Select field to edit: 1-Name, 2-Time-in, 3-Time-out")
        field_choice = int(input("Enter a field to edit: "))
        fields = ["Name", "Time-in", "Time-out"]
        field = fields[field_choice - 1]
        old_value = records[index][field]

        new_value = input(f"Enter a new value for {field} (current: {old_value}): ").strip().title() or old_value
        records[index][field] = new_value

        # If editing time fields, recalculate duration if both times are present.
        if field in ["Time-in", "Time-out"]:
            t_in = records[index]["Time-in"]
            t_out = records[index]["Time-out"]
            if t_in and t_out:
                t_in_dt = datetime.datetime.strptime(t_in, "%Y-%m-%d %H:%M:%S")
                t_out_dt = datetime.datetime.strptime(t_out, "%Y-%m-%d %H:%M:%S")
                duration = t_out_dt - t_in_dt
                hours = duration.seconds // 3600
                minutes = (duration.seconds % 3600) // 60
                records[index]["Duration"] = f"{hours}h {minutes}m"

        # Log the edit if the value has changed.
        if new_value != old_value:
            self.log_edit_history(get_name, field, old_value, new_value)

        self.write_record(records)
        print("Record Updated Successfully!\n")
        time.sleep(2)

    def delete_record(self):
        get_name = input("Enter the name for deletion: ").strip().title()
        records = self.read_record()
        user_record = [record for record in records if record['Name'] == get_name]

        if not user_record:
            print(f"No records for {get_name}\n")
            time.sleep(2)
            return

        for i, r in enumerate(user_record, 1):
            print(f"{i}: {r}")

        print("---------" * 6)
        record_number = int(input("Enter the record number for deletion: "))
        record = user_record[record_number - 1]

        # Log the deletion before removing the record.
        self.log_delete_history(get_name, record)

        records.remove(record)
        self.write_record(records)
        print("Record deleted successfully!")
        print("---------" * 6 + "\n")
        time.sleep(2)

    def main(self):
        while True:
            print("Welcome to Employee Clock System (Clock in and out)!")
            print("\n\t1. Clock-In/Clock-Out")
            print("\t2. Edit a Record")
            print("\t3. List all Records")
            print("\t4. Delete A Record")
            print("\t5. Exit")

            choice = int(input("\nEnter your choice(1-5): ").strip())

            if choice == 1:
                self.add_record()
            elif choice == 2:
                self.edit_record()
            elif choice == 3:
                self.list_record()
            elif choice == 4:
                self.delete_record()
            elif choice == 5:
                print("Exiting...")
                time.sleep(2)
                print("Thank you for using this system!")
                break
            else:
                print("Invalid choice!")
                time.sleep(1)

if __name__ == "__main__":
    AttendanceSystem().main()
