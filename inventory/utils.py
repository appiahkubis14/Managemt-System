
from django.db import models

# Item Categories
class ItemCategory(models.TextChoices):
    # 🚗 Vehicles & Transport
    TRUCKS = "Trucks", "Trucks"
    TRAILERS = "Trailers", "Trailers"
    PICKUP_TRUCKS = "Pickup Trucks", "Pickup Trucks"
    CONTAINER_CARRIERS = "Container Carriers", "Container Carriers"
    HEAVY_DUTY_EQUIPMENT = "Heavy Duty Equipment", "Heavy Duty Equipment"
    TANKERS = "Tankers", "Tankers"
    DUMP_TRUCKS = "Dump Trucks", "Dump Trucks"
    FLATBED_TRUCKS = "Flatbed Trucks", "Flatbed Trucks"

    # 🚐 Light & Medium Vehicles
    VANS = "Vans", "Vans"
    MINIVANS = "Minivans", "Minivans"
    PANEL_VANS = "Panel Vans", "Panel Vans"
    REFRIGERATED_VANS = "Refrigerated Vans", "Refrigerated Vans"
    BUSES = "Buses", "Buses"
    MINIBUSES = "Minibuses", "Minibuses"
    COACHES = "Coaches", "Coaches"

    # 🏍️ Motorized Two & Three-Wheelers
    MOTORCYCLES = "Motorcycles", "Motorcycles"
    SCOOTERS = "Scooters", "Scooters"
    TRICYCLES = "Tricycles", "Tricycles"
    AUTO_RICKSHAWS = "Auto Rickshaws", "Auto Rickshaws"

    # 🚜 Industrial & Special Vehicles
    FORKLIFTS = "Forklifts", "Forklifts"
    CRANES = "Cranes", "Cranes"
    EXCAVATORS = "Excavators", "Excavators"
    BULLDOZERS = "Bulldozers", "Bulldozers"
    ROAD_GRADERS = "Road Graders", "Road Graders"
    TOW_TRUCKS = "Tow Trucks", "Tow Trucks"
    STREET_SWEEPERS = "Street Sweepers", "Street Sweepers"
    WRECKING_TRUCKS = "Wrecking Trucks", "Wrecking Trucks"

    # 🚙 Other
    ELECTRIC_VEHICLES = "Electric Vehicles", "Electric Vehicles"
    HYBRID_VEHICLES = "Hybrid Vehicles", "Hybrid Vehicles"
    AUTONOMOUS_VEHICLES = "Autonomous Vehicles", "Autonomous Vehicles"

    # 🛢 Fuel & Fluids
    DIESEL = "Diesel", "Diesel"
    PETROL = "Petrol", "Petrol"
    CNG = "CNG", "Compressed Natural Gas"
    ENGINE_OIL = "Engine Oil", "Engine Oil"
    TRANSMISSION_FLUID = "Transmission Fluid", "Transmission Fluid"
    HYDRAULIC_OIL = "Hydraulic Oil", "Hydraulic Oil"
    COOLANTS = "Coolants", "Coolants"
    BRAKE_FLUID = "Brake Fluid", "Brake Fluid"
    GREASE = "Grease", "Grease"

    # ⚙ Spare Parts & Maintenance
    TIRES = "Tires", "Tires"
    BATTERIES = "Batteries", "Batteries"
    BRAKE_PADS = "Brake Pads", "Brake Pads"
    BRAKE_DISCS = "Brake Discs", "Brake Discs"
    CLUTCH_KITS = "Clutch Kits", "Clutch Kits"
    ALTERNATORS = "Alternators", "Alternators"
    STARTERS = "Starters", "Starters"
    BELTS = "Belts", "Belts"
    FILTERS = "Filters", "Filters"
    SPARK_PLUGS = "Spark Plugs", "Spark Plugs"
    RADIATORS = "Radiators", "Radiators"
    AIRBAGS = "Airbags", "Airbags"
    EXHAUST_SYSTEMS = "Exhaust Systems", "Exhaust Systems"
    FUEL_PUMPS = "Fuel Pumps", "Fuel Pumps"
    TRANSMISSION_SYSTEMS = "Transmission Systems", "Transmission Systems"

    # 🚚 Cargo Handling & Securing
    CARGO_STRAPS = "Cargo Straps", "Cargo Straps"
    CHAINS_AND_BINDERS = "Chains and Binders", "Chains and Binders"
    LOAD_BARS = "Load Bars", "Load Bars"
    PALLETS = "Pallets", "Pallets"
    WOODEN_CRATES = "Wooden Crates", "Wooden Crates"
    PLASTIC_CONTAINERS = "Plastic Containers", "Plastic Containers"
    METAL_CONTAINERS = "Metal Containers", "Metal Containers"
    CARGO_NETS = "Cargo Nets", "Cargo Nets"
    ROPE_AND_CORDAGE = "Rope and Cordage", "Rope and Cordage"
    DOCK_LEVELERS = "Dock Levelers", "Dock Levelers"
    RAMP_PLATES = "Ramp Plates", "Ramp Plates"
    JACKS_AND_LIFTS = "Jacks and Lifts", "Jacks and Lifts"

    # 🚦 Safety & Compliance
    REFLECTIVE_VESTS = "Reflective Vests", "Reflective Vests"
    HELMETS = "Helmets", "Helmets"
    SAFETY_GLOVES = "Safety Gloves", "Safety Gloves"
    SAFETY_GOGGLES = "Safety Goggles", "Safety Goggles"
    FIRST_AID_KITS = "First Aid Kits", "First Aid Kits"
    FIRE_EXTINGUISHERS = "Fire Extinguishers", "Fire Extinguishers"
    WARNING_TRIANGLES = "Warning Triangles", "Warning Triangles"
    EMERGENCY_LIGHTS = "Emergency Lights", "Emergency Lights"
    ROAD_CONES = "Road Cones", "Road Cones"
    SPEED_LIMIT_SIGNS = "Speed Limit Signs", "Speed Limit Signs"
    BREATHALYZERS = "Breathalyzers", "Breathalyzers"
    SEATBELTS = "Seatbelts", "Seatbelts"

    # 📡 Tracking & Communication
    GPS_DEVICES = "GPS Devices", "GPS Devices"
    TELEMATICS_SYSTEMS = "Telematics Systems", "Telematics Systems"
    DASHCAMS = "Dashcams", "Dashcams"
    TWO_WAY_RADIOS = "Two-Way Radios", "Two-Way Radios"
    MOBILE_PHONES = "Mobile Phones", "Mobile Phones"
    VEHICLE_TRACKERS = "Vehicle Trackers", "Vehicle Trackers"
    RFID_SCANNERS = "RFID Scanners", "RFID Scanners"

    # 🏢 Office & Operations
    COMPUTERS = "Computers", "Computers"
    PRINTERS = "Printers", "Printers"
    OFFICE_CHAIRS = "Office Chairs", "Office Chairs"
    DESKS = "Desks", "Desks"
    PAPER_SUPPLIES = "Paper Supplies", "Paper Supplies"
    LOGBOOKS = "Logbooks", "Logbooks"
    INVOICES_AND_RECEIPTS = "Invoices and Receipts", "Invoices and Receipts"
    BARCODE_SCANNERS = "Barcode Scanners", "Barcode Scanners"
    HANDHELD_DEVICES = "Handheld Devices", "Handheld Devices"

    # 🏗 Infrastructure & Workshop Equipment
    GENERATORS = "Generators", "Generators"
    AIR_COMPRESSORS = "Air Compressors", "Air Compressors"
    TOOLBOXES = "Toolboxes", "Toolboxes"
    POWER_TOOLS = "Power Tools", "Power Tools"
    WELDING_EQUIPMENT = "Welding Equipment", "Welding Equipment"
    MECHANIC_TOOLS = "Mechanic Tools", "Mechanic Tools"
    LADDER_AND_STAIRS = "Ladder and Stairs", "Ladder and Stairs"
    STORAGE_SHELVES = "Storage Shelves", "Storage Shelves"
    LIGHTING_EQUIPMENT = "Lighting Equipment", "Lighting Equipment"

    # 🏭 Warehouse & Logistics Equipment
    WAREHOUSE_RACKS = "Warehouse Racks", "Warehouse Racks"
    HAND_TRUCKS = "Hand Trucks", "Hand Trucks"
    PALLET_JACKS = "Pallet Jacks", "Pallet Jacks"
    FORKLIFT_BATTERIES = "Forklift Batteries", "Forklift Batteries"
    CONVEYOR_BELTS = "Conveyor Belts", "Conveyor Belts"
    BARCODE_LABELS = "Barcode Labels", "Barcode Labels"
    INDUSTRIAL_SCALES = "Industrial Scales", "Industrial Scales"
    LOADING_DOCK_SEALS = "Loading Dock Seals", "Loading Dock Seals"

    # 🚧 Roadside Assistance & Recovery
    TOWING_CHAINS = "Towing Chains", "Towing Chains"
    WINCHES = "Winches", "Winches"
    SPARE_TIRES = "Spare Tires", "Spare Tires"
    PORTABLE_BATTERY_BOOSTERS = "Portable Battery Boosters", "Portable Battery Boosters"
    TOOL_KITS = "Tool Kits", "Tool Kits"
    ROADSIDE_REFLECTORS = "Roadside Reflectors", "Roadside Reflectors"
    JUMP_START_CABLES = "Jump Start Cables", "Jump Start Cables"
    PORTABLE_FUEL_CONTAINERS = "Portable Fuel Containers", "Portable Fuel Containers"
    # FUEL_PUMPS = "Fuel Pumps", "Fuel Pumps"

    # ❄ Temperature-Controlled Transport
    REFRIGERATED_CONTAINERS = "Refrigerated Containers", "Refrigerated Containers"
    TEMPERATURE_MONITORS = "Temperature Monitors", "Temperature Monitors"
    INSULATED_COVERINGS = "Insulated Coverings", "Insulated Coverings"

    # 🛑 Others
    MISCELLANEOUS = "Miscellaneous", "Miscellaneous"
