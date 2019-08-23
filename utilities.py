import sys
def convert_to_decimal(x, y, z):
  print x,y,z
  n= (36*(z-1))+(6*(y-1))+(x-1)
  print(n)
  if n >= 200: 
    return "Out of range, rerolling..."
  else:
    result = int(n/2)
    return str(result+100)[1:]

def get_info_lines(index):
    msg = []
    if index == 0:
        msg.append('This machine generates two random digits')
        msg.append('for every roll of three six-sided dice.  It')
        msg.append('uses Python and OpenCV to count and group')
        msg.append('the pips on each die.')
        msg.append('')
    elif index == 1:
        msg.append('Each time the dice are spun, they are each')
        msg.append('treated as a digit in a base-6 number, for')
        msg.append('a possible total of 6*6*6=216.  This number')
        msg.append('is divided in half, for a possible total of')
        msg.append('108.  Anything greater than 100 isn\'t used.')
    elif index == 2:
        msg.append('This is necessary to keep the distribution')
        msg.append('of the random digits even.  Each pair of new')
        msg.append('digits is appended to a file, which is online')
        msg.append('and updated nightly.')
        msg.append('')
    elif index == 3:
        msg.append('Because of the noise the machine generates')
        msg.append('it doesn\'t run during classtime.')
        msg.append('The goal of creating this machine is to')
        msg.append('create a random number one million digits')
        msg.append('long!')
    elif index == 99:
        msg.append('This machine rolls dice to generate a large')
        msg.append('random number.  ')
        msg.append('Because of the noise the machine generates')
        msg.append('it doesn\'t run during classtime.')
        msg.append('Check back later to see it in action!')
        msg.append('')
        msg.append('')
        msg.append('')
        msg.append('')
    return msg
 
def get_stat_lines(lastDigits):
    msg = []
    msg.append("LAST TWENTY DIGITS: " + ''.join(lastDigits))
    with open('random.txt') as infile:
        lines=0
        words=0
        characters=0
        for line in infile:
            wordslist=line.split()
            lines=lines+1
            words=words+len(wordslist)
            characters += sum(len(word) for word in wordslist)
        msg.append("DIGITS GENERATED SO FAR: " + str(characters))
    return msg
