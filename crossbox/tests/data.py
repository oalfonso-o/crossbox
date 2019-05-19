import datetime

EXPECTED_RESERVATION_DAYS = [
    [
        datetime.date(2019, 5, 13),
        {'reservations': [], 'session': 123, 'user_reservated': False, 'session_closed': True, 'hour': '10:00'},
        {'reservations': [], 'session': 124, 'user_reservated': False, 'session_closed': True, 'hour': '11:00'},
        {'reservations': [], 'session': 125, 'user_reservated': False, 'session_closed': True, 'hour': '12:00'},
        {'reservations': [], 'session': 126, 'user_reservated': False, 'session_closed': True, 'hour': '13:00'},
        {'reservations': [], 'session': 127,  'user_reservated': False, 'session_closed': True, 'hour': '17:00'},
        {'reservations': [], 'session': 128, 'user_reservated': False, 'session_closed': True, 'hour': '18:00'},
        {'reservations': [], 'session': 129, 'user_reservated': False, 'session_closed': True, 'hour': '19:00'},
        {'reservations': [], 'session': 130, 'user_reservated': False, 'session_closed': True, 'hour': '20:00'}
    ],
    [
        datetime.date(2019, 5, 14),
        {'reservations': [], 'session': 131, 'user_reservated': False, 'session_closed': False, 'hour': '10:00'},
        {'reservations': [], 'session': 132, 'user_reservated': False, 'session_closed': False, 'hour': '11:00'},
        {'reservations': [], 'session': 133, 'user_reservated': False, 'session_closed': False, 'hour': '12:00'},
        {'reservations': [], 'session': 134, 'user_reservated': False, 'session_closed': False, 'hour': '13:00'},
        {'reservations': [], 'session': 135, 'user_reservated': False, 'session_closed': False, 'hour': '17:00'},
        {'reservations': [], 'session': 136, 'user_reservated': False, 'session_closed': False, 'hour': '18:00'},
        {'reservations': [], 'session': 137, 'user_reservated': False, 'session_closed': False, 'hour': '19:00'},
        {'reservations': [], 'session': 138, 'user_reservated': False, 'session_closed': False, 'hour': '20:00'}
    ],
    [
        datetime.date(2019, 5, 15),
        {'reservations': [], 'session': 139, 'user_reservated': False, 'session_closed': False, 'hour': '10:00'},
        {'reservations': [], 'session': 140, 'user_reservated': False, 'session_closed': False, 'hour': '11:00'},
        {'reservations': [], 'session': 141, 'user_reservated': False, 'session_closed': False, 'hour': '12:00'},
        {'reservations': [], 'session': 142, 'user_reservated': False, 'session_closed': False, 'hour': '13:00'},
        {'reservations': [], 'session': 143, 'user_reservated': False, 'session_closed': False, 'hour': '17:00'},
        {'reservations': [], 'session': 144, 'user_reservated': False, 'session_closed': False, 'hour': '18:00'},
        {'reservations': [], 'session': 145, 'user_reservated': False, 'session_closed': False, 'hour': '19:00'},
        {'reservations': [], 'session': 146, 'user_reservated': False, 'session_closed': False, 'hour': '20:00'}
    ],
    [
        datetime.date(2019, 5, 16),
        {'reservations': [], 'session': 147, 'user_reservated': False, 'session_closed': False, 'hour': '10:00'},
        {'reservations': [], 'session': 148, 'user_reservated': False, 'session_closed': False, 'hour': '11:00'},
        {'reservations': [], 'session': 149, 'user_reservated': False, 'session_closed': False, 'hour': '12:00'},
        {'reservations': [], 'session': 150, 'user_reservated': False, 'session_closed': False, 'hour': '13:00'},
        {'reservations': [], 'session': 151, 'user_reservated': False, 'session_closed': False, 'hour': '17:00'},
        {'reservations': [], 'session': 152, 'user_reservated': False, 'session_closed': False, 'hour': '18:00'},
        {'reservations': [], 'session': 153, 'user_reservated': False, 'session_closed': False, 'hour': '19:00'},
        {'reservations': [], 'session': 154, 'user_reservated': False, 'session_closed': False, 'hour': '20:00'}
    ],
    [
        datetime.date(2019, 5, 17),
        {'reservations': [], 'session': 155, 'user_reservated': False, 'session_closed': False, 'hour': '10:00'},
        {'reservations': [], 'session': 156, 'user_reservated': False, 'session_closed': False, 'hour': '11:00'},
        {'reservations': [], 'session': 157, 'user_reservated': False, 'session_closed': False, 'hour': '12:00'},
        {'reservations': [], 'session': 158, 'user_reservated': False, 'session_closed': False, 'hour': '13:00'},
        {'reservations': [], 'session': 159, 'user_reservated': False, 'session_closed': False, 'hour': '17:00'},
        {'reservations': [], 'session': 160, 'user_reservated': False, 'session_closed': False, 'hour': '18:00'},
        {'reservations': [], 'session': 161, 'user_reservated': False, 'session_closed': False, 'hour': '19:00'},
        {'reservations': [], 'session': 162, 'user_reservated': False, 'session_closed': False, 'hour': '20:00'}
    ],
    [
        datetime.date(2019, 5, 18),
        {'reservations': [], 'session': None, 'user_reservated': False, 'session_closed': None, 'hour': '10:00'},
        {'reservations': [], 'session': None, 'user_reservated': False, 'session_closed': None, 'hour': '11:00'},
        {'reservations': [], 'session': None, 'user_reservated': False, 'session_closed': None, 'hour': '12:00'},
        {'reservations': [], 'session': None, 'user_reservated': False, 'session_closed': None, 'hour': '13:00'},
        {'reservations': [], 'session': None, 'user_reservated': False, 'session_closed': None, 'hour': '17:00'},
        {'reservations': [], 'session': None, 'user_reservated': False, 'session_closed': None, 'hour': '18:00'},
        {'reservations': [], 'session': None, 'user_reservated': False, 'session_closed': None, 'hour': '19:00'},
        {'reservations': [], 'session': None, 'user_reservated': False, 'session_closed': None, 'hour': '20:00'}
    ]
]
