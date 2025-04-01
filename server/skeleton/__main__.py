import maquina

PORT = 35000
SERVER_ADDRESS = "localhost"

def main():
    maq = maquina.Maquina(SERVER_ADDRESS, PORT)
    maq.exec()

if __name__=="__main__":
    main()