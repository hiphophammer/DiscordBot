import discord
import os

userToken = "Mjg1NjUxMTM3OTU5NTU5MTY4.WLO_Wg.tQOBIlY4j7jyXL7q3ylJhhnZJ0M"


class chatbot(discord.Client):
    async def on_ready(self):
        print('Logged in')

    async def on_message(self, msg):
        if msg.content == '~add':
            fpath = os.path.join('resources', 'wanderer_maps', '아르테미스', '로그힐')
            file = discord.File(fpath, filename="로그힐.png")
            await msg.channel.send("", file=file)
            print('Done')





client = chatbot()
client.run(userToken)
