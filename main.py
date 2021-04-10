from models import Question
from models import Storage
from menu import MainMenu


def main():
    storage = Storage()
    storage.fill_storage()
    
    main_menu = MainMenu()
    main_menu.show()
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Bye!')