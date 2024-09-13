def config() -> dict:
    return {
        "connection_params": {
            "host": "localhost",
            "port": "3306",
            "username": "root",
            "password": "password",
            "autocommit": False,
            "collation": "utf8mb4_unicode_ci",
        },
        "chunksize": 500,
        "data_format": "csv", # "csv" | "json" | "xml"
        "databases": {
            # Setup for the `flight_game` database
            # used in our group project.
            "flight_game": {
                "tables": {
                    "airport": {
                        "data_file": "airports.csv",
                        "data_types": {
                            "id": "INT PRIMARY KEY",
                            "ident": "VARCHAR(15)",
                            "type": "VARCHAR(50)",
                            "name": "VARCHAR(255)",
                            "latitude_deg": "FLOAT",
                            "longitude_deg": "FLOAT",
                            "elevation_ft": "INT",
                            "continent": "VARCHAR(2)",
                            "iso_country": "VARCHAR(2)",
                            "iso_region": "VARCHAR(7)",
                            "municipality": "VARCHAR(255)",
                            "scheduled_service": "VARCHAR(3)",
                            "gps_code": "VARCHAR(4)",
                            "iata_code": "VARCHAR(3)",
                            "local_code": "VARCHAR(7)",
                            "home_link": "VARCHAR(255)",
                            "wikipedia_link": "VARCHAR(255)",
                        },
                        "relationships": {
                            {
                                "foreign_key": "iso_country",
                                "reference_table": "country",
                                "reference_column": "iso_country",
                                "constraint_name": "airport_ibfk_1",
                            }
                        }
                    },
                    "country": {
                        "data_file": "countries.csv",
                        "data_types": {
                            "iso_country": "VARCHAR(40) PRIMARY KEY NOT NULL",
                            "name": "VARCHAR(40)",
                            "continent": "VARCHAR(40)",
                            "wikipedia_link": "VARCHAR(255)",
                            "keywords": "VARCHAR(255)",
                        }
                    },
                    "game": {
                        "data_file": "game.csv",
                        "data_types": {
                            "id": "VARCHAR(40) PRIMARY KEY",
                            "co2_consumed": "INT",
                            "co2_budget": "INT",
                            "location": "VARCHAR(10)",
                            "screen_name": "VARCHAR(40)",
                        },
                        "relationships": {
                            {
                                "foreign_key": "location",
                                "reference_table": "airport",
                                "reference_column": "ident",
                                "constraint_name": "game_ibfk_1",
                            }
                        }
                    },
                    "goal": {
                        "data_file": "goal.csv",
                        "data_types": {
                            "id": "INT PRIMARY KEY",
                            "name": "VARCHAR(40)",
                            "description": "VARCHAR(200)",
                            "icon": "VARCHAR(8)",
                            "target": "VARCHAR(40)",
                            "target_minvalue": "DECIMAL(8,2)",
                            "target_maxvalue": "DECIMAL(8,2)",
                            "target_text": "VARCHAR(40)",
                        }
                    },
                    "goal_reached": {
                        "data_file": "goal_reached.csv",
                        "data_types": {
                            "game_id": "VARCHAR(40)",
                            "goal_id": "INT",
                        },
                        "relationships": {
                            {
                                "foreign_key": "game_id",
                                "reference_table": "game",
                                "reference_column": "id",
                                "constraint_name": "goal_reached_ibfk_1",
                            },
                            {
                                "foreign_key": "goal_id",
                                "reference_table": "goal",
                                "reference_column": "id",
                                "constraint_name": "goal_reached_ibfk_2",
                            }
                        }
                    }
                }
            }
        }
    }
