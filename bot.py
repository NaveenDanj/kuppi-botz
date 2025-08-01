import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Document
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("TOKEN")

# get user ids from @userinfobot
ADMINS = ['7709496043']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''Welcome to UniNotes — your personal hub for smarter studying!
    Organize, access, and manage all your university notes in one place.
    Whether you're prepping for exams, catching up on lectures, or collaborating with classmates — we’ve got you covered.

    🗂️ Upload and organize your notes by subject
    🔍 Search instantly across all your materials
    🤝 Share with peers and study better together

    Let’s make learning simpler. 🎯Type /help to get list of available commands.''')
    
    keyboard = [
        [InlineKeyboardButton("1st Year", callback_data='year1')],
        [InlineKeyboardButton("2nd Year", callback_data='year2')],
        [InlineKeyboardButton("3rd Year", callback_data='year3')],
        [InlineKeyboardButton("4th Year", callback_data='year4')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎓 Please select your current *year*:", 
                                    reply_markup=reply_markup, parse_mode='Markdown')



async def handle_year_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    year_selected = query.data.split('year')[1]
    context.user_data['year'] = year_selected

    keyboard = [
        [InlineKeyboardButton("Semester 1", callback_data='sem1')],
        [InlineKeyboardButton("Semester 2", callback_data='sem2')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        f"✅ Year {year_selected} selected. Now select your *semester*:",
        reply_markup=reply_markup, parse_mode='Markdown'
    )



async def handle_semester_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    semester_selected = query.data.split("sem")[1]
    context.user_data['semester'] = semester_selected
    year = context.user_data.get('year', '?')

    await query.edit_message_text(
        f"🎉 Setup complete!\nYou're in *Year {year}, Semester {semester_selected}*.\n\n"
        "You can now use commands like /search to find study materials.",
        parse_mode='Markdown'
    )



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📚 *UniNotes — Command Reference*

    🔹 `/start` — Begin setup and select your year and semester  
    🔹 `/help` — Show this help message  
    🔹 `/search <keyword>` — Search for any material by course code or title  
    🔹 `/notes <course>` — Get all notes for a course (e.g., `/notes CS101`)  
    🔹 `/papers <course>` — Get past papers for a course (e.g., `/papers CS101`)  

    ❗ *Make sure to use /start first to select your year and semester.*

    More features coming soon. Stay tuned! 🚀
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')
    

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



async def notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please specify the course code.\nExample: `/notes CS101` or /note Maths for computing", parse_mode='Markdown')
        return

    course = ' '.join(context.args).upper()

    conn = sqlite3.connect('materials.db')
    c = conn.cursor()

    year = context.user_data['year']
    semester = context.user_data['semester']
    
    query = """
    SELECT DISTINCT title, drive_link FROM materials
    WHERE UPPER(course) LIKE ? AND type = 'notes' AND year = ? AND semester = ?
    """
    like_pattern = f"%{course}%"
    c.execute(query, (like_pattern,year , semester))
    results = c.fetchall()
    conn.close()

    if not results:
        await update.message.reply_text(f"No notes found for course matching `{course}`.", parse_mode='Markdown')
        return

    for title, link in results:
        msg = f"📘 *{title}*\n🔗 [Download]({link})"
        await update.message.reply_text(msg, parse_mode='Markdown')




async def papers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please specify the course code.\nExample: `/papers CS101` or /note Maths for computing", parse_mode='Markdown')
        return

    course = ' '.join(context.args).upper()

    conn = sqlite3.connect('materials.db')
    c = conn.cursor()

    year = context.user_data['year']
    semester = context.user_data['semester']
    
    query = """
    SELECT DISTINCT title, drive_link FROM materials
    WHERE UPPER(course) LIKE ? AND type = 'papers' AND year = ? AND semester = ?
    """
    like_pattern = f"%{course}%"
    c.execute(query, (like_pattern,year , semester))
    results = c.fetchall()
    conn.close()

    if not results:
        await update.message.reply_text(f"No papers found for course matching `{course}`.", parse_mode='Markdown')
        return

    for title, link in results:
        msg = f"📘 *{title}*\n🔗 [Download]({link})"
        await update.message.reply_text(msg, parse_mode='Markdown')



async def ica(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please specify the course code.\nExample: `/ica CS101` or /note Maths for computing", parse_mode='Markdown')
        return

    course = ' '.join(context.args).upper()

    conn = sqlite3.connect('materials.db')
    c = conn.cursor()

    year = context.user_data['year']
    semester = context.user_data['semester']
    
    query = """
    SELECT DISTINCT title, drive_link FROM materials
    WHERE UPPER(course) LIKE ? AND type = 'papers' AND year = ? AND semester = ?
    """
    like_pattern = f"%{course}%"
    c.execute(query, (like_pattern,year , semester))
    results = c.fetchall()
    conn.close()

    if not results:
        await update.message.reply_text(f"No ICA found for course matching `{course}`.", parse_mode='Markdown')
        return

    for title, link in results:
        msg = f"📘 *{title}*\n🔗 [Download]({link})"
        await update.message.reply_text(msg, parse_mode='Markdown')



# ADMIN commands

async def add_material(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ADMINS:
        await update.message.reply_text("🚫 You are not authorized to use this command.")
        return

    if len(context.args) < 6:
        await update.message.reply_text(
            "⚠️ Usage:\n"
            "`/addmaterial <title> | <course> | <type> | <semester> | <year> | <drive_link>`",
            parse_mode='Markdown'
        )
        return

    data_str = ' '.join(context.args)
    parts = [part.strip() for part in data_str.split('|')]

    if len(parts) != 6:
        await update.message.reply_text(
            "❌ Invalid format.\n"
            "Use: `/addmaterial Title | CS101 | notes | 1 | Year 1 | https://drive...`",
            parse_mode='Markdown'
        )
        return

    title, course, type_, semester, year, drive_link = parts

    try:
        conn = sqlite3.connect('materials.db')
        c = conn.cursor()
        c.execute("""
            INSERT INTO materials (title, course, type, semester, year, drive_link)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, course, type_, semester, year, drive_link))
        conn.commit()
        conn.close()

        await update.message.reply_text("✅ Material added successfully.")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to add material: {e}")


async def upload_material_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMINS:
        await update.message.reply_text("❌ You are not authorized to perform this action.")
        return

    document: Document = update.message.document
    if not document or not document.file_name.endswith('.txt'):
        await update.message.reply_text("📄 Please upload a .txt file.")
        return

    file = await document.get_file()
    file_content = await file.download_as_bytearray()
    text = file_content.decode('utf-8')

    conn = sqlite3.connect('materials.db')
    c = conn.cursor()

    inserted = 0
    failed = 0

    for line in text.strip().splitlines():
        try:
            course, title, drive_link, material_type, year, semester = map(str.strip, line.split('|'))
            c.execute(
                "INSERT INTO materials (course, title, drive_link, type, year, semester) VALUES (?, ?, ?, ?, ?, ?)",
                (course.upper(), title, drive_link, material_type, int(year), int(semester))
            )
            inserted += 1
        except Exception as e:
            print(f"Failed to insert line: {line}, Error: {e}")
            failed += 1

    conn.commit()
    conn.close()

    await update.message.reply_text(f"✅ Inserted: {inserted} materials\n❌ Failed: {failed} lines")



# Main application
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_year_selection, pattern='^year'))
app.add_handler(CallbackQueryHandler(handle_semester_selection, pattern='^sem'))

app.add_handler(CommandHandler("search", search))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("notes", notes))
app.add_handler(CommandHandler("papers", papers))
app.add_handler(CommandHandler("addmaterial", add_material))
app.add_handler(CommandHandler("bulkupload", upload_material_file))
app.run_polling()
