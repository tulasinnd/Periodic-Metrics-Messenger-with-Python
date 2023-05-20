import requests
import json
import pandas as pd
import calendar
import asyncio
from telegram import Bot

# Get top 3 states 
def summary(month,df):
    df['date'] = pd.to_datetime(df['date'])
    mask = df['date'].dt.month.isin([month])
    df=df[mask]
    states=df.groupby('state')
    top=states['deaths'].sum().sort_values(ascending=False).head(3) 
    top_df = top.to_frame()
    top_df.reset_index(inplace=True)
    top_df.columns = ['state', 'total_deaths']
    total=df['deaths'].sum()
    data_list = []
    for index, row in top_df.iterrows():
        l=index+1
        state = row['state']
        total_deaths = row['total_deaths']
        percentage = total_deaths / total * 100
        sublist = [l,state, total_deaths, percentage]
        data_list.append(sublist)
    return data_list

# Telegram
bot_token = '6220916841:AAEmwxRHlOoElCy20JlQT_UiCsTk_AX1KRY'
group_id = '-1001809283156'
async def send_summary_to_telegram(message):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=group_id, text=message)    

# Slack 
webhook_url = 'https://hooks.slack.com/services/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'    
def send_summary_to_slack(summary,month):
    try:
        attachments = []
        for i in summary:
            attachment = {
            'title': 'State# {0} {1}, {2} no of deaths, {3:.2f}% of total US deaths'.format(i[0], i[1], i[2], i[3])       
            }
            attachments.append(attachment)
        payload = {
            'text': f'Top 3 states in US with highest number of covid deaths for the month of {calendar.month_name[month]}\nMonth: {calendar.month_name[month]}',            
            'attachments': attachments }
        response = requests.post(webhook_url, data=json.dumps(payload),headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            print('Data summary sent to Slack successfully for the month',calendar.month_name[month])
        else:
            print('Failed to send data summary to Slack. Status code:', response.status_code)
    except Exception as e:
        print('An error occurred:', str(e))

# main function
if __name__ == '__main__':
    df=pd.read_csv(r"C:\Users\91939\OneDrive\Desktop\My Placement\Companies Applied\Guvi_Companies\Qure.ai_Data_Engineer\covid-19-state-level-data.csv", index_col=0)
    months=[3,4,5,6]
    async def main():
        for month in months:
            top3_states=summary(month,df)                  # get the top 3 states from dataframe
            final_message=''
            heading=f'Top 3 states in US with highest number of covid deaths for the month of {calendar.month_name[month]}\nMonth: {calendar.month_name[month]}\n'
            final_message=final_message+heading
            for j in top3_states:
                final_message= final_message+'State# {0} {1}, {2} no of deaths, {3:.2f}% of total US deaths\n'.format(j[0], j[1], j[2], j[3])
            await send_summary_to_telegram(final_message)  # send the message to telegram group      
            print('Data summary sent to Telegram successfully for the month ',calendar.month_name[month]) 
            send_summary_to_slack(top3_states,month)       # send the message to slack channel
            print('The next summary will be sent in 120 seconds\n')
            await asyncio.sleep(120) # periodic updates will be send for every 2 minutes          
    asyncio.run(main())
