import discord
# import lckSchedule

class MyClient(discord.Client):
    # logged on
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    # message parsing
    async def on_message(self, message):
        # channel in which the message's sent
        channel = message.channel
        if message.content.lower() == '$help': # help: commands
            help_list = '$help $lck'
            await channel.send(help_list)

        if message.content.lower() == '$lck': # LCK commands
            help_list = '$오늘LCK: 오늘 LCK 경기\n$다음LCK:다음 LCK 경기\n$다음@@경기: 해당 팀의 다음 경기'
            await channel.send(help_list)

        if message.content.lower() == '$오늘LCK':
            print(message.content.lower())
            await channel.send('몰라.')

        # ------- for debugging: prints all messages --------- #
        if not message.author.bot: # do only if message is sent from user && is testMode
            print('message: ', message)
            print('message type: ', type(message.content))
            print('message content: ', message.content)