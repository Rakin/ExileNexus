def logger(message, is_debug_active):
    if is_debug_active:
        timestamp = time.strftime('%H:%M:%S')
        print(f"[{timestamp}] [DEBUG] {message}")