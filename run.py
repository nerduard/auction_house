import line_parser as lp

print("==[      WELCOME  TO      ]==")
print("==[ THE AUCTION HOUSE APP ]==\n")

# User prompt in the terminal
while True:
    path = str(input("Enter path to input file or 'q' to quit: "))
    if path == 'q':
        break
    print('')
    # parse all the lines in the input file
    with open(path, "r") as file:
        for line in file:
            lp.parse_line(line)
        # clear listing collection dictionary for next input
        lp.lc.dict.clear()
    print('')

print("\n==[  APP WAS QUIT  ]==")