import os


class Book(object):
    def __init__(self):
        self.__contacts = []
        if not os.path.exists("contacts.db"):
            with open("contacts.db", "w"):
                pass

        with open("contacts.db", "r") as f:
            for line in f.readlines():
                number, name = line.strip("\n").split()
                self.__contacts.append({"number": number, "name": name})

    def __save(self):
        with open("contacts.db", "w") as f:
            for contact in self.__contacts:
                f.write("{} {}\n".format(contact["number"], contact["name"]))

        self.__init__()

    def insert(self, number, name):
        if self.contains(number):
            return True
        else:
            self.__contacts.append({"number": number, "name": name})

        self.__save()

    def remove(self, number):
        contact = self.get(number)

        if contact is not None:
            self.__contacts.remove(contact)

        self.__save()

    def update(self, name_or_number, new_name_or_number):
        for contact in self.__contacts:
            if contact["number"] == name_or_number or contact["name"] == name_or_number:
                if new_name_or_number.isdigit():
                    contact["number"] = new_name_or_number
                else:
                    contact["name"] = new_name_or_number
                self.__save()

    def get(self, name_or_number):
        for contact in self.__contacts:
            if (contact["number"] == name_or_number) | (
                contact["name"] == name_or_number
            ):
                return contact
        return None

    def contacts(self):
        return self.__contacts

    def contains(self, number):
        for contact in self.__contacts:
            if contact["number"] == number:
                return True
        return False


def main():
    print("Welcome to Booth v0.1.0")
    print("run `booth help` to learn about available commands")

    book = Book()

    while True:
        print("---------------")
        operation = input("What would you like to do? ")

        match operation:
            case "exit":
                print("-> thanks for using this application!")
                return
            case "help":
                print(
                    "-> available commands: [help, add, remove, find, edit, list, exit]"
                )

            case "add":
                name = input("-> name: ")
                number = input("-> number: ")

                conflict = book.insert(number, name)

                if conflict:
                    print(
                        "-> error: `{}` is already in the phonebook under a different name!".format(
                            number
                        )
                    )
                else:
                    print(
                        "-> added `{}` to the phonebook under the name `{}`".format(
                            number, name
                        )
                    )

            case "remove":
                number = input("-> number: ")

                if book.contains(number):
                    name = book.get(number)["name"]
                    print("number `{}` belongs to `{}`".format(number, name))
                    go_ahead = input(
                        "-> are you sure you want to remove this contact? (yes/no) "
                    )

                    if go_ahead == "yes":
                        book.remove(number)
                        print("-> removed `{}` from the phonebook".format(number))
                    else:
                        print("cancelled remove operations")
                else:
                    print("-> error: number is not currently in the phonebook")

            case "find":
                name = input("-> name: ")

                if book.contains(name):
                    number = book.get(name).number
                    print("-> the number of `{}` is `{}`".format(name, number))

            case "edit":
                name_or_number = input("-> edit (name or number): ")
                new_name_or_number = input("-> new name or number: ")

                error = book.update(name_or_number, new_name_or_number)

                if error:
                    print("-> error: failed to update contact (`{}`)".format(error))

            case "list":
                print("-> listing all contacts in the phonebook")
                for contact in book.contacts():
                    print("# {} - {}".format(contact["number"], contact["name"]))
            case other:
                print("-> error: unknown operation `{}`!".format(other))


if __name__ == "__main__":
    main()
