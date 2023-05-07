# TODO: Backend
import os
import sys
#import pexpect
#import winpexpect
import wexpect

def play_best(fen, moves, time):
    child = wexpect.spawn("stockfish-windows-2022-x86-64-avx2.exe")
    child.sendline("position startpos moves " + " ".join(moves))
    child.sendline(f"go movetime {time}")
    child.sendline("quit")
    out = child.read()
    return out.split("\n")[len(out.split("\n"))-2].split(" ")[1]

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
    child.sendline("d")
    child.sendline("quit")
    fen = child.read()
    print(fen)
    print(fen.split("Fen: ")[1].split("\n")[0])