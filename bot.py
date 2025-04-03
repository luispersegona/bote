import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random
import os
from dotenv import load_dotenv  # Importa dotenv para carregar variáveis de ambiente

# Carrega as variáveis do arquivo .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

class AClient(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.messages = True
        intents.guilds = True
        intents.members = True
        intents.message_content = True  # Ativando acesso ao conteúdo das mensagens

        super().__init__(command_prefix="!", intents=intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            try:
                await self.tree.sync()  # 🔥 Agora os comandos serão globais!
                self.synced = True
                print(f"✅ Comandos sincronizados globalmente.")
            except Exception as e:
                print(f"❌ Erro ao sincronizar os comandos: {e}")

        print(f"🚀 Bot conectado como {self.user}.")
        self.loop.create_task(self.update_presence())

    async def update_presence(self):
        statuses = [
            ("Pubg", discord.ActivityType.playing),
            ("Comando /rank", discord.ActivityType.listening),
            ("Squad-FPP", discord.ActivityType.watching),
        ]
        while True:
            status, activity_type = random.choice(statuses)
            activity = discord.Activity(type=activity_type, name=status)
            await self.change_presence(activity=activity)
            await asyncio.sleep(4)

    async def setup_hook(self):
        for cog in ["cogs.limpar", "cogs.rank", "cogs.menu"]:
            try:
                await self.load_extension(cog)
                print(f"Cog '{cog}' carregada.")
            except Exception as e:
                print(f"Erro ao carregar cog '{cog}': {e}")

# Inicializa o bot
client = AClient()

# Executa o bot
if TOKEN:
    client.run(TOKEN)
else:
    print("❌ Erro: Token do bot não encontrado. Certifique-se de que o arquivo .env está configurado corretamente.")
