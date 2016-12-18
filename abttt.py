#much faster than the original minimax
#for covenience and performance reasons, empty deck strictly require empty string ""
#modified from my modular TreeBuildttt

def TreeBuildAB(S,player,alph=-999,bet=999):
        op="";index=-1;query=[];mm=0
        vic=win(S)
        if vic=="X":
                return [S,player,1,vic,[]]
        elif vic=="O":
                return [S,player,-1,vic,[]]
        elif vic=="Draw":
                return [S,player,0,vic,[]]
        if player=="X":
                op="O"
                mm=-999
        elif player=="O":
                op="X"
                mm=999
        for i in range(9):
                if S[i]=="":
                        ss=S[:i]+[player]+S[i+1:]
                        v=TreeBuildAB(ss,op,alph,bet)
                        query+=[v]
                        if player=="X" and mm<v[2]:
                                mm=v[2];index=i
                                if mm>alph:
                                        alph=mm
                        elif player=="O" and mm>v[2]:
                                mm=v[2];index=i
                                if bet>mm:
                                        bet=mm
                        if alph>=bet:
                                return [S,player,mm,(index%3,index//3),[]]
        ss=S[:index]+[player]+S[index+1:]
        return [S,player,mm,(index%3,index//3),query]


def game():
        xcpu=False
        ocpu=False
        gm = input("Select from 0 player simulation, 1 player mode and 2 player mode:\n")
        if "0" in gm:
                xcpu,ocpu=True,True
        elif "1" in gm:
                xcpu,ocpu=False,True
        elif "2" in gm:
                xcpu,ocpu=False,False
        ini=input("> Enter the initial state:\n")
        state=ini.split(",")#all the 9 spots in a linear sequencial order
        cont="Gameon" #spaceholder used to marginally shave off some processing time
        while cont=="Gameon":
                display(state)#rendering module. currently fashioned in ascii art
                (x,y)=getinput("X",xcpu, state)#x,y coordinate
                state[y*3+x]="X"#converting x and ys of a 3x3 into linear sequence
                cont=win(state)#checked everytime a move i made
                if cont!="Gameon":
                        break
                display(state)
                (x,y)=getinput("O",ocpu, state)
                state[y*3+x]="O"
                cont = win(state)
        display(state)
        if cont=="Draw":
                print("It's a draw. Well played.")
        else:
                print("Woe to the vanquished, for",cont,"player has triumphed")


def occupation(x,y,state):#checks if the coordinate is already occupied
        if x in [0,1,2] and y in [0,1,2] and state[y*3+x]=="":
                return False
        else:
                return True


def display(state):#rendering
        print("> New state:\n")
        for i in range(3):
                print("------------------")
                print("|",state[i*3],"|",state[1+i*3],"|",state[2+i*3],"|")
                print("-------------------")

def win(state):#check of all posssible ways to win or stalemate, returns the victor
        for i in range(3):
                if state[i*3]==state[i*3+1] and state[i*3]==state[i*3+2] and state[i*3]!="":
                        return state[i*3]
                if state[i]==state[3+i] and state[i]==state[6+i] and state[i]!="":
                        return state[i]
        if state[0]==state[4] and state[0]==state[8] and state[0]!="":
                return state[0]
        if state[4]==state[2] and state[4]==state[6] and state[4]!="":
                return state[4]
        for i in range(9):
                if state[i]=="":
                        return "Gameon"
        return "Draw"

def getinput(s, cpu, state):#modular input sequence, with ai support as a parameter
        x,y=-1,-1
        while occupation(x,y,state):
                if cpu:
                        x,y=TreeBuildAB(state,s)[3]
                        print(x,y)
                else:
                        try:
                                (x,y)=eval(input("> "+ s +" player's next move:\n"))
                        except:
                                x=-1
                                y=-1
        return (x,y)

game()
a=input()

