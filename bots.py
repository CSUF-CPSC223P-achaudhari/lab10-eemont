from time import sleep
import threading
import json

f = open('inventory.dat', 'r')
file_contents = json.load(f)
f.close()

def bot_clerk(item_list):
    # All of the items our bots gathered
    cart_list = []
    # Create a list of all bots to store which threads to run one by one
    bots = []
    # Make a list of thread locks for the bots to use
    locks = [threading.Lock(), threading.Lock(), threading.Lock()]
    
    # Simulates a bot grabbing an item for us
    def get_item(bot_id, item_id):
        with locks[bot_id]:
            sleep(file_contents[item_id][1])
            cart_list.append([item_id, file_contents[item_id][0]])
    
    # Generate threads for each bot with their task
    for i, id in enumerate(item_list):
        bot_thread = threading.Thread(target=get_item, args=(i%3, id))
        bots.append(bot_thread)
    
    # Start all the threads
    for bot in bots:
        bot.start()
    
    # Wait for all threads to finish
    for bot in bots:
        bot.join()
    
    # Return everything out bots got
    return cart_list

def bot_fetcher(item_list, cart_list, thread_lock):
    cart_list = cart_list[::-1]
    # Create a list of all bots to store which threads to run one by one
    bots = []
    
    # Simulates a bot grabbing an item for us
    def get_item(bot_id, item_id):
        with thread_lock:
            #print(f'Bot {bot_id} has gone to get item #{item_id}')
            #sleep(1)
            cart_list.append([item_id, file_contents[item_id][0]])
    
    # Generate threads for each bot with their task
    for i, id in enumerate(item_list):
        bot_thread = threading.Thread(target=get_item, args=(i%3+1, id))
        bots.append(bot_thread)
    
    # Start all the threads
    for bot in bots:
        bot.start()
    
    # Wait for all threads to finish
    for bot in bots:
        bot.join()
    
    # Return everything out bots got
    return cart_list