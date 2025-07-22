require("dotenv").config();
const { Client, GatewayIntentBits } = require("discord.js");

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
  ],
});

client.once("ready", () => {
  console.log(`Assistant is online as ${client.user.tag}`);
});

client.on("messageCreate", async (message) => {
  if (message.author.bot) return;

  const botMentioned =
    message.mentions.has(client.user) || message.content.startsWith("!ai");

  if (botMentioned) {
    try {
      const recentMessages = await message.channel.messages.fetch({
        limit: 30,
      });

      const chatHistory = [...recentMessages.values()]
      .reverse()
      .map((msg) => ({
        username: msg.author.username,
        content: msg.content,
        timestamp: msg.createdAt,
        id: msg.id,
      }));

      const payload = {
        userQuery: message.content,
        triggerUser: message.author.username,
        messages: chatHistory,
      };

      console.log("Sending to n8n:", payload);
      const res = await fetch(process.env.N8N_WEBHOOK_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error(`HTTP error ${res.status}`);

      const text = await res.text();
      console.log("Raw response text:", text);

      let data;
      try {
        data = JSON.parse(text);
        console.log("Parsed JSON:", data);
      } catch (e) {
        console.error("JSON parsing failed:", e.message);
        await message.channel.send("Backend response was not valid JSON.");
        return;
      }

      const reply = data?.summary || "No summary returned.";
      await message.channel.send(`${reply}`);
    } catch (error) {
      console.error("Error:", error.message);
      message.channel.send("AI Assistant ran into an error.");
    }
  }
});

client.login(process.env.DISCORD_BOT_TOKEN);
