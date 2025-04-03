import discord
from discord import app_commands

guild_id = 1317859302157058048  # Defina o ID da guilda para registrar o comando

async def setup(bot):
    @bot.tree.command(guild=discord.Object(id=guild_id), name='limpar', description='Apaga todas as mensagens da sala atual')
    async def limpar(interaction: discord.Interaction):
        # Verifica se o usuário tem permissões administrativas
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "Você não tem permissão para usar este comando.", 
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)  # Defer para ganhar tempo enquanto as mensagens são apagadas

        try:
            # Apaga as mensagens da sala
            deleted = await interaction.channel.purge()

            # Confirmação de sucesso
            await interaction.followup.send(
                f"Todas as mensagens ({len(deleted)}) foram apagadas da sala!",
                ephemeral=True
            )
        except Exception as e:
            # Tratamento de erro, caso o bot não consiga apagar mensagens
            await interaction.followup.send(
                f"Erro ao tentar apagar as mensagens: {str(e)}",
                ephemeral=True
            )