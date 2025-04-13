import maquina

PORT = 35001
SERVER_ADDRESS = "localhost"

def main():
    maq = maquina.Maquina(SERVER_ADDRESS, PORT)
    maq.exec()

if __name__=="__main__":
    main()