## intiialize discord
import discord


# create discord aemon class
class DiscordDaemon:
    def __init__(self, token):
        self.token = token
        self.client = discord.Client()
        self.client.run(self.token)

        @self.client.event
        async def on_ready():
            print('Logged in as')
            print(self.client.user.name)
            print(self.client.user.id)
            print('------')

        def start(self):
            self.client.run(self.token)
        
        start(self)

    def stop(self):
        self.client.close()

    def send_message(self, channel, message):
        self.client.send_message(channel, message)

    
