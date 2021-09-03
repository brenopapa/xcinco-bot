GSHEET_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1stCb-l0h1o5Kr0uBnldj4m-GvNX2mzudLvG1rK4GmFk'
DISCORD_TOKEN='ODc5MzM5NjAzMDI5NTQ1MDEw.YSOS0g.V2R4sKrY0EhosFjQGYFaCO3OJtY'
DISCORD_GUILD='205482046062198785'
DISCORD_CHANNEL=473302835098943509
NOME_PLANILHA='Ranking x5 2.0.xlsx'
DATA_TAB='Ranking '

import pandas as pd
import discord
import sys

sys.path.append('./resources')

import data_format
import keep_alive
import pull_gsheet

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == DISCORD_GUILD:
            break

    print(
        f'{client.user} is connected to the following guild: ' 
        f'{guild.name} (id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$ranking'):
      data = pull_gsheet.pull_sheet_data(GSHEET_SCOPES,SPREADSHEET_ID,DATA_TAB)
      df = data_format.formatDF(pd.DataFrame(data=data))

      response = '. \n'
      response += 'RANKING DO 5X DA RAPAZIADA \n'
      response += 'TOP 1: ' + df['Invocador'].iloc[0] + '\n'
      response += 'TOP 2: ' + df['Invocador'].iloc[1] + '\n'
      response += 'TOP 3: ' + df['Invocador'].iloc[2] + '\n'
      response += 'O ranking do X5 está nesse link: '
      response += 'https://docs.google.com/spreadsheets/d/' + SPREADSHEET_ID + '/edit?usp=sharing'

      await message.channel.send(response)

    if message.content.startswith('$membrosonline'):
      data = pull_gsheet.pull_sheet_data(GSHEET_SCOPES,SPREADSHEET_ID,DATA_TAB)
      df = data_format.formatDF(pd.DataFrame(data=data)) 

      membros = client.get_channel(DISCORD_CHANNEL).members
        
      for membro in membros:
          name = str(membro.nick) if str(membro.nick) != 'None' else str(membro.name)
          if data_format.getPDL(name, df) != -1 and str(membro.status) != 'offline':
              await message.channel.send(name + ' - PDL: ' + str(data_format.getPDL(name, df)))

    if message.content.startswith('$tiratime'):
      data = pull_gsheet.pull_sheet_data(GSHEET_SCOPES,SPREADSHEET_ID,DATA_TAB)
      df = data_format.formatDF(pd.DataFrame(data=data))
      
      membros = client.get_channel(DISCORD_CHANNEL).members
      df_tiratime = pd.DataFrame(columns=['Invocador','PDL'])

      for membro in membros:
          name = str(membro.nick) if str(membro.nick) != 'None' else str(membro.name)
          if data_format.getPDL(name, df) != -1 and str(membro.status) != 'offline':
              df_tiratime = df_tiratime.append({'Invocador': name, 'PDL' : data_format.getPDL(name, df)}, ignore_index=True)

      df_tiratime = df_tiratime.sort_values(by='PDL', ascending=False).reset_index()
      print(df_tiratime)
      tamanho = len(df_tiratime)
      print(tamanho)
      if tamanho == 10:
          response = '. \n'
          response += 'TIME 1: \n'
          response += str(df_tiratime['Invocador'][0]) + ', ' + str(df_tiratime['Invocador'][tamanho -1]) + ', ' + str(df_tiratime['Invocador'][2]) + ', ' + str(df_tiratime['Invocador'][tamanho - 3]) + ', ' + str(df_tiratime['Invocador'][4]) + '\n'
          response += 'TOTAL DE PDL DO TIME 1 = '
          response += str(df_tiratime['PDL'][0] + df_tiratime['PDL'][tamanho -1] + df_tiratime['PDL'][2] + df_tiratime['PDL'][tamanho - 3] + df_tiratime['PDL'][4]) + '\n'
          response += 'TIME 2: \n'
          response += str(df_tiratime['Invocador'][1]) + ', ' + str(df_tiratime['Invocador'][tamanho -2]) + ', ' + str(df_tiratime['Invocador'][3]) + ', ' + str(df_tiratime['Invocador'][tamanho - 4]) + ', ' + str(df_tiratime['Invocador'][5]) + '\n'
          response += 'TOTAL DE PDL DO TIME 1 = '
          response += str(df_tiratime['PDL'][1] + df_tiratime['PDL'][tamanho -2] + df_tiratime['PDL'][3] + df_tiratime['PDL'][tamanho - 4] + df_tiratime['PDL'][5]) + '\n'
          await message.channel.send(response)
      else:
          response = 'Não existem 10 jogadores online na sala '+ client.get_channel(DISCORD_CHANNEL).name + ' ou o nick do discord não coincide com o da planilha.'
          await message.channel.send(response)

keep_alive.keep_alive()
client.run(DISCORD_TOKEN)