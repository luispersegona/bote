import discord
from discord import app_commands
import requests
from defi.cargos import rank_info  # Importa o dicionário de cargos


guild_id = 1317859302157058048  # Defina o ID da guilda para registrar o comando

RANK_IMAGES = {
    "Unranked": "https://i.postimg.cc/75NSKRQT/unranked-removebg-preview.png",
    "Bronze 1": "https://i.postimg.cc/34tLzRSm/bronze1-removebg-preview.png",
    "Bronze 2": "https://i.postimg.cc/xqFxRXbS/bronze2-removebg-preview.png",
    "Bronze 3": "https://i.postimg.cc/Btv7HTbg/bronze3-removebg-preview.png",
    "Bronze 4": "https://i.postimg.cc/ct6DWS2j/bronze4-removebg-preview.png",
    "Bronze 5": "https://i.postimg.cc/BXLhwJxP/bronze5-removebg-preview.png",
    "Silver 1": "https://i.postimg.cc/JHBbK491/prata1-removebg-preview.png",
    "Silver 2": "https://i.postimg.cc/t71t927L/prata2-removebg-preview.png",
    "Silver 3": "https://i.postimg.cc/grfyj8Zr/prata3-removebg-preview.pn",
    "Silver 4": "https://i.postimg.cc/7f032h39/prata4-removebg-preview.png",
    "Silver 5": "https://i.postimg.cc/ZWmrFmjS/prata5-removebg-preview.png",
    "Gold 1": "https://i.postimg.cc/jw3XZ12h/ouro1-removebg-preview.png",
    "Gold 2": "https://i.postimg.cc/V0SFTFbP/ouro2-removebg-preview.png",
    "Gold 3": "https://i.postimg.cc/mhqj9K0L/ouro3-removebg-preview.png",
    "Gold 4": "https://i.postimg.cc/MvQDmdSy/ouro4-removebg-preview-2.png",
    "Gold 5": "https://i.postimg.cc/zyYktKz4/ouro5-removebg-preview.png",
    "Platinum 1": "https://i.postimg.cc/G4PxZt9t/platina1-removebg-preview.png",
    "Platinum 2": "https://i.postimg.cc/t1XNybV5/platina2-removebg-preview.png",
    "Platinum 3": "https://i.postimg.cc/CZmHx2GV/platina3-removebg-preview.png",
    "Platinum 4": "https://i.postimg.cc/ZBnPBLHv/platina4-removebg-preview.png",
    "Platinum 5": "https://i.postimg.cc/62PrdGbj/platina5-removebg-preview.png",
    "Diamond 1": "https://i.postimg.cc/dLb5bgBH/dima1-removebg-preview.png",
    "Diamond 2": "https://i.postimg.cc/5X8sbpKx/dima2-removebg-preview.png",
    "Diamond 3": "https://i.postimg.cc/rdcQmW75/dima3-removebg-preview.png",
    "Diamond 4": "https://i.postimg.cc/JyqKB0Wv/dima4-removebg-preview.png",
    "Diamond 5": "https://i.postimg.cc/ZB5HPmbR/dima5-removebg-preview.png",
    "Master": "https://i.postimg.cc/NLLb5QCC/mestre-removebg-preview.png",
    "Grandmaster": "https://i.postimg.cc/NLLb5QCC/mestre-removebg-preview.png"
}


# Define a cog do comando /rank
async def setup(bot):
    @bot.tree.command(guild=discord.Object(id=guild_id), name='rank', description='Consulta as estatísticas da temporada do jogador PUBG.')
    async def rank(interaction: discord.Interaction, player_name: str):
        """
        Consulta as estatísticas da temporada atual para um jogador e envia em uma embed.
        """
        if not player_name:
            await interaction.response.send_message(
                "Por favor, forneça um nome de jogador. Exemplo: `/rank NomeDoJogador`",
                ephemeral=True
            )
            return
        
        api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI3Yzk4YzUzMC1jYzVjLTAxM2ItYzJhMC01ZTVlMTJiNTcwYWEiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjgzMTcyMTIyLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii01OTM5YzQ3Ny1iNjcyLTRkYjQtYWIxOS1hODBiN2I3ZjJmNWIifQ.IkJx78LvxAu8X8-xqLxwIAiYQsxU0jGmbUnRNb2yW84"  # Substitua pela sua chave de API
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/vnd.api+json"
        }

        try:
            # Passo 1: Obter Account ID do jogador
            player_url = f"https://api.pubg.com/shards/steam/players?filter[playerNames]={player_name}"
            player_response = requests.get(player_url, headers=headers)
            player_response.raise_for_status()
            player_data = player_response.json()

            if not player_data.get("data"):
                await interaction.response.send_message("⚠️ Jogador não encontrado.")
                return

            account_id = player_data["data"][0]["id"]
            api_player_name = player_data["data"][0]["attributes"]["name"]  # Nome do jogador

            # Verificar se o nome fornecido corresponde ao nome da API
            if player_name.lower() != api_player_name.lower():
                await interaction.response.send_message(f"O nome fornecido ({player_name}) não corresponde ao jogador encontrado ({api_player_name}).")
                return
                       
            # Passo 2: Obter a temporada atual
            seasons_url = "https://api.pubg.com/shards/steam/seasons"
            seasons_response = requests.get(seasons_url, headers=headers)
            seasons_response.raise_for_status()
            seasons_data = seasons_response.json()

            current_season = next((season for season in seasons_data["data"] if season["attributes"].get("isCurrentSeason", False)), None)
            if not current_season:
                await interaction.response.send_message("Não foi possível identificar a temporada atual.")
                return

            current_season_id = current_season["id"]

            # Passo 3: Obter estatísticas do jogador
            season_url = f"https://api.pubg.com/shards/steam/players/{account_id}/seasons/{current_season_id}/ranked"
            season_response = requests.get(season_url, headers=headers)
            season_response.raise_for_status()
            season_data = season_response.json()

            squad_fpp_stats = season_data["data"]["attributes"]["rankedGameModeStats"].get("squad-fpp")
            if not squad_fpp_stats:
                await interaction.response.send_message("Estatísticas do modo ranked squad-fpp não encontradas.")
                return

            # Extrair corretamente o Tier e SubTier
            tier_info = squad_fpp_stats.get("currentTier", {"tier": "Unranked", "subTier": ""})
            tier = tier_info.get("tier", "Unranked")
            sub_tier = tier_info.get("subTier", "")
            rank = f"{tier} {sub_tier}".strip()

            # Filtrar os dados relevantes
            relevant_data = {
                "Modo": "Ranked Squad-FPP",
                "Season": current_season_id,
                "Kills": squad_fpp_stats.get("kills", 0),
                "Deaths": squad_fpp_stats.get("deaths", 0),
                "Assists": squad_fpp_stats.get("assists", 0),
                "kdRatio": squad_fpp_stats.get("kda", 0),
                "killsPerMatch": squad_fpp_stats.get("killsPerMatch", 0),
                "roundsPlayed": squad_fpp_stats.get("roundsPlayed", 0),
                "wins": squad_fpp_stats.get("wins", 0),
                "losses": squad_fpp_stats.get("loss", 0),
                "wlRatio": squad_fpp_stats.get("winRatio", 0),
                "damageDealt": squad_fpp_stats.get("damageDealt", 0),
                "damagePerMatch": squad_fpp_stats.get("damagePerMatch", 0),
                "knockdowns": squad_fpp_stats.get("dBNOs", 0),
                "top10": squad_fpp_stats.get("top10s", 0),
                "top10Ratio": squad_fpp_stats.get("top10Ratio", 0),
                "avgRank": squad_fpp_stats.get("avgRank", 0),
                "currentRankPoints": squad_fpp_stats.get("currentRankPoint", 0),
                "bestRankPoints": squad_fpp_stats.get("bestRankPoint", 0)
            }

            # Criação da embed
            embed = discord.Embed(title=f"Estatísticas de {player_name}", color=0x00ff00)
            embed.add_field(name="Modo 🛠️", value=relevant_data["Modo"], inline=False)
            embed.add_field(name="Temporada 🏆", value=relevant_data["Season"], inline=False)
            embed.add_field(name="Kills 🔫", value=relevant_data["Kills"], inline=True)
            embed.add_field(name="Deaths 💀", value=relevant_data["Deaths"], inline=True)
            embed.add_field(name="Assists 🤝", value=relevant_data["Assists"], inline=True)
            embed.add_field(name="KD 🔪", value=relevant_data["kdRatio"], inline=True)
            embed.add_field(name="Partidas Jogadas 🎲", value=relevant_data["roundsPlayed"], inline=True)
            embed.add_field(name="Vitórias 🎉", value=relevant_data["wins"], inline=True)
            embed.add_field(name="Taxa de Vitórias 💯", value=relevant_data["wlRatio"], inline=True)
            embed.add_field(name="Rank Médio 🥉", value=relevant_data["avgRank"], inline=True)
            embed.add_field(name="Derrubadas 💤", value=relevant_data["knockdowns"], inline=True)
            embed.add_field(name="Taxa Top 10 📊", value=relevant_data["top10Ratio"], inline=True)
            embed.add_field(name="Dano Total 💥", value=relevant_data["damageDealt"], inline=True)
            embed.add_field(name="Pontos Atuais 🎖️", value=relevant_data["currentRankPoints"], inline=True)
            embed.add_field(name="Melhor Pontuação Temporada 💎", value=relevant_data["bestRankPoints"], inline=True)
            embed.set_footer(text="Ranking atualizado.")

            # Obter a imagem correspondente ao rank
            image_url = RANK_IMAGES.get(rank, RANK_IMAGES["Unranked"])

            # Adicionar a imagem na thumbnail da embed
            embed.set_thumbnail(url=image_url)
            
            # Enviar a embed
            await interaction.response.send_message(embed=embed)
                  
        except requests.exceptions.RequestException as e:
            await interaction.response.send_message(f"Erro na requisição: {e}")
        except Exception as e:
            await interaction.response.send_message(f"Erro inesperado: {e}")
