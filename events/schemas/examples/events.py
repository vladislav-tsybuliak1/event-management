list_example_json = [
    {
        "id": 1,
        "title": "Annual Company Meeting",
        "description": "A meeting to discuss the company's yearly progress and plans.",
        "start_time": "13 Dec 2024 08:00",
        "end_time": "13 Dec 2024 10:00",
        "location": "Headquarters",
        "organizer": "Digital_Dragon (digital.dragon@test.com)",
        "participants": 5,
    },
    {
        "id": 4,
        "title": "Project Kickoff",
        "description": "Initial meeting to kick off a new project with all stakeholders.",
        "start_time": "13 Dec 2024 12:00",
        "end_time": "13 Dec 2024 14:00",
        "location": "Room 301",
        "organizer": "John_Doe (john.doe@test.com)",
        "participants": 7,
    },
    {
        "id": 6,
        "title": "Workshop: AI in Healthcare",
        "description": "A workshop discussing the applications of AI in the healthcare industry.",
        "start_time": "15 Dec 2024 08:00",
        "end_time": "15 Dec 2024 10:00",
        "location": "Lab 5",
        "organizer": "John_Doe (john.doe@test.com)",
        "participants": 5,
    },
    {
        "id": 8,
        "title": "Client Presentation",
        "description": "Presentation of project progress and future plans to the client.",
        "start_time": "22 Dec 2024 13:00",
        "end_time": "22 Dec 2024 14:30",
        "location": "Client Office",
        "organizer": "SkyWalker89 (sky.walker@test.com)",
        "participants": 0,
    },
    {
        "id": 7,
        "title": "Webinar: Future of Blockchain",
        "description": "An online seminar exploring the future developments in blockchain technology.",
        "start_time": "20 Jan 2025 09:00",
        "end_time": "20 Jan 2025 10:30",
        "location": "Online",
        "organizer": "John_Doe (john.doe@test.com)",
        "participants": 5,
    },
]

detail_example_json = {
    "id": 1,
    "title": "Annual Company Meeting",
    "description": "A meeting to discuss the company's yearly progress and plans.",
    "start_time": "13 Dec 2024 08:00",
    "end_time": "13 Dec 2024 10:00",
    "location": "Headquarters",
    "organizer": "Digital_Dragon (digital.dragon@test.com)",
    "participants": [
        "John_Doe (john.doe@test.com)",
        "Techie_Tiger (tiger@test.com)",
        "SkyWalker89 (sky.walker@test.com)",
        "Mystic_Phoenix (mystic.phoenix@test.com)",
        "QuantumQuokka (quantum.quokka@test.com)",
    ],
}

create_update_request_example_json = {
    "title": "Product Launch",
    "description": "Official launch event for the company's new product.",
    "start_time": "2025-03-30T14:00:00",
    "end_time": "2025-03-30T17:00:00",
    "location": "Main Auditorium",
}

create_update_response_example_json = {
    "id": 13,
    "title": "Product Launch",
    "description": "Official launch event for the company's new product.",
    "start_time": "2025-03-30T14:00:00Z",
    "end_time": "2025-03-30T17:00:00Z",
    "location": "Main Auditorium",
    "organizer": "SkyWalker89 (sky.walker@test.com)",
    "participants": 0,
}

unauthorised_401_no_token = {
    "detail": "Authentication credentials were not provided."
}

unauthorised_401_invalid_token = {
    "detail": "Given token not valid for any token type",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "Token is invalid or expired",
        }
    ],
}

bad_request_400_empty_fields = {
    "title": ["This field is required."],
    "start_time": ["This field is required."],
    "end_time": ["This field is required."],
    "location": ["This field is required."],
}

bad_request_400_overlapping_event = {
    "non_field_errors": [
        "An event at 'Main Auditorium' overlaps with this time period."
    ]
}

bad_request_400_event_in_the_past = {
    "non_field_errors": ["Event starting time must be in the future."]
}

bad_request_400_end_time_before_start_time = {
    "non_field_errors": ["Event starting time must be before its ending time."]
}

bad_request_400_update_past_event = {
    "non_field_errors": [
        "This event has already started or is finished and cannot be updated."
    ]
}

bad_request_400_already_registered = {
    "detail": "You are already registered for this event."
}

bad_request_400_organizer_registering = {
    "detail": "You are the organizer of this event."
}

ok_200_registered = {
    "detail": "Successfully registered for the event."
}

not_found_404 = {"detail": "No Event matches the given query."}

forbidden_403 = {
    "detail": "You do not have permission to perform this action."
}
