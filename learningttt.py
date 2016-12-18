#reinforcement learning test for tic-tac-toe
#I would like to thank you for giving me this task.
#Learning and implementing reinforcement learning has been incredibly rewarding


from random import random, randrange

class ai():
    def __init__(self,exp,step,smart=True):
        self.explore=exp
        self.stepsize=step
        self.statevalues=[]
        self.lastmove=[]
    #takes about 7 seconds (with smart initialization on a 2.2GHz Intel mobile processor, your milage may vary)
    #to initialize, would have been a nightmare if minimax is deployed
        for i in range(3**9):#between the ternary choice of "","X","O" on 9 piece
            state=indexinstate(i)
            q=0
            if smart:#initialize the empty array with statevalues with alpha-beta pruning behavior
                q=AB(state,"X")[2]
            else:#alternative, "dumb" initiation that gives it no knowledge of its surroundings
                r=win(state)
                if r=="X":
                    q=1
                elif r=="O":
                    q=-1
            self.statevalues+=[q]
            
    def ai(self,state,player):
        pstep=[];ostep=-1;ext=-999;m=1;op="O"
        if player=="O":
        #lazy hack for maximizing value. don't want aditional if statements
            m=-1
            op="X"
            ext=999
        for i in range(9):
            if state[i]=="":
                pstep+=[i]
                ts=state[:i]+[player]+state[(i+1):]
                sin=stateindex(ts)
                if (self.statevalues[sin])*m>ext*m:
                    ext=self.statevalues[sin]
                    ostep=i
        ts=[];step=0
        if random()>self.explore:
            i=randrange(0,len(pstep))
            step=pstep[i]
        else:
            step=ostep
        ts=state[:step]+[player]+state[(step+1):]
        if self.lastmove!=[] and self.lastmove[1]!=player:
            self.adapt(ts)
        self.lastmove=[ts,player]
        return [ts,(step%3,step//3)]

    def adapt(self,counter):
        idv=stateindex(counter)
        ind=stateindex(self.lastmove)
        self.statevalues[ind]+=self.stepsize*(self.statevalues[idv]-self.statevalues[ind])






def stateindex(state):#the other alternative would be a dictionary, which would be grossly inefficient
    index=0
    for i in range(len(state)):
        q=0
        if state[i]=="X":
            q=1
        elif state[i]=="O":
            q=2
        index+=q*3**i
    return index

def indexinstate(n):
    state=["","","","","","","","",""]
    for i in range(9):
        q=""
        m=(n%(3**(i+1)))//(3**i)
        if m==1:
            q="X"
        elif m==2:
            q="O"
        state[i]=q
    return state



def AB(S,player,alph=-999,bet=999):#light weight Alpha beta ported here to initialize the statevalues
        op="";index=-1;query=[];mm=0
        if player=="X":
                op="O"
                mm=-999
        elif player=="O":
                op="X"
                mm=999
        for i in range(9):
                if S[i]=="":
                        ss=S[:i]+[player]+S[i+1:]
                        v=AB(ss,op,alph,bet)
                        if player=="X" and mm<v[2]:
                                mm=v[2];index=i
                                if mm>alph:
                                        alph=mm
                        elif player=="O" and mm>v[2]:
                                mm=v[2];index=i
                                if bet>mm:
                                        bet=mm
                        if alph>=bet:
                                return [ss,player,mm,(index%3,index//3)]
        ss=S[:index]+[player]+S[index+1:]
        vic=win(ss)
        if vic=="X":
                return [ss,player,1,(index%3,index//3)]
        elif vic=="O":
                return [ss,player,-1,(index%3,index//3)]
        elif vic=="Draw":
                return [ss,player,0,(index%3,index//3)]
        return [ss,player,mm,(index%3,index//3)]




        
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

def display(state):#rendering
        print("> New state:\n")
        for i in range(3):
                print("------------------")
                print("|",state[i*3],"|",state[1+i*3],"|",state[2+i*3],"|")
                print("-------------------")

def game(state,xcpu,ocpu,tai):
        cont="Gameon" #spaceholder used to marginally shave off some processing time
        while cont=="Gameon":
                display(state)#rendering module. currently fashioned in ascii art
                (x,y)=getinput("X",xcpu, state, tai)#x,y coordinate
                state[y*3+x]="X"#converting x and ys of a 3x3 into linear sequence
                if xcpu!=ocpu and ocpu==True:
                    tai.adapt(state)
                cont=win(state)#checked everytime a move i made
                if cont!="Gameon":
                        break
                display(state)
                (x,y)=getinput("O",ocpu, state, tai)
                state[y*3+x]="O"
                if xcpu!=ocpu and xcpu==True:
                    tai.adapt(state)
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


def getinput(s, cpu, state, tai):#modular input sequence, with ai support as a parameter
        x,y=-1,-1
        while occupation(x,y,state):
                if cpu:
                        x,y=tai.ai(state,s)[1]
                        print(x,y)
                else:
                        try:
                                (x,y)=eval(input("> "+ s +" player's next move:\n"))
                        except:
                                x=-1
                                y=-1
        return (x,y)

def main():
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
    n=eval(input("Please enter the number of rounds you wish to play against the AI: "))
    tacnet=ai(0.2,0.5,True)
    for i in range(n):
        print("> New round.\n")
        game(statecpy(state),xcpu,ocpu,tacnet)


def statecpy(state):
    k=[]
    for i in range(len(state)):
        k+=[state[i]]
    return k


main()
   
