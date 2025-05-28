from .fetchData import fetchEquipmentIds, fetchEquipmentName

def generate_equipment_id(category_id_strip, equipment_name):
    
    # if name exists return but pwede ra ni i check before i call ang func
    if equipment_name.strip().lower() in (name.lower() for name in fetchEquipmentName()):
        return None
    
    existing_ids = fetchEquipmentIds()
    
    category = category_id_strip.strip().upper()[:3]
    equipment_type = equipment_name.strip().upper()[:3]
     
    prefix = f"{category}-{equipment_type}"
    
    # matching ids of ABC-DEF
    matching_ids = [id for id in existing_ids if id.startswith(prefix)]
    
    # get highest existing number
    max_num = 1 #default
    for id in matching_ids:
        num_part = id.split("-")[-1]  # Ex. extract "001" from "GLA-BEA-001"
        try:
            num = int(num_part)
            max_num = max(max_num, num)
        except ValueError:
            pass
    
    new_id = f"{prefix}-{max_num + 1:03d}"
    return new_id

# testing
existing_names = fetchEquipmentName()
print("Existing names:", existing_names)

id = generate_equipment_id("GLA", "Graduated Cylinder 10mL")
print(id)
