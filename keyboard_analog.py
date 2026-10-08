from pynput import keyboard

#INPUT MAGNITUDES
LOW = 1/3
MEDIUM = 2/3
HIGH = 1.0

#Map each key to its input group and magnitude
KEY_BINDINGS = {
    #Throttle
    'w': ("throttle", LOW),
    'e': ("throttle", MEDIUM),
    'r': ("throttle", HIGH),

    #Brake
    's': ("brake", LOW),
    'd': ("brake", MEDIUM),
    'f': ("brake", HIGH),

    #Steering left
    'j': ("left", LOW),
    'k': ("left", MEDIUM),
    'l': ("left", HIGH),
    
    #Steering right
    'u': ("right", LOW),
    'i': ("right", MEDIUM),
    'o': ("right", HIGH)
}

#Keep track of currently held keys
held_keys = set()

def get_input(group):
    """
    Return the greatest magnitude of keys held in a group
    """
    magnitudes = [
        KEY_BINDINGS[key][1]
        for key in held_keys
        if key in KEY_BINDINGS and KEY_BINDINGS[key][0] == group
    ]

    return max(magnitudes, default=0.0)

def calculate_inputs():
    """
    Calculate the current input values for throttle, brake, left, and right
    """
    throttle = get_input("throttle")
    brake = get_input("brake")
    steering_left = get_input("left")
    steering_right = get_input("right")

    steering = steering_right - steering_left  # Right is positive, left is negative

    return throttle, brake, steering

def on_press(key):
    """
    Record a key press event
    """
    try:
        character = key.char.lower()
    except AttributeError:
        return  # Ignore non-character keys

    if character in KEY_BINDINGS:
        held_keys.add(character)

def on_release(key):
    """
    Record a key release event
    """
    try:
        character = key.char.lower()
    except AttributeError:
        return  # Ignore non-character keys

    if character in held_keys:
        held_keys.discard(character)

def main():
    print("Keyboard Analog Simulator")
    print("Press 'w', 'e', 'r' for throttle (low, medium, high)")
    print("Press 's', 'd', 'f' for brake (low, medium, high)")
    print("Press 'j', 'k', 'l' for left steering (low, medium, high)")
    print("Press 'u', 'i', 'o' for right steering (low, medium, high)")
    print("Press ESC to exit.")

    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    ) as listener:

        while listener.is_alive():
            throttle, brake, steering = calculate_inputs()
            print(f"Throttle: {float(throttle):.2f}, Brake: {float(brake):.2f}, Steering: {float(steering):.2f}", end='\r', flush=True)

            #Exit when ESC is pressed
            if keyboard.Key.esc in held_keys:
                break
            #The listener also needs to stop
            #We'll handle that in the next version of the code
            import time
            time.sleep(0.05)  # Adjust the sleep time as needed

if __name__ == "__main__":
    main()
