import discord
from discord.ext import commands
from defi.cargos import criar_cargos  # Importa a classe Cargos para usar a lógica de criar cargos
from defi.deletar_cargos import deletar_cargos  # Importa a função de deletar cargos
from defi.criar_salas import Salas  # Importa a classe Salas

guild_id = 1317859302157058048  # Defina o ID da guilda para registrar o comando

async def setup(bot):
    # Registra o comando '/menu' com a interação de slash
    @bot.tree.command(guild=discord.Object(id=guild_id), name='menu', description='Comando de teste com paginação')
    async def slash2(interaction: discord.Interaction):
        # Cria a embed inicial sem o botão "Ação"
        embed = discord.Embed(
            title="Menu 🛠️",
            description="Configure seu bot.\n Use 'Próximo' para avançar.\n\nEscolha a ação desejada e siga os passos.\n\nSe tiver dúvidas, entre em contato com o suporte."
        )
        embed.set_footer(text="Configuração")

        # Cria a view com os botões
        view = TesteView(bot)

        # Envia a mensagem com a embed e a view
        await interaction.response.send_message(embed=embed, view=view, ephemeral=False)


class TesteView(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.current_page = 0  # Página inicial (menu)
        self.update_buttons()

    @discord.ui.button(label="Voltar", style=discord.ButtonStyle.blurple, disabled=True)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            embed = self.create_embed()
            self.update_buttons()
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Próximo", style=discord.ButtonStyle.blurple)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < 3:  # Ajuste de número de páginas
            self.current_page += 1
            embed = self.create_embed()
            self.update_buttons()
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Ação", style=discord.ButtonStyle.green, disabled=True)
    async def action_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Envia mensagem inicial de "aguarde"
        await interaction.response.send_message("Aguarde enquanto a ação é executada...", ephemeral=True)

        try:
            # Executa a ação de criar cargos se estiver na página 1
            if self.current_page == 1:
                await criar_cargos(self.bot, interaction.guild, interaction.user)  # Chama a função diretamente
                success_message = "Cargos criados com sucesso!"  # Mensagem de sucesso após a ação
            elif self.current_page == 3:
                await deletar_cargos(self.bot, interaction.guild, interaction.user)
                success_message = "Cargos deletados com sucesso!"
            elif self.current_page == 2:
                # Criando a instância da classe Salas
                salas = Salas(self.bot)  # Passando o bot para a classe Salas

                # Agora chamamos o método criar_salas com os parâmetros necessários
                response = await salas.criar_salas(interaction.guild, interaction.user)  # Passa a guild e o author
                success_message = response  # Mensagem retornada pela função criar_salas
        
            # Edita apenas a mensagem com o status de sucesso
            await interaction.edit_original_response(content=success_message)

        except Exception as e:
            # Caso ocorra um erro durante a execução da ação
            await interaction.edit_original_response(content=f"Erro: {str(e)}")

    @discord.ui.button(label="Fechar", style=discord.ButtonStyle.red)
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()

    def create_embed(self):
        # Cria uma embed com base na página atual
        embed = discord.Embed(
            title=f"Página {self.current_page}",
            description=f"Conteúdo dinâmico para a página {self.current_page}. Clique no botão para realizar uma ação."
        )

        if self.current_page == 0:
            embed.title = "Menu 🛠️"
            embed.description = "Configure seu bot.\n Use 'Próximo' para avançar.\n\nEscolha a ação desejada e siga os passos.\n\nSe tiver dúvidas, entre em contato com o suporte."
            self.children[2].disabled = True  # Desabilita o botão "Ação" na página inicial
        elif self.current_page == 1:
            embed.title = "Cargos 🥉"
            embed.description = "Clique em 'Ação' para criar os cargos necessários.\nVoçê receberá uma confirmação que foram criados.\n\nOs cargos são necessários para acesso as salas ⚠️"
            self.children[2].disabled = False  # Ativa o botão "Ação" na página 1
        elif self.current_page == 2:
            embed.title = "Salas 🏠"
            embed.description = "Deseja criar as salas configuradas para grupos rankeados?\nClique em 'Ação' para cria-las.\n\nSomente pessoas com ranking e cargo poderão acessá-las 🚨"
            self.children[2].disabled = False  # Ativa o botão "Ação" na página 2
        elif self.current_page == 3:
            embed.title = "Deletar cargos 🗑️"
            embed.description = "Deseja deletar os cargos criados?\nClique em 'Ação' para deleta-los."
            self.children[2].disabled = False  # Desativa o botão "Ação" na página 3, caso não tenha ação

        embed.set_footer(text=f"Página {self.current_page}")
        return embed

    def update_buttons(self):
        # Atualiza os estados dos botões com base na página atual
        self.children[0].disabled = self.current_page == 0  # Desabilita o botão "Voltar" na página inicial
        self.children[1].disabled = self.current_page == 3  # Desabilita o botão "Próximo" na última página
