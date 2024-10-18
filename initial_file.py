def print_hi(name,marks):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    subject = 'Maths'

    match subject:
        case 'Maths' if marks >= 80:
            print("Excellent in Maths!")
        case 'English' if marks >= 80:
            print("Excellent in English!")
        case _:
            print(f"Needs improvement in {subject}!")


if __name__ == '__main__':
    print_hi('PyCharm',marks=45)
