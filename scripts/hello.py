
from scripts.config import TEAM_NAME

class Hello():

    @staticmethod
    def say_hello(prefix: str, **kwargs):
        print(f"Hello: " + prefix + f", gtreetings from {TEAM_NAME}")

def main():
    Hello.say_hello()

if __name__ == "__main__":
    main()