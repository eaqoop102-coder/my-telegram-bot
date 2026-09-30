import os
import logging
from telegram import Update, ReactionTypeEmoji
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get('BOT_TOKEN')

async def auto_reply_and_react(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    
    try:
        await update.message.set_reaction(reaction=[ReactionTypeEmoji("👍")])
    except Exception as e:
        print(f"Error: {e}")

    # الردود التلقائية
    if "روكس" in text:
        await update.message.reply_text("عمك روكس")
    elif "منو حبيبك" in text or "من حبيبك" in text:
        await update.message.reply_text("روكسي👄")
    elif "سلام" in text or "السلام عليكم" in text:
        await update.message.reply_text("وعليكم السلام ورحمة الله وبركاته! نورت القروب ❤️")
    elif "القوانين" in text:
        await update.message.reply_text("📋 قوانين القروب:\n1. الاحترام المتبادل.\n2. يمنع الإعلانات والروابط.")

async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_status = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
    if user_status.status not in ['administrator', 'creator']:
        await update.message.reply_text("⚠️ هذا الأمر للأدمنية فقط!")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ يرجى الرد على رسالة الشخص المراد طرده.")
        return

    target_user = update.message.reply_to_message.from_user
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, target_user.id)
        await update.message.reply_text(f"❌ تم طرد المستخدم {target_user.full_name} بنجاح.")
    except Exception as e:
        await update.message.reply_text(f"فشل الطرد: تأكد أن البوت أدمن ولديه صلاحية الحظر.")

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(f"أهلاً وسهلاً بك {member.full_name} في القروب! 🌹")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("kick", kick_user))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply_and_react))

    print("البوت يعمل الآن...")
    app.run_polling()
  
