def identify_user_tier(tier_code):
    tiers = {
        "kids": "MODE: Playground | UI: GameMaster | Security: Walled_Garden",
        "basic": "MODE: Explorer | UI: Standard | Security: Personal_Local",
        "enthusiast": "MODE: Collaborator | UI: Dev_Dashboard | Security: Community_Mesh",
        "professional": "MODE: Architect | UI: Pro_Suite | Security: Global_Node",
        "school": "MODE: Student_SubMesh | UI: Classroom | Security: Isolated_School_Zone"
    }
    return tiers.get(tier_code, "MODE: Default_User")

if __name__ == "__main__":
    choice = input("Select your role (kids/basic/enthusiast/professional/school): ")
    print(identify_user_tier(choice))
