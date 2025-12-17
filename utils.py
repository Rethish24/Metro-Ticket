# utils.py

STATIONS = [
    "Miyapur", "JNTU College", "KPHB Colony", "Kukatpally", "Balanagar",
    "Moosapet", "Bharatnagar", "Erragadda", "ESI Hospital", "SR Nagar",
    "Ameerpet", "Punjagutta", "Irrum Manzil", "Khairatabad", "Lakdi Ka Pul",
    "Assembly", "Nampally", "Gandhi Bhavan", "Osmania Medical College",
    "MG Bus Station", "Malakpet", "New Market", "Musarambagh",
    "Dilsukhnagar", "Chaitanyapuri", "Victoria Memorial", "LB Nagar",
    "Nagole", "Uppal", "Stadium", "NGRI", "Habsiguda", "Tarnaka",
    "Mettuguda", "Secunderabad East", "Parade Ground", "Begumpet",
    "Madhura Nagar", "Yousufguda", "Jubilee Hills Check Post",
    "Peddamma Gudi", "Madhapur", "Durgam Cheruvu", "HITEC City", "Raidurg"
]

def calculate_distance(frm, to):
    return abs(STATIONS.index(frm) - STATIONS.index(to)) * 1.2  # km

def calculate_fare(distance, tickets):
    return int((15 + distance * 5) * tickets)

def calculate_co2(distance, tickets):
    return round(distance * tickets * 0.12, 2)
