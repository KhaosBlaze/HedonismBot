import sys
import irc.bot
import requests
import re


class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/helix/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        print r
	self.channel_id = r['data'][0]['id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print 'Connecting to ' + server + ' on port ' + str(port) + '...'
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)
        

    def on_welcome(self, c, e):
        print 'Joining ' + self.channel

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
	#c.send('CAP REQ :twitch.tv/membership twitch.tv/tags twitch.tv/commands\r\n'.encode('utf-8'))
        c.join(self.channel)
	
	c.privmsg(self.channel, '.w KhaosBlaze Test')	

    def on_pubmsg(self, c, e):
	msg = e.arguments[0].encode('utf-8')
        # If a chat message starts with an exclamation point, try to run it as a command
        if 'cheer' in msg and 'assassinate' in msg:
	    self.assassinate(e)
	elif e.arguments[0][:1] == '!':
            cmd = e.arguments[0].split(' ')[0][1:]
            print 'Received command: ' + cmd
            self.do_command(e, cmd)
	else:
	    print e.tags[3]['value'] + ': ' + e.arguments[0]
        return

    def do_command(self, e, cmd):
        c = self.connection
	sender = e.tags[3]['value']

        # Poll the API to get current game.
        if cmd == "e":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' is currently playing ' + r['game'])

        # Poll the API the get the current status of the stream
        elif cmd == "t":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' channel title is currently ' + r['status'])

        # Provide basic information to viewers for specific commands

	elif cmd == "senate":
	    message = "/w " + sender +" Currently this bot only does assasinations. You can do this by ensuring your targets name is first word in the message as well as adding your cheer amount and the world 'assassinate'. Do note that the timeout exchange is 1 second per 10 bits "
	    print message
	    c.privmsg(self.channel, message)

	else:
	    pass

	# The command was not recognized

    def assassinate(self, e):
	c = self.connection
	array = e.arguments[0].split(' ')
	sender = e.tags[3]['value']
	bits = 0
	print 'Get this bread'

	array.pop(array.index('assassinate'))
	for i in array:
	    if 'cheer' in i:
		if re.search('cheer1[0]{0,4}', i):
			bits += int(i.strip('cheer'))
		elif i == 'cheer5000':
			bits += 5000
	
	array = [el for el in array if 'cheer' not in el]
	message = ''
	target = array[0]
	array.pop(0)
	message= ' '.join(array).encode('utf-8').strip()
	time = str(bits/10)
	
	if int(time) > 0:
		popoff = 'The death of ' + target + ' has been contracted. A new clone will be ready in  ' + time + ' seconds.'
		c.privmsg(self.channel, popoff)
		#timeout = '/timeout ' + target + ' ' + time
		timeout = '/timeout ' + target + ' ' + time
		print(timeout)
		print(sender)
		c.privmsg(self.channel, timeout)
	elif bits < 10:
		c.privmsg(self.channel, "You need to donate more than 10 bits")
