import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = 'YOUR_BOT_TOKEN'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the University Materials Bot!\n\nUse /search <keyword> to find course materials.")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please enter a keyword.\nExample: `/search CS101`", parse_mode='Markdown')
        return

    keyword = ' '.join(context.args).lower()
    conn = sqlite3.connect('materials.db')
    c = conn.cursor()
    
    query = f"""
    SELECT title, drive_link FROM materials
    WHERE LOWER(title) LIKE ?
       OR LOWER(course) LIKE ?
    """
    c.execute(query, (f"%{keyword}%", f"%{keyword}%"))
    results = c.fetchall()
    conn.close()

    if not results:
        await update.message.reply_text("No materials found for your search.")
    else:
        for title, link in results:
            msg = f"📘 *{title}*\n🔗 [Download]({link})"
            await update.message.reply_text(msg, parse_mode='Markdown')

# Main application
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("search", search))
app.run_polling()
