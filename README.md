# Periodic-Metrics-Messenger-with-Python

The Periodic Metrics Messenger is a Python script designed to send periodic data summaries to a group of users. The script utilizes two messaging platforms, Slack and Telegram, to deliver important metrics updates. It analyzes the monthly trend of COVID-19 deaths in the top 3 states of the US using a provided COVID-19 dataset.

With Slack integration, the script delivers the data summary directly to a designated Slack channel using a webhook. This allows team members to receive real-time updates in a centralized workspace. In addition, the script utilizes the Telegram messaging platform to send the data summary to a specific Telegram group using Telegram Bot API.

Features
Fetches the required data from the COVID-19 dataset.
Performs monthly trend analysis of COVID-19 deaths for the top 3 states in the US.
Sends the data summary to a Slack channel using a webhook in fixed intervals
Sends the data summary to a Telegram group using the Telegram Bot API in fixed intervals
