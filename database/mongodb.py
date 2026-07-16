from pymongo import MongoClient

try:
    MONGO_URI = "mongodb+srv://golusharma8223829102_db_user:golu123@cluster0.d7wuoai.mongodb.net/?retryWrites=true&w=majority"

    client = MongoClient(MONGO_URI)

    client.admin.command("ping")

    db = client["rama123"]

    students_collection = db["students"]
    marks_collection = db["marks"]
    attendance_collection = db["attendance"]
    bmi_collection = db["bmi_report"]

    print("MongoDB connected successfully!")

except Exception as e:
    print("MongoDB Error:", e)
