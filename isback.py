from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes

SECHIMLER = {"0": "Taş 🪨", "1": "Kağıt 📄", "2": "Makas ✂️"}

# Aktif oyunları saklayan sözlük
aktif_oyunlar = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    
    if chat.type == "private":
        await update.message.reply_text(
            f"👋 Selam {user.first_name}!\n\n"
            "Ben Taş-Kağıt-Makas düello botuyum. Beni bir **grup sohbetine** ekleyip arkadaşlarınla "
            "karşılıklı oynamak için `/propango` komutunu gönderebilirsin! 🎮"
        )
        return

    chat_id = chat.id
    aktif_oyunlar[chat_id] = {}
    
    keyboard = [
        [
            InlineKeyboardButton("Taş 🪨", callback_data="0"),
            InlineKeyboardButton("Kağıt 📄", callback_data="1"),
            InlineKeyboardButton("Makas ✂️", callback_data="2"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎮 *Taş, Kağıt, Makas Düellosu Başladı!*\n\n"
        "İkiniz de aşağıdan seçiminizi yapın. Butonlar her hamleden sonra görünmeye devam edecek.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def buton_yakala(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = update.effective_chat.id
    user_id = query.from_user.id
    user_name = query.from_user.first_name
    secim = query.data
    
    if chat_id not in aktif_oyunlar:
        aktif_oyunlar[chat_id] = {}
        
    oyun = aktif_oyunlar[chat_id]
    
    if user_id in oyun:
        await query.answer("Zaten seçimini yaptın!", show_alert=True)
        return
        
    oyun[user_id] = (user_name, secim)
    await query.answer(f"Seçimin kaydedildi: {SECHIMLER[secim]}", show_alert=True)
    
    keyboard = [
        [
            InlineKeyboardButton("Taş 🪨", callback_data="0"),
            InlineKeyboardButton("Kağıt 📄", callback_data="1"),
            InlineKeyboardButton("Makas ✂️", callback_data="2"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if len(oyun) == 2:
        oyuncu_idleri = list(oyun.keys())
        p1_id, p2_id = oyuncu_idleri[0], oyuncu_idleri[1]
        
        p1_isim, p1_secim = oyun[p1_id]
        p2_isim, p2_secim = oyun[p2_id]
        
        p1_s = int(p1_secim)
        p2_s = int(p2_secim)
        
        if p1_s == p2_s:
            sonuc = "🤝 Maç Berabere!"
        elif (p1_s - p2_s) % 3 == 1:
            sonuc = f"🎉 Kazanan: *{p1_isim}*!"
        else:
            sonuc = f"🎉 Kazanan: *{p2_isim}*!"
            
        metin = (
            f"⚔️ *Düello Sonucu* ⚔️\n\n"
            f"👤 {p1_isim}: {SECHIMLER[p1_secim]}\n"
            f"👤 {p2_isim}: {SECHIMLER[p2_secim]}\n\n"
            f"{sonuc}"
        )
        
        del aktif_oyunlar[chat_id]
        
        await query.edit_message_text(text=metin, parse_mode="Markdown")
    else:
        oyuncular_listesi = ", ".join([v[0] for v in oyun.values()])
        await query.edit_message_text(
            text=f"🎮 *Taş, Kağıt, Makas Düellosu*\n\n"
                 f"✅ Oyunu Oynayanlar: *{oyuncular_listesi}*\n"
                 f"⏳ Diğer oyuncunun hamlesi bekleniyor...",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

def main():
    app = ApplicationBuilder().token("8869418228:AAEt4ey5nU8FkIOXudzc5F9UcTkZaoSN-eE").build()
    
    app.add_handler(CommandHandler("propango", start))
    app.add_handler(CallbackQueryHandler(buton_yakala))
    
    print("Bot /propango komutuyla çalışıyor...")
    app.run_polling()

if __name__ == "__main__":
    main()