def provision_environment(tier_code):
    environments = {
        "kids": {"features": ["sandbox", "basic_game_build"], "mesh": "restricted"},
        "basic": {"features": ["assistant", "basic_tools"], "mesh": "personal"},
        "enthusiast": {"features": ["plugin_dev", "market_access"], "mesh": "community"},
        "professional": {"features": ["pro_security", "global_recon"], "mesh": "global"},
        "school": {"features": ["collaborative_lab"], "mesh": "school_submesh"}
    }
    config = environments.get(tier_code, environments["basic"])
    print(f"Provisioning environment: {config['features']} | Mesh Scope: {config['mesh']}")
    return config

if __name__ == "__main__":
    provision_environment("professional")
