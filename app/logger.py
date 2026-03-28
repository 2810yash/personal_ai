from app.memory import store_memory
from datetime import datetime

def log_activity(activity):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    log_text = f"{timestamp} - {activity}"
    
    store_memory(log_text)
    
    print("Logged:", log_text)


if __name__ == "__main__":
    while True:
        activity = input("What are you doing? (type 'exit' to stop): ")
        
        if activity.lower() == "exit":
            break
        
        log_activity(activity)