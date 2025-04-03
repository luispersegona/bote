import discord
from discord.ext import commands

# Dicionário com as informações do cargo para cada rank
rank_info = {
    "Bronze I🥉": {"color": discord.Color.from_rgb(166, 124, 0)},
    "Bronze II 🥉": {"color": discord.Color.from_rgb(166, 124, 0)},
    "Bronze III 🥉": {"color": discord.Color.from_rgb(166, 124, 0)},
    "Bronze IV 🥉": {"color": discord.Color.from_rgb(166, 124, 0)},
    "Bronze V 🥉": {"color": discord.Color.from_rgb(166, 124, 0)},
    "Silver I 🥈": {"color": discord.Color.from_rgb(192, 192, 192)},
    "Silver II 🥈": {"color": discord.Color.from_rgb(192, 192, 192)},
    "Silver III 🥈": {"color": discord.Color.from_rgb(192, 192, 192)},
    "Silver IV 🥈": {"color": discord.Color.from_rgb(192, 192, 192)},
    "Silver V 🥈": {"color": discord.Color.from_rgb(192, 192, 192)},
    "Gold I 🥇": {"color": discord.Color.from_rgb(255, 215, 0)},
    "Gold II 🥇": {"color": discord.Color.from_rgb(255, 215, 0)},
    "Gold III 🥇": {"color": discord.Color.from_rgb(255, 215, 0)},
    "Gold IV 🥇": {"color": discord.Color.from_rgb(255, 215, 0)},
    "Gold V 🥇": {"color": discord.Color.from_rgb(255, 215, 0)},
    "Platinum I 💠": {"color": discord.Color.from_rgb(0, 128, 128)},
    "Platinum II 💠": {"color": discord.Color.from_rgb(0, 128, 128)},
    "Platinum III 💠": {"color": discord.Color.from_rgb(0, 128, 128)},
    "Platinum IV 💠": {"color": discord.Color.from_rgb(0, 128, 128)},
    "Platinum V 💠": {"color": discord.Color.from_rgb(0, 128, 128)},
    "Diamond I 💎": {"color": discord.Color.from_rgb(0, 191, 255)},
    "Diamond II 💎": {"color": discord.Color.from_rgb(0, 191, 255)},
    "Diamond III 💎": {"color": discord.Color.from_rgb(0, 191, 255)},
    "Diamond IV 💎": {"color": discord.Color.from_rgb(0, 191, 255)},
    "Diamond V 💎": {"color": discord.Color.from_rgb(0, 191, 255)},
    "Master 🏆": {"color": discord.Color.from_rgb(230, 25, 75)},
    "Grandmaster 🏆": {"color": discord.Color.from_rgb(128, 0, 128)}
}


class Salas:
    def __init__(self, bot):
        self.bot = bot

    async def criar_salas(self, guild: discord.Guild, author: discord.Member):
        """Cria canais de voz com permissões hierárquicas para os cargos."""
        bot_member = guild.get_member(self.bot.user.id)

        # Verificar se o autor tem um cargo superior ao do bot
        if author.top_role < bot_member.top_role:
            return "Seu cargo precisa ser superior ao do bot para executar esta ação."

        feedback = []
        
        # Agrupar os ranks por tipo (Bronze, Prata, Ouro, etc.) com as medalhas
        rank_groups = {
            "Bronze 🥉": ["Bronze I🥉", "Bronze II 🥉", "Bronze III 🥉", "Bronze IV 🥉", "Bronze V 🥉"],
            "Silver 🥈": ["Silver I 🥈", "Silver II 🥈", "Silver III 🥈", "Silver IV 🥈", "Silver V 🥈"],
            "Gold 🥇": ["Gold I 🥇", "Gold II 🥇", "Gold III 🥇", "Gold IV 🥇", "Gold V 🥇"],
            "Platinum 💠": ["Platinum I 💠", "Platinum II 💠", "Platinum III 💠", "Platinum IV 💠", "Platinum V 💠"],
            "Diamond 💎": ["Diamond I 💎", "Diamond II 💎", "Diamond III 💎", "Diamond IV 💎", "Diamond V 💎"],
            "Master 🏆": ["Master 🏆"],
            "Grandmaster 🏆": ["Grandmaster 🏆"]
        }

        # Lista de todos os ranks ordenados da hierarquia mais baixa para a mais alta
        all_ranks = ["Bronze 🥉", "Silver 🥈", "Gold 🥇", "Platinum 💠", "Diamond 💎", "Master 🏆", "Grandmaster 🏆"]

        for i, (group_name, ranks) in enumerate(rank_groups.items()):
            # Verifica se pelo menos um cargo do grupo existe
            roles = [discord.utils.get(guild.roles, name=rank) for rank in ranks]
            roles = [role for role in roles if role is not None]

            if roles:
                channel_name = group_name  # Nome da sala com a medalha (ex: Bronze 🥉)
                # Verificar se a sala de voz já existe
                existing_channel = discord.utils.get(guild.voice_channels, name=channel_name)

                if existing_channel:
                    feedback.append(f"⚠️ Sala de voz '{channel_name}' já existe.")
                else:  # Se o canal não existir, cria a sala
                    try:
                        overwrites = {
                            guild.default_role: discord.PermissionOverwrite(view_channel=True, connect=False),  # Todos podem ver, mas não podem entrar
                        }

                        # Adicionar permissões para cada cargo dentro do grupo
                        for j, role in enumerate(roles):
                            overwrites[role] = discord.PermissionOverwrite(view_channel=True, connect=True, speak=True)

                        # Cargos superiores (fora do grupo) podem ver e acessar todas as salas
                        for l in range(i + 1, len(all_ranks)):
                            superior_roles = [discord.utils.get(guild.roles, name=rank) for rank in rank_groups[all_ranks[l]]]
                            for superior_role in superior_roles:
                                if superior_role:
                                    overwrites[superior_role] = discord.PermissionOverwrite(view_channel=True, connect=True, speak=True)

                        # Criar o canal de voz com as permissões definidas e limite de 4 usuários
                        new_channel = await guild.create_voice_channel(
                            name=channel_name,
                            overwrites=overwrites,
                            user_limit=4,  # Limitando a 4 usuários no canal
                            reason="Criação automática de salas hierárquicas pelo bot."
                        )
                        feedback.append(f"✅ Sala de voz '{new_channel.name}' criada com sucesso!")
                    except discord.Forbidden:
                        feedback.append(f"❌ Não tenho permissão para criar a sala de voz '{channel_name}'")
                    except discord.HTTPException:
                        feedback.append(f"❌ Erro HTTP ao criar a sala de voz '{channel_name}'")
                    except Exception as e:
                        feedback.append(f"❌ Erro desconhecido ao criar a sala de voz '{channel_name}': {e}")

        if not feedback:
            return "Nenhuma sala de voz foi criada, por favor verifique a ação."
        return "\n".join(feedback)


