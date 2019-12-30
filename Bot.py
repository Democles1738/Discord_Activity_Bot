import discord
import random
# import pytz
# from dateutil import tz
# https://stackoverflow.com/questions/796008/cant-subtract-offset-naive-and-offset-aware-datetimes
from datetime import datetime   # , timezone

server_id = 0
dance_gifs = ["https://media2.giphy.com/media/UQJ5yo5d6dNARSvO8I/giphy.gif", "https://tenor.com/view/thanos-thanos-dancing-twerk-gif-15307482", "https://tenor.com/view/thanos-dancing-fortnite-orange-gif-11793362"]

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    # this function will happen when a message is sent to the server in general
    async def on_message(self, message):
        global server_id
        global dance_gifs
        print('Messsage from {0.author}: {0.content}'.format(message))
        # if the message is for us, it will begin with !activity
        if message.content.startswith("!activity"):
            # the message should be formatted as !command month day
            parsed_msg = message.content.split(' ', 3)   # parsing the string on white spaces with a max split of 3, return a list
            # this is fragile and is now assuming argument 1 is month and argument 2 is day

            # check if we are set up to talk with this server or not
            channel = check_server_id(message)
            # if server_id is 0:     # if it's 0, it has not been setup and we reply in the channel that we were invoked in
            #     print("changing id to: ", message.channel.id)
            #     channel = client.get_channel(message.channel.id)
            # else:
            #     channel = client.get_channel(server_id)
            try:
                month = int(parsed_msg[1])
                if month < 1 or month > 12:
                    string_to_send = "Hey! Stop trying to break me! Put a correct number for the month because " + str(month) + " is just not right"
                    await channel.send(string_to_send)
                    return
                day = int(parsed_msg[2])
                if day < 1 or day > 31:
                    string_to_send = "Hey! Stop trying to break me! Put a correct number for the day because " + str(
                        day) + " is just not right"
                    await channel.send(string_to_send)
                    return
            except IndexError:
                print("Index out of bounds exception ran into")
                await channel.send("Invalid format, after !activity, example of correct format: !activity 12 4")
                return
            print('Reading users...')
            await channel.send("https://media1.tenor.com/images/f1b55c5a0fc1f760ce2b0b5c5d495470/tenor.gif?itemid=14599588")
            tempList = self.users
            active_list = []
            inactive_list = []
            for user in tempList:
                print(user.name)
                inactive_list.append(user.name)
            # everybody is assumed to be inactive, when a message is found from that user, they will be moved to active
            print('Reading messages...')
            text_channel_list = []
            for server in self.guilds:
                for text_channel in server.channels:
                    if text_channel.type is discord.ChannelType.text:   # this is a text channel, we want to read it's messages
                        # https://discordpy.readthedocs.io/en/latest/api.html#discord.abc.GuildChannel
                        # https://stackoverflow.com/questions/23050392/whats-wrong-with-this-tzinfo-variable
                        # https://stackoverflow.com/questions/7065164/how-to-make-an-unaware-datetime-timezone-aware-in-python
                        print("On channel: ", text_channel)
                        try:
                            async for msg in text_channel.history(limit=200, before=None,
                                                             after=datetime(2019, month, day, 0, 0, 0,
                                                                            0)):  # , tzinfo=datetime.now(pytz.utc)), around=None, oldest_first=None): this would make it aware and not naive
                                if msg.author.display_name in inactive_list:
                                    print("Moving: ", msg.author.display_name, " to the active list")
                                    active_list.append(msg.author.display_name)
                                    # now remove that person from the inactive list
                                    inactive_list.remove(msg.author.display_name)
                                    # await message.author.send("Done!")
                        except:
                            await channel.send("Stop it with the bad dates :(")
                            # print(msg.content)
                            # print(msg.author.display_name)
                            return
            await channel.send('Done! Here is the list of all active members: ')
            await channel.send(active_list)
            await channel.send("Here is the list of all inactive members: ")
            await channel.send(inactive_list)

        # Here we are assuming that they want to set up to the bot to reply in the channel they typed this command
        # elif message.content.startswith("!setup"):
        #     print("changing id to: ", message.channel.id)
        #     channel = client.get_channel(message.channel.id)
        #     await channel.send("I will reply here now")

        elif message.content.startswith("!help"):
            channel = check_server_id(message)
            await channel.send("Hello! I'm a bot that looks at the previous messages and determines which users are active and not active. "
                               "It's not a complicated process, if a user has sent a message within the time frame given to me, I consider that as active. "
                               "The format I require is `!activity {month} {day}`, replace {month} {day} with actual numbers and remove the braces as well. "
                               "Month should be between 1-12 and day should be between 1-31, please don't break me by putting February 31st or whatever. Have mercy. "
                               "After that I will send messages with a list of active and inactive members")
            await channel.send("I can also `!dance` and `!die`")

        elif message.content.startswith("!dance"):
            channel = check_server_id(message)
            string_gif = dance_gifs[random.randrange(0, len(dance_gifs))]
            await channel.send(string_gif)

        elif message.content.startswith("!die"):
            channel = check_server_id(message)
            await channel.send("https://tenor.com/view/thanos-endgame-avengers-gone-ashes-gif-14019029")

        elif message.content.startswith("!"):
            channel = check_server_id(message)
            await channel.send("Hey, not sure if you're trying to talk to me, try !help if you need help")


def check_server_id(message):
    """this function checks for the channel id of the message and the channel id that we are currently set up with
    if they do not match, a different server is talking to us and we need to switch ids"""
    global server_id
    if server_id is 0:     # the channel_id is not set up at all
        server_id = message.channel.id  # this is the current server that we're talking to
        channel = client.get_channel(server_id)     # this is the current channel in that server that we will send messages to
    elif server_id is not message.channel.id:      # our current set up is for another server, change it
        server_id = message.channel.id
        channel = client.get_channel(server_id)
    return channel


client = MyClient()
random.seed()
client.run('')   # <== place token here
