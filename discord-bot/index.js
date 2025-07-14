require("dotenv").config();
const { Client, GatewayIntentBits } = require("discord.js");
const axios = require("axios");

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
  ],
});

client.once("ready", () => {
  console.log(`Bot is online as ${client.user.tag}`);
});

client.on("messageCreate", async (message) => {
  if (message.author.bot) return;

  const botMentioned =
    message.mentions.has(client.user) || message.content.startsWith("!ai");

  if (botMentioned) {
    try {
      const recentMessages = await message.channel.messages.fetch({
        limit: 20,
      });
      const chatHistory = [...recentMessages.values()]
        .reverse()
        .map((msg) => `${msg.author.username}: ${msg.content}`);

      const payload = {
        userQuery: message.content,
        triggerUser: message.author.username,
        messages: chatHistory,
      };

      console.log("Sending to n8n:", payload);

      const response = await axios.post(process.env.N8N_WEBHOOK_URL, payload);

      const reply = response?.data?.summary || "No summary returned.";
      await message.channel.send(`${reply}`);
    } catch (error) {
      console.error("Error:", error.message);
      message.channel.send("AI Assistant ran into an error.");
    }
  }
});

client.login(process.env.DISCORD_BOT_TOKEN);
