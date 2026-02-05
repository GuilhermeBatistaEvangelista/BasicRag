from dotenv import load_dotenv

from input import inputHandler


def main():
	load_dotenv()
	handle_input = inputHandler()

	RUN = True
	while RUN:
		handle_input.show()

		if not handle_input.read():
			break

main()