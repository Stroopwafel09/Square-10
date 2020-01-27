import json

import requests
from discord.ext import commands

import teapot.tools.embed as dmbd


class OsuPlayer:

    def __init__(self, player):
        self.id = player["user_id"]
        self.username = player["username"]
        self.join_date = (player["join_date"].split(" "))[0]
        self.c300 = player["count300"]
        self.c100 = player["count100"]
        self.c50 = player["count50"]
        self.playcount = player["playcount"]
        self.ranked = player["ranked_score"]
        self.total = player["total_score"]
        self.pp = player["pp_rank"]
        self.level = player["level"]
        self.pp_raw = player["pp_raw"]
        self.accuracy = player["accuracy"]
        self.count_ss = player["count_rank_ss"]
        self.count_s = player["count_rank_s"]
        self.count_a = player["count_rank_a"]
        self.country = player["country"]
        self.pp_country_rank = player["pp_country_rank"]

    def display(self, author):
        em = dmbd.newembed()
        em.set_author(name=f"{self.country.upper()} | {self.username}", url=f"https://osu.ppy.sh/u/{self.username}")
        em.add_field(name='Performance', value=self.pp_raw + 'pp')
        em.add_field(name='Accuracy', value="{0:.2f}%".format(float(self.accuracy)))
        lvl = int(float(self.level))
        percent = int((float(self.level) - lvl) * 100)
        em.add_field(name='Level', value=f"{lvl} ({percent}%)")
        em.add_field(name='Rank', value=self.pp)
        em.add_field(name='Country Rank', value=self.pp_country_rank)
        em.add_field(name='Playcount', value=self.playcount)
        em.add_field(name='Total Score', value=self.total)
        em.add_field(name='Ranked Score', value=self.ranked)
        em.add_field(name='Registered At', value=self.join_date)
        return em


class Osu(commands.Cog):
    """Osu! Statistics"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def osu(self, ctx, *, args: str):
        """ Look up an osu player """

        args_array = args.split(' ')
        if len(args_array) == 2:
            peppy = args_array[0]
            type = args_array[1]
        elif len(args_array) == 1:
            peppy = args_array[0]
            type = "0"
        else:
            await ctx.send('Invalid Syntax!')
            return
        cookiezi = '05b43eb66b2977d4f2c9148b00e3853688d515cf'
        r = requests.get('http://osu.ppy.sh/api/get_user?k=' + cookiezi + '&u=' + peppy + '&m=' + type)

        if r.status_code != 200:
            print('Unable to fetch osu statistics!')
            return

        await ctx.send(embed=OsuPlayer(json.loads(r.text)[0]).display(ctx.message.author))


def setup(bot):
    bot.add_cog(Osu(bot))
