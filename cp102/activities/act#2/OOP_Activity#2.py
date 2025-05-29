# VINCENT S.

"""ACTIVITY 2: OOP"""

class Employee:

    def __init__(self, name, gender, bdate, position, rate, dayswork):

        self._name = name
        self._gender = gender
        self._bdate = bdate
        self._position = position
        self._rate = rate
        self._dayswork = dayswork

    """GETTERS"""
    def get_name(self):
        return self._name
    def get_gender(self):
        return self._gender
    def get_bdate(self):
        return self._bdate
    def get_position(self):
        return self._position
    def get_rate(self):
        return self._rate
    def get_dayswork(self):
        return self._dayswork

    """SETTERS"""
    def set_name(self, name):
        self._name = name
    def set_gender(self, gender):
        self._gender = gender
    def set_bdate(self, bdate):
        self._bdate = bdate
    def set_position(self, position):
        self._position = position
    def set_rate(self,rate):
        self._rate = rate
    def set_dayswork(self, dayswork):
        self._dayswork = dayswork


    def get_gross(self):
        gross = self._dayswork * self._rate
        return gross

    def get_sss(self):
        gross = self.get_gross()

        if gross < 10000:
            return 500

        elif gross < 20000:
            return 1000

        else:
            return 1500

    def get_tax(self):
        gross = self.get_gross()

        if gross < 10000:
            return 0
        elif gross < 20000:
            return 0.10 * gross
        elif gross <= 30000:
            return 0.20 * gross
        else:
            return 0.25 * gross

    def get_netsalary(self):

        net = self.get_gross() - self.get_sss() - self.get_tax()
        return net

    def get_employee_details(self):
        print("\nEmployee Details:")
        print(f"\nName: {self.get_name()}")
        print(f"Gender: {self.get_gender()}")
        print(f"Birth Date: {self.get_bdate()}")
        print(f"Position: {self.get_position()}")


if __name__ == "__main__":
    name = input("Enter Employee Name: ")
    gender = input("Enter Gender (M/F): ")
    bdate = input("Enter Birthdate (MM-DD-YYYY): ")
    position = input("Enter Position: ")
    rate = float(input("Enter Rate per Day: "))
    dayswork = int(input("Enter Days Worked: "))

    employee = Employee(name, gender, bdate, position, rate, dayswork)

    employee.get_employee_details()

    print("\nSalary Details:")
    print(f"\nGross Salary: P {employee.get_gross():,.2f}")
    print(f"SSS: P {employee.get_sss():,.2f}")
    print(f"Tax: P {employee.get_tax():,.2f}")
    print(f"Net Salary: P {employee.get_netsalary():,.2f}")