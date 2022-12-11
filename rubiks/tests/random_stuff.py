# noinspection PyUnresolvedReferences
from rubiks.env.cube import RubiksCubeEnv
import gym

def main():
    import twophase.start_server as ss
    from threading import Thread
    bg = Thread(target=ss.start, args=(8080, 20, 2))
    bg.start()
    import twophase.client_gui

if __name__ == "__main__":
    main()
