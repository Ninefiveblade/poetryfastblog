class Role:
    """
    Constants for the various roles scoped in the application ecosystem
    """

    GUEST = {
        "name": "GUEST",
        "description": "A Guest Account",
    }
    USER = {
        "name": "ACCOUNT_ADMIN",
        "description": "Primary Administrator/Superuser For an Account",
    }

    MODERATOR = {
        "name": "ACCOUNT_MANAGER",
        "description": "Day to Day Administrator of Events For an Account",
    }
    ADMIN = {
        "name": "ADMIN",
        "description": "Admin of Application Ecosystem",
    }
    SUPER_USER = {
        "name": "SUPER_ADMIN",
        "description": "Super Administrator of Application Ecosystem",
    }
