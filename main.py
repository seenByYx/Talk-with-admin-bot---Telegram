from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, ConversationHandler
from telegram.ext import filters
import json
import os

BOT_TOKEN = '' 
ADMIN_CHAT_ID = 

# Storage
message_links = {}
user_ids = set()
broadcast_waiting = {}  # track if admin is in broadcast mode

# --- Persistence ---
def save_users():
    with open("users.json", "w") as f:
        json.dump(list(user_ids), f)

def load_users():
    global user_ids
    if os.path.exists("users.json"):
        with open("users.json") as f:
            user_ids = set(json.load(f))

# --- Start ---
async def start(update: Update, context: CallbackContext):
    user_id = update.message.chat.id
    if user_id != ADMIN_CHAT_ID:
        user_ids.add(user_id)
        save_users()
    await update.message.reply_text("Welcome! Send me anything — I’ll forward it owner.")

# --- USER → ADMIN ---
async def handle_user_message(update: Update, context: CallbackContext):
    msg = update.message
    user_id = msg.chat.id
    user_ids.add(user_id)
    save_users()

    forwarded = await context.bot.forward_message(
        chat_id=ADMIN_CHAT_ID,
        from_chat_id=msg.chat.id,
        message_id=msg.message_id
    )
    message_links[forwarded.message_id] = user_id
    await msg.reply_text("Sent")

# --- ADMIN → USER ---
async def handle_admin_reply(update: Update, context: CallbackContext):
    msg = update.message

    # If admin is in broadcast mode
    if msg.chat.id == ADMIN_CHAT_ID and broadcast_waiting.get(ADMIN_CHAT_ID):
        await do_broadcast(update, context)
        broadcast_waiting[ADMIN_CHAT_ID] = False
        return

    # Normal reply mode
    if not msg.reply_to_message:
        return

    replied_id = msg.reply_to_message.message_id
    if replied_id not in message_links:
        await msg.reply_text("⚠️ Couldn't find which user this message belongs to.")
        return

    user_id = message_links[replied_id]

    # Forward text, media, sticker, etc.
    if msg.text:
        await context.bot.send_message(chat_id=user_id, text=msg.text)
    elif msg.photo:
        await context.bot.send_photo(chat_id=user_id, photo=msg.photo[-1].file_id)
    elif msg.video:
        await context.bot.send_video(chat_id=user_id, video=msg.video.file_id)
    elif msg.document:
        await context.bot.send_document(chat_id=user_id, document=msg.document.file_id)
    elif msg.voice:
        await context.bot.send_voice(chat_id=user_id, voice=msg.voice.file_id)
    elif msg.sticker:
        await context.bot.send_sticker(chat_id=user_id, sticker=msg.sticker.file_id)

    await msg.reply_text(".")

# --- BROADCAST SETUP ---
async def broadcast_command(update: Update, context: CallbackContext):
    if update.message.chat.id != ADMIN_CHAT_ID:
        await update.message.reply_text("🚫 You’re not authorized to use this command.")
        return
    broadcast_waiting[ADMIN_CHAT_ID] = True
    await update.message.reply_text("📢 Send the text or media you want to broadcast to all users.")

async def do_broadcast(update: Update, context: CallbackContext):
    msg = update.message
    sent_count = 0
    failed = 0

    for uid in user_ids:
        try:
            if msg.text:
                await context.bot.send_message(chat_id=uid, text=f"📢 *Announcement:*\n\n{msg.text}", parse_mode="Markdown")
            elif msg.photo:
                await context.bot.send_photo(chat_id=uid, photo=msg.photo[-1].file_id, caption="📢 Announcement")
            elif msg.video:
                await context.bot.send_video(chat_id=uid, video=msg.video.file_id, caption="📢 Announcement")
            elif msg.document:
                await context.bot.send_document(chat_id=uid, document=msg.document.file_id, caption="📢 Announcement")
            elif msg.sticker:
                await context.bot.send_sticker(chat_id=uid, sticker=msg.sticker.file_id)
            elif msg.voice:
                await context.bot.send_voice(chat_id=uid, voice=msg.voice.file_id)
            sent_count += 1
        except Exception as e:
            print(f"Failed to send to {uid}: {e}")
            failed += 1

    await update.message.reply_text(f"✅ Broadcast sent to {sent_count} users. ({failed} failed)")

# --- DONATE ---
async def donate(update: Update, context: CallbackContext):
    text = (
        "**Support this bot!**\n\n"
        "If you’d like to support its development or say thanks:\n\n"
        "📱 UPI: `yxseen.email@okhdfcbank`\n"
        "🌐 Razorpay: \n"
        "💬 Every small contribution helps keep it running!\n\n"
        "Thank you "
    )
    await update.message.reply_text(text, parse_mode="Markdown", disable_web_page_preview=True)

# --- MAIN ---
def main():
    load_users()
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("donate", donate))
    app.add_handler(CommandHandler("broadcast", broadcast_command))
    app.add_handler(MessageHandler(filters.Chat(ADMIN_CHAT_ID), handle_admin_reply))
    app.add_handler(MessageHandler(~filters.Chat(ADMIN_CHAT_ID), handle_user_message))

    app.run_polling()

if __name__ == "__main__":
    main()
