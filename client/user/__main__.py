from client.stub import interface
import user

# PORT e SERVER ADDRESS
PORT = 35000
SERVER_ADDRESS = "localhost"

def main():
    inter = interface.Interface(SERVER_ADDRESS, PORT)
    utilizador = user.User(inter)
    #inter.exec()
    utilizador.exec()

if __name__=="__main__":
    main()

