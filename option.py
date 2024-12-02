class Option:
    def __init__(self, name, command, prep_call=None, printer=None):
        self.name = name
        self.command = command
        self.prep_call = prep_call
        self.printer = printer

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        message = self.command.execute(data) if data \
            else self.command.execute()
        message = self.printer(message) if self.printer else message
        print(message)

    def __str__(self):
        return self.name
