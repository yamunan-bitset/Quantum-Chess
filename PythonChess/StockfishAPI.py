# TODO: Backend
import os
import sys
#import pexpect
#import winpexpect
import wexpect
import threading
import time


class Eval(threading.Thread):
    def __init__(self, fen):
        threading.Thread.__init__(self)

        self.fen = fen
        self.pos_eval = ""

        self.quit = False

    def load_fen(self, fen):
        self.fen = fen

    def kill(self):
        self.quit = True

    def run(self):
        while not self.quit:
            child = wexpect.spawn("stockfish-windows-2022-x86-64-avx2.exe")
            child.sendline("position fen " + self.fen)
            child.sendline("eval")
            child.sendline("quit")
            out = child.read()
            try:
                self.pos_eval = out.split("\n")[len(out.split("\n")) - 4].split(" ")[8]
            except:
                self.pos_eval = "+/#"

    

def play_best(fen, moves, time=None, depth=None):
    child = wexpect.spawn("stockfish-windows-2022-x86-64-avx2.exe")
    child.sendline("position startpos moves " + " ".join(moves))
    if time == None:
        child.sendline(f"go depth {depth}")
    else:
        child.sendline(f"go movetime {time}")

    child.expect("bestmove ")
    child.sendline("quit")

    out = child.read()
    print(out)
    try:
        return out.split("\n")[0].split(" ")[0]
    except:
        # TODO
        print(out)
        quit()

def get_next_fen(fen, moves):
    child = wexpect.spawn("stockfish-windows-2022-x86-64-avx2.exe")
    child.sendline("position startpos moves " + " ".join(moves))
    child.sendline("d")
    child.sendline("quit")
    out = child.read()
    print(out)
    new_fen = out.split("Fen: ")[1].split("\n")[0][:-1]
    print("Old FEN: " + fen)
    print("New FEN: " + new_fen)
    if new_fen == fen:
        return None
    return new_fen

def test():
    #print(os.popen("stockfish-windows-2022-x86-64-avx2.exe position startpos moves e2e4 d").read())
    child = wexpect.spawn("stockfish-windows-2022-x86-64-avx2.exe")
    child.sendline("position startpos moves")
    child.sendline("go movetime 5000")
    #time.sleep(5000)
    child.expect("bestmove ")
    child.sendline("quit")
    fen = child.read()
    print(fen)