# Mode60
# ======================================================================================================================
# Title.............: 'Super DuckHunt'
# Filename..........: duckhunt.py
# Version...........: 1.9.9 (v1.1.4 ported to zcore) prototype for 2.0.0
# Author............: Mode60
# Description.......: zCore plugin adaptation of Super DuckHunt Bot. '' Super DuckHunt II ''
# Remarks...........: This is the second version generation of the Super DuckHunt IRC bot series.
# ======================================================================================================================
# Port Notes: Some things from the original Super DuckHunt just won't work with zCore. This was expected.
#             Some functions/features had to be rewritten. Other functions/features were modified from their
#             original form in v1.1.4
#             The port's aspiration is to be similar to v1.1.4 but with zcore capabilities of multi-net/chan
#             v1.9.9 will consist of the ported v1.1.4, then building off v1.9.9 with new features and code for v2.0.0
#             v1.9.9 will also contain new i18n support for translators.
import sys_zcore as pc
import asyncio
import logging
# import duckbot as bot  # ported bot.py
import threading  # for duck timer

rdata = {}  # main data map

# set up logging -------------------------------------------------------------------------------------------------------
logging.basicConfig(filename='./zcorelog.txt', level=logging.DEBUG)  # For debug logging
rdata['debuglog'] = 'on'  # turn 'on' for testing, otherwise 'off'

# zCore plugin check
def plugin_chk_():
    return True

# zCore system req check
def system_req_():
    return 'sys_zcore'

# Exit plugin
def plugin_exit_():
    global rdata
    mprint(f'Shutting down...')
    rdata = {}
    return

# Main print
def mprint(string):
    global rdata

    # printing to screen
    if rdata['moduleprint'] is True:
        print(f'[DuckHunt] * {string}')

    # debug logging
    if rdata['debuglog'] is True:
        logging.debug(f'[DuckHunt] * {string}')
    return

# Module init (start up)
def plugin_init_():
    global rdata

    rdata['ptitle'] = 'Super DuckHunt'
    rdata['pversion'] = '1.9.9'  # This is v1.1.4 ported to zCore, the prototype for 2.0.0
    rdata['pauthor'] = 'Mode60'
    rdata['mreqver'] = '0.1x'
    rdata['moduleprint'] = True
    rdata['serverlist'] = pc.cnfread('duckhunt.cnf', 'duckhunt', 'serverlist').lower()
    rdata['server'] = rdata['serverlist'].split(',')

    for x in range(len(rdata['server'])):
        server = rdata['server'][x]
        rdata[server, 'channels'] = pc.cnfread('duckhunt.cnf', server, 'channels').lower()
        rdata[server, 'channel'] = rdata[server, 'channels'].split(',')
        rdata[server, 'botname'] = pc.cnfread('zcore.cnf', server, 'botname')
        for z in range(len(rdata[server, 'channel'])):
            chan = rdata[server, 'channel'][z].replace('#', '')
            rdata[server, chan] = {}
            # ###########################################################################
            rdata[server, chan]['duckhunt'] = True  # Auto Start DuckHunt True or False
            # ###########################################################################
            rdata[server, chan]['game'] = False  # Do not change
            rdata[server, chan]['kick'] = False
            rdata[server, chan]['rules'] = pc.cnfread('duckhunt.cnf', server + '_' + chan, 'rules')
            rdata[server, chan]['maxducks'] = int(pc.cnfread('duckhunt.cnf', server + '_' + chan, 'maxducks'))
            rdata[server, chan]['spawntime'] = int(pc.cnfread('duckhunt.cnf', server + '_' + chan, 'spawntime'))
            rdata[server, chan]['flytime'] = int(pc.cnfread('duckhunt.cnf', server + '_' + chan, 'flytime'))
            rdata[server, chan]['duckexp'] = int(pc.cnfread('duckhunt.cnf', server + '_' + chan, 'duckexp'))
            rdata[server, chan]['duckfear'] = int(pc.cnfread('duckhunt.cnf', server + '_' + chan, 'duckfear'))
            rdata[server, chan]['duckgold'] = int(pc.cnfread('duckhunt.cnf', server + '_' + chan, 'duckgold'))
            rdata[server, chan]['friendrate'] = int(pc.cnfread('duckhunt.cnf', server + '_' + chan, 'friendrate'))
            rdata[server, chan]['relays'] = pc.cnfread('duckhunt.cnf', server + '_' + chan, 'relays').lower()
            rdata[server, chan]['rules'] = pc.cnfread('duckhunt.cnf', server + '_' + chan, 'rules').lower()
            rdata[server, chan]['top_shot'] = pc.cnfread('duckhunt.cnf', server + '_' + chan, 'top_shot').lower()
            rdata[server, chan]['timer'] = '0'
            rdata[server, chan]['thread'] = ''
            rdata[server, chan]['duck'] = {}
            rdata[server, chan]['gun_grease'] = pc.cnfread('duckhunt.cnf', server + '_' + chan, 'gun_grease')
            rdata[server, chan]['silencer'] = pc.cnfread('duckhunt.cnf', server + '_' + chan, 'silencer')
            rdata[server, chan]['lucky_charm'] = pc.cnfread('duckhunt.cnf', server + '_' + chan, 'lucky_charm')
            rdata[server, chan]['sunglasses'] = pc.cnfread('duckhunt.cnf', server + '_' + chan, 'sunglasses')
            rdata[server, chan]['trigger_lock'] = pc.cnfread('duckhunt.cnf', server + '_' + chan, 'trigger_lock')
            rdata[server, chan]['bread_lock'] = pc.cnfread('duckhunt.cnf', server + '_' + chan, 'bread_lock')
            rdata[server, chan]['accident_insurance'] = pc.cnfread('duckhunt.cnf', server + '_' + chan, 'accident_insurance')
            rdata[server, chan]['rain_coat'] = pc.cnfread('duckhunt.cnf', server + '_' + chan, 'rain_coat')
            rdata[server, chan]['duck_bomb'] = pc.cnfread('duckhunt.cnf', server + '_' + chan, 'duck_bomb')
            rdata[server, chan]['bombed'] = pc.cnfread('duckhunt.cnf', server + '_' + chan, 'bombed')
            rdata[server, chan]['bedazzled'] = pc.cnfread('duckhunt.cnf', server + '_' + chan, 'bedazzled')
            rdata[server, chan]['soggy'] = pc.cnfread('duckhunt.cnf', server + '_' + chan, 'soggy')
            rdata[server, chan]['expl_ammo'] = pc.cnfread('duckhunt.cnf', server + '_' + chan, 'expl_ammo')
            rdata[server, chan]['popcorn'] = pc.cnfread('duckhunt.cnf', server + '_' + chan, 'popcorn')
            rdata[server, chan]['sabotage'] = pc.cnfread('duckhunt.cnf', server + '_' + chan, 'sabotage')
            rdata[server, chan]['duck_jam'] = pc.cnfread('duckhunt.cnf', server + '_' + chan, 'duck_jam')
            rdata[server, chan]['confiscated'] = pc.cnfread('duckhunt.cnf', server + '_' + chan, 'confiscated')
            rdata[server, chan]['disarmed'] = pc.cnfread('duckhunt.cnf', server + '_' + chan, 'disarmed')
            rdata[server, chan]['jammed'] = pc.cnfread('duckhunt.cnf', server + '_' + chan, 'jammed')
            rdata[server, chan]['fear_factor'] = False  # do not change

            for y in range(rdata[server, chan]['maxducks']):
                rdata[server, chan]['duck'][y] = '0'
                continue
            continue
            # y = 0
            # mxdk = rdata[server, chan]['maxducks'] - 1
            # while y <= mxdk:
            #     rdata[server, chan]['duck'][y] = '0'
            #     y += 1
            #     continue
            # continue
        continue

    mprint(f'{rdata['ptitle']} * Version: {rdata['pversion']} By: {rdata['pauthor']} - Loaded successfully.')

# ======================================================================================================================
# KICK Event (for timer correspondance)
# evt_kick('servername', b':Neo_Nemesis!~TheOne@th3.m4tr1x.h4ck3d.y0u KICK #testduck zcore :testing 1 2 3')
async def evt_kick(server, kickdata):
    global rdata
    kdata = kickdata.split(b' ')

    # Ignore anything not listed in duckhunt.cnf server/channel info.
    if pc.iistok(rdata['serverlist'], server, ',') is False:
        return
    if pc.iistok(rdata[server, 'channels'], str(kdata[2].decode()).lower(), ',') is False:
        return

    dchannel = kdata[2].decode()
    dchannel = dchannel.lower()
    chan = dchannel.replace('#', '')

    # This lets the script know it has been kicked (see the JOIN event below)
    # zcore is programmed to rejoin a channel after being kicked
    # This value prevents duckhunt from 'auto starting' when rejoining the channel
    rdata[server, chan]['kick'] = True
    return

# ======================================================================================================================
# JOIN Event (for self)
# evt_join('servername', b':Username!~Host@mask.net JOIN :#Channel')
async def evt_join(server, joindata):
    global rdata
    jdata = joindata.split(b' ')

    # Ignore anything not listed in duckhunt.cnf server/channel info.
    if pc.iistok(rdata['serverlist'], server, ',') is False:
        return
    jdata2 = jdata[2].decode()
    jdata2 = jdata2.lower()
    jdata2 = jdata2.replace(':', '')
    if pc.iistok(rdata[server, 'channels'], jdata2, ',') is False:
        return

    username = pc.gettok(jdata[0], 0, b'!')
    username = username.replace(b':', b'')
    dusername = username.decode()
    channel = jdata[2].replace(b':', b'')
    dchannel = channel.decode()
    dchannel = dchannel.lower()
    chan = dchannel.replace('#', '')

    # If it is not self joining, ignore
    if dusername.lower() != rdata[server, 'botname'].lower():
        return
    else:
        # If the bot was kicked, and is rejoining the channel (from KICK event)
        if rdata[server, chan]['kick'] is True:
            rdata[server, chan]['kick'] = False
            return
        # Auto start on join
        if rdata[server, chan]['duckhunt'] is True:
            await duckhunt(server, dchannel, 'start')
#  =====================================================================================================================
# PRIVMSG Event
# evt_privmsg('servername', b':Username!~Host@mask.net PRIVMSG target :Message data')


async def evt_privmsg(server, message):
    global rdata
    mdata = message.split(b' ')
    # Ignore abything not listed in duckhunt.cnf server/channel info.
    if pc.iistok(rdata['serverlist'], server, ',') is False:
        return
    if b'#' in mdata[2] and pc.iistok(rdata[server, 'channels'], str(mdata[2].decode()).lower(), ',') is False:
        return
    username = pc.gettok(mdata[0], 0, b'!')
    username = username.replace(b':', b'')
    dusername = str(username.decode()).lower()
    channel = mdata[2]
    dchannel = str(channel.decode()).lower()
    chan = dchannel.replace('#', '')
    sect = server + '_' + chan
    dsect = server + '_' + chan + '_ducks'

    # admin controls
    if b'#' in channel and pc.is_admin(server, dusername) is True:
        if mdata[3].lower() == b':!duckhunt' and len(mdata) > 4:
            if mdata[4].lower() == b'on':
                if rdata[server, chan]['duckhunt'] is True:
                    pc.privmsg_(server, channel, 'Super DuckHunt is already turned on')
                    return
                else:
                    rdata[server, chan]['duckhunt'] = True
                    # pc.privmsg_(server, channel, 'Super DuckHunt has been turned on')
                    await duckhunt(server, dchannel, 'start')
                    return
            elif mdata[4].lower() == b'off':
                if rdata[server, chan]['duckhunt'] is False:
                    pc.privmsg_(server, channel, 'Super DuckHunt is already turned off.')
                    return
                else:
                    rdata[server, chan]['duckhunt'] = False
                    # pc.privmsg_(server, channel, 'Super DuckHunt has been turned off.')
                    await duckhunt(server, dchannel, 'stop')
                    return

    # put this here so you can use admin controls at any time
    if b'#' in channel and rdata[server, chan]['game'] is False:
        return

    # ==================================================================================================================
    # CHANNEL User Commands !<commands>
    # ==================================================================================================================
    if b'#' in channel:
        # --------------------------------------------------------------------------------------------------------------
        # !topduck
        # ################################### NOT FINISHED
        if mdata[3].lower() == b':!topduck':
            print(f'Top duck!')
            pc.privmsg_(server, channel, 'async TopDuck!')
            return

        # --------------------------------------------------------------------------------------------------------------
        # !duckstats
        if mdata[3].lower() == b':!duckstats':
            if len(mdata) >= 4:
                if len(mdata) == 4:
                    if pc.cnfexists('duckhunt.cnf', dsect, dusername) is False:
                        pc.privmsg_(server, channel, 'User ' + username.decode() + " has not played yet.")
                        return
                    # dst = pc.cnfread('duckhunt.cnf', dsect, dusername)
                    # pc.privmsg_(server, channel, 'TEST DuckStats: ' + username.decode() + ' ' + dst + ' [.]')
                    await duckstats(server, channel, username, username)
                    return
                if len(mdata) == 5:
                    dsuser = mdata[4].decode()
                    if pc.cnfexists('duckhunt.cnf', dsect, dsuser.lower()) is False:
                        pc.privmsg_(server, channel, 'User ' + dsuser + " has not played yet.")
                        return
                    # dst = pc.cnfread('duckhunt.cnf', dsect, duser.lower())
                    # pc.privmsg_(server, channel, 'TEST DuckStats: ' + duser + ' ' + dst + ' [.]')
                    await duckstats(server, channel, username, mdata[4])
                    return
            return
        # --------------------------------------------------------------------------------------------------------------
        # Shop
        if mdata[3].lower() == b':!shop':
            if pc.cnfexists('duckhunt.cnf', dsect, dusername) is False:
                pc.notice_(server, username, username.decode() + " you can't use the shop yet because you haven't played. Shoot some ducks first.")
                return
            # !shop - shop menu
            if len(mdata) == 4:
                await shopmenu(server, channel, username)
                return
            if len(mdata) >= 5:
                shopid = mdata[4].decode()
                if shopid.isnumeric() is False or isinstance(str(shopid), float) is True:
                    pc.notice_(server, username, 'Invalid shop request!')
                    return
                if int(shopid) > 24 or int(shopid) <= 0:
                    pc.notice_(server, username, 'Invalid item ID!')
                    return
                # print(f'async Shop Item {shopid}')
                # pc.privmsg_(server, channel, 'async Shop Item ' + str(shopid))
                if len(mdata) >= 6:
                    await shop(server, channel, username, int(shopid), mdata[5])
                else:
                    await shop(server, channel, username, int(shopid))
                return
            return

        # --------------------------------------------------------------------------------------------------------------
        # !bang
        if mdata[3].lower() == b':!bang':
            if game_rules(server, dchannel, 'bang') == 'off':
                return

            # pc.privmsg_(server, channel, 'Bang!')
            # await bang(server, channel, username)
            bang(server, channel, username)
            return

        # --------------------------------------------------------------------------------------------------------------
        # !reload
        if mdata[3].lower() == b':!reload':
            if game_rules(server, dchannel, 'bang') == 'off':
                return

            # pc.privmsg_(server, channel, 'Reload!')
            # await reload(server, channel, username)
            reload(server, channel, username)
            return

        # --------------------------------------------------------------------------------------------------------------
        # !bef
        if mdata[3].lower() == b':!bef':
            if game_rules(server, dchannel, 'bef') == 'off':
                return

            # print(f'Bef!')
            # pc.privmsg_(server, channel, 'Bef!')
            # await bef(server, channel, username)
            bef(server, channel, username)
            return

        # --------------------------------------------------------------------------------------------------------------
        # !bread
        if mdata[3].lower() == b':!bread' or mdata[3].lower() == b':!reloaf':
            if game_rules(server, dchannel, 'bef') == 'off':
                return

            # print(f'Reloaf!')
            # pc.privmsg_(server, channel, 'Reloaf!')
            # await reloaf(server, channel, username)
            reloaf(server, channel, username)
            return

        # --------------------------------------------------------------------------------------------------------------
        # !lastduck
        # ################################### NOT FINISHED
        if mdata[3].lower() == b':!lastduck':
            print(f'Last duck!')
            pc.privmsg_(server, channel, 'LastDuck!')
            return
        # ################################################

        # --------------------------------------------------------------------------------------------------------------
        # !rearm
        # ###### needs its out async function ###### #
        if mdata[3].lower() == b':!rearm' and pc.is_admin(server, dusername) is True:
            # rules disabled
            if game_rules(server, dchannel, 'bang') == 'off':
                return
            # !rearm (self rearm) --------------------------------------------------------------------------------------
            if len(mdata) == 4:
                if pc.iistok(rdata[server, chan]['confiscated'], dusername, ',') is False:
                    pc.privmsg_(server, channel, username.decode() + ' > Your gun is not confiscated.')
                    return
                ctrl_data(server, dchannel, dusername, 'confiscated', 'rem')
                pc.privmsg_(server, channel, '\x01ACTION returns ' + username.decode() + "'s gun.\x01")
                return
            # !rearm username and !rearm all ---------------------------------------------------------------------------
            if len(mdata) == 5:
                if mdata[4] == b'all':
                    ctrl_data(server, dchannel, dusername, 'confiscated', 'clear')
                    pc.privmsg_(server, channel, '\x01ACTION returns all confiscated guns to the hunters.\x01')
                    return
                duser = mdata[4].decode()
                duser = duser.lower()
                if pc.is_on_chan(server, channel, mdata[4]) is False:
                    pc.privmsg_(server, channel, mdata[4].decode() + ' is not in the channel.')
                    return
                if pc.iistok(rdata[server, chan]['confiscated'], duser, ',') is False:
                    pc.privmsg_(server, channel, mdata[4].decode() + "'s gun is not confiscated.")
                    return
                if pc.iistok(rdata[server, chan]['confiscated'], duser, ',') is True:
                    ctrl_data(server, dchannel, duser, 'confiscated', 'rem')
                    pc.privmsg_(server, channel, '\x01ACTION returns ' + mdata[4].decode() + "'s gun.\x01")
                    return
            # print(f'Rearm!')
            # pc.privmsg_(server, channel, 'Rearm!')
            return

        # --------------------------------------------------------------------------------------------------------------
        # !disarm
        # ###### needs its out async function ###### #
        if mdata[3].lower() == b':!disarm' and pc.is_admin(server, dusername) is True:
            if game_rules(server, dchannel, 'bang') == 'off':
                return
            if len(mdata) == 5:
                if pc.is_on_chan(server, channel, mdata[4]) is False:
                    pc.privmsg_(server, channel, mdata[4].decode() + ' is not in the channel.')
                    return
                duser = mdata[4].decode()
                duser = duser.lower()
                if duser == dusername:
                    pc.notice_(server, username, "Don't do that to yourself!")
                    return
                if duser == rdata[server, 'botname'].lower():
                    pc.notice_(server, username, 'Nice try ;-)')
                    return
                if pc.iistok(rdata[server, chan]['confiscated'], duser, ',') is True:
                    pc.privmsg_(server, channel, mdata[4].decode() + "'s gun is already confiscated.")
                    return
                ctrl_data(server, dchannel, duser, 'confiscated', 'add')
                pc.privmsg_(server, channel, '\x01ACTION > frisks ' + mdata[4].decode() + ' and confiscates the gun.     \x034[GUN CONFISCATED: By order of ' + username.decode() + ']\x03')
            # print(f'Disarm!')
            # pc.privmsg_(server, channel, 'Disarm!')
            return

        # --------------------------------------------------------------------------------------------------------------
        # !bomb
        # ################################### NOT FINISHED
        if mdata[3].lower() == b':!bomb':
            print(f'Bomb!')
            pc.privmsg_(server, channel, 'Bomb!')
            return
        # #################################################

        # --------------------------------------------------------------------------------------------------------------
        # !swim
        if mdata[3].lower() == b':!swim':
            # print(f'Swim!')
            if pc.cnfexists('duckhunt.cnf', dsect, dusername) is False:
                pc.privmsg_(server, channel, "You haven't played yet. Shoot some ducks first.")
                return
            # pc.privmsg_(server, channel, 'Swim!')
            await swim(server, channel, username)
            return

        # --------------------------------------------------------------------------------------------------------------
        # !rules
        if mdata[3].lower() == b':!rules':
            game_rules(server, dchannel, 'msg', dusername)
            return

        return
        # --------------------------------------------------------------------------------------------------------------

    # ==================================================================================================================
    # PRIVMSG Commands /msg duckhunt <commands>
    # ==================================================================================================================
    if b'#' not in channel:
        # --------------------------------------------------------------------------------------------------------------
        # BotMaster and Admin Commands
        # ----------------------------------------------------------------------------------------------------------
        # /msg duckhunt spawn #channel <type> (BOTMASTER & ADMIN)
        if mdata[3].lower() == b':spawn' and pc.is_admin(server, dusername) is True:
            # invalid syntax ---------------------------------------------------------------------------------------
            if len(mdata) == 4:
                pc.notice_(server, username, '[DuckHunt] * Invalid syntax.')
                return
            # invalid channel name ---------------------------------------------------------------------------------
            if len(mdata) >= 5:
                if b'#' not in mdata[4] and len(mdata) == 5:
                    pc.notice_(server, username, '[DuckHunt] * Invalid channel name.')
                    return
                # channel is not a duckhunt channel ----------------------------------------------------------------
                if pc.iistok(rdata[server, 'channels'], str(mdata[4].decode()).lower(), ',') is False:
                    pc.notice_(server, username, '[DuckHunt] * Channel name is not a listed DuckHunt channel.')
                    return
                # changes these values to the input data
                dchannel = str(mdata[4].decode()).lower()
                chan = dchannel.replace('#', '')
                # maximum ducks are already spawned in channel ---------------------------------------------------------
                if ducksdata(server, dchannel) >= rdata[server, chan]['maxducks']:
                    pc.notice_(server, username, '[DuckHunt] * The maximum amount of ducks exist.')
                # /msg duckhunt spawn #channel - spawn random duck in channel --------------------------------------
                if len(mdata) == 5:
                    await spawnduck(server, dchannel)
                    return
                # /msg duckhunt spawn #channel <normal/golden> - spawn a normal or golden duck in channel ----------
                elif len(mdata) == 6:
                    # /msg duckhunt spawn #channel normal ----------------------------------------------------------
                    if mdata[5] == b'normal':
                        await spawnduck(server, dchannel, 'normal')
                        return
                    # /msg duckhunt spawn #chnnael golden ----------------------------------------------------------
                    elif mdata[5] == b'gold' or mdata[5] == b'golden':
                        await spawnduck(server, dchannel, 'gold')
                        return
                    # invalid duck type ----------------------------------------------------------------------------
                    else:
                        pc.notice_(server, username, '[DuckHunt] * Invalid duck type.')
                        return
                else:
                    return 0
        # --------------------------------------------------------------------------------------------------------------
        # /msg duckhunt rules <name> <args>
        if mdata[3].lower() == b':rules' and pc.is_botmaster(dusername) is True:
            if len(mdata) == 4 or len(mdata) < 6 or len(mdata) > 6:
                pc.notice_(server, username, '[DuckHunt] * Invalid input. Use: /msg ' + rdata[server, 'botname'] + ' rules <rule> <args>')
                return
            if len(mdata) == 6:
                # /msg duckhunt rules gunricochet <args> ---------------------------------------------------------------
                if mdata[4].lower() == b'gunricochet':
                    if mdata[5].lower() == b'0':
                        if str(game_rules(server, dchannel, 'gunricochet')) == '0':
                            pc.notice_(server, username, '[DuckHunt] * Bullet ricochet is already turned off.')
                        game_rules(server, dchannel, 'gunricochet', '0')
                        pc.notice_(server, username, '[DuckHunt] * Bullet ricochet has been turned OFF at: 0%')
                        return
                    mdata5 = mdata[5].decode()
                    if mdata5.isnumeric() is False or isinstance(str(mdata5), float) is True:
                        pc.notice_(server, username, '[DuckHunt] * Invalid request: Bullet ricochet value must be an integer.\r\n')
                        return
                    game_rules(server, channel, 'gunricochet', str(data5))
                    pc.notice_(server, username, '[DuckHunt] * Bullet ricochet has been set to ON at: ' + str(data5), + '%.\r\n')
                    return
                # /msg duckhunt rules thebushes <args> -----------------------------------------------------------------
                if mdata[4].lower() == b'thebushes':
                    if mdata[5].lower() == b'0':
                        if str(game_rules(server, dchannel, 'thebushes')) == '0':
                            pc.notice_(server, username, '[DuckHunt] * Searching the bushes is already turned off.')
                        game_rules(server, dchannel, 'thebushes', '0')
                        pc.notice_(server, username, '[DuckHunt] * Searching the bushes has been turned OFF at: 0%')
                        return
                    mdata5 = mdata[5].decode()
                    if mdata5.isnumeric() is False or isinstance(str(mdata5), float) is True:
                        pc.notice_(server, username, '[DuckHunt] * Invalid request: Searching the bushes value must be an integer.\r\n')
                        return
                    game_rules(server, channel, 'thebushes', str(data5))
                    pc.notice_(server, username, '[DuckHunt] * Searching the bushes has been set to ON at: ' + str(data5), + '%.\r\n')
                    return
                # /msg duckhunt rules gunconf <args> -------------------------------------------------------------------
                if mdata[4].lower() == b'gunconf':
                    if mdata[5].lower() == b'on':
                        if game_rules(server, dchannel, 'gunconf') == 'on':
                            pc.notice_(server, username, '[DuckHunt] * Gun confiscation is already turned on.')
                            return
                        game_rules(server, dchannel, 'gunconf', 'on')
                        pc.notice_(server, username, '[DuckHunt] * Gun confiscation has been turned on.')
                        return
                    if mdata[5].lower() == b'off':
                        if game_rules(server, channel, 'gunconf') == 'off':
                            pc.notice_(server, username, '[DuckHunt] * Gun confiscation is already turned off.')
                            return
                        game_rules(server, dchannel, 'gunconf', 'off')
                        pc.notice_(server, username, '[DuckHunt] * Gun confiscation has been turned off.')
                        return
                # /msg duckhunt rules infammo <args> -------------------------------------------------------------------
                if mdata[4].lower() == b'infammo':
                    if mdata[5].lower() == b'on':
                        if game_rules(server, dchannel, 'infammo') == 'on':
                            pc.notice_(server, username, '[DuckHunt] * Infinite ammo is already turned on.')
                            return
                        game_rules(server, dchannel, 'infammo', 'on')
                        pc.notice_(server, username, '[DuckHunt] * Infinite ammo has been turned on.')
                        return
                    if mdata[5].lower() == b'off':
                        if game_rules(server, channel, 'infammo') == 'off':
                            pc.notice_(server, username, '[DuckHunt] * Infinite ammo is already truend off.')
                            return
                        game_rules(server, dchannel, 'infammo', 'off')
                        pc.notice_(server, username, '[DuckHunt] * Infinite ammo has been turned off.')
                        return
                # /msg duckhunt rules bang <args> ----------------------------------------------------------------------
                if mdata[4].lower() == b'bang':
                    if mdata[5].lower() == b'on':
                        if game_rules(server, dchannel, 'bang') == 'on':
                            pc.notice_(server, username, '[DuckHunt] * !bang command set is already enabled.')
                            return
                        game_rules(server, dchannel, 'bang', 'on')
                        pc.notice_(server, username, '[DuckHunt] * !bang command set has been enabled.')
                        return
                    if mdata[5].lower() == b'off':
                        if game_rules(server, dchannel, 'bang') == 'off':
                            pc.notice_(server, username, '[DuckHunt] * !bang command set is already disabled.')
                            return
                        if game_rules(server, dchannel, 'bef') == 'off':
                            pc.notice_(server, username, '[DuckHunt] * Invalid request: !bef command set is also turned off. First enable !bef, then try again.')
                            return
                        game_rules(server, dchannel, 'bang', 'off')
                        pc.notice_(server, username, '[DuckHunt] * !bang command set has been disabled.')
                        return
                # /msg duckhunt rules bef <args> -----------------------------------------------------------------------
                if mdata[4].lower() == b'bef':
                    if mdata[5].lower() == b'on':
                        if game_rules(server, dchannel, 'bef') == 'on':
                            pc.notice_(server, username, '[DuckHunt] * !bef command set is already enabled.')
                            return
                        game_rules(server, dchannel, 'bef', 'on')
                        pc.notice_(server, username, '[DuckHunt] * !bef command set has been enabled.')
                        return
                    if mdata[5].lower() == b'off':
                        if game_rules(server, dchannel, 'bef') == 'off':
                            pc.notice_(server, username, '[DuckHunt] * !bef command set is already disabled.')
                            return
                        if game_rules(server, dchannel, 'bang') == 'off':
                            pc.notice_(server, username, '[DuckHunt] * Invalid request: !bang command set is also turned off. First enable !bang, then try again.')
                            return
                        game_rules(server, dchannel, 'bef', 'off')
                        pc.notice_(server, username, '[DuckHunt] * !bef command set has been disabled.')
                        return
    return

# ======================================================================================================================
# DuckHunt functions
# ======================================================================================================================
# Eventually put a list here?

# DuckHunt control function ============================================================================================
# duckhunt('serverid', '#channel', <args>, <ext=''>)
async def duckhunt(server, channel, args, ext=''):
    global rdata
    chan = channel.replace('#', '')

    if args == 'start':
        rdata[server, chan]['game'] = True
        rdata[server, chan]['timer'] = pc.cputime()
        mprint(f'{server} * Super DuckHunt {rdata['pversion']} has started up on {channel} at {pc.ctime()} on {pc.cdate()}')

        pc.privmsg_(server, channel.encode(), 'Super Duck-Hunt ' + rdata['pversion'] + ' is now ON.')

        rdata[server, chan]['thread'] = threading.Thread(target=ducktimer, args=(server, channel,), daemon=True)
        rdata[server, chan]['thread'].start()

    if args == 'stop':
        rdata[server, chan]['game'] = False
        rdata[server, chan]['timer'] = '0'
        mprint(f'{server} * Super DuckHunt {rdata['pversion']} has stopped on {channel} at {pc.ctime()} on {pc.cdate()}')
        pc.privmsg_(server, channel.encode(), 'Super Duck-Hunt ' + rdata['pversion'] + ' is now OFF.')
        rdata[server, chan]['thread'].join()

# Game rules control ===================================================================================================
# game_rules(<rule>, <on/off>)
def game_rules(server, channel, rule, args=''):
    global rdata
    chan = channel.replace('#', '')
    rt = 0
    # game_rules('serverid', '#channel', 'msg', 'username')
    if rule == 'msg':
        confgun = 'Gun confiscation: ' + str(pc.gettok(rdata[server, chan]['rules'], 2, ',')).upper()
        ricogun = 'Bullets ricochet: ON'
        if str(pc.gettok(rdata[server, chan]['rules'], 0, ',')) == '0':
            ricogun = 'Bullets ricochet: OFF'
        searchbush = 'Searching the bushes: ON'
        if str(pc.gettok(rdata[server, chan]['rules'], 1, ',')) == '0':
            searchbush = 'Searching the bushes: OFF'
        ammomode = 'Ammo supply: NORMAL'
        if pc.gettok(rdata[server, chan]['rules'], 3, ',') == 'on':
            ammomode = 'Ammo supply: INFINITE'
        if pc.gettok(rdata[server, chan]['rules'], 4, ',') == 'off':
            ammomode = 'Bread supply: NORMAL'
            if pc.gettok(rdata[server, chan]['rules'], 3, ',') == 'on':
                ammomode = 'Bread supply: INFINITE'
        gamemode = 'Game mode: NORMAL'
        if pc.gettok(rdata[server, chan]['rules'], 4, ',') == 'off':
            gamemode = 'Game mode: NO GUNS'
        if pc.gettok(rdata[server, chan]['rules'], 5, ',') == 'off':
            gamemode = 'Game mode: HUNTING ONLY'

        # if data3 == b'!rules' and datarelay is True:
        #    irc.send(b'PRIVMSG ' + duckchan + b' :[' + duckchan + b' Super-DuckHunt In-Game Rules:] ' + confgun.encode() + b' | ' + ricogun.encode() + b' | ' + searchbush.encode() + b' | ' + ammomode.encode() + b' | ' + gamemode.encode() + b'\r\n')
        #    continue
        # irc.send(b'NOTICE ' + username + b' :[' + duckchan + b' Super-DuckHunt In-Game Rules:] ' + confgun.encode() + b' | ' + ricogun.encode() + b' | ' + searchbush.encode() + b' | ' + ammomode.encode() + b' | ' + gamemode.encode() + b'\r\n')
        pc.notice_(server, args.encode(), '[' + channel + ' Super DuckHunt In-Game Rules:] ' + confgun + ' | ' + ricogun + ' | ' + searchbush + ' | ' + ammomode + ' | ' + gamemode)
        return
    elif rule == 'gunricochet':
        rt = 0
    elif rule == 'thebushes':
        rt = 1
    elif rule == 'gunconf':
        rt = 2
    elif rule == 'infammo':
        rt = 3
    elif rule == 'bang':
        rt = 4
    elif rule == 'bef':
        rt = 5
    else:
        return 0

    if args == '':
        return pc.gettok(rdata[server, chan]['rules'], rt, ',')
    if args != '':
        newdat = pc.reptok(rdata[server, chan]['rules'], rt, ',', str(args))
        pc.cnfwrite('duckhunt.cnf', server + '_' + chan, 'therules', newdat)
        rdata[server, chan]['rules'] = newdat
        return 1
    return 0

# Duck timer and loop ==================================================================================================
# ducktimer('serverid', '#channel')
def ducktimer(server, channel):
    global rdata

    chan = str(channel.replace('#', '')).lower()
    # duckid = 0
    while rdata[server, chan]['game'] is True:
        pc.bot_sleep(0.01)
        if rdata[server, chan]['duckhunt'] is False:
            break
        # Determine if its time to spawn a duck
        calc = pc.cputime() - float(rdata[server, chan]['timer'])
        if calc >= rdata[server, chan]['spawntime'] and ducksdata(server, channel) < rdata[server, chan]['maxducks']:
            rdata[server, chan]['timer'] = pc.cputime()
            asyncio.run(spawnduck(server, channel))

        # Check flytimes of any existing ducks
        for x in range(len(rdata[server, chan]['duck'])):

            # duckX is not flying, move on to the next.
            if x == 6:  # IDK?
                break
            # print(f'Duck {x}...')
            if rdata[server, chan]['duck'][x] == '0':
                continue

            # duckX is flying, check flytime
            # rdata[server, chan]['duck'][X] = time,type,hp,fear
            # sptime = float(pc.gettok(rdata[server, chan]['duck'][x], 0, ','))
            math = pc.cputime() - float(pc.gettok(rdata[server, chan]['duck'][x], 0, ','))
            # print(f'{math} Time')
            if math >= float(rdata[server, chan]['flytime']):
                asyncio.run(fleeduck(server, channel, x))
                continue
            # Next duck
            continue
        # continue timer loop
        continue
    return

# ======================================================================================================================
# returns the total number of spawned ducks for channel on server
def ducksdata(server, channel):
    global rdata
    chan = str(channel.replace('#', '')).lower()
    t = 0
    for x in range(len(rdata[server, chan]['duck'])):
        # print(f'Duck {x}...')
        # IDK??
        if x == 6:
            print(f'Duck 6??: {rdata[server, chan]['duck']}')
            del rdata[server, chan]['duck']['0']
            break
        if rdata[server, chan]['duck'][x] == '0':
            continue
        else:
            t += 1
            continue
    return t

# Main duck spawn function =============================================================================================
# spawnduck('serverid', '#channel') - spawns a random duck to channel
# spawnduck('serverid', '#channel', 'gold') - spawns golden duck
# spawnduck('serverid', '#channel', 'normal') = spawns a normal duck
# rdata[server, chan]['duck'][x] = time,type,hp,fear
async def spawnduck(server, channel, dtype=''):
    global rdata
    chan = str(channel.replace('#', '')).lower()

    for x in range(len(rdata[server, chan]['duck'])):
        if rdata[server, chan]['duck'][x] == '0':
            if dtype == '':
                if pc.rand(0, 100) <= rdata[server, chan]['duckgold']:
                    # DIFFICULTY SETTINGS PT. 1 #######################################################################
                    # Golden duck difficulty is determined by the pc.rand(5, 8)
                    # pc.rand(min HP, max HP)
                    #       5 = minimum HP acceptable (easier golden ducks)
                    #       8 = highest golden HP acceptable (harder ducks)
                    # To alter difficulty change these numbers. lowest HP must be at least 3.
                    # MUST ALSO CHANGE THE 2ND OPTION FURTHER DOWN PT.2
                    # MODIFY BELOW THIS LINE ------------------------------------------------------>
                    rdata[server, chan]['duck'][x] = str(pc.cputime()) + ',' + 'gold,' + str(pc.rand(5, 8)) + ',0'
                    # #################################################################################################
                else:
                    rdata[server, chan]['duck'][x] = str(pc.cputime()) + ',' + 'normal,1,0'
            if dtype == 'gold':
                # DIFFICULTY SETTINGS PT. 2 ###########################################################################
                # Below setting must match the PT. 1 setting in pc.rand(X, X) ----------------->
                rdata[server, chan]['duck'][x] = str(pc.cputime()) + ',' + 'gold,' + str(pc.rand(5, 8)) + ',0'
                # #####################################################################################################
            if dtype == 'normal':
                rdata[server, chan]['duck'][x] = str(pc.cputime()) + ',' + 'normal,1,0'

            pc.privmsg_(server, channel.encode(), b"\x0314-.,\xc2\xb8\xc2\xb8.-\xc2\xb7\xc2\xb0'`'\xc2\xb0\xc2\xb7-.,\xc2\xb8\xc2\xb8.-\xc2\xb7\xc2\xb0'`'\xc2\xb0\xc2\xb7\x0f \x02\\_O<\x02   \x0314QUACK\x0f")
            return 1
        continue
    return 0

# Duck flies away ======================================================================================================
# fleeduck('serverid', '#channel', X)
# Have duckX fly away and disappear. (see scareduck for frightened ducks)
async def fleeduck(server, channel, duckid):
    global rdata
    chan = str(channel.replace('#', '')).lower()
    rdata[server, chan]['duck'][int(duckid)] = '0'
    pc.privmsg_(server, channel.encode(), b"A duck flies away.     \x0314\xc2\xb7\xc2\xb0'`'\xc2\xb0-.,\xc2\xb8\xc2\xb8.\xc2\xb7\xc2\xb0'`")
    return

# Duck scared away =====================================================================================================
# scareduck('serverid', '#channel', X)
# Have one or all ducks get scared and fly away
async def scareduck(server, channel, duckid=''):
    global rdata

    # scareduck('serverid', '#channel') - Scare all ducks
    if duckid == '':
        for x in range(len(rdata[server, chan]['duck'])):
            rdata[server, chan]['duck'][x] = '0'
            continue
        pc.privmsg_(server, channel.encode(), b"\x034Frightened by so much noise, all ducks in the area have fled.\x03     \x0314\xc2\xb7\xc2\xb0'`'\xc2\xb0-.,\xc2\xb8\xc2\xb8.\xc2\xb7\xc2\xb0'`")
        return

    # scareduck('serverid', '#channel', duckid) - Scare one duck
    else:
        rdata[server, chan]['duck'][int(duckid)] = '0'
        pc.privmsg_(server, channel.encode(), b"\x034Frightened by so much noise, a duck in the area has fled.\x03     \x0314\xc2\xb7\xc2\xb0'`'\xc2\xb0-.,\xc2\xb8\xc2\xb8.\xc2\xb7\xc2\xb0'`")
        return

# ======================================================================================================================
# Player data control
# ctrl_data('serverid', '#channel', 'username', 'control name', args='')
# Controls the storage and handling for controlled statuses: gun confiscation, disarmed, bombed and duck_jam
def ctrl_data(server, channel, user, ctrl_name, args=''):
    global rdata
    duser = user.lower()
    dchannel = channel.lower()
    chan = dchannel.replace('#', '')

    # Jammed Guns ------------------------------------------------------------------------------------------------------
    if ctrl_name == 'jammed':

        # ctrl_data('serverid', '#channel', 'username', 'jammed', 'add') -----------------------------------------------
        # Adds user to the jammed gun list
        if args == 'add':
            if rdata[server, chan]['jammed'] == '0':
                rdata[server, chan]['jammed'] = duser
                pc.cnfwrite('duckhunt.cnf', server + '_' + chan, 'jammed', rdata[server, chan]['jammed'])
                return 1
            else:
                tok = rdata[server, chan]['jammed']
                rdata[server, chan]['jammed'] = tok + ',' + duser
                pc.cnfwrite('duckhunt.cnf', server + '_' + chan, 'jammed', rdata[server, chan]['jammed'])
                return 1
        # ctrl_data('serverid', '#channel', 'username', 'jammed', 'rem') -----------------------------------------------
        # removes user from the jammed gun list
        if args == 'rem':
            if rdata[server, chan]['jammed'] == duser or pc.numtok(rdata[server, chan]['jammed'], ',') == 1:
                rdata[server, chan]['jammed'] = '0'
                pc.cnfwrite('duckhunt.cnf', server + '_' + chan, 'jammed', rdata[server, chan]['jammed'])
                return 1
            else:
                token = rdata[server, chan]['jammed'].split(',')
                newstring = '0'
                for x in range(len(token)):
                    if token[x] == duser:
                        continue
                    else:
                        if newstring != '0':
                            newstring = newstring + ',' + token[x]
                            continue
                        else:
                            newstring = token[x]
                            continue
                rdata[server, chan]['jammed'] = newstring
                pc.cnfwrite('duckhunt.cnf', server + '_' + chan, 'jammed', rdata[server, chan]['jammed'])
                return 1
    # Duck Jam (used with gun jamming) ---------------------------------------------------------------------------------
    # This is used to prevent the gun from jamming twice in a row
    if ctrl_name == 'duck_jam':

        # ctrl_data('serverid', '#channel', 'username', 'duck_jam', 'add')
        # add user to duck_jam list
        if args == 'add':
            if rdata[server, chan]['duck_jam'] == '0':
                rdata[server, chan]['duck_jam'] = duser
                pc.cnfwrite('duckhunt.cnf', server + '_' + chan, 'duck_jam', rdata[server, chan]['duck_jam'])
                return 1
            else:
                tok = rdata[server, chan]['duck_jam']
                rdata[server, chan]['duck_jam'] = tok + ',' + duser
                pc.cnfwrite('duckhunt.cnf', server + '_' + chan, 'duck_jam', rdata[server, chan]['duck_jam'])
                return 1

        # ctrl_data('serverid', '#channel', 'username', 'duck_jam', 'rem')
        # remove user from duck_jam list
        if args == 'rem':
            if rdata[server, chan]['duck_jam'] == duser:
                rdata[server, chan]['duck_jam'] = '0'
                pc.cnfwrite('duckhunt.cnf', server + '_' + chan, 'duck_jam', rdata[server, chan]['duck_jam'])
                return 1
            else:
                token = rdata[server, chan]['duck_jam'].split(',')
                newstring = '0'
                for x in range(len(token)):
                    if token[x] == duser:
                        continue
                    else:
                        if newstring != '0':
                            newstring = newstring + ',' + token[x]
                            continue
                        else:
                            newstring = token[x]
                            continue
                rdata[server, chan]['duck_jam'] = newstring
                pc.cnfwrite('duckhunt.cnf', server + '_' + chan, 'duck_jam', rdata[server, chan]['duck_jam'])
                return 1

    # Gun Confiscation -------------------------------------------------------------------------------------------------
    if ctrl_name == 'confiscated':

        # ctrl_data('serverid', '#channel', 'username', 'confiscated') -------------------------------------------------
        # returns True if username exists in the confiscated guns list
        if args == '':
            if pc.iistok(rdata[server, chan]['confiscated'], duser, ',') is True:
                return True
            else:
                return False
        # ctrl_data('serverid', '#channel', 'username', 'confiscated', 'add') ------------------------------------------
        # adds user name to confiscated list (name must not already exist or it will be doubled)
        if args == 'add':
            if rdata[server, chan]['confiscated'] == '0':
                rdata[server, chan]['confiscated'] = duser
                pc.cnfwrite('duckhunt.cnf', server + '_' + chan, 'confiscated', rdata[server, chan]['confiscated'])
                return 1
            else:
                tok = rdata[server, chan]['confiscated']
                rdata[server, chan]['confiscated'] = tok + ',' + duser
                pc.cnfwrite('duckhunt.cnf', server + '_' + chan, 'confiscated', rdata[server, chan]['confiscated'])
                return 1
        # ctrl_data('serverid', '#channel', 'username', 'confiscated', 'rem') ------------------------------------------
        # remove user name from confiscated list, if it exists in the list
        if args == 'rem':
            # print(f'HERE 932')
            if rdata[server, chan]['confiscated'] == duser:
                rdata[server, chan]['confiscated'] = '0'
                pc.cnfwrite('duckhunt.cnf', server + '_' + chan, 'confiscated', rdata[server, chan]['confiscated'])
                # print(f'HERE 932')
                return 1
            else:
                token = rdata[server, chan]['confiscated'].split(',')
                newstring = '0'
                for x in range(len(token)):
                    if token[x] == duser:
                        continue
                    else:
                        if newstring != '0':
                            newstring = newstring + ',' + token[x]
                            continue
                        else:
                            newstring = token[x]
                            continue
                rdata[server, chan]['confiscated'] = newstring
                pc.cnfwrite('duckhunt.cnf', server + '_' + chan, 'confiscated', rdata[server, chan]['confiscated'])
                return 1
        # ctrl_data('serverid', '#channel', 'username', 'confiscated', 'clear')
        # Clears the confiscation list (for !rearm all)
        if args == 'clear':
            rdata[server, chan]['confiscated'] = '0'
            pc.cnfwrite('duckhunt.cnf', server + '_' + chan, 'confiscated', rdata[server, chan]['confiscated'])
            return 1
        return 0

    # Disarmed Status (new!) -------------------------------------------------------------------------------------------
    # This is a permanent or timed gun confiscation. Player will not be able to purchase gun back from the shop.
    # !disarm is the only command that will add this status.
    # !rearm is the only command that will remove this status.

    # Bombed Status ----------------------------------------------------------------------------------------------------
    # This is a permanent version of 'soggy' that happens when players are the target of !bomb.
    # !bomb <username> is the only command that will add this status.
    # !shop 12 or !swim are the only commands that will remove this status.

# Timed effects and timed inventory ====================================================================================
# time_data('serverid', '#channel', 'username', <effect/item name>, <args='', <data=''>)
# Porting this from v1.1.4 to zCore would not work and had to
# write a new function to fit into the system.
# This is a combination of data_check() and iecheck() from v1.1.4
# rdata['serverid', 'channel']['item/effect']['username'] = time.time() OR 'data'
def time_data(server, channel, user, eff_name, args='', data=''):
    global rdata
    dchannel = channel.lower()
    try:
        dchannel = dchannel.decode()
    except AttributeError:
        dchannel = channel.lower()
    chan = dchannel.replace('#', '')

    # time_data('serverid', '#channel', 'username', 'all-time')
    # checks for and removes expired time entries for username.
    if eff_name == 'all-time' and args == '':
        stringlist = 'bedazzled,soggy,gun_grease,silencer,sunglasses,accident_insurance,rain_coat,lucky_charm'
        listitem = stringlist.split(',')
        for z in range(len(listitem)):

            if pc.istok_n(rdata[server, chan][listitem[z]], user.lower(), ',', '^', 0) is True:
                tok = rdata[server, chan][listitem[z]].split(',')
                for x in range(len(tok)):
                    usrtok = pc.gettok(tok[x], 0, '^')
                    utime = pc.gettok(tok[x], 1, '^')
                    newtok = '0'
                    if usrtok.lower() == user.lower():
                        timem = pc.cputime() - float(utime)
                        if round(timem) >= pc.hour1():
                            if pc.numtok(rdata[server, chan][listitem[z]], ',') < 2:
                                newtok = '0'
                            else:
                                newtok = pc.deltok(rdata[server, chan][listitem[z]], tok[x], ',')
                            pc.cnfwrite('duckhunt.cnf', server + '_' + chan, listitem[z], newtok)
                            rdata[server, chan][listitem[z]] = newtok
                            break
                        else:
                            continue
                    else:
                        continue
            continue

    # time_data('serverid', '#channel', 'username', 'effect name', 'check')
    # checks specified effect for username
    if args == 'check':
        if pc.istok_n(rdata[server, chan][eff_name], user.lower(), ',', '^', 0) is True:
            tok = rdata[server, chan][eff_name].split(',')
            for x in range(len(tok)):
                usrtok = pc.gettok(tok[x], 0, '^')
                utime = pc.gettok(tok[x], 1, '^')
                newtok = '0'
                if usrtok.lower() == user.lower():
                    timem = pc.cputime() - float(utime)
                    if eff_type(eff_name) == 1 and timem >= pc.hour1():
                        if pc.numtok(rdata[server, chan][eff_name], ',') < 2:
                            newtok = '0'
                        else:
                            newtok = pc.deltok(rdata[server, chan][eff_name], tok[x], ',')
                        pc.cnfwrite('duckhunt.cnf', server + '_' + chan, eff_name, newtok)
                        rdata[server, chan][eff_name] = newtok
                        return
                    if eff_type(eff_name) == 2 and timem >= pc.hour24():
                        if pc.numtok(rdata[server, chan][eff_name], ',') < 2:
                            newtok = '0'
                        else:
                            newtok = pc.deltok(rdata[server, chan][eff_name], tok[x], ',')
                        pc.cnfwrite('duckhunt.cnf', server + '_' + chan, eff_name, newtok)
                        rdata[server, chan][eff_name] = newtok
                        return
                    if eff_type(eff_name) == 3 and timem >= pc.hour24():
                        if pc.numtok(rdata[server, chan][eff_name], ',') < 2:
                            newtok = '0'
                        else:
                            newtok = pc.deltok(rdata[server, chan][eff_name], tok[x], ',')
                        pc.cnfwrite('duckhunt.cnf', server + '_' + chan, eff_name, newtok)
                        rdata[server, chan][eff_name] = newtok
                    if eff_type(eff_name) >= 4:
                        return
                else:
                    continue
            return

    # time_data('serverid', '#channel', 'username', 'effect name', 'add', <data='new data'>)
    # Adds data to rdata[server, chan][eff_name] and overwrites/updates previous existing data
    if args == 'add':
        if eff_type(eff_name) == 1 or eff_type(eff_name) == 2:
            if rdata[server, chan][eff_name] != '0':
                rdata[server, chan][eff_name] = rdata[server, chan][eff_name] + ',' + user.lower() + '^' + str(pc.cputime())
            else:
                rdata[server, chan][eff_name] = user.lower() + '^' + str(pc.cputime())
            pc.cnfwrite('duckhunt.cnf', server + '_' + chan, eff_name, rdata[server, chan][eff_name])
            return

        if eff_type(eff_name) == 3:
            if rdata[server, chan][eff_name] != '0':
                rdata[server, chan][eff_name] = rdata[server, chan][eff_name] + ',' + user.lower() + '^' + str(pc.cputime()) + '^' + str(data)
            else:
                rdata[server, chan][eff_name] = user.lower() + '^' + str(pc.cputime()) + '^' + str(data)
            pc.cnfwrite('duckhunt.cnf', server + '_' + chan, eff_name, rdata[server, chan][eff_name])
            return

        if eff_type(eff_name) >= 4:
            if rdata[server, chan][eff_name] != '0':
                rdata[server, chan][eff_name] = rdata[server, chan][eff_name] + ',' + user.lower() + '^' + str(data)
            else:
                rdata[server, chan][eff_name] = user.lower() + '^' + str(data)
            pc.cnfwrite('duckhunt.cnf', server + '_' + chan, eff_name, rdata[server, chan][eff_name])
            return

    # time_data('serverid', '#channel', 'username', 'effect name', 'rem')
    # Removes player entry from effect
    if args == 'rem':
        if pc.numtok(rdata[server, chan][eff_name], ',') > 1:
            tokn = rdata[server, chan][eff_name].split(',')
            newt = '0'
            for x in range(len(tokn)):
                if pc.istok_n(tokn[x], user.lower(), ',', '^', '0') is True:
                    continue
                else:
                    if newt == '0':
                        newt = tokn[x]
                        continue
                    else:
                        newt = newt + ',' + tokn[x]
                        continue
            rdata[server, chan][eff_name] = newt
            pc.cnfwrite('duckhunt.cnf', server + '_' + chan, eff_name, rdata[server, chan][eff_name])
            return
        else:
            rdata[server, chan][eff_name] = '0'
            pc.cnfwrite('duckhunt.cnf', server + '_' + chan, eff_name, '0')
            return

# This is for time_data() to determine effect type.
def eff_type(eff_name):
    # Type 1 effect type (1 hour effect)
    if eff_name == 'bedazzled' or eff_name == 'soggy':
        return 1
    # Type 2 effect type (24 hour single effect)
    if eff_name == 'gun_grease' or eff_name == 'silencer' or eff_name == 'sunglasses' or eff_name == 'accident_insurance' or eff_name == 'rain_coat':
        return 2
    # Type 3 effect type (24 hour double effect)
    if eff_name == 'lucky_charm':
        return 3
    # Type 4 effect type (permanent time)
    if eff_name == 'bombed':
        return 4
    # Type 5 effect type (quantity effect)
    if eff_name == 'expl_ammo' or eff_name == 'popcorn' or eff_name == 'trigger_lock' or eff_name == 'bread_lock':
        return 5

# Player stats and data handling =======================================================================================
# duckinfo('serverid', '#channel', 'username', <stat>, <data>)
# playername = Rounds?Mags?MaxRounds?MaxMags,Ducks,GoldenDucks,xp,level,levelup,notusedanymore,notusedanymore,Accuracy?Reliability?MaxReliability,BestTime,Accidents,Bread?MaxBread?Loaf?MaxLoaf,DuckFriends
# playername = Ammo,Ducks,GoldenDucks,xp,level,levelup,NOTUSED,NOTUSED,gunstats,besttime,accidents,bread,duckfriends
# Returns or changes specified user Duck stats
def duckinfo(server, channel, user, req, data=''):
    global rdata

    chan = str(channel.replace('#', '')).lower()
    userl = user.lower()
    sect = server + '_' + chan + '_ducks'
    cnfdat = pc.cnfread('duckhunt.cnf', sect, userl)

    # Ammo rounds, maxrounds, mags, maxmags ----------------------------------------------------------------------------

    # Rounds - ammo is Rounds?MaxRounds?Mags?MaxMags -------------------------------------------------------------------
    # duckinfo('serverid', '#channel', 'username', 'ammo-r', <data=''>
    if req == 'ammo-r':
        ammo = pc.gettok(cnfdat, 0, ',')
        if data == '':
            return int(pc.gettok(ammo, 0, '?'))
        else:
            ammo = pc.reptok(ammo, 0, '?', str(data))
            newdat = pc.reptok(cnfdat, 0, ',', ammo)
            pc.cnfwrite('duckhunt.cnf', sect, userl, newdat)
            return 1

    # Max Rounds - ammo is Rounds?MaxRounds?Mags?MaxMags ---------------------------------------------------------------
    # duckinfo('serverid', '#channel', 'username', 'ammo-mr', <data=''>
    if req == 'ammo-mr':
        ammo = pc.gettok(cnfdat, 0, ',')
        if data == '':
            return int(pc.gettok(ammo, 2, '?'))
        else:
            ammo = pc.reptok(ammo, 2, '?', str(data))
            newdat = pc.reptok(cnfdat, 0, ',', ammo)
            pc.cnfwrite('duckhunt.cnf', sect, userl, newdat)
            return 1
    # Magazines - ammo is Rounds?MaxRounds?Mags?MaxMags ----------------------------------------------------------------
    # duckinfo('serverid', '#channel', 'username', 'ammo-m', <data=''>
    if req == 'ammo-m':
        ammo = pc.gettok(cnfdat, 0, ',')
        if data == '':
            return int(pc.gettok(ammo, 1, '?'))
        else:
            ammo = pc.reptok(ammo, 1, '?', str(data))
            newdat = pc.reptok(cnfdat, 0, ',', ammo)
            pc.cnfwrite('duckhunt.cnf', sect, userl, newdat)
            return 1
    # Max Magazines - ammo is Rounds?MaxRounds?Mags?MaxMags ------------------------------------------------------------
    # duckinfo('serverid', '#channel', 'username', 'ammo-mr', <data=''>
    if req == 'ammo-mm':
        ammo = pc.gettok(cnfdat, 0, ',')
        if data == '':
            return int(pc.gettok(ammo, 3, '?'))
        else:
            ammo = pc.reptok(ammo, 3, '?', str(data))
            newdat = pc.reptok(cnfdat, 0, ',', ammo)
            pc.cnfwrite('duckhunt.cnf', sect, userl, newdat)
            return 1

    # Bread bread, maxbread, load, maxloaf -----------------------------------------------------------------------------
    # bread is Bread?MaxBread?Loaf?MaxLoaf
    if req == 'bread-b':
        bread = pc.gettok(cnfdat, 11, ',')
        if data == '':
            return int(pc.gettok(bread, 0, '?'))
        else:
            bread = pc.reptok(bread, 0, '?', str(data))
            newdat = pc.reptok(cnfdat, 11, ',', bread)
            pc.cnfwrite('duckhunt.cnf', sect, userl, newdat)
            return 1
    if req == 'bread-mb':
        bread = pc.gettok(cnfdat, 11, ',')
        if data == '':
            return int(pc.gettok(bread, 1, '?'))
        else:
            bread = pc.reptok(bread, 1, '?', str(data))
            newdat = pc.reptok(cnfdat, 11, ',', bread)
            pc.cnfwrite('duckhunt.cnf', sect, userl, newdat)
            return 1
    if req == 'bread-l':
        bread = pc.gettok(cnfdat, 11, ',')
        if data == '':
            return int(pc.gettok(bread, 2, '?'))
        else:
            bread = pc.reptok(bread, 2, '?', str(data))
            newdat = pc.reptok(cnfdat, 11, ',', bread)
            pc.cnfwrite('duckhunt.cnf', sect, userl, newdat)
            return 1
    if req == 'bread-ml':
        bread = pc.gettok(cnfdat, 11, ',')
        if data == '':
            return int(pc.gettok(bread, 3, '?'))
        else:
            bread = pc.reptok(bread, 3, '?', str(data))
            newdat = pc.reptok(cnfdat, 11, ',', bread)
            pc.cnfwrite('duckhunt.cnf', sect, userl, newdat)
            return 1

    # Player stats info ------------------------------------------------------------------------------------------------

    # TO BE DELETED. See ammo-r/-mr/-m/-mm
    # if req == 'ammo':
    #    if data == '':
    #        return pc.gettok(cnfdat, 0, ',')
    #    else:
    #        duck_info = pc.reptok(cnfdat, 0, ',', str(data))
    #        pc.cnfwrite('duckhunt.cnf', sect, userl, duck_info)
    #        return 1

    if req == 'ducks':
        if data == '':
            return pc.gettok(cnfdat, 1, ',')
        else:
            duck_info = pc.reptok(cnfdat, 1, ',', str(str(data)))
            pc.cnfwrite('duckhunt.cnf', sect, userl, duck_info)
            return 1
    if req == 'gducks':
        if data == '':
            return pc.gettok(cnfdat, 2, ',')
        else:
            duck_info = pc.reptok(cnfdat, 2, ',', str(data))
            pc.cnfwrite('duckhunt.cnf', sect, userl, duck_info)
            return 1
    if req == 'xp':
        if data == '':
            return pc.gettok(cnfdat, 3, ',')
        else:
            duck_info = pc.reptok(cnfdat, 3, ',', str(str(data)))
            pc.cnfwrite('duckhunt.cnf', sect, userl, duck_info)
            return 1
    if req == 'level':
        if data == '':
            return pc.gettok(cnfdat, 4, ',')
        else:
            duck_info = pc.reptok(cnfdat, 4, ',', str(data))
            pc.cnfwrite('duckhunt.cnf', sect, userl, duck_info)
            return 1
    if req == 'levelup':
        if data == '':
            return pc.gettok(cnfdat, 5, ',')
        else:
            duck_info = pc.reptok(cnfdat, 5, ',', str(data))
            pc.cnfwrite('duckhunt.cnf', sect, userl, duck_info)
            return 1
    if req == 'effects':  # NOT USED TO BE RE-ASSIGNED
        if data == '':
            return pc.gettok(cnfdat, 6, ',')
        else:
            duck_info = pc.reptok(cnfdat, 6, ',', str(data))
            pc.cnfwrite('duckhunt.cnf', sect, userl, duck_info)
            return 1
    if req == 'inv':  # NOT USED TO BE RE-ASSIGNED
        if data == '':
            return pc.gettok(cnfdat, 7, ',')
        else:
            duck_info = pc.reptok(cnfdat, 7, ',', str(data))
            pc.cnfwrite('duckhunt.cnf', sect, userl, duck_info)
            return 1
    # guninfo =
    if req == 'guninfo':
        if data == '':
            return pc.gettok(cnfdat, 8, ',')
        else:
            duck_info = pc.reptok(cnfdat, 8, ',', str(data))
            pc.cnfwrite('duckhunt.cnf', sect, userl, duck_info)
            return 1
    if req == 'best':
        if data == '':
            return pc.gettok(cnfdat, 9, ',')
        else:
            duck_info = pc.reptok(cnfdat, 9, ',', str(data))
            pc.cnfwrite('duckhunt.cnf', sect, userl, duck_info)
            return 1
    if req == 'accidents':
        if data == '':
            return pc.gettok(cnfdat, 10, ',')
        else:
            duck_info = pc.reptok(cnfdat, 10, ',', str(data))
            pc.cnfwrite('duckhunt.cnf', sect, userl, duck_info)
            return 1
    # TO BE DELETED see 'bread-b/-mb/-l/-lm'
    # if req == 'bread':
    #    if data == '':
    #        return pc.gettok(cnfdat, 11, ',')
    #    else:
    #        duck_info = pc.reptok(cnfdat, 11, ',', str(data))
    #        pc.cnfwrite('duckhunt.cnf', sect, userl, duck_info)
    #        return 1
    if req == 'friend':
        if data == '':
            return pc.gettok(cnfdat, 12, ',')
        else:
            duck_info = pc.reptok(cnfdat, 12, ',', str(data))
            pc.cnfwrite('duckhunt.cnf', sect, userl, duck_info)
            return 1
    return -1


# Inventory and effects (duckstats display) ============================================================================
# inveffect('serverid', '#channel', 'username')
# Returns a formatted string for use in !duckstats for inventory and effects display
def inveffect(server, channel, user):
    global rdata
    chan = str(channel.replace('#', '')).lower()
    huntingbag = '0'
    effects = '0'
    duser = str(user.decode()).lower()

    # check time data for user
    time_data(server, channel, duser, 'all-time')

    # gun grease
    if pc.istok_n(rdata[server, chan]['gun_grease'], duser, ',', '^', 0) is True:
        huntingbag = '\x037,1Gun Grease'

    # gun lock
    if pc.istok_n(rdata[server, chan]['trigger_lock'], duser, ',', '^', 0) is True:
        invuse = pc.gettok_n(rdata[server, chan]['trigger_lock'], duser, ',', '^', 0, 1)
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 ' + 'Gun Lock \x034,1[' + str(invuse) + ']'
        if huntingbag == '0':
            huntingbag = '\x037,1Gun Lock\x034,1 [' + str(invuse) + ']'

    # silencer
    if pc.istok_n(rdata[server, chan]['silencer'], duser, ',', '^', 0) is True:
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 ' + 'Silencer'
        if huntingbag == '0':
            huntingbag = '\x037,1Silencer'

    # lucky charm
    if pc.istok_n(rdata[server, chan]['lucky_charm'], duser, ',', '^', 0) is True:
        invuse = pc.gettok_n(rdata[server, chan]['lucky_charm'], duser, ',', '^', 0, 2)
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 Lucky Charm \x034,1[+' + str(invuse) + 'xp]'
        if huntingbag == '0':
            huntingbag = '\x037,1Lucky Charm \x034,1[+' + str(invuse) + 'xp]'

    # sunglasses
    if pc.istok_n(rdata[server, chan]['sunglasses'], duser, ',', '^', 0) is True:
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 ' + 'Sunglasses'
        if huntingbag == '0':
            huntingbag = '\x037,1Sunglasses'

    # accident insurance
    if pc.istok_n(rdata[server, chan]['accident_insurance'], duser, ',', '^', 0) is True:
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 ' + 'Accident Insurance'
        if huntingbag == '0':
            huntingbag = '\x037,1Accident Insurance'

    # rain coat
    if pc.istok_n(rdata[server, chan]['rain_coat'], duser, ',', '^', 0) is True:
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 ' + 'Rain Coat'
        if huntingbag == '0':
            huntingbag = '\x037,1Rain Coat'

    # bread lock
    if pc.istok_n(rdata[server, chan]['bread_lock'], duser, ',', '^', 0) is True:
        invuse = pc.gettok_n(rdata[server, chan]['bread_lock'], duser, ',', '^', 0, 1)
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 Bread Box Lock \x034,1[' + str(invuse) + ']'
        if huntingbag == '0':
            huntingbag = '\x037,1Bread Box Lock \x034,1[' + str(invuse) + ']'

    # expl ammo
    if pc.istok_n(rdata[server, chan]['expl_ammo'], duser, ',', '^', 0) is True:
        invuse = pc.gettok_n(rdata[server, chan]['expl_ammo'], duser, ',', '^', 0, 1)
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 Explosive Ammo \x034,1[' + str(invuse) + ']'
        if huntingbag == '0':
            huntingbag = '\x037,1Explosive Ammo \x034,1[' + str(invuse) + ']'

    # bag of popcorn
    if pc.istok_n(rdata[server, chan]['popcorn'], duser, ',', '^', 0):
        invuse = pc.gettok_n(rdata[server, chan]['popcorn'], duser, ',', '^', 0, 1)
        if huntingbag != '0':
            huntingbag = huntingbag + ' \x030,1|\x037,1 Bag of Popcorn \x034,1[' + str(invuse) + ']'
        if huntingbag == '0':
            huntingbag = '\x037,1Bag of Popcorn \x034,1[' + str(invuse) + ']'

    # assemble hunting bag
    if huntingbag != '0':
        huntingbag = '\x030,1[HUNTING BAG] ' + huntingbag
    if huntingbag == '0':
        huntingbag = '\x030,1[HUNTING BAG]\x034,1 None'

    # bedazzled
    if pc.istok_n(rdata[server, chan]['bedazzled'], duser, ',', '^', 0) is True:
        if effects != '0':
            effects = effects + ' \x030,1|\x037,1 ' + 'Bedazzled'
        if effects == '0':
            effects = '\x037,1Bedazzled'

    # soggy
    if pc.istok_n(rdata[server, chan]['soggy'], duser, ',', '^', 0) is True:
        if effects != '0':
            effects = effects + ' \x030,1|\x037,1 ' + 'Soggy'
        if effects == '0':
            effects = '\x037,1Soggy'

    # sabotaged
    if pc.istok_n(rdata[server, chan]['sabotage'], duser, ',', '^', 0) is True:
        if effects != '0':
            effects = effects + ' \x030,1|\x037,1 ' + 'Sabotage'
        if effects == '0':
            effects = '\x037,1Sabotage'

    # bombed
    if pc.istok_n(rdata[server, chan]['bombed'], duser, ',', '^', 0) is True:
        if effects != '0':
            effects = effects + ' \x030,1|\x037,1 Duck Bombed'
        if effects == '0':
            effects = '\x037,1Duck Bombed'

    # assemble effects box
    if effects != '0':
        effects = '\x030,1[EFFECTS] ' + effects
    if effects == '0':
        effects = '\x030,1[EFFECTS]\x034,1 None'
    # return formatted message
    return huntingbag + '::' + effects
# ===> inveffect

# duckstats function ===================================================================================================
async def duckstats(server, channel, user, ruser, ext=''):
    global rdata
    dchannel = channel.decode()
    dchannel = dchannel.lower()
    duser = str(user.decode()).lower()
    druser = str(ruser.decode()).lower()

    chan = str(dchannel.replace('#', '')).lower()

    # prep stats
    time_data(server, dchannel, druser, 'all-time')

    rounds = str(duckinfo(server, dchannel, druser, 'ammo-r')).encode()
    mrounds = str(duckinfo(server, dchannel, druser, 'ammo-mr')).encode()
    mags = str(duckinfo(server, dchannel, druser, 'ammo-m')).encode()
    mmags = str(duckinfo(server, dchannel, druser, 'ammo-mm')).encode()

    bread = str(duckinfo(server, dchannel, druser, 'bread-b')).encode()
    mbread = str(duckinfo(server, dchannel, druser, 'bread-mb')).encode()
    loaf = str(duckinfo(server, dchannel, druser, 'bread-l')).encode()
    mloaf = str(duckinfo(server, dchannel, druser, 'bread-ml')).encode()

    tducks = str(duckinfo(server, dchannel, druser, 'ducks')).encode()
    gducks = str(duckinfo(server, dchannel, druser, 'gducks')).encode()
    xp = str(duckinfo(server, dchannel, druser, 'xp')).encode()
    level = str(duckinfo(server, dchannel, druser, 'level')).encode()
    accuracy = pc.gettok(duckinfo(server, dchannel, druser, 'guninfo'), 0, '?').encode()
    reliability = pc.gettok(duckinfo(server, dchannel, druser, 'guninfo'), 1, '?').encode()
    mreliability = pc.gettok(duckinfo(server, dchannel, druser, 'guninfo'), 2, '?').encode()
    besttime = duckinfo(server, dchannel, druser, 'best').encode()

    if besttime == b'0':
        besttime = b'NA'

    scorebox = ''
    gunbox = ''
    breadbox = ''

    if float(reliability) <= 65:
        gunstatus = b'Needs cleaning'
    elif pc.istok(rdata[server, chan]['jammed'], druser, ',') is True:
        gunstatus = b'Jammed'
    elif pc.istok(rdata[server, chan]['confiscated'], druser, ',') is True and game_rules(server, dchannel, 'gunconf') == 'on':
        gunstatus = b'Confiscated'
    else:
        gunstatus = b'OK'

    accidents = duckinfo(server, dchannel, druser, 'accidents').encode()
    friend = duckinfo(server, dchannel, druser, 'friend').encode()

    if game_rules(server, dchannel, 'infammo') == 'on':
        scorebox = b'\x030,1[SCORE]\x037,1 Best Time:\x034,1 ' + besttime + b' \x030,1|\x037,1 Level:\x034,1 ' + level + b' \x030,1|\x037,1 xp:\x034,1 ' + xp + b' \x030,1|\x037,1 Ducks:\x034,1 ' + tducks + b' \x030,1|\x037,1 Golden Ducks:\x034,1 ' + gducks + b' \x030,1|\x037,1 Befriended Ducks:\x034,1 ' + friend + b' \x030,1|\x037,1 Accidents:\x034,1 ' + accidents
        breadbox = b'\x030,1[BREAD BOX]\x037,1 Bread Pieces:\x034,1 ' + bread + b'/' + mbread + b' \x030,1|\x037,1 Loaf: \x02\x033Inf\x02'
        gunbox = b'\x030,1[GUN STATS]\x037,1 Status:\x034,1 ' + gunstatus + b' \x030,1|\x037,1 Rounds:\x034,1 ' + rounds + b'/' + mrounds + b' \x030,1|\x037,1 Magazines: \x02\x033Inf\x02\x03 \x030,1|\x037,1 Accuracy:\x034,1 ' + accuracy + b'% \x030,1|\x037,1 Current Reliability:\x034,1 ' + reliability + b'% \x030,1|\x037,1 Max Reliability:\x034,1 ' + mreliability + b'%'
    if game_rules(server, dchannel, 'infammo') == 'off':
        scorebox = b'\x038,1[SCORE]\x037,1 Best Time:\x034,1 ' + besttime + b' \x030,1|\x037,1 Level:\x034,1 ' + level + b' \x030,1|\x037,1 xp:\x034,1 ' + xp + b' \x030,1|\x037,1 Ducks:\x034,1 ' + tducks + b' \x030,1|\x037,1 Golden Ducks:\x034,1 ' + gducks + b' \x030,1|\x037,1 Befriended Ducks:\x034,1 ' + friend + b' \x030,1|\x037,1 Accidents:\x034,1 ' + accidents
        breadbox = b'\x038,1[BREAD BOX]\x037,1 Bread Pieces:\x034,1 ' + bread + b'/' + mbread + b' \x030,1|\x037,1 Loaf:\x034,1 ' + loaf + b'/' + mloaf
        gunbox = b'\x038,1[GUN STATS]\x037,1 Status:\x034,1 ' + gunstatus + b' \x030,1|\x037,1 Rounds:\x034,1 ' + rounds + b'/' + mrounds + b' \x030,1|\x037,1 Magazines:\x034,1 ' + mags + b'/' + mmags + b' \x030,1|\x037,1 Accuracy:\x034,1 ' + accuracy + b'% \x030,1|\x037,1 Current Reliability:\x034,1 ' + reliability + b'% \x030,1|\x037,1 Max Reliability:\x034,1 ' + mreliability + b'%'
    # left off here need to finish porting inveffect
    hbe = inveffect(server, dchannel, ruser)
    huntingbag = pc.gettok(hbe, 0, '::')
    huntingbag = huntingbag.encode()
    effectsbox = pc.gettok(hbe, 1, '::')
    effectsbox = effectsbox.encode()
    pc.notice_(server, user, b'\x038,1[DuckStats:\x037,1 ' + ruser + b'\x038,1] ' + scorebox + b' ' + gunbox)
    pc.notice_(server, user, breadbox + b' ' + effectsbox)
    pc.notice_(server, user, huntingbag)
    # irc.send(b'NOTICE ' + user + b' :\x038,1[DuckStats:\x037,1 ' + ruser + b'\x038,1] ' + scorebox + b' ' + gunbox + b'\r\n')
    # irc.send(b'NOTICE ' + user + b' :' + breadbox + b' ' + effectsbox + b'\r\n')
    # irc.send(b'NOTICE ' + user + b' :' + huntingbag + b'\r\n')
    return


# Shop menu ============================================================================================================
# Builds specific menu and sends the shop menu to user
# ======================================================================================================================
async def shopmenu(server, channel, user, opt=''):
    global rdata

    dchannel = str(channel.decode()).lower()
    chan = dchannel.replace('#', '')
    duser = str(user.decode()).lower()

    # ammo = bot.duckinfo(user, b'ammo')
    # rounds = bot.gettok(ammo, 0, '?')
    # mags = bot.gettok(ammo, 1, '?')
    # mrounds = bot.gettok(ammo, 2, '?')
    # mmags = bot.gettok(ammo, 3, '?')

    # single bullet
    shop1 = '1:\x037,1 Single Round\x034,1 (' + str(shopprice(server, channel, user, 1)) + ' xp)'
    if game_rules(server, dchannel, 'infammo') == 'on':
        shop1 = '1:\x0314,1 Single Round (' + str(shopprice(server, channel, user, 1)) + ' xp)'
    # refill magazine
    shop2 = '2:\x037,1 Refill Magazine\x034,1 (' + str(shopprice(server, channel, user, 2)) + ' xp)'
    if game_rules(server, dchannel, 'infammo') == 'on':
        shop2 = '2:\x0314,1 Refill Magazine (' + str(shopprice(server, channel, user, 2)) + ' xp)'
    # gun cleaning
    shop3 = '3:\x037,1 Gun Cleaning\x034,1 (' + str(shopprice(server, channel, user, 3)) + ' xp)'
    # explosive ammo
    shop4 = '4:\x037,1 Explosive Ammo\x034,1 (' + str(shopprice(server, channel, user, 4)) + ' xp)'
    # return confiscated gun
    shop5 = '5:\x037,1 Return Confiscated Gun\x034,1 (' + str(shopprice(server, channel, user, 5)) + ' xp)'
    if game_rules(server, dchannel, 'gunconf') == 'off':
        shop5 = '5:\x0314,1 Return Confiscated Gun (' + str(shopprice(server, channel, user, 5)) + ' xp)'
    # gun grease
    shop6 = '6:\x037,1 Gun Grease\x034,1 (' + str(shopprice(server, channel, user, 6)) + ' xp)'
    # gun upgrade
    shop7 = '7:\x037,1 Gun Upgrade\x034,1 (' + str(shopprice(server, channel, user, 7)) + ' xp)'
    # Gun Lock
    shop8 = '8:\x037,1 Gun Lock\x034,1 (' + str(shopprice(server, channel, user, 8)) + ' xp)'
    # silencer
    shop9 = '9:\x037,1 Silencer\x034,1 (' + str(shopprice(server, channel, user, 9)) + ' xp)'
    # lucky charm
    shop10 = '10:\x037,1 Lucky Charm\x034,1 (' + str(shopprice(server, channel, user, 10)) + ' xp)'
    # sunglasses
    shop11 = '11:\x037,1 Sunglasses\x034,1 (' + str(shopprice(server, channel, user, 11)) + ' xp)'
    # new clothes
    shop12 = '12:\x037,1 New Clothes\x034,1 (' + str(shopprice(server, channel, user, 12)) + ' xp)'
    # eye drops
    shop13 = '13:\x037,1 Eye Drops\x034,1 (' + str(shopprice(server, channel, user, 13)) + ' xp)'
    # mirror
    shop14 = '14:\x037,1 Mirror\x034,1 (' + str(shopprice(server, channel, user, 14)) + ' xp)'
    # handful of sand
    shop15 = '15:\x037,1 Handful of Sand\x034,1 (' + str(shopprice(server, channel, user, 15)) + ' xp)'
    # water bucket
    shop16 = '16:\x037,1 Water Bucket\x034,1 (' + str(shopprice(server, channel, user, 16)) + ' xp)'
    # sabotage
    shop17 = '17:\x037,1 Sabotage\x034,1 (' + str(shopprice(server, channel, user, 17)) + ' xp)'
    # accident insurance
    shop18 = '18:\x037,1 Accident Insurance\x034,1 (' + str(shopprice(server, channel, user, 18)) + ' xp)'
    if game_rules(server, dchannel, 'gunconf') == 'off':
        shop18 = '18:\x0314,1 Accident Insurance (' + str(shopprice(server, channel, user, 18)) + ' xp)'
    # loaf of bread
    shop19 = '19:\x037,1 Loaf of Bread\x034,1 (' + str(shopprice(server, channel, user, 19)) + ' xp)'
    if game_rules(server, dchannel, 'infammo') == 'on':
        shop19 = '19:\x0314,1 Loaf of Bread (' + str(shopprice(server, channel, user, 19)) + ' xp)'
    # bag of popcorn
    shop20 = '20:\x037,1 Bag of Popcorn\x034,1 (' + str(shopprice(server, channel, user, 20)) + ' xp)'
    # bread box lock
    shop21 = '21:\x037,1 Bread Box Lock\x034,1 (' + str(shopprice(server, channel, user, 21)) + ' xp)'
    # rain coat
    shop22 = '22:\x037,1 Rain Coat\x034,1 (' + str(shopprice(server, channel, user, 22)) + ' xp)'
    # magazine upgrade
    shop23 = '23:\x037,1 Magazine Upgrade\x034,1 (' + str(shopprice(server, channel, user, 23)) + ' xp)'
    # additional magazine
    shop24 = '24:\x037,1 Additional Magazine\x034,1 (' + str(shopprice(server, channel, user, 24)) + ' xp)'
    if game_rules(server, dchannel, 'infammo') == 'on':
        shop24 = '24:\x0314,1 Additional Magazine (' + str(shopprice(server, channel, user, 24)) + ' xp)'

    # prepares menus
    # !bang off !bef on menu
    if game_rules(server, dchannel, 'bang') == 'off' and game_rules(server, dchannel, 'bef') == 'on':
        menu1 = '\x038,1[Shop Menu]\x034,1 ' + shop10 + ' \x037,1|\x034,1 ' + shop11 + ' \x037,1|\x034,1 ' + shop12 + ' \x037,1|\x034,1 ' + shop13 + ' \x037,1|\x034,1 ' + shop14
        menu2 = '\x038,1[Shop Menu]\x034,1 ' + shop16 + ' \x037,1|\x034,1 ' + shop19 + ' \x037,1|\x034,1 ' + shop20 + ' \x037,1|\x034,1 ' + shop21 + ' \x037,1|\x034,1 ' + shop22
        # if opt != '':
        #    irc.send(b'PRIVMSG ' + duckchan + b' :' + bytes(str(menu1), 'utf-8') + b'\r\n')
        #    irc.send(b'PRIVMSG ' + duckchan + b' :' + bytes(str(menu2), 'utf-8') + b'\r\n')
        #    irc.send(b'PRIVMSG ' + duckchan + b' :\x034,1Syntax:\x037,1 !shop \x037,1[\x037,1id\x037,1] [\x037,1target\x037,1]\r\n')
        #    return
        pc.notice_(server, user, menu1.encode())
        pc.notice_(server, user, menu2.encode())
        pc.notice_(server, user, '\x034,1Syntax:\x037,1 !shop \x037,1[\x037,1id\x037,1] [\x037,1target\x037,1]')
        return

    # !bang on !bef off menu
    elif game_rules(server, dchannel, 'bang') == 'on' and game_rules(server, dchannel, 'bef') == 'off':
        menu1 = '\x038,1[Shop Menu]\x034,1 ' + shop1 + ' \x037,1|\x034,1 ' + shop2 + ' \x037,1|\x034,1 ' + shop3 + ' \x037,1|\x034,1 ' + shop4 + ' \x037,1|\x034,1 ' + shop5 + ' \x037,1|\x034,1 ' + shop6 + ' \x037,1|\x034,1 ' + shop7 + ' \x037,1|\x034,1 ' + shop8 + ' \x037,1|\x034,1 ' + shop9 + ' \x037,1|\x034,1 ' + shop10
        menu2 = '\x038,1[Shop Menu]\x034,1 ' + shop11 + ' \x037,1|\x034,1 ' + shop12 + ' \x037,1|\x034,1 ' + shop13 + ' \x037,1|\x034,1 ' + shop14 + ' \x037,1|\x034,1 ' + shop15 + ' \x037,1|\x034,1 ' + shop16 + ' \x037,1|\x034,1 ' + shop17 + ' \x037,1|\x034,1 ' + shop18 + ' \x037,1|\x034,1 ' + shop22
        menu3 = '\x038,1[Shop Menu]\x034,1 ' + shop23 + ' \x037,1|\x034,1 ' + shop24
        # if opt != '':
        #    irc.send(b'PRIVMSG ' + duckchan + b' :' + bytes(str(menu1), 'utf-8') + b'\r\n')
        #    irc.send(b'PRIVMSG ' + duckchan + b' :' + bytes(str(menu2), 'utf-8') + b'\r\n')
        #    irc.send(b'PRIVMSG ' + duckchan + b' :' + bytes(str(menu3), 'utf-8') + b'\r\n')
        #    irc.send(b'PRIVMSG ' + duckchan + b' :\x034,1Syntax:\x037,1 !shop \x037,1[\x037,1id\x037,1] [\x037,1target\x037,1]\r\n')
        #    return
        pc.notice_(server, user, menu1.encode())
        pc.notice_(server, user, menu2.encode())
        pc.notice_(server, user, menu3.encode())
        pc.notice_(server, user, '\x034,1Syntax:\x037,1 !shop \x037,1[\x037,1id\x037,1] [\x037,1target\x037,1]')
        return

    # normal menu (!bang on, !bef on)
    elif game_rules(server, dchannel, 'bang') == 'on' and game_rules(server, dchannel, 'bef') == 'on':
        menu1 = '\x038,1[Shop Menu]\x034,1 ' + shop1 + ' \x037,1|\x034,1 ' + shop2 + ' \x037,1|\x034,1 ' + shop3 + ' \x037,1|\x034,1 ' + shop4 + ' \x037,1|\x034,1 ' + shop5 + ' \x037,1|\x034,1 ' + shop6 + ' \x037,1|\x034,1 ' + shop7 + ' \x037,1|\x034,1 ' + shop8 + ' \x037,1|\x034,1 ' + shop9 + ' \x037,1|\x034,1 ' + shop10
        menu2 = '\x038,1[Shop Menu]\x034,1 ' + shop11 + ' \x037,1|\x034,1 ' + shop12 + ' \x037,1|\x034,1 ' + shop13 + ' \x037,1|\x034,1 ' + shop14 + ' \x037,1|\x034,1 ' + shop15 + ' \x037,1|\x034,1 ' + shop16 + ' \x037,1|\x034,1 ' + shop17 + ' \x037,1|\x034,1 ' + shop18 + ' \x037,1|\x034,1 ' + shop19 + ' \x037,1|\x034,1 ' + shop20
        menu3 = '\x038,1[Shop Menu]\x034,1 ' + shop21 + ' \x037,1|\x034,1 ' + shop22 + ' \x037,1|\x034,1 ' + shop23 + ' \x037,1|\x034,1 ' + shop24
        # if opt != '':
        #    irc.send(b'PRIVMSG ' + duckchan + b' :' + bytes(str(menu1), 'utf-8') + b'\r\n')
        #    irc.send(b'PRIVMSG ' + duckchan + b' :' + bytes(str(menu2), 'utf-8') + b'\r\n')
        #    irc.send(b'PRIVMSG ' + duckchan + b' :' + bytes(str(menu3), 'utf-8') + b'\r\n')
        #    irc.send(b'PRIVMSG ' + duckchan + b' :\x034,1Syntax:\x037,1 !shop \x037,1[\x037,1id\x037,1] [\x037,1target\x037,1]\r\n')
        #    return
        pc.notice_(server, user, menu1.encode())
        pc.notice_(server, user, menu2.encode())
        pc.notice_(server, user, menu3.encode())
        pc.notice_(server, user, '\x034,1Syntax:\x037,1 !shop \x037,1[\x037,1id\x037,1] [\x037,1target\x037,1]')
        return

# shopprice ============================================================================================================
# Determines price of specified item. CHANGE YOUR PRICE VALUES HERE
# Item prices vary based on user stats, for !shop
def shopprice(server, channel, user, itemid):
    global rdata

    dchannel = channel.decode()
    dchannel = dchannel.lower()
    duser = user.decode()
    duser = duser.lower()
    chan = dchannel.replace('#', '')

    # data prep
    mrounds = duckinfo(server, dchannel, duser, 'ammo-mr')
    mmags = duckinfo(server, dchannel, duser, 'ammo-mm')
    guninfo = duckinfo(server, dchannel, duser, 'guninfo')
    accuracy = pc.gettok(guninfo, 0, '?')
    mreliability = pc.gettok(guninfo, 2, '?')
    # 1 Extra Bullet ---------------------------------------------------------------------------------------------------
    if int(itemid) == 1:
        return 7
    # 2 Refill Magazine ------------------------------------------------------------------------------------------------
    if int(itemid) == 2:
        if int(mrounds) == 7:
            return 20
        if int(mrounds) == 8:
            return 25
        if int(mrounds) == 9:
            return 30
        if int(mrounds) == 10:
            return 35
        if int(mrounds) >= 11:
            return 40
    # 3 gun cleaning ---------------------------------------------------------------------------------------------------
    if int(itemid) == 3:
        if int(mreliability) <= 80:
            return 30
        if 80 < int(mreliability) < 85:
            return 35
        if 85 <= int(mreliability) < 90:
            return 40
        if 90 <= int(mreliability) < 95:
            return 45
        if 95 <= int(mreliability) <= 100:
            return 50
    # 4 explosive ammo -------------------------------------------------------------------------------------------------
    if int(itemid) == 4:
        return 35
    # 5 return confiscated gun -----------------------------------------------------------------------------------------
    if int(itemid) == 5:
        return 30
    # 6 gun grease -----------------------------------------------------------------------------------------------------
    if int(itemid) == 6:
        return 15
    # 7 gun uprade -----------------------------------------------------------------------------------------------------
    # Notes: change this for 2.0.0
    if int(itemid) == 7:
        if 90 < int(accuracy) < 100 <= int(mreliability):
            return 350
        elif int(accuracy) <= 75 and int(mreliability) <= 80:
            return 200
        elif int(accuracy) > 75 and int(mreliability) > 80:
            return 300
        else:
            return 250
    # 8 Gun Lock -------------------------------------------------------------------------------------------------------
    if int(itemid) == 8:
        if int(mrounds) == 7:
            return 25
        elif int(mrounds) == 8:
            return 30
        elif int(mrounds) == 9:
            return 35
        elif int(mrounds) == 10:
            return 40
        elif int(mrounds) == 11:
            return 45
        # if int(mrounds) >= 12:
        else:
            return 50
    # 9 silencer -------------------------------------------------------------------------------------------------------
    if int(itemid) == 9:
        return 20
    # 10 lucky charm ---------------------------------------------------------------------------------------------------
    if int(itemid) == 10:
        return 30
    # 11 sunglasses ----------------------------------------------------------------------------------------------------
    if int(itemid) == 11:
        return 20
    # 12 dry clothes ---------------------------------------------------------------------------------------------------
    if int(itemid) == 12:
        if duser not in rdata[server, chan]['soggy'] and duser not in rdata[server, chan]['bombed']:
            return 25
        if duser in rdata[server, chan]['soggy'] and duser not in rdata[server, chan]['bombed']:
            return 25
        if duser not in rdata[server, chan]['soggy'] and duser in rdata[server, chan]['bomed']:
            return 50
        if duser in rdata[server, chan]['soggy'] and duser in rdata[server, chan]['bombed']:
            return 75
    # 13 eye drops -----------------------------------------------------------------------------------------------------
    if int(itemid) == 13:
        return 35
    # 14 mirror --------------------------------------------------------------------------------------------------------
    if int(itemid) == 14:
        return 35
    # 15 handful of sand -----------------------------------------------------------------------------------------------
    if int(itemid) == 15:
        return 15
    # 16 water bucket --------------------------------------------------------------------------------------------------
    if int(itemid) == 16:
        return 20
    # 17 sabotage ------------------------------------------------------------------------------------------------------
    if int(itemid) == 17:
        return 15
    # 18 accident insurance --------------------------------------------------------------------------------------------
    if int(itemid) == 18:
        return 25
    # 19 loaf of bread -------------------------------------------------------------------------------------------------
    if int(itemid) == 19:
        return 30
    # 20 bag of popcorn ------------------------------------------------------------------------------------------------
    if int(itemid) == 20:
        return 40
    # 21 bread box lock ------------------------------------------------------------------------------------------------
    if int(itemid) == 21:
        return 35
    # 22 rain coat -----------------------------------------------------------------------------------------------------
    if int(itemid) == 22:
        return 30
    # 23 magazine upgrade ----------------------------------------------------------------------------------------------
    if int(itemid) == 23:
        if int(mrounds) == 7:
            return 40
        elif int(mrounds) == 8:
            return 45
        elif int(mrounds) == 9:
            return 50
        elif int(mrounds) == 10:
            return 55
        # if int(mrounds) >= 11:
        else:
            return 60
    # 24 additional magazine -------------------------------------------------------------------------------------------
    if int(itemid) == 24:
        if int(mmags) == 3:
            return 75
        if int(mmags) >= 4:
            return 100
    # unkown item/ID ---------------------------------------------------------------------------------------------------
    return 0

# shop =================================================================================================================
# controls the purchasing and interaction of the shop
async def shop(server, channel, user, itemid, target=''):
    global rdata
    # dchannel = str(channel.decode()).lower()
    dchannel = channel.decode()
    dchannel = dchannel.lower()
    chan = dchannel.replace('#', '')
    # duser = str(user.decode()).lower()
    duser = user.decode()
    duser = duser.lower()
    
    dtarget = ''
    if target != '':
        dtarget = target.decode()
        dtarget = dtarget.lower()

    # check for expired item entries in player inventory
    time_data(server, dchannel, duser, 'all-time')
    sect = server + '_' + chan
    dsect = server + '_' + chan + '_ducks'

    rounds = int(duckinfo(server, dchannel, duser, 'ammo-r'))
    mags = int(duckinfo(server, dchannel, duser, 'ammo-m'))
    mrounds = int(duckinfo(server, dchannel, duser, 'ammo-mr'))
    mmags = int(duckinfo(server, dchannel, duser, 'ammo-mm'))
    xp = int(duckinfo(server, dchannel, duser, 'xp'))
    gunstats = duckinfo(server, dchannel, duser, 'guninfo')
    accuracy = int(pc.gettok(gunstats, 0, '?'))
    reliability = float(pc.gettok(gunstats, 1, '?'))
    mreliability = int(pc.gettok(gunstats, 2, '?'))
    bread = int(duckinfo(server, dchannel, duser, 'bread-b'))
    mbread = int(duckinfo(server, dchannel, duser, 'bread-mb'))
    loaf = int(duckinfo(server, dchannel, duser, 'bread-l'))
    mloaf = int(duckinfo(server, dchannel, duser, 'bread-ml'))

    # not enough xp to purchase -----------------------------------------------------------------------------------
    if xp < shopprice(server, channel, user, int(itemid)):
        pc.notice_(server, user, 'You do not have enough xp for this purchase.')
        return
    # if a target is specified -------------------------------------------------------------------------------------
    if target != '':
        # target not on channel -----------------------------------------------------------------------------------
        if pc.is_on_chan(server, channel, target) is False:
            pc.privmsg_(server, channel, target.decode() + ' is not in the channel.')
            return
        # targeted item checks ------------------------------------------------------------------------------------------
        if int(itemid) == 14 or int(itemid) == 15 or int(itemid) == 16 or int(itemid) == 17:
            if game_rules(server, dchannel, 'bang') == 'off':
                if int(itemid) == 15 or int(itemid) == 17:
                    pc.notice_(server, user, 'Based on current rules this item is not available.')
                    return
            # can't use it on yourself ---------------------------------------------------------------------------------
            if dtarget == duser:
                pc.notice_(server, user, "Don't do that to yourself!")
                return
            # can't use it on the bot ----------------------------------------------------------------------------------
            if str(dtarget).lower() == rdata[server, 'botname'].lower():
                pc.notice_(server, user, 'Nice try ;-)')
                return
            # target hasnt played yet ----------------------------------------------------------------------------------
            if pc.cnfexists('duckhunt.cnf', dsect, str(dtarget).lower()) is False:
                pc.notice_(server, user, target.decode() + " hasn't played yet.")
                return

    # 1 - Single Bullet -----------------------------------------------------------------------------------------------
    if int(itemid) == 1:
        # rules disabled
        if game_rules(server, dchannel, 'infammo') == 'on' or game_rules(server, chan, 'bang') == 'off':
            pc.notice_(server, user, 'Based on current game rules, this item is not available.')
            return
        # mag is full
        if rounds == mrounds:
            pc.notice_(server, user, 'The current magazine is full.')
            return
        # shop purchase
        xp = int(xp) - shopprice(server, channel, user, 1)
        rounds += 1
        duckinfo(server, dchannel, duser, 'xp', str(xp))
        duckinfo(server, dchannel, duser, 'ammo-r', str(rounds))
        pc.notice_(server, user, 'You purchased a single bullet.')
        return
    # 2 - Refill Magazine -----------------------------------------------------------------------------------------
    if int(itemid) == 2:
        # rules disabled
        if game_rules(server, dchannel, 'infammo') == 'on' or game_rules(server, chan, 'bang') == 'off':
            pc.notice_(server, user, 'Based on current game rules, this item is not available.')
            return
        # already full
        if mags == mmags:
            pc.notice_(server, user, 'All your magazines are full.')
            return
        # purchase
        xp = int(xp) - shopprice(server, channel, user, 2)
        mags += 1
        duckinfo(server, dchannel, duser, 'xp', str(xp))
        duckinfo(server, dchannel, duser, 'ammo-m', str(mags))
        pc.notice_(server, user, 'You refilled 1 magazine.')
        return
    # 3 - Gun Cleaning --------------------------------------------------------------------------------------------
    if int(itemid) == 3:
        # rules disabled
        if game_rules(server, dchannel, 'bang') == 'off':
            pc.notice_(server, user, 'Based on current game rules, this item is not available.')
            return
        # don't need it
        if reliability == float(mreliability):
            pc.notice_(server, user, "Your gun doesn't need to be cleaned.")
            return
        # purchase
        xp = int(xp) - shopprice(server, channel, user, 3)
        reliability = mreliability
        gunstats = str(accuracy) + '?' + str(reliability) + '?' + str(mreliability)
        duckinfo(server, dchannel, duser, 'guninfo', gunstats)
        duckinfo(server, dchannel, duser, 'xp', str(xp))
        pc.notice_(server, user, 'Your gun is now cleaned and reliability is restored to maximum.')
        return
    # 4 - Explosive Ammo --------------------------------------------------------------------------------------------
    if int(itemid) == 4:
        # rules disabled
        if game_rules(server, dchannel, 'bang') == 'off':
            pc.notice_(server, user, 'Based on current game rules, this item is not available.')
            return
        # don't need it
        if pc.istok_n(rdata[server, chan]['expl_ammo'], duser, ',', '^', 0) is True:
            pc.notice_(server, user, 'You already own Explosive Ammo. [Rounds left: ' + str(pc.gettok_n(rdata[server, chan]['expl_ammo'], duser, ',', '^', 0, 1)) + ']')
            return
        # purchase
        xp = int(xp) - shopprice(server, channel, user, 4)
        duckinfo(server, dchannel, duser, 'xp', str(xp))
        time_data(server, dchannel, duser, 'expl_ammo', 'add', '50')
        pc.notice_(server, user, 'You bought 50 rounds of Explosive Ammo. Increased damage. These rounds are 15% more likely to hit their targets.')
        return
    # 5 - Return Confiscated Gun ---------------------------------------------------------------------------------------
    if int(itemid) == 5:
        # rules disabled
        if game_rules(server, dchannel, 'gunconf') == 'off' or game_rules(server, dchannel, 'bang') == 'off':
            pc.notice_(server, user, 'Based on current game rules, this item is not available.')
            return
        # don't need it
        # if duser not in rdata[server, chan]['confiscated']:
        if pc.iistok(rdata[server, chan]['confiscated'], duser, ',') is False:
            pc.notice_(server, user, 'Your gun is not currently confiscated.')
            return
        # purchase
        xp = int(xp) - shopprice(server, channel, user, 5)
        duckinfo(server, dchannel, duser, 'xp', str(xp))
        del rdata[server, chan]['confiscated'][duser]
        pc.privmsg_(server, channel, '\x01ACTION returns ' + user.decode() + "'s gun.\x01")
        return
    # 6 - Gun Grease ---------------------------------------------------------------------------------------------------
    if int(itemid) == 6:
        # rules disabled
        if game_rules(server, dchannel, 'bang') == 'off':
            pc.notice_(server, user, 'Based on current game rules, this item is not available.')
            return
        # don't need it
        # if duser in rdata[server, chan]['gun_grease']:
        if pc.istok_n(rdata[server, chan]['gun_grease'], duser, ',', '^', 0) is True:
            # time math here
            ptime = pc.gettok_n(rdata[server, chan]['gun_grease'], duser, ',', '^', 0, 1)
            ptime = pc.cputime() - float(ptime)
            timeval = pc.timeconvert(ptime)
            pc.notice_(server, user, 'You already own Gun Grease. [Time Remaining: ' + str(timeval) + ']')
            return
        # purchase
        xp = int(xp) - shopprice(server, channel, user, 6)
        duckinfo(server, dchannel, duser, 'xp', str(xp))
        time_data(server, channel, duser, 'gun_grease', 'add')
        # rdata[server, chan]['gun_grease'][duser] = pc.cputime()
        pc.notice_(server, user, 'You purchased Gun Grease. Lower jamming odds and gun reliability will last longer for 24 hours.')
        return
    # 7 - Gun Upgrade ------------------------------------------------------------------------------------------------------
    if int(itemid) == 7:
        # rules disabled
        if game_rules(server, dchannel, 'bang') == 'off':
            pc.notice_(server, user, 'Based on current game rules, this item is not available.')
            return
        # don't need it
        if str(accuracy) == '100' and str(mreliability) == '100':
            pc.notice_(server, user, 'Your gun is already fully upgraded.')
            return
        # purchase
        xp = int(xp) - shopprice(server, channel, user, 7)
        duckinfo(server, dchannel, duser, 'xp', str(xp))
        if int(accuracy) < 100:
            accuracy = int(accuracy) + 5
        if int(mreliability) < 100:
            mreliability = int(mreliability) + 5
            reliability = mreliability
        gunstats = str(accuracy) + '?' + str(reliability) + '?' + str(mreliability)
        duckinfo(server, dchannel, duser, 'guninfo', gunstats)
        pc.notice_(server, user, 'You have upgraded your gun. Accuracy and reliability have increased.')
        return
    # 8 - Gun Lock -----------------------------------------------------------------------------------------------------
    if int(itemid) == 8:
        # rules disabled
        if game_rules(server, dchannel, 'bang') == 'off':
            pc.notice_(server, user, 'Based on current game rules, this item is not available.')
            return
        # dont need it
        # if duser in rdata[server, chan]['trigger_lock']:
        if pc.istok_n(rdata[server, chan]['trigger_lock'], duser, ',', '^', 0) is True:
            useleft = pc.gettok_n(rdata[server, chan]['trigger_lock'], duser, ',', '^', 0, 1)
            pc.notice_(server, user, 'You already own Gun Lock. [Remaining Use: ' + str(useleft) + ']')
            return
        # purchase
        xp = int(xp) - shopprice(server, channel, user, 8)
        duckinfo(server, dchannel, duser, 'xp', str(xp))
        # rdata[server, chan]['trigger_lock'][duser] = mrounds
        time_data(server, channel, duser, 'trigger_lock', 'add', str(mrounds))
        pc.notice_(server, user, 'You purchased Gun Lock. The gun will have a safety lock when no ducks are sighted for ' + str(mrounds) + ' uses.')
        return
    # 9 - Silencer ----------------------------------------------------------------------------------------------------
    if int(itemid) == 9:
        # rules disabled
        if game_rules(server, dchannel, 'bang') == 'off':
            pc.notice_(server, user, 'Based on current game rules, this item is not available.')
            return
        # dont need it
        # if duser in rdata[server, chan]['silencer']:
        if pc.istok_n(rdata[server, chan]['silencer'], duser, ',', '^', 0) is True:
            # time math here
            ptime = pc.gettok_n(rdata[server, chan]['silencer'], duser, ',', '^', 0, 1)
            ptime = pc.cputime() - float(ptime)
            timeval = pc.timeconvert(ptime)
            pc.notice_(server, user, 'You already own Silencer. [Time Remaining: ' + str(timeval) + ']')
            return
        # purchase
        xp = int(xp) - shopprice(server, channel, user, 8)
        duckinfo(server, dchannel, duser, 'xp', str(xp))
        # rdata[server, chan]['silencer'][duser] = pc.cputime()
        time_data(server, channel, duser, 'silencer', 'add')
        pc.notice_(server, user, 'You purchased a Silencer for your gun. You will not scare away ducks for 24 hours.')
        return
    # 10 - Lucky Charm -------------------------------------------------------------------------------------------------
    # v1.9.9 - changed from 3-10 random to 4-12 random.
    if int(itemid) == 10:
        # rules disabled
        if game_rules(server, dchannel, 'bang') == 'off':
            pc.notice_(server, user, 'Based on current game rules, this item is not available.')
            return
        # dont need it
        if pc.istok_n(rdata[server, chan]['lucky_charm'], duser, ',', '^', 0) is True:
            # time math here
            ptime = pc.gettok_n(rdata[server, chan]['gun_grease'], duser, ',', '^', 0, 1)
            ptime = pc.cputime() - float(ptime)
            timeval = pc.timeconvert(ptime)
            pc.notice_(server, user, 'You already own Lucky Charm. [Time Remaining: ' + str(timeval) + ']')
            return
        # purchase
        xp = int(xp) - shopprice(server, channel, user, 10)
        duckinfo(server, dchannel, duser, 'xp', str(xp))
        lcxp = pc.rand(4, 12)
        time_data(server, channel, duser, 'lucky_charm', 'add', str(lcxp))
        pc.notice_(server, user, 'You purchased a Lucky Charm. You will earn an extra ' + str(lcxp) + ' xp for 24 hours.')
        return
    # 11 - sunglasses --------------------------------------------------------------------------------------------------
    if int(itemid) == 11:
        # dont need it
        if pc.istok_n(rdata[server, chan]['sunglasses'], duser, ',', '^', 0) is True:
            # time math here
            ptime = pc.gettok_n(rdata[server, chan]['sunglasses'], duser, ',', '^', 0, 1)
            ptime = pc.cputime() - float(ptime)
            timeval = pc.timeconvert(ptime)
            pc.notice_(server, user, 'You already own Sunglasses. [Time Remaining: ' + str(timeval) + ']')
            return
        # cannot buy sunglasses if currently bedazzled
        if pc.istok_n(rdata[server, chan]['bedazzled'], duser, ',', '^', 0) is True:
            # time math here
            # time math here
            ptime = pc.gettok_n(rdata[server, chan]['bedazzled'], duser, ',', '^', 0, 1)
            ptime = pc.cputime() - float(ptime)
            timeval = pc.timeconvert(ptime)
            pc.notice_(server, user, 'You are currently bedazzled and have to wait for it to wear off to use Sunglasses. [Time Remaining: ' + str(timeval) + ']')
            return
        # purchase
        xp = int(xp) - shopprice(server, channel, user, 11)
        duckinfo(server, dchannel, duser, 'xp', str(xp))
        time_data(server, channel, duser, 'sunglasses', 'add')
        pc.notice_(server, user, 'You purchased Sunglasses. You are protected from bedazzlement for 24 hours.')
        return
    # 12 - dry clothes / new clothes -----------------------------------------------------------------------------------
    if int(itemid) == 12:
        # not soggy or bombed
        if pc.istok_n(rdata[server, chan]['soggy'], duser, ',', '^', 0) is False and pc.istok_n(rdata[server, chan]['bombed'], duser, ',', '^', 0) is False:
            pc.notice_(server, user, 'Your clothes are not wet or dirty.')
            return
        # purchase
        xp = int(xp) - shopprice(server, channel, user, 12)
        duckinfo(server, dchannel, duser, 'xp', str(xp))
        # remove soggy
        if pc.istok_n(rdata[server, chan]['soggy'], duser, ',', '^', '0') is True:
            time_data(server, channel, duser, 'soggy', 'rem')
        # remove bombed
        if pc.istok_n(rdata[server, chan]['bombed'], duser, ',', '^', '0') is True:
            time_data(server, channel, duser, 'bombed', 'rem')
        pc.notice_(server, user, 'You purchased New Clothes. You are no longer soggy and/or duck bombed.')
        return
    # 13 - eye drops ---------------------------------------------------------------------------------------------------
    if int(itemid) == 13:
        # not bedazzled
        if pc.istok_n(rdata[server, chan]['bedazzled'], duser, ',', '^', 0) is False:
            pc.notice_(server, user, 'You are not currently bedazzled.')
            return
        # purchase
        xp = int(xp) - shopprice(server, channel, user, 13)
        duckinfo(server, dchannel, duser, 'xp', str(xp))
        # remove bedazzled
        time_data(server, channel, duser, 'bedazzled', 'rem')
        pc.notice_(server, user, 'You purchased Eye Drops. You are no longer bedazzled.')
        return
    # 14 - mirror ------------------------------------------------------------------------------------------------------
    if int(itemid) == 14:
        # invalid stntax --!--
        if target == '':
            # ?? for now
            return
        # target already bedazzled
        if pc.istok_n(rdata[server, chan]['bedazzled'], dtarget, ',', '^', 0) is True:
            pc.notice_(server, user, target.decode() + ' is already bedazzled.')
            return
        # purchase
        xp = int(xp) - shopprice(server, channel, user, 14)
        duckinfo(server, dchannel, duser, 'xp', str(xp))
        # target wearing sunglasses!
        if pc.istok_n(rdata[server, chan]['sunglasses'], dtarget, ',', '^', 0) is True:
            pc.privmsg_(server, channel, user.decode() + ' > Bedazzles ' + target.decode() + ', with a mirror, but ' + target.decode() + ' is wearing sunglasses so the mirror has no effect.')
            return
        # target is bedazzled
        time_data(server, channel, dtarget, 'bedazzled', 'add')
        pc.privmsg_(server, channel, user.decode() + ' > Bedazzles ' + target.decode() + ' with a mirror, who is now blinded for 1 hour.')
        return
    # 15 - handful of sand --------------------------------------------------------------------------------------
    if int(itemid) == 15:
        if target == '':
            # ?? for now
            return
        # rules disabled
        if game_rules(server, dchannel, 'bang') == 'off':
            pc.notice_(server, user, 'Based on current game rules, this item is not available.')
            return
        # purchase
        xp = int(xp) - shopprice(server, channel, user, 15)
        duckinfo(server, dchannel, duser, 'xp', str(xp))
        # sand drops gun reliability by 5%
        # will change this soon to name it random 4-12%
        tacc = pc.gettok(duckinfo(server, dchannel, dtarget, 'guninfo'), 0, '?')
        trel = pc.gettok(duckinfo(server, dchannel, dtarget, 'guninfo'), 1, '?')
        tmrel = pc.gettok(duckinfo(server, dchannel, dtarget, 'guninfo'), 2, '?')
        if float(trel) < 5:
            trel = 0
        if float(trel) >= 5:
            trel = float(trel) - 5
        tgunstats = str(tacc) + '?' + str(trel) + '?' + str(tmrel)
        duckinfo(server, dchannel, dtarget, 'guninfo', tgunstats)
        pc.privmsg_(server, channel, user.decode() + ' > Pours a handful of sand into ' + target.decode() + "'s gun, reducing its reliability by 5%.")
        return
    # 16 - water bucket -------------------------------------------------------------------------------------------
    if int(itemid) == 16:
        if target == '':
            # ?? For now
            return
        # target is already soggy
        if pc.istok_n(rdata[server, chan]['soggy'], dtarget, ',', '^', 0) is True:
            pc.notice_(server, user, target.decode() + ' is already soggy.')
            return
        # purchase
        xp = int(xp) - shopprice(server, channel, user, 16)
        duckinfo(server, dchannel, duser, 'xp', str(xp))
        # target has a rain coat
        if pc.istok_n(rdata[server, chan]['rain_coat'], dtarget, ',', '^', 0) is True:
            pc.privmsg_(server, channel, user.decode() + ' > Dumps a bucket of water on ' + target.decode() + ', but thanks to a rain coat, ' + target.decode() + ' is protected from being soggy.')
            return
        # target is soggy
        time_data(server, channel, dtarget, 'soggy', 'add')
        pc.privmsg_(server, channel, user.decode() + ' > Dumps a bucket of water on ' + target.decode() + '. ' + target.decode() + ' is now soggy for 1 hour.')
        return
    # 17 - sabotage ------------------------------------------------------------------------------------------
    if int(itemid) == 17:
        if target == '':
            # ?? For now
            return
        # rules disabled
        if game_rules(server, dchannel, 'bang') == 'off':
            pc.notice_(server, user, 'Based on current game rules, this item is not available.')
            return
        # target is already sabotaged
        if pc.istok_n(rdata[server, chan]['sabotage'], dtarget, ',', '^', 0) is True:
            pc.notice_(server, channel, target.decode() + "'s gun is already sabotaged.")
            return
        # purchase
        xp = int(xp) - shopprice(server, channel, user, 17)
        duckinfo(server, dchannel, duser, 'xp', str(xp))
        # target is sabotaged
        time_data(server, channel, dtarget, 'sabotage', 'add', '0Z')
        pc.privmsg_(server, channel, user.decode() + ' > Sabotages the gun while ' + target.decode() + " isn't looking.")
        return
    # 18 - accident insurance ------------------------------------------------------------------------------------
    if int(itemid) == 18:
        # rules disabled
        if game_rules(server, dchannel, 'bang') == 'off' or game_rules(server, dchannel, 'gunconf') == 'off':
            pc.notice_(server, user, 'Based on current game rules, this item is not available.')
            return
        # don't need it
        if pc.istok_n(rdata[server, chan]['accident_insurance'], duser, ',', '^', 0) is True:
            # time math here
            # time math here
            ptime = pc.gettok_n(rdata[server, chan]['accident_insurance'], duser, ',', '^', 0, 1)
            ptime = pc.cputime() - float(ptime)
            timeval = pc.timeconvert(ptime)
            pc.notice_(server, user, 'You already own Accident Insurance. [Time Remaining: ' + str(timeval) + ']')
            return
        # purchase
        xp = int(xp) - shopprice(server, channel, user, 18)
        duckinfo(server, dchannel, duser, 'xp', str(xp))
        # add insurance
        time_data(server, channel, duser, 'accident_insurance', 'add')
        pc.notice_(server, user, 'You purchased Accident Insurance. This will prevent gun confiscation for 24 hours.')
        return
    # 19 - bread 'ammo' for feeding ducks -------------------------------------------------------------------------
    if int(itemid) == 19:
        # rules disabled
        if game_rules(server, dchannel, 'infammo') == 'on' or game_rules(server, dchannel, 'bef') == 'off':
            pc.notice_(server, user, 'Based on current game rules, this item is not available.')
            return
        # bread box is full
        if int(loaf) == int(mloaf):
            pc.notice_(server, user, 'Your bread box is full.')
            return
        # purchase
        xp = int(xp) - shopprice(server, channel, user, 19)
        duckinfo(server, dchannel, duser, 'xp', str(xp))
        # get bread
        loaf = int(loaf) + 1
        duckinfo(server, dchannel, duser, 'bread-l', str(loaf))
        pc.notice_(server, user, 'You purchased 1 loaf of bread.')
        return
    # 20 - bag of popcorn -----------------------------------------------------------------------------------------
    if int(itemid) == 20:
        # rules disabled
        if game_rules(server, dchannel, 'bef') == 'off':
            pc.notice_(server, user, 'Based on current game rules, this item is not available.')
            return
        # dont need it
        if pc.istok_n(rdata[server, chan]['popcorn'], duser, ',', '^', 0) is True:
            useleft = pc.gettok_n(rdata[server, chan]['popcorn'], duser, ',', '^', 0, 1)
            pc.notice_(server, user, 'You already have a bag of popcorn. [Remaining pieces: ' + str(useleft) + ']')
            return
        # purchase
        xp = int(xp) - shopprice(server, channel, user, 20)
        duckinfo(server, dchannel, duser, 'xp', str(xp))
        # get popcorn
        time_data(server, dchannel, duser, 'popcorn', 'add', '50')
        pc.notice_(server, user, 'You purchased a Bag of Popcorn. You can now have better luck at befriending ducks for 50 pieces.')
        return
    # 21 - bread box lock ------------------------------------------------------------------------------------------
    if int(itemid) == 21:
        # rules disabled
        if game_rules(server, dchannel, 'bef') == 'off':
            pc.notice_(server, user, 'Based on current game rules, this item is not available.')
            return
        # already own this item
        if pc.istok_n(rdata[server, chan]['bread_lock'], duser, ',', '^', 0) is True:
            useleft = pc.gettok_n(rdata[server, chan]['bread_lock'], duser, ',', '^', 0, 1)
            pc.notice_(server, user, 'You already own Bread Box Lock. [Remaining uses: ' + str(useleft) + ']')
            return
        # purchase
        xp = int(xp) - shopprice(server, channel, user, 21)
        duckinfo(server, dchannel, duser, 'xp', str(xp))
        # get lock
        time_data(server, dchannel, duser, 'bread_lock', 'add', str(mbread))
        pc.notice_(server, user, 'You purchased Bread Box Lock. You can not toss bread when no ducks are around for ' + str(mbread) + ' uses.')
        return
    # 22 - rain coat -------------------------------------------------------------------------------------------------
    if int(itemid) == 22:
        # currently soggy
        if pc.istok_n(rdata[server, chan]['soggy'], duser, ',', '^', 0) is True:
            # time math here
            ptime = pc.gettok_n(rdata[server, chan]['soggy'], duser, ',', '^', 0, 1)
            ptime = pc.cputime() - float(ptime)
            timeval = pc.timeconvert(ptime)
            pc.notice_(server, user, 'You are currently soggy and cannot purchase Rain Coat until you are dry. [Time Remaining: ' + str(timeval) + ']')
            return
        # don't need it
        if pc.istok_n(rdata[server, chan]['rain_coat'], duser, ',', '^', 0) is True:
            # time math here
            ptime = pc.gettok_n(rdata[server, chan]['rain_coat'], duser, ',', '^', 0, 1)
            ptime = pc.cputime() - float(ptime)
            timeval = pc.timeconvert(ptime)
            pc.notice_(server, user, 'You already own Rain Coat. [Time Remaining: ' + str(timeval) + ']')
            return
        # purchase
        xp = int(xp) - shopprice(server, channel, user, 22)
        duckinfo(server, dchannel, duser, 'xp', str(xp))
        # get rain coat
        time_data(server, dchannel, duser, 'rain_coat', 'add')
        pc.notice_(server, user, 'You purchased Rain Coat. This will protect against water buckets and duck bombs for 24 hours.')
        return
    # 23 - magazine upgrade ----------------------------------------------------------------------------------------
    if int(itemid) == 23:
        # rules disabled
        if game_rules(server, dchannel, 'bang') == 'off':
            pc.notice_(server, user, 'Based on current game rules, this item is not available.')
            return
        # no more upgradse
        if int(mrounds) == 12:
            pc.notice_(server, user, 'Your magazines are already fully upgraded, and cannot be upgraded further.')
            return
        # purchase
        xp = int(xp) - shopprice(server, channel, user, 23)
        duckinfo(server, dchannel, duser, 'xp', str(xp))
        # get upgrade
        mrounds = int(mrounds) + 1
        duckinfo(server, dchannel, duser, 'bread-mb', str(mrounds))
        pc.notice_(server, user, 'You upgraded your magazines! They can now hold ' + str(mrounds) + ' rounds.')
        return
    # 24 - additional magazine -----------------------------------------------------------------------------------
    if int(itemid) == 24:
        # rules disabled
        if game_rules(server, dchannel, 'bang') == 'off':
            pc.notice_(server, user, 'Based on current game rules, this item is not available.')
            return
        # no more upgrade
        if int(mmags) == 5:
            pc.notice_(server, user, 'You cannot carry any more additional magazines.')
            return
        # purchase
        xp = int(xp) - shopprice(server, channel, user, 24)
        duckinfo(server, dchannel, duser, 'xp', str(xp))
        # get magazine
        mmags = int(mmags) + 1
        duckinfo(server, dchannel, duser, 'ammo-mm', str(mmags))
        pc.notice_(server, user, 'You purchased an additional magazine, you can now carry ' + str(mmags) + ' magazines.')
        return
    return

# ======================================================================================================================
# Swimming !swim
async def swim(server, channel, user):
    global rdata

    dchannel = channel.decode()
    dchannel = dchannel.lower()
    chan = dchannel.replace('#', '')
    duser = user.decode()
    duser = duser.lower()

    xp = duckinfo(server, dchannel, duser, 'xp')
    level = duckinfo(server, dchannel, duser, 'level')

    # deterimine xp subtract
    rxp = 2
    if int(xp) >= 10000 or int(level) >= 10:
        rxp = 12
    elif 5000 <= int(xp) < 10000 and int(level) < 10:
        rxp = 8
    elif 5000 > int(xp) >= 1500:
        rxp = 4
    # deduct xp
    if int(rxp) >= int(xp):
        xp = 0
        duckinfo(server, dchannel, duser, 'xp', str(xp))
    if int(rxp) < int(xp):
        xp = int(xp) - int(rxp)
        duckinfo(server, dchannel, duser, 'xp', str(xp))
    # apply soggy
    if pc.istok_n(rdata[server, chan]['soggy'], duser, ',', '^', 0) is True:
        time_data(server, channel, duser, 'soggy', 'rem')
    time_data(server, channel, duser, 'soggy', 'add')
    # wash duck bomb off
    if pc.istok_n(rdata[server, chan]['bombed'], duser, ',', '^', 0) is True:
        time_data(server, channel, duser, 'bombed', 'rem')
        pc.privmsg_(server, channel, user.decode() + ' > Jumps into the duck pond, and rinses off the duck bombs, but ' + user.decode() + ' is now soggy for 1 hour \x034[-' + str(rxp) + ' xp]\x03')
        return
    # confirmation
    pc.privmsg_(server, channel, user.decode() + ' > Decideds to jump in the duck pond. What are you doing? ' + user.decode() + ' is now soggy for 1 hour \x034[-' + str(rxp) + ' xp]\x03')
    return

# ======================================================================================================================
# Shooting guns

# !bang ----------------------------------------------------------------------------------------------------------------
# async def bang(server, channel, user):
def bang(server, channel, user):
    global rdata
    dchannel = channel.decode()
    dchannel = dchannel.lower()
    chan = dchannel.replace('#', '')
    duser = user.decode()
    duser = duser.lower()

    # new users with no stats
    # b'playername' = Rounds?Mags?MaxRounds?MaxMags,Ducks,GoldenDucks,xp,level,levelup,
    #                 notusedanymore,notusedanymore,Accuracy?Reliability?MaxReliability,BestTime,
    #                 Accidents,Bread?MaxBread,Loaf,MaxLoaf,DuckFriends
    if not pc.cnfexists('duckhunt.cnf', server + '_' + chan + '_ducks', duser):
        dinfo = '7?3?7?3,0,0,0,1,200,0,0,75?80?80,0,0,12?12?3?3,0'
        pc.cnfwrite('duckhunt.cnf', server + '_' + chan + '_ducks', duser, str(dinfo))
        # pc.cnfwrite('duckhunt.cnf', dsect, 'cache', '1')  # ???

    # gun is confiscated
    if pc.iistok(rdata[server, chan]['confiscated'], duser, ',') is True:
        pc.privmsg_(server, channel, user.decode() + ' > \x034You are not armed.\x03')
        return

    # check all timed items/effects
    time_data(server, dchannel, duser, 'all-time')

    # player is soggy
    if pc.istok_n(rdata[server, chan]['soggy'], duser, ',', '^', 0) is True:
        # determine time remaining
        ptime = pc.gettok_n(rdata[server, chan]['gun_grease'], duser, ',', '^', 0, 1)
        ptime = pc.cputime() - float(ptime)
        timeval = pc.timeconvert(ptime)
        pc.privmsg_(server, channel, user.decode() + " > \x034Your clothes are all soggy. You cannot hunt ducks until you're dry. \x033[Time Remaining: " + str(timeval) + ']\x03')
        return

    # player is bombed
    if pc.istok_n(rdata[server, chan]['bombed'], duser, ',', '^', 0) is True:
        pc.privmsg_(server, channel, user.decode() + " > \x034Your clothes are crusty and filthy from being duck bombed. You cannot hunt ducks like this, you need new clothes.")
        return

    # gun is sabotaged
    # add duck exists to this statement
    if pc.istok_n(rdata[server, chan]['sabotage'], duser, ',', '^', 0) is True and pc.istok_n(rdata[server, chan]['trigger_lock'], duser, ',', '^', 0) is False:
        time_data(server, channel, duser, 'sabotage', 'rem')
        pc.privmsg_(server, channel, "Sabotaged")
        return

    # shooting data
    # ammo = ''
    rounds = int(duckinfo(server, dchannel, duser, 'ammo-r'))
    mrounds = int(duckinfo(server, dchannel, duser, 'ammo-mr'))
    mags = int(duckinfo(server, dchannel, duser, 'ammo-m'))
    mmags = int(duckinfo(server, dchannel, duser, 'ammo-mm'))

    # gun data
    gunstats = duckinfo(server, dchannel, duser, 'guninfo')
    accuracy = int(pc.gettok(gunstats, 0, '?'))
    reliability = float(pc.gettok(gunstats, 1, '?'))
    mreliability = int(pc.gettok(gunstats, 2, '?'))
    # player data
    xp = duckinfo(server, dchannel, duser, 'xp')
    best = duckinfo(server, dchannel, duser, 'best')
    ducks = duckinfo(server, dchannel, duser, 'ducks')
    gducks = duckinfo(server, dchannel, duser, 'gducks')
    accidents = duckinfo(server, dchannel, duser, 'accidents')
    level = duckinfo(server, dchannel, duser, 'level')
    levelup = duckinfo(server, dchannel, duser, 'levelup')

    # player gun needs service
    if float(reliability) <= 60:
        pc.privmsg_(server, channel, user.decode() + ' > \x0314*CLICK-CLACK*\x03     \x034Your gun is too dirty and needs to be cleaned...\x03')
        return

    # empty magazine
    if int(rounds) == 0:
        if game_rules(server, dchannel, 'infammo') == 'on':
            pc.privmsg_(server, channel, user.decode() + ' > \x0314*CLICK*\x03     \x034EMPTY MAGAZINE\x03 | Rounds:\x034 ' + str(rounds) + '\x03/' + str(mrounds) + ' | Magazines: \x02\x033Inf\x02\x03')
            return
        else:
            pc.privmsg_(server, channel, user.decode() + ' > \x0314*CLICK*\x03     \x034EMPTY MAGAZINE\x03 | Rounds:\x034 ' + str(rounds) + '\x03/' + str(mrounds) + ' | Magazines: ' + str(mags) + '/' + str(mmags))
            return

    # gun lock
    if pc.istok_n(rdata[server, chan]['trigger_lock'], duser, ',', '^', 0) is True and ducksdata(server, dchannel) == 0:
        useleft = pc.gettok_n(rdata[server, chan]['trigger_lock'], duser, ',', '^', 0, 1)
        if int(useleft) == 1:
            useleft = 0
            user_data(server, dchannel, duser, 'trigger_lock', 'rem')
        if int(useleft) > 1:
            useleft = int(useleft) - 1
            user_data(server, dchannel, duser, 'trigger_lock', 'edit', str(useleft))
        pc.privmsg_(server, channel, user.decode() + ' > \x0314*CLICK*\x03    \x034GUN LOCKED   [' + str(useleft) + ']\x03')
        return

    # gun jamming
    if pc.iistok(rdata[server, chan]['duck_jam'], duser, ',') is False or pc.iistok(rdata[server, chan]['jammed'], duser, ',') is True:
        jam = round(float(reliability))
        jammed = pc.rand(1, 100)

        if 70 >= int(jam) > 60:
            # user has gun grease
            if pc.istok_n(rdata[server, chan]['gun_grease'], duser, ',', '^', 0) is True:
                jam = jam + 13
                jammed = random.randint(1, int(jam))
            # user does not have gun grease
            if pc.istok_n(rdata[server, chan]['gun_grease'], duser, ',', '^', 0) is False:
                jam = jam + 25
                jammed = random.randint(1, int(jam))

        if jammed >= float(reliability) or pc.iistok(rdata[server, chan]['jammed'], duser, ',') is True:
            # add user to jammed list if list is empty
            if rdata[server, chan]['jammed'] == '0':
                rdata[server, chan]['jammed'] = duser
            # check for user, and add if not listed
            if pc.iistok(rdata[server, chan]['jammed'], duser, ',') is False:
                newdat = rdata[server, chan]['jammed'] + ',' + duser
                rdata[server, chan]['jammed'] = newdat
            pc.cnfwrite('duckhunt.cnf', server + '_' + chan, 'jammed', rdata[server, chan]['jammed'])
            pc.privmsg_(server, channel, user.decode() + ' > \x0314*CLACK*\x03     \x034Your gun is jammed, you must reload to unjam it...\x03')
            return

    # not jammed
    if pc.iistok(rdata[server, chan]['duck_jam'], duser, ',') is True:
        if pc.numtok(rdata[server, chan]['duck_jam'], ',') == 1:
            rdata[server, chan]['duck_jam'] = '0'
            pc.cnfwrite('duckhunt.cnf', server + '_' + chan, 'duck_jam', rdata[server, chan]['duck_jam'])
        else:
            token = rdata[server, chan]['duck_jam'].split(',')
            newstring = '0'
            for x in range(len(token)):
                if token[x] == duser:
                    continue
                if newstring == '0':
                    newstring = token[x]
                    continue
                if newstring != '0':
                    newstring = newstring + ',' + token[x]
                    continue
            rdata[server, chan]['duck_jam'] = newstring
            pc.cnfwrite('duckhunt.cnf', server + '_' + chan, 'duck_jam', rdata[server, chan]['duck_jam'])

    # fired a round
    rounds = int(rounds) - 1
    # ammo deduction
    duckinfo(server, dchannel, duser, 'ammo-r', str(rounds))

    # has expl ammo
    if pc.istok_n(rdata[server, chan]['expl_ammo'], duser, ',', '^', 0) is True:
        expammo = pc.gettok_n(rdata[server, chan]['expl_ammo'], duser, ',', '^', 0, 1)
        if int(expammo) > 1:
            # use 1 expl_ammo
            expammo = int(expammo) - 1
            user_data(server, dchannel, duser, 'expl_ammo', 'edit', str(expammo))
            # extra wear for ammo type
            reliability = float(reliability) - 0.03
        if int(expammo) == 1:
            # used up the last expl_ammo
            user_data(server, dchannel, duser, 'expl_ammo', 'rem')
            reliability = float(reliability) - 0.03

    # reliability deduction
    # does not have gun_grease
    if pc.istok_n(rdata[server, chan]['gun_grease'], duser, ',', '^', 0) is False:
        reliability = float(reliability) - 0.1

    # has gun_grease
    if pc.istok_n(rdata[server, chan]['gun_grease'], duser, ',', '^', 0) is True:
        reliability = float(reliability) - 0.01

    reliability = round(reliability, 2)
    guninfo = str(accuracy) + '?' + str(reliability) + '?' + str(mreliability)
    duckinfo(server, dchannel, duser, 'guninfo', guninfo)

    # a duck exists
    if ducksdata(server, dchannel) > 0:

        # duck fear management
        # user does not have silencer
        if pc.istok_n(rdata[server, chan]['silencer'], duser, ',', '^', 0) is False:
            if not rdata[server, chan]['fear_factor']:
                rdata[server, chan]['fear_factor'] = 0
            # scared the ducks away
            if rdata[server, chan]['fear_factor'] >= rdata[server, chan]['duckfear']:
                for x in range(len(rdata[server, chan]['duck'])):
                    if rdata[server, chan]['duck'][x] != '0':
                        rdata[server, chan]['duck'][x] = '0'
                    continue
                pc.privmsg_(server, channel, b"\x034Frightened by so much noise, all ducks in the area have fled.\x03     \x0314\xc2\xb7\xc2\xb0'`'\xc2\xb0-.,\xc2\xb8\xc2\xb8.\xc2\xb7\xc2\xb0'`")
                rdata[server, chan]['fear_factor'] = False
                rdata[server, chan]['gold_factor'] = False
                return
            # ducks are not scared
            if rdata[server, chan]['fear_factor'] < rdata[server, chan]['duckfear']:
                scare = pc.rand(2, 8)
                newdata = rdata[server, chan]['fear_factor'] + scare
                rdata[server, chan]['fear_factor'] = int(newdata)

        # check if player is bedazzled
        if pc.istok_n(rdata[server, chan]['bedazzled'], duser, ',', '^', 0) is True:
            # player is bedazzled
            accidents = int(accidents) + 1
            duckinfo(server, dchannel, duser, 'accidents', str(accidents))

            damage = ''
            dmg = pc.rand(1, 3)

            # determine xp subtract
            rxp = dmg
            if int(xp) >= 10000:
                rxp = dmg * 2
            if 5000 <= int(xp) < 10000:
                rxp = dmg + 3
            # if int(xp) < 5000 and int(xp) >= 1500:
            if 5000 > int(xp) >= 1500:
                rxp = dmg + 1

            # gunconf off is off, extra -4 xp
            if game_rules(server, dchannel, 'gunconf') == 'off':
                rxp = rxp + 4

            if int(xp) <= rxp:
                xp = 0
            if int(xp) > rxp:
                xp = int(xp) - rxp
                duckinfo(server, dchannel, duser, 'xp', str(xp))

            # determine accident
            if dmg == 1:
                damage = 'Shot a distant window!'
            if dmg == 2:
                damage = 'Shot another hunter!'
            if dmg == 3:
                damage = 'Wildfire!'

            # bedazzled - gun confiscation is turned OFF
            if game_rules(server, dchannel, 'gunconf') == 'off':
                pc.privmsg_(server, channel, user.decode() + ' > \x0314*BANG*\x034     Missed due to being bedazzled. [-' + str(rxp) + ' xp] [' + str(damage) + ']\x03')
                return

            # bedazzled - gun confiscation is ON and player has accident insurance
            if pc.istok_n(rdata[server, chan]['accident_insurance'], duser, ',', '^', 0) is True:
                pc.privmsg_(server, channel, user.decode() + ' > \x0314*BANG*\x034     Missed due to being bedazzled. [-' + str(rxp) + ' xp] \x033[GUN NOT CONFISCATED: Accident Insurance]\x03')
                return
            # bedazzled - gun confiscation is ON and player DOES NOT have accident insurance
            if pc.istok_n(rdata[server, chan]['accident_insurance'], duser, ',', '^', 0) is False:
                if rdata[server, chan]['confiscated'] != '0':
                    newdata = rdata[server, chan]['confiscated'] + ',' + duser
                    rdata[server, chan]['confiscated'] = newdata
                if rdata[server, chan]['confiscated'] == '0':
                    rdata[server, chan]['confiscated'] = duser
                pc.cnfwrite('duckhunt.cnf', server + '_' + chan, 'confiscated', rdata[server, chan]['confiscated'])
                pc.privmsg_(server, channel, user.decode() + ' > \x0314*BANG*\x034     Missed due to being debazzled. [-' + str(rxp) + ' xp] [GUN CONFISCATED: ' + damage + ']\x03')
                return

        # determine duck
        duckdata = '0'
        duckid = ''
        duck_time = '0'
        for x in range(len(rdata[server, chan]['duck'])):
            if rdata[server, chan]['duck'][x] == '0':
                continue
            if rdata[server, chan]['duck'][x] != '0':
                duckdata = rdata[server, chan]['duck'][x]
                duckid = str(x)
                duck_time = pc.gettok(duckdata, 0, ',')
                break

        # determine hit or miss
        # hit or miss normal duck
        hitormiss = pc.rand(1, 100)

        # normal-gold duck
        if pc.gettok(duckdata, 1, ',') == 'gold':
            hitormiss = pc.rand(1, 200)

        # golden duck
        if pc.gettok(duckdata, 1, ',') == 'golden':
            hitormiss = pc.rand(1, 140)

        # expl ammo adds +15 accuracy
        if pc.istok_n(rdata[server, chan]['expl_ammo'], duser, ',', '^', 0) is True:
            hitormiss = hitormiss - 15

        # missed
        if hitormiss > int(accuracy):
            ricochet = pc.rand(1, 100)
            # missed shot ricochet
            if int(game_rules(server, dchannel, 'gunricochet')) > 0 and ricochet < int(game_rules(server, dchannel, 'gunricochet')):

                # accidents
                accidents = int(accidents) + 1
                duckinfo(server, dchannel, duser, 'accidents', str(accidents))

                # determine damage
                damage = ''
                dmg = pc.rand(1, 3)
                if dmg == 1:
                    damage = 'strikes a distant window!'
                if dmg == 2:
                    damage = 'strikes another hunter!'
                if dmg == 3:
                    damage = 'starts a wildfire!'

                # determine xp subtract
                rxp = dmg
                if int(xp) >= 10000:
                    rxp = dmg * 2
                # if int(xp) >= 5000 and int(xp) < 10000:
                if 5000 <= int(xp) < 10000:
                    rxp = dmg + 3
                # if int(xp) < 5000 and int(xp) >= 1500:
                if 5000 > int(xp) >= 1500:
                    rxp = dmg + 1

                # gunconf is off
                if game_rules(server, dchannel, 'gunconf') == 'off':
                    # deduct xp
                    rxp = rxp + 4
                    if int(xp) <= rxp:
                        xp = 0
                    if int(xp) > rxp:
                        xp = int(xp) - rxp
                    duckinfo(server, dchannel, duser, 'xp', str(xp))
                    pc.privmsg_(server, channel, user.decode() + ' > \x0314*BANG*    *PEEEWWWWW*\x03    The bullet ricochets and ' + str(damage) + ' \x034[-' + str(dmg) + ' xp] [Ricochet]\x03')
                    return

                # gun conf is ON, player has accident insurance
                if pc.istok_n(rdata[server, chan]['accident_insurance'], duser, ',', '^', 0) is True:
                    # deduct xp
                    rxp = rxp + 4
                    if int(xp) <= rxp:
                        xp = 0
                    if int(xp) > rxp:
                        xp = int(xp) - rxp
                    duckinfo(server, dchannel, duser, 'xp', str(xp))
                    pc.privmsg_(server, channel, user.decode() + ' > \x0314*BANG*    *PEEEWWWWW*\x03    The bullet ricochets and ' + damage + ' \x034[-' + str(dmg) + ' xp]\x03 \x033[GUN NOT CONFISCATED: Accident Insurance]\x03')
                    return

                # gun conf is ON, player does not have accident insurance
                if pc.istok_n(rdata[server, chan]['accident_insurance'], duser, ',', '^', 0) is False:
                    # deduct xp
                    if int(xp) <= rxp:
                        xp = 0
                    if int(xp) > rxp:
                        xp = int(xp) - rxp
                    duckinfo(server, dchannel, duser, 'xp', str(xp))
                    # gun confiscated
                    ctrl_data(server, dchannel, duser, 'confiscated', 'add')
                    pc.privmsg_(server, channel, user.decode() + ' > \x0314*BANG*    *PEEEWWWWW*\x03    The bullet ricochets and ' + damage + ' \x034[-' + str(dmg) + ' xp] [GUN CONFISCATED: Ricochet]\x03')
                    return

            # normal missed shot
            if pc.gettok(duckdata, 1, ',') == 'normal':
            # determine xp tier
                if int(xp) >= 10000 or int(level) >= 10:
                    rxp = 7
                # elif int(xp) >= 5000 and int(xp) < 10000 and int(level) < 10:
                elif 5000 <= int(xp) < 10000 and int(level) < 10:
                    rxp = 5
                # elif int(xp) < 5000 and int(xp) >= 1500:
                elif 5000 > int(xp) >= 1500:
                    rxp = 2
                else:
                    rxp = 1
                # deduct xp
                if int(xp) <= int(rxp):
                    xp = 0
                if int(xp) > int(rxp):
                    xp = int(xp) - int(rxp)
                duckinfo(server, dchannel, duser, 'xp', str(xp))
                pc.privmsg_(server, channel, user.decode() + ' > \x0314*BANG*\x03     \x034MISSED   [-' + str(rxp) + ' xp]\x03')
                return

            # normal-gold missed shot
            if pc.gettok(duckdata, 1, ',') == 'gold':
                # determine xp tier
                if int(xp) >= 10000 or int(level) >= 10:
                    rxp = 7
                # elif int(xp) >= 5000 and int(xp) < 10000 and int(level) < 10:
                elif 5000 <= int(xp) < 10000 and int(level) < 10:
                    rxp = 5
                # elif int(xp) < 5000 and int(xp) >= 1500:
                elif 5000 > int(xp) >= 1500:
                    rxp = 2
                else:
                    rxp = 1
                # deduct xp
                if int(xp) <= int(rxp):
                    xp = 0
                if int(xp) > int(rxp):
                    xp = int(xp) - int(rxp)
                duckinfo(server, dchannel, duser, 'xp', str(xp))

                # first miss, not golden yet
                if pc.numtok(duckdata, ',') == 4:
                    duckdata = duckdata + ',1'
                    rdata[server, chan]['duck'][int(duckid)] = duckdata
                    pc.privmsg_(server, channel, user.decode() + ' > \x0314*BANG*\x03     \x034MISSED   [-' + str(rxp) + ' xp]\x03')
                    return

                # determine if duck will turn golden
                if pc.numtok(duckdata, ',') == 5 and pc.gettok(duckdata, 1, ',') == 'gold':
                    if int(pc.gettok(duckdata, 4, ',')) > 1:
                        duckstat = pc.rand(4, 7)
                        duckdata = pc.gettok(duckdata, 0, ',') + ',golden,' + str(duckstat) + ',' + pc.gettok(duckdata, 3, ',')
                        rdata[server, chan]['duck'][int(duckid)] = duckdata
                        pc.privmsg_(server, channel, user.decode() + ' > \x0314*BANG*\x03     \x034MISSED   [-' + str(rxp) + ' xp]\x037   \x02\\_O<    * GOLDEN DUCK DETECTED *\x02\x03')
                        return
                    if int(pc.gettok(duckdata, 4, ',')) <= 1:
                        duckstat = int(pc.gettok(duckdata, 4, ',')) + 1
                        duckdata = pc.gettok(duckdata, 0, ',') + ',' + pc.gettok(duckdata, 1, ',') + ',' + pc.gettok(duckdata, 2, ',') + ',' + pc.gettok(duckdata, 3, ',') + ',' + str(duckstat)
                        rdata[server, chan]['duck'][int(duckid)] = duckdata
                        pc.privmsg_(server, channel, user.decode() + ' > \x0314*BANG*\x03     \x034MISSED   [-' + str(rxp) + ' xp]\x03')
                        return

            # golden missed shot
            if pc.gettok(duckdata, 1, ',') == 'golden':
                # determine xp tier
                if int(xp) >= 10000 or int(level) >= 10:
                    rxp = 8
                elif int(xp) >= 5000 and int(xp) < 10000 and int(level) < 10:
                    rxp = 6
                elif int(xp) < 5000 and int(xp) >= 1500:
                    rxp = 4
                else:
                    rxp = 2
                # deduct xp
                if int(xp) <= int(rxp):
                    xp = 0
                if int(xp) > int(rxp):
                    xp = int(xp) - int(rxp)
                duckinfo(server, dchannel, duser, 'xp', str(xp))
                pc.privmsg_(server, channel, user.decode() + ' > \x0314*BANG*\x03     \x034MISSED   [-' + str(rxp) + ' xp]\x03')
                return
        # hit
        if hitormiss <= int(accuracy):

            # normal ducks
            if pc.gettok(duckdata, 1, ',') == 'normal':

                # top shot counter
                # tshotplus(server, dchannel)

                # player reaction time determination
                reacttime = round(pc.cputime() - float(duck_time), 2)
                if best == '0':
                    duckinfo(server, dchannel, duser, 'best', str(reacttime))
                    best = reacttime
                if float(best) > reacttime:
                    duckinfo(server, dchannel, duser, 'best', str(reacttime))
                # player duck count increase
                ducks = int(ducks) + 1
                duckinfo(server, dchannel, duser, 'ducks', str(ducks))
                # increase player xp - does not have lucky charm
                if pc.istok_n(rdata[server, chan]['lucky_charm'], duser, ',', '^', 0) is False:
                    exp = rdata[server, chan]['duckexp']
                    xp = int(xp) + exp
                    duckinfo(server, dchannel, duser, 'xp', str(xp))
                    pc.privmsg_(server, channel, user.decode() + ' > \x0314*BANG*\x03     you shot down the duck in ' + str(reacttime) + ' seconds.     \x02\\_X<\x02   \x0314*KWAK*\x03   \x033[+' + str(exp) + ' xp] [TOTAL DUCKS: ' + str(ducks) + ']\x03')
                # increase player xp - has lucky charm
                if pc.istok_n(rdata[server, chan]['lucky_charm'], duser, ',', '^', 0) is True:
                    lcxp = pc.gettok_n(rdata[server, chan]['lucky_charm'], duser, ',', '^', 0, 2)
                    exp = rdata[server, chan]['duckexp'] + int(lcxp)
                    xp = int(xp) + exp
                    duckinfo(server, dchannel, duser, 'xp', str(xp))
                    pc.privmsg_(server, channel, user.decode() + ' > \x0314*BANG*\x03     you shot down the duck in ' + str(reacttime) + ' seconds.     \x02\\_X<\x02   \x0314*KWAK*\x03   \x033[+' + str(exp) + ' xp - Lucky Charm] [TOTAL DUCKS: ' + str(ducks) + ']\x03')
                # reset duck info
                rdata[server, chan]['duck'][int(duckid)] = '0'
                rdata[server, chan]['timer'] = pc.cputime()
                # silently rearms all confiscated guns
                if game_rules(server, dchannel, 'gunconf') == 'on':
                    ctrl_data(server, dchannel, '0', 'confiscated', 'clear')
                # searching the bushes
                if int(game_rules(server, dchannel, 'thebushes')) > 0:
                    thebushes = game_rules(server, dchannel, 'thebushes')
                    searchbush = pc.rand(1, 100)
                    if int(searchbush) < int(thebushes):
                        bushes = bush_search(server, dchannel, user.decode())
                        pc.privmsg_(server, channel, user.decode() + ' > ' + str(bushes))
                # check for level up
                if int(xp) >= int(levelup):
                    level_up(server, dchannel, user.decode())
                return

            # normal-gold ducks
            if pc.gettok(duckdata, 1, ',') == 'gold':
                # on first hit, turns golden (golden duck detected)
                ddmg = 1

                # has expl_ammo
                if pc.istok_n(rdata[server, chan]['expl_ammo'], duser, ',', '^', 0) is True:
                    ddmg = 2

                duckhp = pc.gettok(duckdata, 2, ',')
                duckhp = int(duckhp) - int(ddmg)
                duckstat = pc.gettok(duckdata, 0, ',') + ',golden,' + str(duckhp) + ',' + pc.gettok(duckdata, 3, ',')
                rdata[server, chan]['duck'][int(duckid)] = duckstat
                # duckdata = duckstat

                pc.privmsg_(server, channel, user.decode() + ' > \x0314*BANG*\x03     The duck surivived!     \x02\x034\\_O< [Life -' + str(ddmg) + ']\x03\x02     \x02\x037* GOLDEN DUCK DETECTED *\x02\x03')
                return

            # golden ducks
            if pc.gettok(duckdata, 1, ',') == 'golden':
                
                duckhp = pc.gettok(duckdata, 2, ',')

                # duck survived - expl_ammo
                if pc.istok_n(rdata[server, chan]['expl_ammo'], duser, ',', '^', 0) is True and int(duckhp) > 2:
                    ddmg = 2
                    duckhp = int(duckhp) - int(ddmg)
                    duckstat = pc.gettok(duckdata, 0, ',') + ',' + pc.gettok(duckdata, 1, ',') + ',' + str(duckhp) + ',' + pc.gettok(duckdata, 3, ',')
                    rdata[server, chan]['duck'][int(duckid)] = duckstat
                    duckdata = duckstat
                    pc.privmsg_(server, channel, user.decode() + ' > \x0314*BANG*\x03     The GOLDEN DUCK surivived!     \x02\x034\\_O< [Life -' + str(ddmg) + ']\x03\x02')
                    return

                # duck survived - regular ammo
                if pc.istok_n(rdata[server, chan]['expl_ammo'], duser, ',', '^', 0) is False and int(duckhp) > 1:
                    ddmg = 1
                    duckhp = int(duckhp) - int(ddmg)
                    duckstat = pc.gettok(duckdata, 0, ',') + ',' + pc.gettok(duckdata, 1, ',') + ',' + str(duckhp) + ',' + pc.gettok(duckdata, 3, ',')
                    rdata[server, chan]['duck'][int(duckid)] = duckstat
                    duckdata = duckstat
                    pc.privmsg_(server, channel, user.decode() + ' > \x0314*BANG*\x03     The GOLDEN DUCK surivived!     \x02\x034\\_O< [Life -' + str(ddmg) + ']\x03\x02')
                    return

                # shot down the golden duck
                expl = False
                if pc.istok_n(rdata[server, chan]['expl_ammo'], duser, ',', '^', 0) is True and int(duckhp) <= 2:
                    expl = True

                if int(duckhp) == 1 or expl is True:

                    # TOP SHOT COUNTER

                    if expl is True:
                        expl = False

                    # player reaction time determination
                    reacttime = round(pc.cputime() - float(duck_time), 2)
                    if best == '0':
                        duckinfo(server, dchannel, duser, 'best', str(reacttime))
                        best = reacttime
                    if float(best) > reacttime:
                        duckinfo(server, dchannel, duser, 'best', str(reacctime))
                    # increase golden ducks
                    gducks = int(gducks) + 1
                    duckinfo(server, dchannel, duser, 'gducks', str(gducks))
                    # increase xp
                    exp = int(rdata[server, chan]['duckexp']) * 3
                    # does not have lucky charm
                    if pc.istok_n(rdata[server, chan]['lucky_charm'], duser, ',', '^', 0) is False:
                        # exp = int(rdata[server, chan]['duckexp']) * 3
                        xp = int(xp) + exp
                        duckinfo(server, dchannel, duser, 'xp', str(xp))
                        pc.privmsg_(server, channel, user.decode() + ' > \x0314*BANG*\x03     you shot down the GOLDEN DUCK in ' + str(reacttime) + ' seconds.     \x02\\_X<\x02   \x0314*KWAK*\x03   \x033[+' + str(exp) + ' xp] [TOTAL GOLDEN DUCKS: ' + str(gducks) + ']\x03')
                    # increase xp has lucky charm
                    if pc.istok_n(rdata[server, chan]['lucky_charm'], duser, ',', '^', 0) is True:
                        # exp = int(rdata[server, chan]['duckexp']) * 3
                        lcxp = pc.gettok_n(rdata[server, chan]['lucky_charm'], duser, ',', '^', 0, 2)
                        exp = int(exp) + int(lcxp)
                        xp = int(xp) + int(exp)
                        duckinfo(server, dchannel, duser, 'xp', str(xp))
                        pc.privmsg_(server, channel, user.decode() + ' > \x0314*BANG*\x03     you shot down the GOLDEN DUCK in ' + str(reacttime) + ' seconds.     \x02\\_X<\x02   \x0314*KWAK*\x03   \x033[+' + str(exp) + ' xp - Lucky Charm] [TOTAL GOLDEN DUCKS: ' + str(gducks) + ']\x03')
                    # reset duck info
                    rdata[server, chan]['duck'][int(duckid)] = '0'
                    rdata[server, chan]['timer'] = pc.cputime()
                    # silently rearms all confiscated guns
                    if game_rules(server, dchannel, 'gunconf') == 'on':
                        ctrl_data(server, dchannel, '0', 'confiscated', 'clear')
                    # searching the bushes
                    if int(game_rules(server, dchannel, 'thebushes')) > 0:
                        thebushes = game_rules(server, dchannel, 'thebushes')
                        searchbush = pc.rand(1, 100)
                        if int(searchbush) < int(thebushes):
                            bushes = bush_search(server, dchannel, user.decode())
                            pc.privmsg_(server, channel, user.decode() + ' > ' + str(bushes))
                    # check for level up
                    if int(xp) >= int(levelup):
                        level_up(server, dchannel, user.decode())
                    return

    # missed - a duck does not exist
    if ducksdata(server, dchannel) == 0:

        accidents = int(accidents) + 1
        duckinfo(server, dchannel, duser, 'accidents', str(accidents))

        # ricochet
        ricochet = pc.rand(1, 100)
        if int(game_rules(server, dchannel, 'gunricochet')) > 0 and ricochet < int(game_rules(server, dchannel, 'gunricochet')):
            damage = ''
            dmg = pc.rand(1, 3)
            if dmg == 1:
                damage = 'strikes a distant window!'
            if dmg == 2:
                damage = 'strikes another hunter!'
            if dmg == 3:
                damage = 'starts a wildfire!'

            # determine xp subtract
            rxp = dmg
            if int(xp) >= 10000:
                rxp = dmg * 2
            if int(xp) >= 5000 and int(xp) < 10000:
                rxp = dmg + 3
            if int(xp) < 5000 and int(xp) >= 1500:
                rxp = dmg + 1

            # gunconf is off
            if gunconf == 'off':
                # deduct xp
                rxp = rxp + 4
                if int(xp) <= rxp:
                    xp = 0
                if int(xp) > rxp:
                    xp = int(xp) - rxp
                duckinfo(server, dchannel, duser, 'xp', str(xp))
                pc.privmsg_(server, channel, user.decode() + ' > \x0314*BANG*    *PEEEWWWWW*\x03    The bullet ricochets and ' + str(damage) + ' \x034[-' + str(dmg) + ' xp] [Ricochet]\x03')
                return

            # has accident insurance
            if pc.istok_n(rdata[server, chan]['accident_insurance'], duser, ',', '^', 0) is True:
                # deduct xp
                rxp = rxp + 4
                if int(xp) <= rxp:
                    xp = 0
                if int(xp) > rxp:
                    xp = int(xp) - rxp
                duckinfo(server, dchannel, duser, 'xp', str(xp))
                pc.privmsg_(server, channel, user.decode() + ' > \x0314*BANG*    *PEEEWWWWW*\x03    The bullet ricochets and ' + str(damage) + ' \x034[-' + str(rxp) + ' xp]\x03 \x033[GUN NOT CONFISCATED: Accident Insurance]\x03')
                return

            # does not have accident insurance
            if pc.istok_n(rdata[server, chan]['accident_insurance'], duser, ',', '^', 0) is False:
                # deduct xp
                if int(xp) <= rxp:
                    xp = 0
                if int(xp) > rxp:
                    xp = int(xp) - rxp
                duckinfo(server, dchannel, duser, 'xp', str(xp))
                # gun confiscated
                ctrl_data(server, dchannel, duser, 'confiscated', 'add')
                pc.privmsg_(server, channel, user.decode() + ' > \x0314*BANG*    *PEEEWWWWW*\x03    The bullet ricochets and ' + damage + ' \x034[-' + str(dmg) + ' xp] [GUN CONFISCATED: Ricochet]\x03')
                return

        # no ricochet
        else:

            damage = ''
            dmg = pc.rand(1, 3)
            if dmg == 1:
                damage = 'Shot a distant window!'
            if dmg == 2:
                damage = 'Shot another hunter!'
            if dmg == 3:
                damage = 'Wildfire!'

            # determine xp subtract
            rxp = dmg
            if int(xp) >= 10000:
                rxp = dmg * 2
            if int(xp) >= 5000 and int(xp) < 10000:
                rxp = dmg + 3
            if int(xp) < 5000 and int(xp) >= 1500:
                rxp = dmg + 1
            if int(xp) < 1500:
                rxp = dmg
            # gunconf is off
            if game_rules(server, dchannel, 'gunconf') == 'off':
                # deduct xp
                rxp = rxp + 4
                if int(xp) <= rxp:
                    xp = 0
                if int(xp) > rxp:
                    xp = int(xp) - rxp
                duckinfo(server, dchannel, duser, 'xp', str(xp))
                pc.privmsg_(server, channel, user.decode() + ' > \x0314*BANG*\x03    What did you shoot at? There is no duck in the area...   \x034[-' + str(rxp) + ' xp] [' + str(damage) + ']\x03')
                return

            # has accident insurance
            if pc.istok_n(rdata[server, chan]['accident_insurance'], duser, ',', '^', 0) is True:
                # deduct xp
                rxp = rxp + 4
                if int(xp) <= rxp:
                    xp = 0
                if int(xp) > rxp:
                    xp = int(xp) - rxp
                duckinfo(server, dchannel, duser, 'xp', str(xp))
                pc.privmsg_(server, channel, user.decode() + ' > \x0314*BANG*\x03    What did you shoot at? There is no duck in the area...    \x034[-' + str(rxp) + ' xp]\x03 \x033[GUN NOT CONFISCATED: Accident Insurance]\x03')
                return

            # does not have accident insurance
            if pc.istok_n(rdata[server, chan]['accident_insurance'], duser, ',', '^', 0) is False:
                # deduct xp
                if int(xp) <= rxp:
                    xp = 0
                if int(xp) > rxp:
                    xp = int(xp) - rxp
                duckinfo(server, dchannel, duser, 'xp', str(xp))
                # gun confiscation
                ctrl_data(server, dchannel, duser, 'confiscated', 'add')
                pc.privmsg_(server, channel, user.decode() + ' > \x0314*BANG*\x03    What did you shoot at? There is no duck in the area...   \x034[-' + str(rxp) + ' xp] [GUN CONFISCATED: ' + str(damage) + ']\x03')
                return
        # pc.privmsg_(server, channel, user.decode() + ' > Missed!')
        return

# !reload --------------------------------------------------------------------------------------------------------------
# async def reload(server, channel, user):
def reload(server, channel, user):
    global rdata
    dchannel = channel.decode()
    dchannel = dchannel.lower()
    chan = dchannel.replace('#', '')
    duser = user.decode()
    duser = duser.lower()

    # check all timed items/effects
    time_data(server, dchannel, duser, 'all-time')

    rounds = int(duckinfo(server, dchannel, duser, 'ammo-r'))
    mrounds = int(duckinfo(server, dchannel, duser, 'ammo-mr'))
    mags = int(duckinfo(server, dchannel, duser, 'ammo-m'))
    mmags = int(duckinfo(server, dchannel, duser, 'ammo-mm'))

    # check if player's gun is confiscated
    if game_rules(server, dchannel, 'gunconf') == 'on' and pc.istok(rdata[server, chan]['confiscated'], duser,
                                                                    ',') is True:
        pc.privmsg_(server, channel, user.decode() + ' > \x034You are not armed.\x03')
        return

    # Unjam gun
    if pc.istok(rdata[server, chan]['jammed'], duser, ',') is True:
        ctrl_data(server, dchannel, duser, 'jammed', 'rem')
        ctrl_data(server, dchannel, duser, 'duck_jam', 'add')
        pc.privmsg_(server, channel, user.decode() + ' > \x0314*Crr..CLICK*\x03     You unjam your gun.')
        return

    # new users with no stats
    if pc.cnfexists('duckhunt.cnf', server + '_' + chan + '_ducks', duser) is False:
        if game_rules(server, dchannel, 'infammo') == 'on':
            pc.privmsg_(server, channel, user.decode() + " > Your gun doesn't need to be reloaded. | Rounds: 7/7 | Magazines: \x02\x033Inf\x02\x03")
            return
        if game_rules(server, dchannel, 'infammo') == 'off':
            pc.privmsg_(server, channel, user.decode() + " > Your gun doesn't need to be reloaded. | Rounds: 7/7 | Magazines: 3/3")
            return
        return

    # reloading gun
    if int(rounds) == 0:

        # out of magazines
        if int(mags) == 0 and game_rules(server, dchannel, 'infammo') == 'off':
            pc.privmsg_(server, channel, user.decode() + " > \x034You are out of magazines.\x03 | Rounds:\x034 0\x03/" + str(mrounds) + " | Magazines:\x034 0\x03/" + str(mmags))
            return

        # successful reload
        if game_rules(server, dchannel, 'infammo') == 'off':
            mags = int(mags) - 1
        rounds = mrounds
        duckinfo(server, dchannel, duser, 'ammo-r', str(rounds))
        duckinfo(server, dchannel, duser, 'ammo-m', str(mags))
        if game_rules(server, dchannel, 'infammo') == 'on':
            pc.privmsg_(server, channel, user.decode() + " > \x0314*CLACK CLACK*\x03     You reload. | Rounds: " + str(rounds) + '/' + str(mrounds) + ' | Magazines: \x02\x033Inf\x02\x03')
        if game_rules(server, dchannel, 'infammo') == 'off':
            pc.privmsg_(server, channel, user.decode() + " > \x0314*CLACK CLACK*\x03     You reload. | Rounds: " + str(rounds) + '/' + str(mrounds) + ' | Magazines: ' + str(mags) + '/' + str(mmags))
        return

    # gun doesn't need to be reloaded
    if int(rounds) != 0:
        if game_rules(server, dchannel, 'infammo') == 'on':
            pc.privmsg_(server, channel, user.decode() + " > Your gun doesn't need to be reloaded. | Rounds: " + str(rounds) + '/' + str(mrounds) + ' | Magazines: \x02\x033Inf\x02\x03')
        if game_rules(server, dchannel, 'infammo') == 'off':
            pc.privmsg_(server, channel, user.decode() + " > Your gun doesn't need to be reloaded. | Rounds: " + str(rounds) + '/' + str(mrounds) + ' | Magazines: ' + str(mags) + '/' + str(mmags))
        return

# ======================================================================================================================
# Feeding ducks (!bef)

# ----------------------------------------------------------------------------------------------------------------------
# !bef function
# async def bef(server, channel, user):
def bef(server, channel, user):
    global rdata
    dchannel = channel.decode()
    dchannel = dchannel.lower()
    chan = dchannel.replace('#', '')
    duser = user.decode()
    duser = duser.lower()

    # new users with no stats
    # b'playername' = Rounds?Mags?MaxRounds?MaxMags,Ducks,GoldenDucks,xp,level,levelup,
    #                 notusedanymore,notusedanymore,Accuracy?Reliability?MaxReliability,BestTime,
    #                 Accidents,Bread?MaxBread,Loaf,MaxLoaf,DuckFriends
    if not pc.cnfexists('duckhunt.cnf', server + '_' + chan + '_ducks', duser):
        dinfo = '7?3?7?3,0,0,0,1,200,0,0,75?80?80,0,0,12?12?3?3,0'
        pc.cnfwrite('duckhunt.cnf', server + '_' + chan + '_ducks', duser, str(dinfo))
        # pc.cnfwrite('duckhunt.cnf', dsect, 'cache', '1')  # ???

    # player is bombed
    if pc.istok_n(rdata[server, chan]['bombed'], duser, ',', '^', 0) is True:
        pc.privmsg_(server, channel, user.decode() + ' > \x034Your clothes are crusty and filthy from being duck bombed. You cannot befriend ducks like this, you need new clothes.\x03')
        return

    # player is soggy
    if pc.istok_n(rdata[server, chan]['soggy'], duser, ',', '^', 0) is True:
        # determine time remaining
        ptime = pc.gettok_n(rdata[server, chan]['soggy'], duser, ',', '^', 0, 1)
        ptime = pc.cputime() - float(ptime)
        timeval = pc.timeconvert(ptime)
        pc.privmsg_(server, channel, user.decode() + " > \x034Your clothes are all soggy. You cannot befriend ducks until you're dry. \x033[Time Remaining: " + str(timeval) + ']\x03')
        return

    # check all timed items/effects
    time_data(server, dchannel, duser, 'all-time')

    # feeding/friending data
    xp = duckinfo(server, dchannel, duser, 'xp')
    bread = duckinfo(server, dchannel, duser, 'bread-b')
    mbread = duckinfo(server, dchannel, duser, 'bread-mb')
    loaf = duckinfo(server, dchannel, duser, 'bread-l')
    mloaf = duckinfo(server, dchannel, duser, 'bread-ml')
    friend = duckinfo(server, dchannel, duser, 'friend')
    level = duckinfo(server, dchannel, duser, 'level')
    levelup = duckinfo(server, dchannel, duser, 'levelup')
    best = duckinfo(server, dchannel, duser, 'best')

    # bread box lock
    if pc.istok_n(rdata[server, chan]['bread_lock'], duser, ',', '^', 0) is True:
        useleft = pc.gettok_n(rdata[server, chan]['bread_lock'], duser, ',', '^', 0, 1)
        if int(useleft) == 1:
            useleft = 0
            user_data(server, dchannel, duser, 'bread_lock', 'rem')
        if int(useleft) > 1:
            useleft = int(useleft) - 1
            user_data(server, dchannel, duser, 'bread_lock', 'edit', str(useleft))
        pc.privmsg_(server, channel, user.decode() + ' > \x0314*Bzzt..Click*\x03     \x034BREAD BOX LOCKED   [' + str(useleft) + ']\x03')
        return

    # out of bread
    if int(bread) == 0 and pc.istok_n(rdata[server, chan]['popcorn'], duser, ',', '^', 0) is False:
        if game_rules(server, dchannel, 'infammo') == 'on':
            pc.privmsg_(server, channel, user.decode() + " > \x0314*BZZT*\x03     \x034EMPTY BOX\x03 | Bread pieces:\x034 0\x03/" + str(mbread) + " | Loaf: \x02\x033Inf\x02\x03   [\x02Reloaf\x02 your bread box.]")
        if game_rules(server, dchannel, 'infammo') == 'off':
            pc.privmsg_(server, channel, user.decode() + " > \x0314*BZZT*\x03     \x034EMPTY BOX\x03 | Bread pieces:\x034 0\x03/" + str(mbread) + " | Loaf: " + str(loaf) + "/" + str(mloaf) + '   [\x02Reloaf\x02 your bread box.]')
        return

    # tosses a peice of bread (doesn't have popcorn)
    if pc.istok_n(rdata[server, chan]['popcorn'], duser, ',', '^', 0) is False:
        bread = int(bread) - 1
        duckinfo(server, dchannel, duser, 'bread-b', str(bread))

    # tosses a peice of popcorn (doesn't use bread)
    if pc.istok_n(rdata[server, chan]['popcorn'], duser, ',', '^', 0) is True:
        popc = pc.gettok_n(rdata[server, chan]['popcorn'], duser, ',', '^', 0, 1)
        if int(popc) == 1:
            user_data(server, dchannel, duser, 'popcorn', 'rem')
            popc = 0
        if int(popc) > 1:
            popc = int(popc) - 1
            user_data(server, dchannel, duser, 'popcorn', 'edit', str(popc))

    # no duck in the area
    if ducksdata(server, dchannel) == 0:

        # deduct xp
        rxp = pc.rand(1, 2)
        if int(xp) >= 10000 or int(level) >= 10:
            rxp = rxp + pc.rand(5, 6)
        elif int(xp) >= 5000 and int(xp) < 10000 and int(level) < 10:
            rxp = rxp + pc.rand(4, 5)
        elif int(xp) < 5000 and int(xp) >= 1500:
            rxp = rxp + pc.rand(2, 3)
        # deduction
        if int(xp) <= rxp:
            xp = 0
        if int(xp) > rxp:
            xp = int(xp) - rxp
        duckinfo(server, dchannel, duser, 'xp', str(xp))

        # has popcorn
        if pc.istok_n(rdata[server, chan]['popcorn'], duser, ',', '^', 0) is True:
            pc.privmsg_(server, channel, user.decode() + ' > Tosses a piece of popcorn at nothing? There are no ducks in the area. \x034[-1 Popcorn] [-' + str(rxp) + ' xp]\x03')
            return

        # bread (does not have popcorn)
        if pc.istok_n(rdata[server, chan]['popcorn'], duser, ',', '^', 0) is False:
            pc.privmsg_(server, channel, user.decode() + ' > Tosses a piece of bread at nothing? There are no ducks in the area. \x034[-1 Bread] [-' + str(rxp) + ' xp]\x03')
            return

    # duck exists in the area
    if ducksdata(server, dchannel) > 0:

        # player is bedazzled
        if pc.istok_n(rdata[server, chan]['bedazzled'], duser, ',', '^', 0) is True:
            # deduct xp
            rxp = random.randint(1, 2)
            if int(xp) >= 10000 or int(level) >= 10:
                rxp = rxp * 6
            elif int(xp) >= 5000 and int(xp) < 10000 and int(level) < 10:
                rxp = rxp * 4
            elif int(xp) < 5000 and int(xp) >= 1500:
                rxp = rxp * 2
            
            if int(xp) <= rxp:
                xp = 0
            if int(xp) > rxp:
                xp = int(xp) - rxp
            duckinfo(server, dchannel, duser, 'xp', str(xp))
            pc.privmsg_(server, channel, username + " > \x034UNLUCKY\x03     You tossed in the wrong direction because you're bedazzled!     \x034[-" + str(rxp) + ' xp] [Bedazzled]\x03')
            return

        # determine duck
        duckdata = '0'
        duckid = ''
        duck_time = '0'
        for x in range(len(rdata[server, chan]['duck'])):
            if rdata[server, chan]['duck'][x] == '0':
                continue
            if rdata[server, chan]['duck'][x] != '0':
                duckdata = rdata[server, chan]['duck'][x]
                duckid = str(x)
                duck_time = pc.gettok(duckdata, 0, ',')
                break

        # determine friend or not
        friendornot = pc.rand(1, 100)
        # normal duck

        # normal-gold duck
        if pc.gettok(duckdata, 1, ',') == 'gold':
            friendornot = pc.rand(1, 200)
        # golden duck
        if pc.gettok(duckdata, 1, ',') == 'golden':
            friendornot = pc.rand(1, 140)

        # has popcorn
        if pc.istok_n(rdata[server, chan]['popcorn'], duser, ',', '^', 0) is True:
            friendornot = int(friendornot) - 15

        # unlucky
        # mprint(f'Unlucky, missed bread ---------------------------------------')
        if int(friendornot) > int(rdata[server, chan]['friendrate']):
            rxp = pc.rand(1, 2)
            if int(xp) >= 10000 or int(level) >= 10:
                rxp = rxp + pc.rand(5, 6)
            elif int(xp) >= 5000 and int(xp) < 10000 and int(level) < 10:
                rxp = rxp + pc.rand(4, 5)
            elif int(xp) < 5000 and int(xp) >= 1500:
                rxp = rxp + pc.rand(2, 3)
            if pc.gettok(duckdata, 1, ',') == 'golden':
                rxp = int(rxp) + pc.rand(1, 3)
            # deduct xp
            if int(xp) <= rxp:
                xp = 0
            if int(xp) > rxp:
                xp = int(xp) - rxp
            duckinfo(server, dchannel, duser, 'xp', str(xp))

            # normal duck
            # mprint(f'normal duck unlucky missed bread ----------------------------')
            if pc.gettok(duckdata, 1, ',') == 'normal':
                pc.privmsg_(server, channel, user.decode() + " > \x034UNLUCKY\x03     The duck didn't seem to notice. Try again.     \x02\\_O< QUACK\x02    \x034[-" + str(rxp) + ' xp]\x03')
                return

            # normal-gold
            # mprint(f'normal-gold duck unlucky missed bread ----------------------------')
            if pc.gettok(duckdata, 1, ',') == 'gold':

                # first miss, not golden yet
                if pc.numtok(duckdata, ',') == 4:
                    duckdata = duckdata + ',1'
                    rdata[server, chan]['duck'][int(duckid)] = duckdata
                    pc.privmsg_(server, channel, user.decode() + " > \x034UNLUCKY\x03     The duck didn't seem to notice. Try again.     \x02\\_O< QUACK\x02    \x034[-" + str(rxp) + ' xp]\x03')
                    return

                # 2nd miss determine if duck will turn golden
                if pc.numtok(duckdata, ',') == 5 and pc.gettok(duckdata, 1, ',') == 'gold':
                    if int(pc.gettok(duckdata, 4, ',')) >= 1:
                        duckstat = pc.rand(4, 7)
                        duckdata = pc.gettok(duckdata, 0, ',') + ',golden,' + str(duckstat) + ',' + pc.gettok(duckdata, 3, ',')
                        rdata[server, chan]['duck'][int(duckid)] = duckdata
                        pc.privmsg_(server, channel, user.decode() + " > \x034UNLUCKY\x03     The duck didn't seem to notice. Try again.\x037    \x02\\_O<    * GOLDEN DUCK DETECTED *\x02\x03")
                        return
            # golden
            # mprint(f'golden duck unlucky missed bread ----------------------------')
            if pc.gettok(duckdata, 1, ',') == 'golden':
                pc.privmsg_(server, channel, user.decode() + " > \x034UNLUCKY\x03     The GOLDEN DUCK didn't seem to notice. Try again.     \x02\\_O< QUACK\x02    \x034[-" + str(rxp) + ' xp]\x03')
                return

        # friend
        if int(friendornot) <= int(rdata[server, chan]['friendrate']):

            # normal duck
            # mprint(f'Normal Duck Friend -----------------------------')
            if pc.gettok(duckdata, 1, ',') == 'normal':

                # reaction time
                reacttime = round(pc.cputime() - float(duck_time), 2)
                if best == '0':
                    duckinfo(server, dchannel, duser, 'best', str(reacttime))
                if float(best) > reacttime:
                    duckinfo(server, dchannel, duser, 'best', str(reacttime))

                # increase friends
                friend = int(friend) + 1
                duckinfo(server, dchannel, duser, 'friend', str(friend))

                # increase xp - does not have lucky charm
                if pc.istok_n(rdata[server, chan]['lucky_charm'], duser, ',', '^', 0) is False:
                    exp = rdata[server, chan]['duckexp']
                    xp = int(xp) + exp
                    duckinfo(server, dchannel, duser, 'xp', str(xp))
                    wooid = 'bread'
                    if pc.istok_n(rdata[server, chan]['popcorn'], duser, ',', '^', 0) is True:
                        wooid = 'popcorn'
                    pc.privmsg_(server, channel, user.decode() + ' > \x0314FRIEND\x03     The duck ate the piece of ' + str(wooid) + '!     \x02\\_O< QUAACK!\x02\x033   [BEFRIENDED DUCKS: ' + str(friend) + '] [+' + str(exp) + ' xp]\x03')

                # increase xp - has lucky charm
                if pc.istok_n(rdata[server, chan]['lucky_charm'], duser, ',', '^', 0) is True:
                    lcxp = pc.gettok_n(rdata[server, chan]['lucky_charm'], duser, ',', '^', 0, 2)
                    exp = rdata[server, chan]['duckexp'] + int(lcxp)
                    xp = int(xp) + exp
                    duckinfo(server, dchannel, duser, 'xp', str(xp))
                    wooid = 'bread'
                    if pc.istok_n(rdata[server, chan]['popcorn'], duser, ',', '^', 0) is True:
                        wooid = 'popcorn'
                    pc.privmsg_(server, channel, user.decode() + ' > \x0314FRIEND\x03     The duck ate the piece of ' + str(wooid) + '!     \x02\\_O< QUAACK!\x02\x033   [BEFRIENDED DUCKS: ' + str(friend) + '] [+' + str(exp) + ' xp - Lucky Charm]\x03')

                # reset duck info
                rdata[server, chan]['duck'][int(duckid)] = '0'
                rdata[server, chan]['timer'] = pc.cputime()

                # silent rearm (for !bang)
                if game_rules(server, dchannel, 'gunconf') == 'on' and game_rules(server, dchannel, 'bang') == 'on':
                    ctrl_data(server, dchannel, '0', 'confiscated', 'clear')

                # searching the bushes
                if int(game_rules(server, dchannel, 'thebushes')) > 0:
                    thebushes = game_rules(server, dchannel, 'thebushes')
                    searchbush = pc.rand(1, 100)
                    if int(searchbush) < int(thebushes):
                        bushes = bush_search(server, dchannel, user.decode())
                        pc.privmsg_(server, channel, user.decode() + ' > ' + str(bushes))
                # check for level up
                if int(xp) >= int(levelup):
                    level_up(server, dchannel, user.decode())
                return

            # normal-gold duck
            # mprint(f'normal-gold duck ate the bread---------------------------')
            if pc.gettok(duckdata, 1, ',') == 'gold':
                ddmg = 1
                woid = 'bread'
                # has popcorn
                if pc.istok_n(rdata[server, chan]['expl_ammo'], duser, ',', '^', 0) is True:
                    ddmg = 2
                    woid = 'popcorn'

                duckhp = pc.gettok(duckdata, 2, ',')
                duckhp = int(duckhp) - int(ddmg)
                duckstat = pc.gettok(duckdata, 0, ',') + ',golden,' + str(duckhp) + ',' + pc.gettok(duckdata, 3, ',')
                rdata[server, chan]['duck'][int(duckid)] = duckstat
                pc.privmsg_(server, channel, user.decode() + ' > \x0314QUACK!!\x03     The duck ate the piece of ' + str(woid) + ' and kept flying! Try again.    \x034\x02\\_O< [ <3 +' + str(ddmg) + ' ]\x02\x03     \x02\x037* GOLDEN DUCK DETECTED *\x02\x03')
                return

            # golden
            # mprint(f'golden duck ate the bread--------------------------------')
            if pc.gettok(duckdata, 1, ',') == 'golden':
                duckhp = pc.gettok(duckdata, 2, ',')

                # the duck kept flying - has popcorn
                if pc.istok_n(rdata[server, chan]['popcorn'], duser, ',', '^', 0) is True and int(duckhp) > 2:
                    ddmg = 2
                    duckhp = int(duckhp) - int(ddmg)
                    duckstat = pc.gettok(duckdata, 0, ',') + ',' + pc.gettok(duckdata, 1, ',') + ',' + str(duckhp) + ',' + pc.gettok(duckdata, 3, ',')
                    rdata[server, chan]['duck'][int(duckid)] = duckstat
                    pc.privmsg_(server, channel, user.decode() + ' > \x0314QUACK!!\x03     The GOLDEN DUCK ate the piece of popcorn and kept flying! Try again.     \x034\x02\\_O< [ <3 +' + str(ddmg) + ' ]\x02\x03')
                    return

                # the duck kept flying - bread
                if pc.istok_n(rdata[server, chan]['popcorn'], duser, ',', '^', 0) is False and int(duckhp) > 1:
                    ddmg = 1
                    duckhp = int(duckhp) - int(ddmg)
                    duckstat = pc.gettok(duckdata, 0, ',') + ',' + pc.gettok(duckdata, 1, ',') + ',' + str(duckhp) + ',' + pc.gettok(duckdata, 3, ',')
                    rdata[server, chan]['duck'][int(duckid)] = duckstat
                    pc.privmsg_(server, channel, user.decode() + ' > \x0314QUACK!!\x03     The GOLDEN DUCK ate the piece of bread and kept flying! Try again.     \x034\x02\\_O< [ <3 +' + str(ddmg) + ' ]\x02\x03')
                    return

                # befriended the golden duck
                # popcorn
                popc = False
                if pc.istok_n(rdata[server, chan]['popcorn'], duser, ',', '^', 0) is True and int(duckhp) <= 2:
                    popc = True

                if int(duckhp) == 1 or popc is True:
                    woid = 'bread'
                    if popc is True:
                        woid = 'popcorn'
                        # popc = False
                    # reaction time determination
                    reacttime = round(pc.cputime() - float(duck_time), 2)
                    if best == '0':
                        duckinfo(server, dchannel, duser, 'best', str(reacttime))
                    if float(best) > reacttime:
                        duckinfo(server, dchannel, duser, 'best', str(reacttime))
                    # increase friends
                    friend = int(friend) + 1
                    duckinfo(server, dchannel, duser, 'friend', str(friend))

                    # increase xp - lucky charm
                    if pc.istok_n(rdata[server, chan]['lucky_charm'], duser, ',', '^', 0) is True:
                        exp = int(rdata[server, chan]['duckexp']) * 3
                        lcxp = pc.gettok_n(rdata[server, chan]['lucky_charm'], duser, ',', '^', 0, 1)
                        exp = int(exp) + int(lcxp)
                        xp = int(xp) + int(exp)
                        duckinfo(server, dchannel, duser, 'xp', str(xp))
                        pc.privmsg_(server, channel, user.decode() + ' > \x0314FRIEND\x03     The GOLDEN DUCK ate the piece of ' + str(woid) + '!     \x02\\_0< QUAACK!\x02\x033   [BEFRIENDED DUCKS: ' + str(friend) + '] [+' + str(exp) + ' xp - Lucky Charm]\x03')

                    # increase xp - does not have lucky charm
                    if pc.istok_n(rdata[server, chan]['lucky_charm'], duser, ',', '^', 0) is False:
                        exp = int(rdata[server, chan]['duckexp']) * 3
                        xp = int(xp) + int(exp)
                        duckinfo(server, dchannel, duser, 'xp', str(xp))
                        pc.privmsg_(server, channel, user.decode() + ' > \x0314FRIEND\x03     The GOLDEN DUCK ate the piece of ' + str(woid) + '!     \x02\\_0< QUAACK!\x02\x033   [BEFRIENDED DUCKS: ' + str(friend) + '] [+' + str(exp) + ' xp]\x03')

                    # reset duck info
                    rdata[server, chan]['duck'][int(duckid)] = '0'
                    rdata[server, chan]['timer'] = pc.cputime()

                    # silent rearm (for !bang)
                    if game_rules(server, dchannel, 'gunconf') == 'on' and game_rules(server, dchannel, 'bang') == 'on':
                        ctrl_data(server, dchannel, '0', 'confiscated', 'clear')

                    # searching the bushes
                    if int(game_rules(server, dchannel, 'thebushes')) > 0:
                        thebushes = game_rules(server, dchannel, 'thebushes')
                        searchbush = pc.rand(1, 100)
                        if int(searchbush) < int(thebushes):
                            bushes = bush_search(server, dchannel, user.decode())
                            pc.privmsg_(server, channel, user.decode() + ' > ' + str(bushes))
                    # check for level up
                    if int(xp) >= int(levelup):
                        level_up(server, dchannel, user.decode())
                    return

# !bread or !reloaf ----------------------------------------------------------------------------------------------------
# reloaf('serverid', b'#Channel', b'Username')
# async def reloaf(server, channel, user):
def reloaf(server, channel, user):
    global rdata
    dchannel = channel.decode()
    dchannel = dchannel.lower()
    chan = dchannel.replace('#', '')

    duser = user.decode()
    duser = duser.lower()

    if not pc.cnfexists('duckhunt.cnf', server + '_' + chan + '_ducks', duser):
        if game_rules(server, dchannel, 'infammo') == 'on':
            pc.privmsg_(server, channel, user.decode() + " > Your bread doesn't need to be reloaded. | Bread Pieces: 12/12 | Loaf: \x02\x033Inf\x02\x03")
            return
        if game_rules(server, dchannel, 'infammo') == 'off':
            pc.privmsg_(server, channel, user.decode() + " > Your bread doesn't need to be reloaded. | Bread Pieces: 12/12 | Loaf: 3/3")
            return

    # reloading bread box
    bread = duckinfo(server, dchannel, duser, 'bread-b')
    mbread = duckinfo(server, dchannel, duser, 'bread-mb')
    loaf = duckinfo(server, dchannel, duser, 'bread-l')
    mloaf = duckinfo(server, dchannel, duser, 'bread-ml')

    if int(bread) == 0:

        # out of loaf
        if int(loaf) == 0 and game_rules(server, dchannel, 'infammo') == 'off':
            pc.privmsg_(server, channel, user.decode() + ' > \x034You are out of bread loaves.\x03 | Bread Pieces:\x034 0\x03/' + str(mbread) + ' | Loaf:\x034 0\x03/' + str(mloaf))
            return

        # successful reload
        if game_rules(server, dchannel, 'infammo') == 'off':
            loaf = int(loaf) - 1
            bread = int(mbread)
            duckinfo(server, dchannel, duser, 'bread-l', str(loaf))
            duckinfo(server, dchannel, duser, 'bread-b', str(bread))

        if game_rules(server, dchannel, 'infammo') == 'on':
            pc.privmsg_(server, channel, user.decode() + ' > \x0314*Shmp..CLICK*\x03     You reload your bread box. | Bread Pieces: ' + str(bread) + '/' + str(mbread) + ' | Loaf: \x02\x033Inf\x02\x03')
            return
        if game_rules(server, dchannel, 'infammo') == 'off':
            pc.privmsg_(server, channel, user.decode() + ' > \x0314*Shmp..CLICK*\x03     You reload your bread box. | Bread Pieces: ' + str(bread) + '/' + str(mbread) + ' | Loaf: ' + str(loaf) + '/' + str(mloaf))
            return

    # doesn't need to be reloaded
    if int(bread) > 0:
        if game_rules(server, dchannel, 'infammo') == 'on':
            pc.privmsg_(server, channel, user.decode() + " > your bread box doesn't need to be reloaded. | Bread Pieces: " + str(bread) + '/' + str(mbread) + ' | Loaf: \x02\x033Inf\x02\x03')
            return
        if game_rules(server, dchannel, 'infammo') == 'off':
            pc.privmsg_(server, channel, user.decode() + " > your bread box doesn't need to be reloaded. | Bread Pieces: " + str(bread) + '/' + str(mbread) + ' | Loaf: ' + str(loaf) + '/' + str(mloaf))
            return
    return

# ======================================================================================================================
# Level Up function
def level_up(server, channel, user):
    global rdata
    duser = user.lower()
    pc.privmsg_(server, channel.encode(), 'Level up!')
    return

# Searching the bushes function
def bush_search(server, channel, user):
    global rdata
    duser = user.lower()
    return 'Searching the bushes'

# User Data handles type 5 (non-timed) item user data: trigger_lock, bread_lock, expl_ammo, popcorn
def user_data(server, channel, user, dataname, args, data=''):
    global rdata
    # dchannel = channel.decode()
    dchannel = channel.lower()
    chan = dchannel.replace('#', '')
    # duser = user.decode()
    duser = user.lower()

    # dataname can be one of these: trigger_lock, bread_lock, expl_ammo, popcorn ---------------------------------------
    # see functon eff_type() for return values
    if eff_type(dataname) == 5:
        # adds a new entry to the data list for dataname ---------------------------------------------------------------
        # user_data('serverid', b'#channel', b'username', 'data_name', 'add', 'newdata')
        if args == 'add' and data != '':
            newdat = duser + '^' + str(data)
            if rdata[server, chan][dataname] != '0':
                rdata[server, chan][dataname] = rdata[server, chan][dataname] + ',' + newdat
            if rdata[server, chan][dataname] == '0':
                rdata[server, chan][dataname] = newdat
            pc.cnfwrite('duckhunt.cnf', server + '_' + chan, dataname, rdata[server, chan][dataname])
            return 1
        # finds and overwrites existing entry --------------------------------------------------------------------------
        # user_data('serverid', b'#channel', b'username', 'data_name', 'edit', 'newdata')
        if args == 'edit':
            token = rdata[server, chan][dataname].split(',')
            newstring = '0'
            for x in range(len(token)):
                if pc.gettok(token[x], 0, '^') == duser:
                    token[x] = duser + '^' + str(data)
                if newstring != '0':
                    newstring = newstring + ',' + token[x]
                    continue
                if newstring == '0':
                    newstring = token[x]
                    continue
            rdata[server, chan][dataname] = newstring
            pc.cnfwrite('duckhunt.cnf', server + '_' + chan, dataname, rdata[server, chan][dataname])
            return 1
        # finds and removes username's entry from data_name ------------------------------------------------------------
        # user_data('serverid', b'#channel', b'username', 'data_name', 'rem')
        if args == 'rem':
            token = rdata[server, chan][dataname].split(',')
            newstring = '0'
            for x in range(len(token)):
                if pc.gettok(token[x], 0, '^') == duser:
                    continue
                if newstring != '0':
                    newstring = newstring + ',' + token[x]
                    continue
                if newstring == '0':
                    newstring = token[x]
                    continue
            rdata[server, chan][dataname] = newstring
            pc.cnfwrite('duckhunt.cnf', server + '_' + chan, dataname, rdata[server, chan][dataname])
            return 1