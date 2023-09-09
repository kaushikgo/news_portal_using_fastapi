def Userschema(item):
    return{ "ID" : item["_id"],
    "First_Name" : item["First_Name"],
    "Last_Name" : item["Last_Name"],
    "UserImage" : item["UserImage"],
    "Email" : item["Email"],
    "Bio": item["Bio"],
    "Role" : item["Role"], 
    "Created_at" : item["Created_at"],
    "Is_Activated" : item["Is_Activated"]
    }

def Newsupdatingschema(item):
    return{
        "News_Title": item["News_Title"],
        "BriefDescription": item["BriefDescription"],
        "Content": item["Content"],
        "Tags": item["Tags"],
        "Category": item["Category"]
    }