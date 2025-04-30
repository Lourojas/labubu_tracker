if __name__ == "__main__":
    print("Checking Labubu availability...")
    try:
        if is_labubu_available():
            print("Labubu is available! Sending notification...")
            send_push_notification()
        else:
            print("Still not available.")
    except Exception as e:
        print(f"Error: {e}")
