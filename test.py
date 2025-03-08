from SNEK2 import SNEKCallable, SNEKProgram

def main():
    with open("exp.snek") as f:
        source = f.read()
    
    program = SNEKProgram(source, {
        "barf": SNEKCallable(lambda: print("Eww, I just barfed!"), 0)
    })
    program.run()


if __name__ == "__main__":
    main()