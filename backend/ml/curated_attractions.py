"""
Curated famous tourist attractions for the 73 Indian destinations in Triip_HF_v4_10k.csv.
Provides verified landmarks and attractions to guarantee specific, authentic recommendations.
"""

DESTINATION_ATTRACTIONS = {
    "Agra": [
        "Taj Mahal", "Agra Fort", "Fatehpur Sikri", "Mehtab Bagh",
        "Itmad-ud-Daulah (Baby Taj)", "Akbar's Tomb (Sikandra)", "Kinari Bazaar"
    ],
    "Aihole": [
        "Durga Temple Complex", "Lad Khan Temple", "Ravanaphadi Cave",
        "Huchimalli Temple", "Meguti Jain Temple", "Archaeological Museum Aihole"
    ],
    "Alleppey": [
        "Alleppey Backwaters & Houseboat", "Alappuzha Beach & Lighthouse", "Marari Beach",
        "Kuttanad Paddy Fields", "Vembanad Lake", "Pathiramanal Island", "Mullakkal Temple"
    ],
    "Amritsar": [
        "Golden Temple (Harmandir Sahib)", "Jallianwala Bagh", "Wagah Border Ceremony",
        "Partition Museum", "Gobindgarh Fort", "Durgiana Temple", "Hall Bazaar"
    ],
    "Araku": [
        "Borra Caves", "Araku Tribal Museum", "Padmapuram Gardens",
        "Chapaparai Waterfalls", "Katiki Waterfalls", "Coffee Plantations Viewpoint"
    ],
    "Aurangabad": [
        "Ajanta Caves", "Ellora Caves", "Bibi Ka Maqbara",
        "Daulatabad Fort", "Grishneshwar Temple", "Panchakki"
    ],
    "Badami": [
        "Badami Cave Temples", "Agastya Lake", "Bhutanatha Temples",
        "Badami Fort", "Archaeological Museum", "Banashankari Amma Temple"
    ],
    "Bangalore": [
        "Bangalore Palace", "Lalbagh Botanical Garden", "Cubbon Park",
        "Tipu Sultan's Summer Palace", "ISKCON Temple Bangalore", "Vidhana Soudha", "UB City & MG Road"
    ],
    "Bhopal": [
        "Upper Lake (Bhojtal) & Boat Club", "Van Vihar National Park", "Sanchi Stupa (Day Trip)",
        "Bhimbetka Rock Shelters", "Taj-ul-Masajid", "Tribal Museum Bhopal", "Shaukat Mahal"
    ],
    "Bhubaneswar": [
        "Lingaraj Temple", "Udayagiri and Khandagiri Caves", "Mukteshwara Temple",
        "Dhauli Shanti Stupa", "Nandankanan Zoological Park", "Odisha State Museum"
    ],
    "Chandigarh": [
        "Rock Garden of Chandigarh", "Sukhna Lake", "Zakir Hussain Rose Garden",
        "Sector 17 Shopping Plaza", "Capitol Complex (UNESCO)", "Government Museum and Art Gallery"
    ],
    "Chennai": [
        "Marina Beach", "Kapaleeshwarar Temple", "Fort St. George",
        "San Thome Basilica", "Government Museum Egmore", "DakshinaChitra Heritage Village", "Besant Nagar Beach"
    ],
    "Chikmagalur": [
        "Mullayanagiri Peak", "Baba Budangiri", "Hebbe Falls",
        "Jhari (Buttermilk) Falls", "Bhadra Wildlife Sanctuary", "Coffee Museum", "Z Point"
    ],
    "Coimbatore": [
        "Adiyogi Shiva Statue", "Marudhamalai Murugan Temple", "Dhyanalinga Temple",
        "Gass Forest Museum", "Siruvani Waterfalls", "VOC Park and Zoo"
    ],
    "Coorg": [
        "Abbey Falls", "Raja's Seat Sunset Viewpoint", "Namdroling Monastery (Golden Temple)",
        "Dubare Elephant Camp", "Madikeri Fort", "Talakaveri (Cauvery Origin)", "Mandalpatti Peak"
    ],
    "Darjeeling": [
        "Tiger Hill Sunrise", "Batasia Loop", "Darjeeling Himalayan Railway (Toy Train)",
        "Happy Valley Tea Estate", "Himalayan Mountaineering Institute & Zoo", "Peace Pagoda", "Mall Road"
    ],
    "Delhi": [
        "Red Fort", "Qutub Minar", "Humayun's Tomb", "India Gate & Kartavya Path",
        "Lotus Temple", "Akshardham Temple", "Jama Masjid & Chandni Chowk", "National Museum", "Lodi Gardens"
    ],
    "Dharamshala": [
        "Tsuglagkhang Complex (Dalai Lama Temple)", "Bhagsunag Waterfall", "Namgyal Monastery",
        "HPCA Cricket Stadium", "Norbulingka Institute", "Kangra Fort", "St. John in the Wilderness Church"
    ],
    "Diu": [
        "Diu Fort & Lighthouse", "Naida Caves", "Nagoa Beach",
        "St. Paul's Church", "Gangeshwar Mahadev Temple", "Jallore Beach", "Shell Museum"
    ],
    "Gangtok": [
        "Tsomgo (Changu) Lake", "Nathula Pass", "Rumtek Monastery",
        "Banjhakri Falls", "MG Marg", "Do Drul Chorten Stupa", "Tashi Viewpoint", "Ganesh Tok"
    ],
    "Goa": [
        "Baga & Calangute Beaches", "Fort Aguada", "Basilica of Bom Jesus (Old Goa)",
        "Dudhsagar Waterfalls", "Anjuna Beach & Flea Market", "Chapora Fort", "Palolem Beach", "Fontainhas Latin Quarter"
    ],
    "Guwahati": [
        "Kamakhya Temple", "Umananda Island Temple", "Brahmaputra River Sunset Cruise",
        "Assam State Museum", "Pobitora Wildlife Sanctuary", "Srimanta Sankaradeva Kalakshetra"
    ],
    "Gwalior": [
        "Gwalior Fort", "Jai Vilas Palace", "Sas Bahu Temples",
        "Teli Ka Mandir", "Tomb of Tansen", "Sun Temple Gwalior", "Gopachal Parvat"
    ],
    "Hampi": [
        "Virupaksha Temple", "Vijaya Vittala Temple & Stone Chariot", "Lotus Mahal",
        "Elephant Stables", "Matanga Hill Sunrise", "Hemakuta Hill Temples", "Tungabhadra River Coracle Ride"
    ],
    "Haridwar": [
        "Har Ki Pauri & Ganga Aarti", "Mansa Devi Temple Cable Car", "Chandi Devi Temple",
        "Shanti Kunj", "Bharat Mata Mandir", "Maya Devi Temple", "Bara Bazaar"
    ],
    "Hyderabad": [
        "Charminar", "Golconda Fort", "Hussain Sagar Lake & Buddha Statue",
        "Salar Jung Museum", "Chowmahalla Palace", "Ramoji Film City", "Qutb Shahi Tombs", "Birla Mandir"
    ],
    "Indore": [
        "Rajwada Palace", "Lal Bagh Palace", "Sarafa Bazaar (Night Food Market)",
        "Chappan Dukan", "Kanch Mandir (Glass Temple)", "Patalpani Waterfall", "Annapurna Temple"
    ],
    "Jaipur": [
        "Amber Fort", "Hawa Mahal (Palace of Winds)", "City Palace Jaipur",
        "Jantar Mantar Observatory", "Nahargarh Fort", "Jaigarh Fort", "Jal Mahal", "Johari & Bapu Bazaars"
    ],
    "Jodhpur": [
        "Mehrangarh Fort", "Jaswant Thada", "Umaid Bhawan Palace",
        "Clock Tower & Sardar Market", "Mandore Gardens", "Toorji Ka Jhalra Stepwell", "Rao Jodha Desert Rock Park"
    ],
    "Kanyakumari": [
        "Vivekananda Rock Memorial", "Thiruvalluvar Statue", "Kanyakumari Sunset & Sunrise Viewpoint",
        "Bhagavathy Amman Temple", "Gandhi Memorial Mandapam", "Padmanabhapuram Palace"
    ],
    "Kasauli": [
        "Gilbert Trail", "Monkey Point (Manki Point)", "Christ Church Kasauli",
        "Sunset Point", "Mall Road Kasauli", "Timber Trail Cable Car", "Gurkha Fort"
    ],
    "Kerala": [
        "Alleppey Backwaters & Houseboat", "Munnar Tea Gardens", "Periyar National Park Thekkady",
        "Fort Kochi & Chinese Fishing Nets", "Kovalam Beach", "Athirappilly Waterfalls", "Varkala Cliff Beach"
    ],
    "Khajuraho": [
        "Western Group of Temples (Kandariya Mahadeva)", "Eastern Group of Temples",
        "Southern Group of Temples", "Light and Sound Show at Western Group", "Raneh Falls & Canyon", "Archaeological Museum"
    ],
    "Kochi": [
        "Fort Kochi & Chinese Fishing Nets", "Mattancherry Dutch Palace", "Paradesi Jewish Synagogue",
        "Santa Cruz Cathedral Basilica", "Marine Drive Kochi", "Kerala Kathakali Centre", "Cherai Beach"
    ],
    "Kodaikanal": [
        "Kodaikanal Lake & Boating", "Coaker's Walk", "Bryant Park",
        "Pillar Rocks", "Silver Cascade Falls", "Dolphin's Nose", "Pine Forest Kodaikanal"
    ],
    "Kolkata": [
        "Victoria Memorial", "Howrah Bridge", "Dakshineswar Kali Temple",
        "Indian Museum", "Princep Ghat", "Park Street", "Belur Math", "St. Paul's Cathedral"
    ],
    "Leh": [
        "Pangong Tso Lake", "Nubra Valley & Hunder Sand Dunes", "Khardung La Pass",
        "Leh Palace", "Shanti Stupa", "Hemis Monastery", "Thiksey Monastery", "Magnetic Hill"
    ],
    "Lucknow": [
        "Bara Imambara & Bhool Bhulaiya", "Chota Imambara", "Rumi Darwaza",
        "British Residency", "Hazratganj Shopping", "Ambedkar Memorial Park", "Dilkusha Kothi"
    ],
    "Madurai": [
        "Meenakshi Amman Temple", "Thirumalai Nayakkar Mahal", "Gandhi Memorial Museum",
        "Alagar Kovil (Kallazhagar Temple)", "Vandiyur Mariamman Teppakulam", "Koodal Azhagar Temple"
    ],
    "Manali": [
        "Hadimba Devi Temple", "Solang Valley Adventures", "Rohtang Pass (or Atal Tunnel)",
        "Old Manali Cafes & Wooden Houses", "Vashisht Hot Springs & Temple", "Jogini Waterfall Trek", "Mall Road Manali"
    ],
    "Mcleodganj": [
        "Tsuglagkhang Complex (Dalai Lama Temple)", "Bhagsunag Temple & Waterfall",
        "Triund Trek (or Viewpoint)", "Dal Lake Mcleodganj", "St. John in the Wilderness", "Tibetan Market"
    ],
    "Mount Abu": [
        "Dilwara Jain Temples", "Nakki Lake & Boating", "Guru Shikhar Peak",
        "Sunset Point Mount Abu", "Achalgarh Fort", "Toad Rock", "Peace Park"
    ],
    "Mumbai": [
        "Gateway of India", "Marine Drive & Nariman Point", "Elephanta Caves",
        "Chhatrapati Shivaji Maharaj Terminus (CSMT)", "Colaba Causeway", "Bandra Bandstand", "Siddhi Vinayak Temple", "Juhu Beach"
    ],
    "Munnar": [
        "Eravikulam National Park (Nilgiri Tahr)", "Mattupetty Dam & Lake", "Tea Museum Munnar",
        "Top Station Viewpoint", "Attukad Waterfalls", "Kundala Lake", "Anamudi Peak View"
    ],
    "Mussoorie": [
        "Kempty Falls", "Gun Hill Ropeway", "Camel's Back Road",
        "Mall Road Mussoorie", "Lal Tibba Scenic Point", "Company Garden", "Cloud's End"
    ],
    "Mysore": [
        "Mysore Palace (Amba Vilas)", "Chamundeshwari Temple (Chamundi Hill)", "Brindavan Gardens & Musical Fountain",
        "St. Philomena's Cathedral", "Mysore Zoo (Sri Chamarajendra)", "Jaganmohan Palace Art Gallery", "Devaraja Market"
    ],
    "Nainital": [
        "Naini Lake & Yacht Boating", "Naina Devi Temple", "Snow View Point Cable Car",
        "Tiffin Top (Dorothy's Seat)", "Mall Road Nainital", "Eco Cave Gardens", "High Altitude Nainital Zoo"
    ],
    "Nashik": [
        "Sula Vineyards & Wine Tasting", "Trimbakeshwar Shiva Temple", "Panchavati & Sita Gufa",
        "Pandavleni Caves", "Godavari Ghats (Ramkund)", "Muktidham Temple", "Anjaneri Hills"
    ],
    "Ooty": [
        "Nilgiri Mountain Railway (Toy Train)", "Ooty Botanical Gardens", "Ooty Lake & Boating",
        "Doddabetta Peak", "Rose Garden Ooty", "Pykara Falls & Lake", "Tea Factory & Museum"
    ],
    "Orchha": [
        "Orchha Fort Complex", "Raja Mahal & Jahangir Mahal", "Chaturbhuj Temple",
        "Ram Raja Temple", "Chhatris (Cenotaphs) along Betwa River", "Betwa River Rafting"
    ],
    "Patna": [
        "Golghar Granary", "Patna Museum (and Bihar Museum)", "Takht Sri Patna Sahib",
        "Kumhrar Ancient Mauryan Ruins", "Buddha Smriti Park", "Mahavir Mandir", "Gandhi Ghat on River Ganga"
    ],
    "Pondicherry": [
        "Promenade Beach & Rock Beach", "Auroville & Matrimandir", "Sri Aurobindo Ashram",
        "French Quarter (White Town)", "Paradise Beach & Chunnambar Boat House", "Basilica of Sacred Heart", "Arikamedu"
    ],
    "Pune": [
        "Shaniwar Wada", "Aga Khan Palace", "Sinhagad Fort",
        "Dagdusheth Halwai Ganpati Temple", "Osho Teerth Park & Ashram", "Raja Dinkar Kelkar Museum", "FC Road & Koregaon Park"
    ],
    "Puri": [
        "Jagannath Temple Puri", "Golden Beach Puri", "Konark Sun Temple (UNESCO Day Trip)",
        "Chilika Lake & Dolphin Sanctuary", "Puri Beach Market", "Raghurajpur Heritage Crafts Village", "Gundicha Temple"
    ],
    "Pushkar": [
        "Brahma Temple Pushkar", "Pushkar Lake & 52 Ghats", "Savitri Mata Temple Hilltop",
        "Varaha Temple", "Pushkar Desert Safari & Dunes", "Pushkar Camel Fair Grounds & Bazaars"
    ],
    "Raipur": [
        "Swami Vivekananda Sarovar (Budha Talab)", "Nandan Van Zoo & Safari", "Purkhouti Muktangan",
        "Mahant Ghasidas Memorial Museum", "Ghatarani Waterfalls (Day Trip)", "MM Fun City", "Jatmai Temple"
    ],
    "Rameswaram": [
        "Ramanathaswamy Temple & 22 Theerthams", "Dhanushkodi Ghost Town & Beach", "Dr. A.P.J. Abdul Kalam Memorial",
        "Pamban Bridge Viewpoint", "Agnitheertham", "Ariyamangalam Beach", "Kothandaramaswamy Temple"
    ],
    "Ranchi": [
        "Dassam Falls", "Hundru Falls", "Jonha Falls",
        "Pahari Mandir", "Tagore Hill", "Patratu Valley Viewpoint", "Birsa Zoological Park"
    ],
    "Rann of Kutch": [
        "White Desert of Kutch (Dhordo Salt Flats)", "Kala Dungar (Black Hill)", "Rann Utsav Cultural Village",
        "Kutch Fossil Park", "Aina Mahal & Prag Mahal (Bhuj)", "Kutch Museum", "Hodka Craft Village"
    ],
    "Rishikesh": [
        "Laxman Jhula & Ram Jhula", "Triveni Ghat Evening Ganga Aarti", "Beatles Ashram (Chaurasi Kutia)",
        "Ganga River Rafting & Cliff Jumping", "Neer Garh Waterfall", "Parmarth Niketan", "Kunjapuri Sunrise Trek"
    ],
    "Shillong": [
        "Elephant Falls", "Umiam Lake (Barapani)", "Shillong Peak & Viewpoint",
        "Don Bosco Museum of Indigenous Cultures", "Police Bazar", "Ward's Lake", "Laitlum Canyons"
    ],
    "Shimla": [
        "The Ridge & Christ Church", "Mall Road Shimla", "Jakhoo Temple & Hanuman Statue",
        "Kalka-Shimla Toy Train", "Kufri Adventure Park & Snow Points", "Viceregal Lodge (Indian Institute of Advanced Study)", "Tara Devi Temple"
    ],
    "Srinagar": [
        "Dal Lake Shikara Ride & Houseboats", "Mughal Gardens (Shalimar & Nishat Bagh)", "Shankaracharya Temple",
        "Indira Gandhi Memorial Tulip Garden", "Chashme Shahi Garden", "Hazratbal Shrine", "Old City Zaina Kadal Bazaar", "Pari Mahal"
    ],
    "Thanjavur": [
        "Brihadeeswara Temple (Big Temple - UNESCO)", "Thanjavur Maratha Palace & Art Gallery",
        "Saraswathi Mahal Library", "Schwartz Church", "Rajarajan Manimandapam", "Punnainallur Mariamman Temple"
    ],
    "Thiruvananthapuram": [
        "Padmanabhaswamy Temple", "Kovalam Beach & Lighthouse", "Napier Museum & Art Gallery",
        "Kanakakkunnu Palace", "Shanghumukham Beach & Giant Mermaid", "Poovar Island Backwaters", "Attukal Bhagavathy Temple"
    ],
    "Tirupati": [
        "Sri Venkateswara Swamy Temple (Tirumala)", "Silathoranam (Natural Rock Arch)", "Kapila Theertham Waterfalls",
        "Sri Padmavathi Ammavari Temple (Tiruchanur)", "ISRO Space Museum / Planetarium", "Chandragiri Fort", "Deer Park"
    ],
    "Udaipur": [
        "City Palace Udaipur", "Lake Pichola & Boat Cruise", "Jag Mandir Island Palace",
        "Saheliyon Ki Bari (Courtyard of Maidens)", "Jagdish Temple", "Bagore Ki Haveli Folk Dance", "Fateh Sagar Lake", "Monsoon Palace (Sajjangarh)"
    ],
    "Ujjain": [
        "Mahakaleshwar Jyotirlinga Temple & Bhasma Aarti", "Ram Ghat along Shipra River", "Harsiddhi Temple",
        "Kal Bhairav Temple", "Vedh Shala (Jantar Mantar Ujjain)", "Mangalnath Temple", "Sandipani Ashram"
    ],
    "Varanasi": [
        "Kashi Vishwanath Temple (Golden Temple)", "Dashashwamedh Ghat Evening Ganga Aarti", "Morning Boat Ride on River Ganges",
        "Sarnath (Dhamek Stupa & Deer Park)", "Assi Ghat & Subah-e-Banaras", "Manikarnika Ghat", "BHU & New Vishwanath Temple", "Banarasi Silk Weaver Colony"
    ],
    "Vellore": [
        "Vellore Fort & Jalakanteswarar Temple", "Sripuram Golden Temple (Maha Lakshmi)", "Government Museum Vellore",
        "Amirthi Zoological Park", "French Cemetery Vellore", "Palamathi Hills Viewpoint"
    ],
    "Vizag": [
        "Submarine Museum (INS Kursura)", "RK Beach (Ramakrishna Beach)", "Kailasagiri Hilltop & Cable Car",
        "Rushi Konda Beach", "TU 142 Aircraft Museum", "Dolphin's Nose & Lighthouse", "Simhachalam Temple", "Borra Caves (Day Trip)"
    ],
    "Warangal": [
        "Warangal Fort & Kakatiya Kala Thoranam", "Thousand Pillar Temple", "Bhadrakali Temple & Lake",
        "Ramappa Temple (UNESCO Day Trip)", "Laknavaram Lake & Hanging Bridge", "Pakhal Lake", "Khush Mahal"
    ],
    "Wayanad": [
        "Edakkal Caves", "Banasura Sagar Dam", "Chembra Peak & Heart Lake Trek",
        "Pookode Lake", "Soochipara (Sentinel Rock) Falls", "Wayanad Wildlife Sanctuary (Muthanga)", "Lakkidi Viewpoint"
    ]
}


def get_attractions_for_destination(dest_name):
    """
    Returns a list of famous attractions for a destination, or an empty list if unknown.
    Matches case-insensitively and handles common variations.
    """
    clean_dest = str(dest_name or "").strip().lower()
    for key, places in DESTINATION_ATTRACTIONS.items():
        if key.lower() == clean_dest or clean_dest in key.lower() or key.lower() in clean_dest:
            return places
    return []
