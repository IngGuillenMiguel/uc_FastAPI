from schemas import StatusType

taskWithOutORM = {
    "normal_1": {
        "summary": "A normal example 1",
        "description": "A normal example",
        "value": {
            "id": 1,
            "name": "Tarea 1 por hacer",
            "description": "Tarea 1 por realizar",
            "status": StatusType.PENDING,
            "tag": ["Tag 1", "Tag 2"],
            "category": {
                "id": 1,
                "name": "Category 1"
            },
            "user": {
                "id": 1,
                "name": "Miguel",
                "lastname": "Guillen",
                "email": "miguel.guillen@merqry.mx",
                "website": "https://www.merqry.mx"
            }
        }
    },
    "normal_2": {
        "summary": "A normal example 2",
        "description": "A normal example",
        "value": {
            "id": 1,
            "name": "Tarea 1 por hacer",
            "description": "Tarea 1 por realizar",
            "status": StatusType.PENDING,
            "tag": ["Tag 1", "Tag 2"],
            "category": {
                "id": 1,
                "name": "Category 1"
            },
            "user": {
                "id": 1,
                "name": "Miguel",
                "lastname": "Guillen",
                "email": "miguel.guillen@merqry.mx",
                "website": "https://www.merqry.mx"
            }
        }
    },
    "invalid": {
        "summary": "A invalid example 1",
        "description": "A invalid example",
        "value": {
            "id": 12,
            "name": "Tarea 1 por hacer",
            "description": "Tarea 1 por realizar",
            "status": StatusType.PENDING,
            "tag": ["Tag 1"],
            "user": {
                "id": 1,
                "name": "Miguel",
                "lastname": "Guillen",
                "email": "miguel.guillen@merqry.mx",
                "website": "https://www.merqry.mx"
            }
        }
    }
}

taskWithORM = {
    "normal_1": {
        "summary": "A normal example 1",
        "description": "A normal example",
        "value": {
            "id": 1,
            "name": "Tarea 1 por hacer",
            "description": "Tarea 1 por realizar",
            "status": StatusType.PENDING,
            "tag": ["Tag 1"],
            "category_id": 1,
            "user_id": 1
        }
    },
    "normal_2": {
        "summary": "A normal example 2",
        "description": "A normal example",
        "value": {
            "id": 1,
            "name": "Tarea 1 por hacer",
            "description": "Tarea 1 por realizar",
            "status": StatusType.PENDING,
            "tag": ["Tag 1"],
            "category_id": 1,
            "user_id": 1
        }
    },
    "invalid": {
        "summary": "A invalid example 1",
        "description": "A invalid example",
        "value": {
            "id": 12,
            "name": "Tarea 1 por hacer",
            "description": "Tarea 1 por realizar",
            "status": StatusType.PENDING,
            "tag": ["Tag 1"],
            "user_id": 1
        }
    }
}
