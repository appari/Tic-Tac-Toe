import random
import datetime
import copy
import collections

class Team57:

    def __init__(self):
        self.arr= [0.2,1,2,7,27]
        self.dict = {}
        self.timeLimit = datetime.timedelta(seconds = 14.5)
        self.uh_pos = [(1,1),(2,2),(1,2),(2,1)]
        self.h_pos = [(0,1),(0,2),(1,0),(2,0),(3,1),(3,2),(2,3),(1,3)]
        self.l_pos = [(0,0),(3,3),(0,3),(3,0)]
        self.begin = 0
        self.values = {}
        
        
    def timeout(self):
        if datetime.datetime.utcnow() - self.begin > self.timeLimit:
            return True
        return False


    def minimax(self,old_move, depth, max_depth, alpha, beta, isMax, p_board, p_block, flag1, best_node):
        if self.timeout():
            return (0,(-1,-1))
        terminal_state = p_board.find_terminal_state()
        if terminal_state[1] == 'WON' :
            if terminal_state[0] == flag1 :
                return (1000,old_move)
            elif terminal_state[0] == self.notflag(flag1)  :
                return (-1000,old_move)

        if depth==max_depth:
            utility = self.check_utility(p_block,p_board,flag1,depth)
            return (utility,old_move)
        else:
            children_list = p_board.find_valid_move_cells(old_move)
            # if random.randint(1,4) == 2:
            #random.shuffle(children_list)
            if len(children_list) == 0:
                utility = self.check_utility(p_block,p_board,flag1,depth)
                return (utility,old_move)
                
            
            for child in children_list:
                if isMax:
                    x=0
                    p_board.update(old_move,child,flag1)
                    if p_board.block_status[child[0]%4][child[1]%4]!='-':
                        x=-0.01
                    score = self.minimax (child,depth+1,max_depth,alpha,beta,False,p_board,p_block,flag1,best_node)
                    if self.timeout():
                        p_board.block_status[child[0]/4][child[1]/4] = '-'
                        p_board.board_status[child[0]][child[1]] = '-'
                        return (0,(-1,-1))
                    if (score[0]+x > alpha):
                        best_node = child
                        alpha = score[0] +x
                else:
                    x=0
                    p_board.update(old_move,child,self.notflag(flag1))
                    if p_board.block_status[child[0]%4][child[1]%4]!='-':
                        x=0.01
                    score = self.minimax (child,depth+1,max_depth,alpha,beta,True,p_board,p_block,flag1,best_node)
                    if self.timeout():
                        p_board.block_status[child[0]/4][child[1]/4] = '-'
                        p_board.board_status[child[0]][child[1]] = '-'
                        return (0,(-1,-1))
                    if (score[0] + x < beta):
                        best_node = child
                        beta = score[0] + x
                p_board.block_status[child[0]/4][child[1]/4] = '-'
                p_board.board_status[child[0]][child[1]] = '-'
                if (beta <= alpha):
                    break
        if not isMax:
            return (beta, best_node)
        else:
            return(alpha, best_node)

    def check_utility(self,block,board,flag,depth) :
        ans = 0
        ans += 10*self.block_utility(board.block_status,flag) - 0.01*depth
        ans -= 10*self.block_utility(board.block_status,self.notflag(flag))+0.01*depth
        for i in range(0,4):
            for j in range(0,4):
                if(board.block_status[i][j] == flag and self.is_centre(i,j)):
                    ans += (self.arr[4]-7)*3/2
                elif(board.block_status[i][j] == flag and self.is_corner(i,j)):
                    ans += (self.arr[4]-7)*4/3
                elif(board.block_status[i][j] == flag):
                    ans += (self.arr[4]-7)
                elif(board.block_status[i][j] == self.notflag(flag) and self.is_centre(i,j)):
                    ans -= (self.arr[4]-7)*3/2
                elif(board.block_status[i][j] == self.notflag(flag) and self.is_corner(i,j)):
                    ans -= (self.arr[4]-7)*4/3
                elif(board.block_status[i][j] == self.notflag(flag)):
                    ans -= (self.arr[4]-7)
                elif(board.block_status[i][j] == '-'):
                    temp = [[0 for y in range(4)] for x in range(4)]
                    for x in range(4):
                        for y in range(4):
                            temp[x][y]=board.board_status[4*i+x][4*j+y] 
                    ans += self.block_utility(temp,flag)
                    ans -= self.block_utility(temp,self.notflag(flag))
        
        return ans

    def is_centre(self,row, col):
        if row == 1 and col == 1:
            return 1
        if row == 1 and col == 2:
            return 1
        if row == 2 and col == 1:
            return 1
        if row == 2 and col == 2:
            return 1
        return 0

    def is_corner(self,row, col):
        if row == 0 and col == 0:
            return 1
        if row == 0 and col == 3:
            return 1
        if row == 3 and col == 0:
            return 1
        if row == 3 and col == 3:
            return 1
        return 0

    def move(self,board,old_move,flag1) :
        self.timeLimit = datetime.timedelta(seconds = 14.8)
        self.begin = 0
        self.begin = datetime.datetime.utcnow()
        temp_board = copy.deepcopy(board)
        maxDepth = 3
        while not self.timeout():
            (g,g_node) = self.minimax(old_move,0,maxDepth,-100000000,100000000,True,temp_board, (1,1), flag1, (7,7))
            if g_node != (-1,-1) :
                best_node = g_node
            maxDepth += 1
        return best_node

    
    def notflag(self,flag):
        if flag=='o':
            return 'x'
        else:
            return 'o'

    def block_utility(self,block,flag):
        block_1 = tuple([tuple(block[i]) for i in range(4)])
        if (block_1, flag) not in self.dict:
            ans = 0
            for col in range(4):
                countflag = 0
                opponentflag = 0
                for row in range(4):
                    if(block[row][col] == flag):
                        countflag += 1
                    elif((block[row][col] == self.notflag(flag)) or (block[row][col] == 'd')):
                        opponentflag += 1
                if opponentflag == 0:
                    if countflag ==2:
                        ans+=self.arr[2]
                    elif countflag ==3:
                        ans+=self.arr[3]
                    elif countflag ==4:
                        ans+=self.arr[4]
                countflag =0
                opponentflag =0
                for row in range(4):
                    if(block[col][row] == flag):
                        countflag += 1
                    elif((block[col][row] == self.notflag(flag)) or (block[col][row] == 'd')):
                        opponentflag += 1
                if opponentflag == 0:
                    if countflag ==2:
                        ans+=self.arr[2]
                    elif countflag ==3:
                        ans+=self.arr[3]
                    elif countflag ==4:
                        ans+=self.arr[4]
                        
            for v_diam in range(0,2):
                for h_diam in range(1,3):
                    countflag = 0
                    opponentflag = 0
                    if(block[v_diam][h_diam] == flag):
                        countflag+=1
                        if(block[v_diam+1][h_diam-1] == flag):
                            countflag+=1
                        elif((block[v_diam+1][h_diam-1] == self.notflag(flag)) or (block[v_diam+1][h_diam] == 'd')):
                            opponentflag+=1
                        if(block[v_diam+1][h_diam+1] == flag):
                            countflag+=1
                        elif((block[v_diam+1][h_diam+1] == self.notflag(flag)) or (block[v_diam+1][h_diam+1] == 'd')):
                            opponentflag+=1
                        if(block[v_diam+2][h_diam] == flag):
                            countflag+=1
                        elif((block[v_diam+2][h_diam] == self.notflag(flag)) or (block[v_diam+2][h_diam] == 'd')):
                            opponentflag+=1
                    elif((block[v_diam][h_diam] == self.notflag(flag)) or (block[v_diam+2][h_diam] == 'd')):
                        opponentflag+=1
                    if opponentflag == 0:
                        if countflag ==2:
                            ans+=self.arr[2]
                        elif countflag ==3:
                            ans+=self.arr[3]
                        elif countflag ==4:
                            ans+=self.arr[4]
            for pos in self.uh_pos:
                if block[pos[0]][pos[1]] == flag:
                   ans +=self.arr[0]

            for pos in self.h_pos:
                if block[pos[0]][pos[1]]==flag:
                    ans += self.arr[0]*0.8

            for pos in self.l_pos:
                if block[pos[0]][pos[1]]==flag:
                    ans += self.arr[0]*0.5                   

            self.dict[(block_1, flag)] = ans
            return self.dict[(block_1, flag)]

        else :
            return self.dict[(block_1, flag)]
