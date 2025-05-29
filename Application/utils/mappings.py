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
    1: "Borrow_date",
    2: "EquipmentID",
    3: "BorrowerID",
    4: "ProfessorID",
    5: "State",
    6: "Quantity"
}

SORT_FIELDS_RETURNED = {
    0: "Return_date",
    1: "Return_date",
    2: "EquipmentID",
    3: "BorrowerID",
    4: "ProfessorID",
    5: "State",
    6: "Quantity"
}

SORT_FIELDS_REPLACED = {
    0: "Replacement_date",
    1: "Replacement_date",
    2: "EquipmentID",
    3: "BorrowerID",
    4: "ProfessorID",
    5: "Quantity"
}

SORT_FIELDS_BORROWER = {
    0: "BorrowerID",
    1: "BorrowerID",
    2: "FirstName",
    3: "LastName",
    4: "Program",
    5: "YearLevel"
}

SORT_FIELDS_EQUIPMENT = {
    0: "EquipmentID",
    1: "EquipmentID",
    2: "Equipment_name",
    3: "Category",
    4: "Available"
}

SORT_FIELDS_PROFESSOR = {
    0: "ProfessorID",
    1: "ProfessorID",
    2: "FirstName",
    3: "LastName"
}

CATEGORY_MAP = {
    0: None,
    1: "Measuring & Observation Tools",
    2: "Glassware & Containers",
    3: "Heating & Mixing Equipment",
    4: "Biology-Specific Tools",
    5: "Physics & Electronics",
    6: "Miscellaneous Lab Tools"
}