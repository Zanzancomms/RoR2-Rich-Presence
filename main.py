import copy
import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join('python', 'packages')))
sys.path.append(os.path.abspath(os.path.join('python')))
import psutil
import psutil._exceptions as ps_exceptions
from discoIPC import ipc


def main():
    Player_log_path = "{}\\AppData\\LocalLow\\Hopoo Games, LLC\\Risk of Rain 2\\Player.log".format(os.getenv('UserProfile'))

    start_time = int(time.time())
    activity = {'details': 'Loading game',  # this is what gets modified and sent to Discord via discoIPC
                'timestamps': {'start': start_time},
                'assets': {'small_image': ' ', 'small_text': 'Risk of Rain 2', 'large_image': 'logo', 'large_text': 'Risk of Rain 2'},
                'state': 'Not in lobby'}
    client_connected = False
    has_mention_not_running = False

    while True:
        game_is_running = False
        discord_is_running = False
        next_delay = 5

        for process in psutil.process_iter():
            if game_is_running and discord_is_running:
                break
            else:
                try:
                    with process.oneshot():
                        p_name = process.name()

                        if p_name == 'Risk of Rain 2.exe':
                            start_time = int(process.create_time())
                            activity['timestamps']['start'] = start_time
                            game_is_running = True
                        elif 'Discord' in p_name:
                            discord_is_running = True
                except ps_exceptions.NoSuchProcess:
                    pass
                except ps_exceptions.AccessDenied:
                    pass

                time.sleep(0.001)

        if game_is_running and discord_is_running:
            if not client_connected:
                # connects to Discord
                client = ipc.DiscordIPC('954183647328620554')
                client.connect()
                client_connected = True

            with open(Player_log_path, 'r', errors='replace') as Player_log:
                Player = Player_log.readlines()

            old_details_state = copy.copy((activity['details'], activity['state'], activity['assets']['small_image'], activity['assets']['small_text']))

            for line in Player:
                    
                if 'survivorIndex=8' in line:
                    activity['assets']['small_image'] = 'commando'
                    activity['assets']['small_text'] = 'Commando'

                if 'survivorIndex=10' in line:
                    activity['assets']['small_image'] = 'engineer'
                    activity['assets']['small_text'] = 'Engineer'

                if 'survivorIndex=12' in line:
                    activity['assets']['small_image'] = 'huntress'
                    activity['assets']['small_text'] = 'Huntress'

                if 'survivorIndex=16' in line:
                    activity['assets']['small_image'] = 'toolbot'
                    activity['assets']['small_text'] = 'MUL-T'

                if 'survivorIndex=14' in line:
                    activity['assets']['small_image'] = 'mage'
                    activity['assets']['small_text'] = 'Artificer'

                if 'survivorIndex=15' in line:
                    activity['assets']['small_image'] = 'merc'
                    activity['assets']['small_text'] = 'Mercenary'

                if 'survivorIndex=17' in line:
                    activity['assets']['small_image'] = 'treebot'
                    activity['assets']['small_text'] = 'REX'

                if 'survivorIndex=6' in line:
                    activity['assets']['small_image'] = 'bandit'
                    activity['assets']['small_text'] = 'Bandit'

                if 'survivorIndex=3' in line:
                    activity['assets']['small_image'] = 'sniper'
                    activity['assets']['small_text'] = 'Sniper'

                if 'survivorIndex=2' in line:
                    activity['assets']['small_image'] = 'han-d'
                    activity['assets']['small_text'] = 'HAN-D'

                if 'survivorIndex=3' in line:
                    activity['assets']['small_image'] = 'han-d'
                    activity['assets']['small_text'] = 'HAN-D'

                if 'survivorIndex=9' in line:
                    activity['assets']['small_image'] = 'acrid'
                    activity['assets']['small_text'] = 'Acrid'

                if 'survivorIndex=7' in line:
                    activity['assets']['small_image'] = 'captain'
                    activity['assets']['small_text'] = 'Captain'
                    
                if 'survivorIndex=18' in line:
                    activity['assets']['small_image'] = 'railgunner'
                    activity['assets']['small_text'] = 'Railgunner'

                if 'survivorIndex=19' in line:
                    activity['assets']['small_image'] = 'void_fiend'
                    activity['assets']['small_text'] = '「V??oid Fiend』'

                if 'survivorIndex=19' in line:
                    activity['assets']['small_image'] = 'void_fiend'
                    activity['assets']['small_text'] = '「V??oid Fiend』'
                    

                if 'Loaded scene' in line:
                    activity = switch_image_mode(activity)

                    if 'title' in line:
                        activity['details'] = "Main menu"
                        activity['state'] = "Not in lobby"
                    elif 'lobby loadSceneMode=Single' in line:
                        activity['details'] = "In lobby"
                        activity['state'] = "Singleplayer"
                    elif 'crystalworld' in line:
                        activity['state'] = "Prismatic Trials"

                    elif 'golemplains' in line:
                        activity = switch_image_mode(activity, ('golemplains', 'Golem Plains, Titanic Plains'))
                    elif 'blackbeach' in line:
                        activity = switch_image_mode(activity, ('blackbeach', 'Black Beach, Distant Roost'))
                    elif 'blackbeach2' in line:
                        activity = switch_image_mode(activity, ('blackbeach2', 'Black Beach, Distant Roost'))
                    elif 'goolake' in line:
                        activity = switch_image_mode(activity, ('goolake', 'Goo Lake, Abandoned Aqueduct'))
                    elif 'frozenwall' in line:
                        activity = switch_image_mode(activity, ('frozenwall', 'Frozen Wall, Rallypoint Delta'))
                    elif 'dampcavesimple' in line:
                        activity = switch_image_mode(activity, ('dampcavesimple', 'Tectonic Relics, Abyssal Depths'))
                    elif 'mysteryspace' in line:
                        activity = switch_image_mode(activity, ('mysteryspace', 'Hidden Realm: A Moment, Fractured'))
                    elif 'bazaar' in line:
                        activity = switch_image_mode(activity, ('bazaar', 'Hidden Realm: Bazaar Between Time'))
                    elif 'foggyswamp' in line:
                        activity = switch_image_mode(activity, ('foggyswamp', 'Foggy Swamp, Wetland Aspect'))
                    elif 'wispgraveyard' in line:
                        activity = switch_image_mode(activity, ('wispgraveyard', 'Wisp Graveyard, Scorched Acres'))
                    elif 'shipgraveyard' in line:
                        activity = switch_image_mode(activity, ('shipgraveyard', 'Ship Graveyard, Sirens Call'))
                    elif 'skymeadow' in line:
                        activity = switch_image_mode(activity, ('skymeadow', 'Sprite Fields, Sky Meadow'))
                    elif 'snowyforest' in line:
                        activity = switch_image_mode(activity, ('snowyforest', 'Siphoned Forest'))
                    elif 'sulfurpools' in line:
                        activity = switch_image_mode(activity, ('sulfurpools', 'Sulfur Pools'))
                    elif 'rootjungle' in line:
                        activity = switch_image_mode(activity, ('rootjungle', 'Root Jungle, Sundered Grove'))
                    elif 'ancientloft' in line:
                        activity = switch_image_mode(activity, ('ancientloft', 'Ancient Loft, Aphelian Sanctuary'))
                    elif 'moon' in line:
                        activity = switch_image_mode(activity, ('moon', 'Commencement , Moon of Petrichor V'))

                    elif 'lobby' in line:
                        activity = switch_image_mode(activity, ('lobby', 'Lobby'))
                    elif 'title' in line:
                        activity = switch_image_mode(activity, ('title', 'title'))

                elif 'lobby creation succeeded' in line:
                    activity['details'] = "In lobby"
                    activity['state'] = "Multiplayer"
                    activity = switch_image_mode(activity)
                elif 'Left lobby' in line:
                    activity['details'] = "Main menu"
                    activity['state'] = "Not in lobby"
                    activity = switch_image_mode(activity)
                    
                if 'survivorIndex=8' in line:
                    activity['assets']['small_image'] = 'commando'
                    activity['assets']['small_text'] = 'Commando'

                if 'survivorIndex=10' in line:
                    activity['assets']['small_image'] = 'engineer'
                    activity['assets']['small_text'] = 'Engineer'

                if 'survivorIndex=12' in line:
                    activity['assets']['small_image'] = 'huntress'
                    activity['assets']['small_text'] = 'Huntress'

                if 'survivorIndex=16' in line:
                    activity['assets']['small_image'] = 'toolbot'
                    activity['assets']['small_text'] = 'MUL-T'

                if 'survivorIndex=14' in line:
                    activity['assets']['small_image'] = 'mage'
                    activity['assets']['small_text'] = 'Artificer'

                if 'survivorIndex=15' in line:
                    activity['assets']['small_image'] = 'merc'
                    activity['assets']['small_text'] = 'Mercenary'

                if 'survivorIndex=17' in line:
                    activity['assets']['small_image'] = 'treebot'
                    activity['assets']['small_text'] = 'REX'

                if 'survivorIndex=6' in line:
                    activity['assets']['small_image'] = 'bandit'
                    activity['assets']['small_text'] = 'Bandit'

                if 'survivorIndex=3' in line:
                    activity['assets']['small_image'] = 'sniper'
                    activity['assets']['small_text'] = 'Sniper'

                if 'survivorIndex=2' in line:
                    activity['assets']['small_image'] = 'han-d'
                    activity['assets']['small_text'] = 'HAN-D'

                if 'survivorIndex=3' in line:
                    activity['assets']['small_image'] = 'han-d'
                    activity['assets']['small_text'] = 'HAN-D'

                if 'survivorIndex=9' in line:
                    activity['assets']['small_image'] = 'acrid'
                    activity['assets']['small_text'] = 'Acrid'

                if 'survivorIndex=7' in line:
                    activity['assets']['small_image'] = 'captain'
                    activity['assets']['small_text'] = 'Captain'
                    
                if 'survivorIndex=18' in line:
                    activity['assets']['small_image'] = 'railgunner'
                    activity['assets']['small_text'] = 'Railgunner'

                if 'survivorIndex=19' in line:
                    activity['assets']['small_image'] = 'void_fiend'
                    activity['assets']['small_text'] = '「V??oid Fiend』'

                if 'survivorIndex=19' in line:
                    activity['assets']['small_image'] = 'void_fiend'
                    activity['assets']['small_text'] = '「V??oid Fiend』'
                    




            if time.time() - start_time < 10:
                activity['details'] = "Loading game"

            if old_details_state != (activity['details'], activity['state'], activity['assets']['small_image'], activity['assets']['small_text']):
                next_delay = 2

            print(activity['details'])
            print(activity['state'])
            print(activity['assets']['small_image'])
            print(activity['assets']['small_text'])
            
            time_elapsed = time.time() - start_time
            print("{:02}:{:02} elapsed\n".format(int(time_elapsed / 60), round(time_elapsed % 60)))

            if not os.path.exists('history.txt'):
                open('history.txt', 'w').close()

            activity_str = f'{activity}\n'
            with open('history.txt', 'r') as history_file_r:
                history = history_file_r.readlines()
            if activity_str not in history:
                with open('history.txt', 'a') as history_file_a:
                    history_file_a.write(activity_str)

            # send everything to discord
            client.update_activity(activity)
        elif not discord_is_running:
            print("{}\nDiscord isn't running\n")
        else:
            if client_connected:
                try:
                    client.disconnect()  # doesn't work...
                except:
                    pass

                raise SystemExit  # ...but this does
            else:
                if not has_mention_not_running:
                    print("Risk of Rain 2 isn't running\n")
                    has_mention_not_running = True

            # to prevent connecting when already connected
            client_connected = False

        time.sleep(next_delay)


def switch_image_mode(temp_activity, stage=()):
    if stage == ():
        temp_activity['assets']['large_image'] = 'logo'
        temp_activity['assets']['large_text'] = 'Risk of Rain 2'
    else:
        temp_activity['assets']['large_image'] = stage[0]
        temp_activity['assets']['large_text'] = stage[1]
        temp_activity['details'] = stage[1]

    return temp_activity


if __name__ == '__main__':
    main()