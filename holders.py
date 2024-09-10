from move_eggs import move_egg_out, hatch
from time import sleep

class egg_holder():
    def __init__(self): 
        self.holder = {
            'pos1': {'is_empty': True, 'pred': None, 'timer': None},
            'pos2': {'is_empty': True, 'pred': None, 'timer': None},
            'pos3': {'is_empty': True, 'pred': None, 'timer': None},
            'pos4': {'is_empty': True, 'pred': None, 'timer': None},
            'pos5': {'is_empty': True, 'pred': None, 'timer': None},
            'pos6': {'is_empty': True, 'pred': None, 'timer': None},
            'pos7': {'is_empty': True, 'pred': None, 'timer': None},
            'pos8': {'is_empty': True, 'pred': None, 'timer': None},
            'pos9': {'is_empty': True, 'pred': None, 'timer': None}
        }
        self.action_queue = [None] * 10
        self.curr_action_queue = 0
        self.front_action_queue = 0 
        self.tail_action_queue = 0 

        
    def enqueue(self,pos,action):
        if (self.tail_action_queue +1)% len(self.action_queue) == self.front_action_queue : 
            raise ValueError("queue is full!! there is an error in the enqueueing of the circular queue")
        else:
            self.action_queue[self.tail_action_queue] = (pos,action) 
            self.tail_action_queue = (self.tail_action_queue + 1) % len(self.action_queue)
            print(self.tail_action_queue)
            
    def dequeue(self):
        if self.tail_action_queue == self.front_action_queue : 
            print("queue is empty!!")
        else :
            pos = self.action_queue[self.front_action_queue][0]
            action = self.action_queue[self.front_action_queue][1]
            self.front_action_queue = (self.front_action_queue + 1) % len(self.action_queue)
            return (pos,action)
                
    def add_egg(self,pos): 
        self.holder[f'pos{pos}'] = { 
        'is_empty' : False ,
        'pred' : True ,
        'timer' :0.4 # 345600 # 4 days * 24 hours * 60 min * 60 sec
        }
        
    def remove_egg(self,pos): 
        self.holder[f'pos{pos}'] = { 
        'is_empty' : True ,
        'pred' : None ,
        'timer' : 0
        }
        
    def check_eggs(self):
        """checks all egges for their prediction state , if an egg'd pred is false it adds it to queue in (position , action ) format 
        where the action is "move_out" string 
        if the egg slot is empty, the function skips that slot 
        """
        for pos in range(1,10):
            if self.holder[f'pos{pos}']['is_empty'] == True:
                pass
            elif self.holder[f'pos{pos}']['pred'] == False:
                
                    # self.enqueue(pos,"move_out")
                    # self.remove_egg(pos)
                try : 
                    self.enqueue(pos,"move_out")
                    self.remove_egg(pos)
                except : 
                    # self.dequeue()
                    print('need to dequeue')
                    
                
    def update_eggs_time(self):
        """decreses the timer for all eggs by 100 ms , if an egg's timer is reduced to less than zero , it is added to queue in (position , action ) format 
        where the action is "hatch" string 
        if the egg slot is empty, the function  skips that slot 
        """
        for pos in range(1,10):
            # print(pos)
            if self.holder[f'pos{pos}']['is_empty'] == True:
                continue
            self.holder[f'pos{pos}']['timer'] -= 0.1
            print(f"time at {pos} is {self.holder[f'pos{pos}']['timer']}")
            if self.holder[f'pos{pos}']['timer'] < 0:
                
                #     self.enqueue(pos,"hatch")
                #     self.remove_egg(pos)
                try : 
                    self.enqueue(pos,"hatch")
                    self.remove_egg(pos)
                except : 
                    # self.dequeue()
                    print('need to dequeue')


if __name__ == "__main__" : 
    inc_holder = egg_holder()
    for i in range(1,10):
        inc_holder.add_egg(i)
    while True :
        inc_holder.check_eggs()
        inc_holder.update_eggs_time()
        try :
            (pos, action) = inc_holder.dequeue()
            
            if action == "hatch":
                hatch(pos,None)
            elif action == "move_out":
                move_egg_out(pos,None)
        except :   
            sleep(1)

        
            
