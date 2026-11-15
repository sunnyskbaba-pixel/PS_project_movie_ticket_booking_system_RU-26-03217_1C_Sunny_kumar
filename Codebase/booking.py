TICKET_PRICE = 200
ROWS = ["A", "B", "C"]
SEATS_PER_ROW = 5
FILE_NAME = "bookings.txt"


# Empty hall banana
def create_empty_hall():
    return [[None for _ in range(5)] for _ in range(3)]


# Seat validate karna
def seat_position(seat_code):
    seat_code = seat_code.strip().upper()

    if len(seat_code) != 2:
        return None

    row = seat_code[0]
    number = seat_code[1]

    if row not in ROWS or number not in "12345":
        return None

    return ROWS.index(row), int(number) - 1


# Booking file mein save karna
def save_bookings(hall):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        for i, row in enumerate(hall):
            for j, name in enumerate(row):
                if name is not None:
                    seat = ROWS[i] + str(j + 1)
                    file.write(seat + "|" + name + "\n")


# File se bookings load karna
def load_bookings():
    hall = create_empty_hall()

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("|", 1)

                if len(parts) != 2:
                    continue

                seat, name = parts
                position = seat_position(seat)

                if position is not None and name.strip():
                    i, j = position
                    hall[i][j] = name.strip()

    except FileNotFoundError:
        pass

    return hall


# Empty seats count karna
def seats_left(hall):
    count = 0

    for row in hall:
        for seat in row:
            if seat is None:
                count += 1

    return count


# Seat map display karna
def display_seat_map(hall):
    print("\n------ SEAT MAP ------")

    for i, row in enumerate(hall):
        symbols = []

        for seat in row:
            if seat is None:
                symbols.append("_")
            else:
                symbols.append("X")

        print("Row", ROWS[i] + ":", " ".join(symbols))

    print("Seats left:", seats_left(hall))

    if seats_left(hall) == 0:
        print("Show is now housefull!")

    print("----------------------")


# Ticket book karna
def book_seats(hall):

    if seats_left(hall) == 0:
        print("Sorry, hall is housefull.")
        return

    seat_input = input(
        "Enter seat code(s), e.g. A1 or A2,A3: "
    )

    seat_codes = seat_input.upper().replace(" ", "").split(",")

    name = input("Enter customer name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    booked_count = 0

    for seat in seat_codes:

        position = seat_position(seat)

        if position is None:
            print("Invalid seat. Rows A-C and seats 1-5.")
            continue

        i, j = position

        if hall[i][j] is not None:
            print("Seat", seat, "is already booked.")
            continue

        hall[i][j] = name
        booked_count += 1

        print("Seat", seat, "booked for", name + ".")

    if booked_count > 0:
        amount = booked_count * TICKET_PRICE

        save_bookings(hall)

        print("Amount:", amount)
        print("Seats left:", seats_left(hall))

        if seats_left(hall) == 0:
            print("Show is now housefull!")


# Ticket cancel karna
def cancel_booking(hall):

    seat = input("Enter seat code to cancel: ").strip().upper()

    position = seat_position(seat)

    if position is None:
        print("Invalid seat. Rows A-C and seats 1-5.")
        return

    i, j = position

    if hall[i][j] is None:
        print("Seat", seat, "is not booked.")
        return

    name = hall[i][j]

    hall[i][j] = None

    save_bookings(hall)

    print("Booking for", name, "at seat", seat, "cancelled.")


# Main program
def main():

    hall = load_bookings()

    print("Welcome to Movie Ticket Booking System!")

    while True:

        print("\n1. Book")
        print("2. Cancel")
        print("3. Seat map")
        print("4. Exit")

        choice = input("Enter menu option: ").strip()

        if choice == "1":
            book_seats(hall)

        elif choice == "2":
            cancel_booking(hall)

        elif choice == "3":
            display_seat_map(hall)

        elif choice == "4":
            print("Thank you! Goodbye.")
            break

        else:
            print("Invalid menu option.")


if __name__ == "__main__":
    main()
