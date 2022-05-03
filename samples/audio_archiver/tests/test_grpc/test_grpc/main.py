import protogen
from client import audio

if __name__=="__main__":
    stub = audio._create_stub()
    print(stub)