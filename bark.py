import os
from tabulate import tabulate

import commands
from option import Option


def clear_screen():
    clear = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear)


def print_table(table):
    headers = ['ID', 'Title', 'URL', 'Notes', 'Date_added']
    return tabulate(table, headers=headers, tablefmt="psql")

def print_options(options):
    for shortcut, option in options.items():
        print(f'({shortcut}) ({option})')
        print()


def option_choice_is_valid(choice, options):
    return choice in options or choice.upper() in options


def get_option_choice(options):
    choice = input('Enter your choice: ')
    while not option_choice_is_valid(choice, options):
        print('Invalid choice!')
        choice = input('Enter your choice: ')
    return options[choice.upper()]


def get_user_input(label, required=True):
    value = input(f'{label}: ') or None
    while required and not value:
        value = input(f'{label}: ')
    return value


def get_add_bookmark_data():
    title = get_user_input('Title')
    url = get_user_input('URL')
    notes = get_user_input('Notes', required=False)
    return {'title': title, 'url': url, 'notes': notes}


def get_bookmark_id_for_deletion():
    return get_user_input('Enter a bookmark id to delete: ')


if __name__ == "__main__":
    options = {
        'A': Option('Add a bookmark', commands.AddBookmarkCommand(),
                    get_add_bookmark_data),
        'B': Option('List bookmarks by date',
                    commands.ListBookmarksCommand(),
                    printer=print_table),
        'T': Option('List bookmarks by title',
                    commands.ListBookmarksCommand('title'),
                    printer=print_table),
        'D': Option('Delete a bookmark', commands.DeleteBookmarkCommand(),
                    get_bookmark_id_for_deletion),
        'Q': Option('Quit', commands.QuitCommand())
    }
    clear_screen()
    print_options(options)
    chosen_option = get_option_choice(options)
    clear_screen()
    chosen_option.choose()
