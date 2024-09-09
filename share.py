import requests
import threading
import os
import time

def clear_console():
    if os.name == 'nt':  
        os.system('cls')
    else:  
    
        os.system('clear')

def display_logo():
    yellow = '\033[93m'  
    reset = '\033[0m'
    logo = """
██████╗ ███████╗ ██████╗██████╗ 
██╔══██╗██╔════╝██╔════╝██╔══██╗
██████╔╝█████╗  ██║     ██████╔╝
██╔══██╗██╔══╝  ██║     ██╔═══╝ 
██║  ██║██║     ╚██████╗██║     
╚═╝  ╚═╝╚═╝      ╚═════╝╚═╝     
                                
"""
    print(yellow + logo + reset)
    print("Welcome to RFCP TOOLS")


def get_user_inputs():
    global access_tokens, share_url, target_count
    access_tokens = [input('Enter your access token: ')]
    share_url = input('Enter the share URL: ')
    target_count = int(input('Enter the number of shares: '))


    clear_console()
    display_logo()


def print_status(token_index, shared_count, target_count):
    yellow = '\033[93m'
    reset = '\033[0m'
    print(f"{yellow}ℙ𝕠𝕤𝕥 𝕤𝕙𝕒𝕣𝕖𝕕 {shared_count} 𝑜𝑢𝑡 𝑜𝑓 {target_count}{reset}", end="")

delete_after = 60 * 60  

shared_count = 0
token_index = 0
sharing_active = True

def share_post():
    global shared_count, token_index, sharing_active
    if not sharing_active:
        return
    
    current_token = access_tokens[token_index]
    try:
        response = requests.post(
            f'https://graph.facebook.com/me/feed?access_token={current_token}&fields=id&limit=1&published=0',
            json={'link': share_url, 'no_story': True},
            headers={
                'authority': 'graph.facebook.com',
                'cache-control': 'max-age=0',
                'sec-ch-ua-mobile': '?0',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            }
        )

        shared_count += 1
        post_id = response.json().get('id')
        print_status(token_index, shared_count, target_count)
        print()  

        if shared_count >= target_count:
            print('𝕋𝕙𝕒𝕟𝕜𝕤 𝕗𝕠𝕣 𝕦𝕤𝕚𝕟𝕘 𝕃𝕖𝕚𝕟𝕒𝕥𝕙𝕒𝕟 𝕋𝕠𝕠𝕝𝕤')
            sharing_active = False
            if post_id:
                threading.Timer(delete_after, delete_post, args=[post_id]).start()

        
        token_index = (token_index + 1) % len(access_tokens)

    except requests.RequestException as e:
        print('Failed to share post:', e)

def delete_post(post_id):
    current_token = access_tokens[token_index]
    try:
        response = requests.delete(f'https://graph.facebook.com/{post_id}?access_token={current_token}')
        if response.status_code == 200:
            print(f'\nPost deleted: {post_id}')
        else:
            print(f'\nFailed to delete post: {response.status_code} - {response.text}')
    except requests.RequestException as e:
        print('Failed to delete post:', e)

def start_sharing():
    while sharing_active:
        share_post()
        time.sleep(0)  
display_logo()

while True:

    get_user_inputs()
    sharing_thread = threading.Thread(target=start_sharing)
    sharing_thread.start()
  
    sharing_thread.join()
    response = input('\nDo you want to share again? (yes/no): ').strip().lower()
    if response != 'yes':
        break

print('Exiting the program. Thank you for using RFCP TOOLS.')
