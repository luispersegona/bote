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

async def criar_cargos(bot: commands.Bot, guild: discord.Guild, author: discord.Member):
    """
    Cria os cargos baseados no dicionário rank_info.
    Verifica permissões, hierarquia e já existentes.
    """
    bot_member = guild.get_member(bot.user.id)

    # Validações iniciais
    if not guild.me.guild_permissions.manage_roles:
        return "❌ Não tenho permissão para gerenciar cargos."
    if author.top_role <= bot_member.top_role:
        return "Seu cargo precisa ser superior ao do bot para executar esta ação."

    feedback = {"success": [], "failed": [], "existing": []}

    # Criação dos cargos
    for rank_name, rank_details in rank_info.items():
        role = discord.utils.get(guild.roles, name=rank_name)
        if role:
            feedback["existing"].append(f"⚠️ Cargo '{rank_name}' já existe.")
            continue

        try:
            new_role = await guild.create_role(
                name=rank_name,
                color=rank_details["color"],
                hoist=True,
                reason="Criação automática pelo bot."
            )
            feedback["success"].append(f"✅ Cargo '{rank_name}' criado com sucesso!")
        except discord.Forbidden:
            feedback["failed"].append(f"❌ Não tenho permissão para criar o cargo '{rank_name}'")
        except discord.HTTPException:
            feedback["failed"].append(f"❌ Erro HTTP ao criar o cargo '{rank_name}'")
        except Exception as e:
            feedback["failed"].append(f"❌ Erro desconhecido ao criar o cargo '{rank_name}': {e}")

    # Compilação do feedback
    messages = []
    if feedback["success"]:
        messages.append("**Cargos criados com sucesso:**\n" + "\n".join(feedback["success"]))
    if feedback["existing"]:
        messages.append("**Cargos já existentes:**\n" + "\n".join(feedback["existing"]))
    if feedback["failed"]:
        messages.append("**Falhas na criação dos cargos:**\n" + "\n".join(feedback["failed"]))

    return "\n\n".join(messages)