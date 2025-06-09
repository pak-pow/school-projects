Inventory Management System - README
Last updated: 05/10/2025 11:48 PM

[NEW NAME]: main_menu.exe -> InventoryManagement.exe

Menu:

-> View (Top Corner): Toggles between light and dark themes.
-> File (Top Corner): Exits the application.

Main Menu:

-> Manage Inventory
-> Manage Suppliers
-> Exit

Manage Inventory:

-> There are two tables in the Manage Inventory section: Items and Suppliers Contact Information.

	Tabs:
		-> Inventory
		-> Edit

		[INVENTORY] Tab:
			Max Quantity Spinbox:
				Use the spinbox to enter a number. This will filter the items and display only those with that quantity.

			Refresh Button:
				Click to refresh the table and display all available items.

		[EDIT] Tab:
			Input Boxes:
				Enter item details in the provided fields.

			Navigation Buttons:

				" > " and " < " : Navigate to the next or previous item in the table.

				" >> " and " << " : Jump to the last or first item in the table.

			Action Buttons:

				[CREATE]: Creates a new item after filling out the input fields.

				[UPDATE]: Select a row to update by clicking the "><" button, then click "Update" to modify the selected row.

				[DELETE]: Similar to the update process, select a row and click "Delete" to remove the item.


Manage Suppliers:
The logic here is the same as in the "Manage Inventory" section:
Select a row to update or delete.
Fill out the input boxes to create a new supplier or update existing information.


[GENERAL NOTE]
Make sure to refresh the table to ensure the latest data is displayed.
Actions like create, update, and delete require selecting the item from the table.

