# 📦 Inventory Management System

**Last Updated:** 05/10/2025 – 11:48 PM  
**Executable Name:** `InventoryManagement.exe` (previously `main_menu.exe`)

---

## 🗂️ Menu Overview

### 🔍 View (Top Menu)
- Toggle between **Light** and **Dark** themes.

### 📁 File (Top Menu)
- **Exit** the application.

---

## 🏠 Main Menu Options

- **Manage Inventory**
- **Manage Suppliers**
- **Exit**

---

## 📋 Manage Inventory

This section includes two primary tables:
- **Items**
- **Suppliers Contact Information**

### 📑 Tabs

#### 🔸 Inventory Tab
- **Max Quantity Spinbox**  
  Filter items by quantity using the spinbox.

- **Refresh Button**  
  Click to reload and display all current inventory data.

#### 🔸 Edit Tab
- **Input Fields**  
  Enter item details like name, quantity, and supplier.

- **Navigation Buttons**  
  - `>` / `<` : Go to the next or previous item.  
  - `>>` / `<<` : Jump to the last or first item.

- **Action Buttons**  
  - **[CREATE]**: Add a new item using the input fields.  
  - **[UPDATE]**: Select an item via the `><` button, modify its fields, and click **Update**.  
  - **[DELETE]**: Select an item using `><`, then click **Delete** to remove it.

---

## 🧾 Manage Suppliers

The logic here mirrors the **Manage Inventory** section:

- Use input boxes to **create** or **update** supplier information.
- Select a row in the table to **update** or **delete** a supplier.

---

## 📌 General Notes

- Always click **Refresh** after making changes to ensure the table shows the most recent data.
- To **create**, **update**, or **delete** records, make sure an item or supplier is selected from the table first.
