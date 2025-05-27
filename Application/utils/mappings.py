DATE_OPTIONS = {
        1: ("HOUR", 1),
        2: ("HOUR", 3),
        3: ("DAY", 1),
        4: ("DAY", 7),
        5: ("DAY", 30),
        6: ("DAY", 90),
        7: ("DAY", 180),
    }

SORT_FIELDS_BORROWED = {
    0: "Borrow_date",
    1: "EquipmentID",
    2: "BorrowerID",
    3: "State",
    4: "Quantity"
}

SORT_FIELDS_RETURNED = {
    0: "Return_date",
    1: "EquipmentID",
    2: "BorrowerID",
    3: "State",
    4: "Quantity"
}

SORT_FIELDS_REPLACED = {
    0: "Replacement_date",
    1: "EquipmentID",
    2: "BorrowerID",
    3: "Quantity"
}

SORT_FIELDS_BORROWER = {
    0: "ProfessorID",
    1: "BorrowerID",
    2: "FirstName",
    3: "LastName",
    4: "Program",
    5: "YearLevel"
}

SORT_FIELDS_EQUIPMENT = {
    0: "EquipmentID",
    1: "Equipment_name",
    2: "Category",
    3: "Available"
}

SORT_FIELDS_PROFESSOR = {
    0: "ProfessorID",
    1: "FirstName",
    2: "LastName"
}