import bot_interface
import lckSchedule

myToken = 'Mjg1NjUxMTM3OTU5NTU5MTY4.WLO_Wg.LPIpDJqacW5eMTBms8GfGyyfSSQ'
testMode = True


class MyClient(discord.Client):
    # logged on
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    # message parsing
    async def on_message(self, message):
        # channel in which the message's sent
        channel = message.channel
        if message.content.lower() == '#help': # help: commands
            help_list = '#help #lck'
            await channel.send(help_list)

        if message.content.lower() == '#lck': #
            print('')

        # ------- for debugging: prints all messages --------- #
        if not message.author.bot and testMode: # do only if message is sent from user && is testMode
            print('message: ', message)
            print('message type: ', type(message.content))
            print('message content: ', message.content)




# client = MyClient()
# client.run(myToken)
