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
        self.presence_task = None  # Variável para armazenar a tarefa de presença

    async def on_ready(self):
        print(f"🚀 Bot conectado como {self.user}.")

        # 🔥 Lista os servidores conectados
        if self.guilds:
            print("✅ O bot está presente nos seguintes servidores:")
            for guild in self.guilds:
                print(f"  📌 {guild.name} (ID: {guild.id})")
        else:
            print("⚠️ O bot não está em nenhum servidor.")

        if self.presence_task is None:  # Evita a criação de múltiplos loops
            self.presence_task = self.loop.create_task(self.update_presence())

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
        # 🔥 Carregar as Cogs
        for cog in ["cogs.limpar", "cogs.rank", "cogs.menu"]:
            try:
                await self.load_extension(cog)
                print(f"✅ Cog '{cog}' carregada.")
            except Exception as e:
                print(f"❌ Erro ao carregar cog '{cog}': {e}")

        # 🔥 Sincronizar comandos
        try:
            synced = await self.tree.sync()
            print(f"✅ {len(synced)} comandos sincronizados globalmente.")
        except Exception as e:
            print(f"❌ Erro ao sincronizar comandos: {e}")

# Inicializa o bot
client = AClient()

# Executa o bot
if TOKEN:
    try:
        client.run(TOKEN)
    except discord.LoginFailure:
        print("❌ Erro: Token inválido. Verifique se o .env contém o token correto.")
else:
    print("❌ Erro: Token do bot não encontrado. Certifique-se de que o arquivo .env está configurado corretamente.")
