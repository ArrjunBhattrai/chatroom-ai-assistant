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

  try {
    const storePayload = {
      message_id: message.id,
      username: message.author.username,
      channel: message.channel.name || "DM",
      message: message.content,
      timestamp: message.createdAt.toISOString(),
    };

    await fetch("http://localhost:8000/storeMessage", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(storePayload),
    });
  } catch (e) {
    console.error("Failed to send to /storeMessage:", e.message);
  }

  const botMentioned =
    message.mentions.has(client.user) || message.content.startsWith("!ai");

  if (botMentioned) {
    try {
      const recentMessages = await message.channel.messages.fetch({
        limit: 30,
      });

      const chatHistory = [...recentMessages.values()].reverse().map((msg) => ({
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

      // Format response nicely
      let replyParts = [];

      if (data.summary) {
        replyParts.push(`**Summary**:\n${data.summary}`);
      }
      if (data.tasks) {
        replyParts.push(`**Tasks**:\n${data.tasks}`);
      }
      if (data.questions) {
        replyParts.push(`**Questions**:\n${data.questions}`);
      }
      if (data.decisions) {
        replyParts.push(`**Decisions**:\n${data.decisions}`);
      }
      if (data.deadlines) {
        replyParts.push(`**Deadlines**:\n${data.deadlines}`);
      }
      if (data.mentions) {
        replyParts.push(`**Mentions**:\n${data.mentions}`);
      }
      if (data.followups) {
        replyParts.push(`**Follow-Ups**:\n${data.followups}`);
      }

      let reply = replyParts.join("\n\n");

      if (reply.length > 2000) {
        reply = reply.slice(0, 1990) + "\n...[truncated]";
      }

      await message.channel.send(reply || "No relevant info found.");
    } catch (error) {
      console.error("Error:", error.message);
      await message.channel.send("AI Assistant ran into an error.");
    }
  }
});

client.login(process.env.DISCORD_BOT_TOKEN);
