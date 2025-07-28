from ui.interface import MainApp


main_app = MainApp()
app = main_app.app
server = main_app.server

if __name__ == '__main__':
    main_app.run(8054)