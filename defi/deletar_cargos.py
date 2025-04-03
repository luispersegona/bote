import discord
from discord.ext import commands
from defi.cargos import rank_info  # Importa o dicionário rank_info

async def deletar_cargos(bot: commands.Bot, guild: discord.Guild, author: discord.Member):
    """Lógica para deletar os cargos baseados no dicionário rank_info."""
    bot_member = guild.get_member(bot.user.id)

    # Verificar se o autor tem um cargo superior ao do bot
    if author.top_role <= bot_member.top_role:
        return "Seu cargo precisa ser superior ao do bot para executar esta ação."

    feedback = []  # Lista para armazenar mensagens de feedback

    # Itera pelos cargos no dicionário e tenta deletá-los
    for rank_name in rank_info.keys():
        role = discord.utils.get(guild.roles, name=rank_name)
        if role:
            try:
                await role.delete(reason="Remoção automática pelo bot.")
                feedback.append(f"✅ Cargo '{rank_name}' deletado com sucesso!")
            except discord.Forbidden:
                feedback.append(f"❌ Não tenho permissão para deletar o cargo '{rank_name}'.")
            except discord.HTTPException:
                feedback.append(f"❌ Erro HTTP ao deletar o cargo '{rank_name}'.")
            except Exception as e:
                feedback.append(f"❌ Erro desconhecido ao deletar o cargo '{rank_name}': {e}")
        else:
            feedback.append(f"⚠️ Cargo '{rank_name}' não encontrado.")

    return "\n".join(feedback)  # Retorna todas as mensagens como uma string
