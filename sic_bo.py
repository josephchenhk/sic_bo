# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 17:30:57 2017

@author: joseph.chen
"""
#import sys
import random
import csv
import time

def random_pick(lst, weights):
    rand = random.random()
    cumprob = 0.0
    for n, w in enumerate(weights):
        cumprob += w
        if cumprob>=rand:
            return n, lst[n]
    

class Dice(object):
    
    ODD = {"total_score":
        {4: 50,
         5:	18,
         6:	14,
         7:	12,
         8:	8,
         9:	6,
         10: 6,
         11:6,
         12: 6,
         13: 8,
         14: 12,
         15: 14,
         16: 18,
         17: 50
         },
         
         "dice_combination":
        {"1,2": 5,
         "1,3": 5,
         "1,4": 5,  
         "1,5": 5,
         "1,6": 5,
         "2,3": 5,
         "2,4": 5,
         "2,5": 5,
         "2,6": 5,
         "3,4": 5,
         "3,5": 5,
         "3,6": 5,
         "4,5": 5,
         "4,6": 5,
         "5,6": 5
         },
         
         "specific_doubles":
        {1:	8,
         2:	8,
         3:	8,
         4:	8,
         5:	8,
         6:	8
         },
         
         "specific_triples":
        {1:	150,
         2:	150,
         3:	150,
         4:	150,
         5:	150,
         6:	150
         },
         
         "any_triple":
        {"1/2/3/4/5/6": 24
         },
         
         "specific_score":
        {1:{1:1, 2:2, 3:3},    
         2:{1:1, 2:2, 3:3},  
         3:{1:1, 2:2, 3:3},
         4:{1:1, 2:2, 3:3},  
         5:{1:1, 2:2, 3:3},  
         6:{1:1, 2:2, 3:3}
         }
    }
        
    WEIGHT_X2 = {"total_score":
        {4: 49,
         5:	370,
         6:	102,
         7:	15,
         8:	22,
         9:	44,
         10: 22,
         11: 22,
         12: 44,
         13: 22,
         14: 15,
         15: 102,
         16: 370,
         17: 49
         },
         
         "dice_combination":
        {"1,2": 36,
         "1,3": 36,
         "1,4": 36,  
         "1,5": 36,
         "1,6": 36,
         "2,3": 36,
         "2,4": 36,
         "2,5": 36,
         "2,6": 36,
         "3,4": 36,
         "3,5": 36,
         "3,6": 36,
         "4,5": 36,
         "4,6": 36,
         "5,6": 36
         },
         
         "specific_doubles":
        {1: 123,
         2:	123,
         3:	123,
         4:	123,
         5:	123,
         6:	123
         },
         
         "specific_triples":
        {1:	52,
         2:	52,
         3:	52,
         4:	52,
         5:	52,
         6:	52
         },
         
         "any_triple":
        {"1/2/3/4/5/6": 102
         },
         
         "specific_score":
        {1: 10,    
         2: 10,  
         3: 10,
         4: 10,  
         5: 10,  
         6: 10
         }
    }
    
    WEIGHT_NUM_X2 = {9: 0.2142,
                     10: 0.2138,
                     11: 0.2128,
                     12: 0.1764,
                     13: 0.1828}
    
    def __init__(self):
        item_list, item_occur, item_odd = self.prepare_item_lists()
        self.item_list = item_list
        self.item_occur = item_occur
        self.item_odd = item_odd
    
    def pick_x2_number(self):  
        _, x2_number = random_pick(list(self.WEIGHT_NUM_X2.keys()), 
                           list(self.WEIGHT_NUM_X2.values())
                           )
        return x2_number

    def prepare_item_lists(self):
        """Prepare the initial `item names`, `item occurance`, and `item odd`
        Note: `item odd` has included the wager (+1)
        """
        item_list = []
        item_occur = []
        item_odd = [] # include wager
        for item_cat in self.WEIGHT_X2:
            for item_choice in self.WEIGHT_X2[item_cat]:
                item_list.append(item_cat+":"+str(item_choice))
                item_occur.append(self.WEIGHT_X2[item_cat][item_choice])
                odd = self.ODD[item_cat][item_choice]
                if type(odd)==int: # currently all odds are given as integers
                    odd += 1 # include the wager
                elif type(odd)==dict: # for specific score
                    odd2 = {}
                    for k,v in odd.items():
                        odd2[k] = v + 1 # include the wager
                    odd = odd2
                item_odd.append(odd)
        return item_list, item_occur, item_odd
    
    def get_x2_items(self, x2_number):
        """Randomly select items to apply x2 effects.
        """
        item_list = self.item_list[:]
        item_occur = self.item_occur[:]
        x2_items = []
        for _ in range(x2_number):
            sum_occur = sum(item_occur)
            item_weight = [w*1.0/sum_occur for w in item_occur]
            n, item = random_pick(item_list, item_weight)
            # item was chosen
            x2_items.append(item)            
            # remove the item in occurance list
            del item_list[n]
            del item_occur[n]
        return x2_items
    
    def apply_x2_effects(self, x2_items):
        """Apply x2 effects to the odds of selected items.
        """
        item_odd = self.item_odd
        item_list = self.item_list
        x2_item_odd = item_odd[:]
        for item in x2_items:
            n = item_list.index(item)
            # update x2_item_odd
            if "specific_score" in item:
                odd2 = {}
                odd = item_odd[n]
                for k,v in odd.items():
                    odd2[k] = v * 2
                odd = odd2
            else:
                odd = item_odd[n] * 2
            x2_item_odd[n] = odd
        return x2_item_odd

    def roll(self):
        """Roll and get outcomes of the three dices
        """
        dice_face = [1,2,3,4,5,6]
        dice_prob = [1./6]*6
        _, self.d1 = random_pick(dice_face, dice_prob)
        _, self.d2 = random_pick(dice_face, dice_prob)
        _, self.d3 = random_pick(dice_face, dice_prob)
        
    def play(self):
        """Play the game for one time and return the payment dict.
        """
        # Firstly, we need to determine the number of x2 in this round.
        x2_number = self.pick_x2_number()
        
        # next, we need to randomly pick up the x2 items according to their 
        # weights dynamically.
        # Construct different items, and their corresponding weight numbers
        item_list, item_occur, item_odd = self.prepare_item_lists() # include wager              
        # 2.2 Dynamically choose the items and apply x2 effects.
        x2_items = self.get_x2_items(x2_number)
        x2_item_odd = self.apply_x2_effects(x2_items)
        
        # Thirdly, we roll the dice now
        self.roll()
        outcome = [self.d1, self.d2, self.d3]
        
        # Finally, we check the results
        hit_outputs = []
        payment = {}        
        for item in self.item_list:
            payment[item] = 0
        ## check total score
        total_score = self.d1 + self.d2 + self.d3
        if (total_score>3 and total_score<18):
            hit = "total_score:{}".format(total_score)
            hit_outputs.append(hit)
        ## check dice combination
        for comb in self.ODD["dice_combination"]:
            c1, c2 = [int(d) for d in comb.split(",")]
            if ((c1 in outcome) and (c2 in outcome)):
                hit = "dice_combination:{},{}".format(c1,c2)
                hit_outputs.append(hit)
        ## check specific_doubles
        duplicates = set([x for x in outcome if outcome.count(x) > 1])
        for d in duplicates:
            hit = "specific_doubles:{}".format(d)
            hit_outputs.append(hit)
        ## check specific triples and any triples
        if (self.d1==self.d2 and self.d2==self.d3):
            hit = "specific_triples:{}".format(self.d1)
            hit_outputs.append(hit)
            hit = "any_triple:1/2/3/4/5/6"
            hit_outputs.append(hit)
        ## check specific score
        specific_score_occur = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
        for score in specific_score_occur:
            if (score in outcome):
                specific_score_occur[score] += outcome.count(score)
                hit = "specific_score:{}".format(score)
                hit_outputs.append(hit)          
        ## update payments
        for hit in hit_outputs:
            n = self.item_list.index(hit)
            if "specific_score" in hit:
                score = int(hit.split(":")[1])
                occur = specific_score_occur[score]
                odd = x2_item_odd[n][occur]
            else:
                odd = x2_item_odd[n]
            payment[hit] += odd
#        print(self.d1, self.d2, self.d3)
#        print(payment)
        return payment
        
        
    def run_sim(self, N):
        """Run N times simulations to output the payment to csv
        """
        # Initialize payment 
        payment = {} 
        for item in self.item_list:
            payment[item] = 0
        # Play the game N times
        n = 0
        while n<N:
            pmt = self.play()
            # update payment book
            for item in payment:
                payment[item] += pmt[item]
            n += 1
#        print(payment)
        
        # Output the results to csv
        with open("output.csv", "w") as f:
            w = csv.writer(f, lineterminator='\n') # csv.writer(sys.stderr)
            w.writerows(payment.items())
            
        
if __name__=="__main__":
    dice = Dice()
    #payment = dice.play()
    tic = time.time()
    dice.run_sim(10000000)
    toc = time.time()
    print("Elapsed time: {:.3f}".format(toc-tic))