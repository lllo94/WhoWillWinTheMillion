import telebot
import random
import time
import threading
import os
from telebot import types

API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)

questions = [
    {"question": "ما هو أكبر كوكب في المجموعة الشمسية؟", "answers": ["الأرض", "المشتري", "المريخ", "الزهرة"], "correct": "المشتري"},
    {"question": "ما هي عاصمة فرنسا؟", "answers": ["برلين", "مدريد", "باريس", "روما"], "correct": "باريس"},
    {"question": "من هو أخطر هكر في العالم؟", "answers": ["سيزر", "كوز", "سايلنت", "هيمو"], "correct": "هيمو"},
    {"question": "ما هو العنصر الكيميائي الذي يرمز له بالرمز 'Au'؟", "answers": ["فضة", "ذهب", "نحاس", "حديد"], "correct": "ذهب"},
    {"question": "من هو مؤلف رواية '1984'؟", "answers": ["ألدوس هكسلي", "جورج أورويل", "مارجريت أتوود", "كازو إيشيجورو"], "correct": "جورج أورويل"},
    {"question": "ما هو أكبر المحيطات على الأرض؟", "answers": ["الأطلسي", "الهادي", "الهندي", "القطب الشمالي"], "correct": "الهادي"},
    {"question": "ما هو اسم الجبل الذي يقع بين آسيا وأوروبا؟", "answers": ["الهملايا", "الجبال الصخرية", "الألب", "الأورال"], "correct": "الأورال"},
    {"question": "ما هو العنصر الأكثر وفرة في القشرة الأرضية؟", "answers": ["الأكسجين", "الحديد", "السيليكون", "الألمنيوم"], "correct": "السيليكون"},
    {"question": "من هو مؤسس شركة مايكروسوفت؟", "answers": ["ستيف جوبز", "مارك زوكربيرج", "بيل غيتس", "لاري بيدج"], "correct": "بيل غيتس"},
    {"question": "ما هو العنصر الكيميائي الذي يرمز له بالرمز 'O'؟", "answers": ["أكسجين", "أرجون", "نيتروجين", "هيدروجين"], "correct": "أكسجين"},
    {"question": "ما هي أقدم جامعة في العالم؟", "answers": ["جامعة هارفارد", "جامعة القرويين", "جامعة أوكسفورد", "جامعة كامبريدج"], "correct": "جامعة القرويين"},
    {"question": "ما هو اسم أول إنسان سافر إلى الفضاء؟", "answers": ["نيل أرمسترونغ", "يوري غاغارين", "مايكل كولينز", "جوني كارسون"], "correct": "يوري غاغارين"},
    {"question": "ما هو أكبر كوكب قزم في النظام الشمسي؟", "answers": ["بلوتو", "سيريس", "ماكيماكي", "هاوميا"], "correct": "سيريس"},
    {"question": "من هو أول رئيس للولايات المتحدة الأمريكية؟", "answers": ["أبراهام لينكون", "جورج واشنطن", "توماس جيفرسون", "ثيودور روزفلت"], "correct": "جورج واشنطن"},
    {"question": "ما هو اسم أعظم شاعر إنجليزي في القرن السابع عشر؟", "answers": ["ويليام شكسبير", "جون ميلتون", "جورج جوردون", "كريستوفر مارلو"], "correct": "جون ميلتون"},
    {"question": "ما هو أصل الألوان في قوس قزح؟", "answers": ["تشتت الضوء", "انعكاس الضوء", "امتصاص الضوء", "تشبع الضوء"], "correct": "تشتت الضوء"},
    {"question": "ما هو اسم المحطة الفضائية التي تم بناؤها بواسطة التعاون الدولي؟", "answers": ["محطة مير", "محطة الفضاء الدولية", "محطة سكاي لاب", "محطة شينجيو"], "correct": "محطة الفضاء الدولية"},
    {"question": "من هو مكتشف قانون الجاذبية؟", "answers": ["ألبرت أينشتاين", "إسحاق نيوتن", "جاليليو جاليلي", "نيكولا تسلا"], "correct": "إسحاق نيوتن"},
    {"question": "ما هو العنصر الأكثر شيوعاً في الكون؟", "answers": ["الهيدروجين", "الهيليوم", "الأكسجين", "النيتروجين"], "correct": "الهيدروجين"},
    {"question": "ما هي أكبر مدينة من حيث عدد السكان في العالم؟", "answers": ["طوكيو", "شنغهاي", "نيويورك", "مومباي"], "correct": "طوكيو"},
    {"question": "من هو أول إنسان هبط على سطح القمر؟", "answers": ["نيل أرمسترونغ", "باز ألدرين", "مايكل كولينز", "يوري غاغارين"], "correct": "نيل أرمسترونغ"},
    {"question": "ما هو الحيوان الذي يعتبر أطول حيوان بري؟", "answers": ["الفيل", "الزرافة", "الحصان", "النمر"], "correct": "الزرافة"},
    {"question": "ما هو اسم أقرب كوكب إلى الشمس؟", "answers": ["عطارد", "الزهرة", "الأرض", "المريخ"], "correct": "عطارد"},
    {"question": "من هو مؤلف رواية 'موبي ديك'؟", "answers": ["هيرمان ملفيل", "مارك توين", "تشارلز ديكنز", "فيودور دوستويفسكي"], "correct": "هيرمان ملفيل"},
    {"question": "ما هو اسم أكبر صحراء باردة في العالم؟", "answers": ["صحراء ساهارا", "صحراء جوبى", "صحراء الأطلس", "الصحراء القطبية"], "correct": "الصحراء القطبية"},
    {"question": "ما هو اسم أصغر عظمة في جسم الإنسان؟", "answers": ["الركاب", "الصفيرة", "الجمجمة", "الساعد"], "correct": "الركاب"},
    {"question": "ما هو اسم أكبر محيط في الأرض؟", "answers": ["المحيط الهادي", "المحيط الأطلسي", "المحيط الهندي", "المحيط القطبي"], "correct": "المحيط الهادي"},
    {"question": "ما هي أكبر قارة من حيث المساحة؟", "answers": ["آسيا", "أفريقيا", "أوروبا", "أمريكا الشمالية"], "correct": "آسيا"},
    {"question": "ما هو اسم القارة التي تعرف باسم القارة السوداء؟", "answers": ["أفريقيا", "آسيا", "أوروبا", "أمريكا الجنوبية"], "correct": "أفريقيا"},
    {"question": "من هو الفنان الذي رسم لوحة 'الموناليزا'؟", "answers": ["ليوناردو دا فينشي", "ميخائيل أنجلو", "رافاييل", "فان جوخ"], "correct": "ليوناردو دا فينشي"},
    {"question": "ما هو اسم أصغر كوكب في المجموعة الشمسية؟", "answers": ["عطارد", "المريخ", "الأرض", "الزهرة"], "correct": "عطارد"},
    {"question": "ما هو اسم أول دولة حققت الاستقلال في أمريكا اللاتينية؟", "answers": ["الأرجنتين", "البرازيل", "كولومبيا", "تشيلي"], "correct": "الأرجنتين"},
    {"question": "من هو الكاتب الذي كتب 'الأخوة كارامازوف'؟", "answers": ["دوستويفسكي", "تولستوي", "غوركي", "تشايكوفسكي"], "correct": "دوستويفسكي"},
    {"question": "ما هو اسم الجبل الذي يقع بين قارة آسيا وقارة أوروبا؟", "answers": ["الهملايا", "الألب", "الأورال", "الجبال الصخرية"], "correct": "الأورال"},
    {"question": "ما هو اسم أول قمر صناعي أطلق إلى الفضاء؟", "answers": ["سبوتنيك 1", "أبولو 11", "هابل", "غاليليو"], "correct": "سبوتنيك 1"},
    {"question": "ما هو اسم أكبر بحيرة في العالم من حيث المساحة؟", "answers": ["بحيرة قزوين", "بحيرة فكتوريا", "بحيرة البحيرات الكبرى", "بحيرة تيتيكاكا"], "correct": "بحيرة قزوين"},
    {"question": "ما هو اسم أطول نهر في العالم؟", "answers": ["نهر النيل", "نهر الأمازون", "نهر اليانغتسي", "نهر المسيسيبي"], "correct": "نهر النيل"},
    {"question": "من هو أول إنسان صنع طائرة؟", "answers": ["الأخوان رايت", "تشارلز ليندبيرغ", "ليو دا فينشي", "غاغارين"], "correct": "الأخوان رايت"},
    {"question": "ما هو اسم أطول برج في العالم؟", "answers": ["برج خليفة", "برج إيفل", "برج شارد", "برج سي إن"], "correct": "برج خليفة"},
    {"question": "ما هو اسم أكبر حيوان بحري في العالم؟", "answers": ["الحوت الأزرق", "القرش الأبيض", "الحوت القاتل", "الأسد البحري"], "correct": "الحوت الأزرق"},
    {"question": "ما هو اسم أكبر حيوان على اليابسة؟", "answers": ["الفيل الإفريقي", "الزرافة", "الحوت الأزرق", "النمر"], "correct": "الفيل الإفريقي"},
    {"question": "ما هو اسم الأديب الذي كتب 'أوليفر تويست'؟", "answers": ["تشارلز ديكنز", "جورج أورويل", "مارك توين", "بيل غيتس"], "correct": "تشارلز ديكنز"},
    {"question": "ما هو اسم أعظم مؤلف موسيقي في التاريخ؟", "answers": ["بيتهوفن", "موتسارت", "باخ", "شوبرت"], "correct": "موتسارت"},
    {"question": "ما هو اسم أول قمر صناعي أمريكي أطلق إلى الفضاء؟", "answers": ["إكسبلورر 1", "سبوتنيك 1", "تلستار 1", "هابل"], "correct": "إكسبلورر 1"},
    {"question": "ما هو اسم أطول نهر في قارة أمريكا الجنوبية؟", "answers": ["نهر الأمازون", "نهر بارانا", "نهر أورينوكو", "نهر المسيسيبي"], "correct": "نهر الأمازون"},
    {"question": "ما هو اسم أول إنسان نجح في الصعود إلى قمة إيفرست؟", "answers": ["إدموند هيلاري", "تنزينج نورغاي", "راسل كيرك", "جورج مالوري"], "correct": "إدموند هيلاري"},
    {"question": "ما هو اسم أول جهاز كمبيوتر شخصي تم إنتاجه تجارياً؟", "answers": ["ألتير 8800", "أبل 1", "IBM PC", "كومودور 64"], "correct": "ألتير 8800"}
]

user_data = {}
message_ids = {}
user_stats = {}

# Paths to stats files
play_stats_file = "play_stats.txt"
win_stats_file = "win_stats.txt"

def save_stats():
    with open(play_stats_file, "w") as f:
        for chat_id, stats in user_stats.items():
            f.write(f"{chat_id}: {stats['plays']}\n")

    with open(win_stats_file, "w") as f:
        for chat_id, stats in user_stats.items():
            f.write(f"{chat_id}: {stats['wins']}\n")

def load_stats():
    """تحميل إحصائيات اللعب والفوز من الملفات النصية."""
    if os.path.exists(play_stats_file):
        with open(play_stats_file, "r") as f:
            for line in f:
                chat_id, plays = line.strip().split(": ")
                user_stats[int(chat_id)] = {"plays": int(plays), "wins": user_stats.get(int(chat_id), {}).get("wins", 0)}

    if os.path.exists(win_stats_file):
        with open(win_stats_file, "r") as f:
            for line in f:
                chat_id, wins = line.strip().split(": ")
                if int(chat_id) in user_stats:
                    user_stats[int(chat_id)]["wins"] = int(wins)

load_stats()

def send_reminder(chat_id):
    """إرسال رسالة تذكير بالوقت المتبقي كل 5 ثوانٍ."""
    user_info = user_data.get(chat_id)
    if user_info:
        current_time = time.time()
        time_elapsed = int(current_time - user_info['start_time'])
        time_remaining = max(0, 40 - time_elapsed)
        
        if time_remaining > 0:
            bot.send_message(chat_id, f"الوقت المتبقي: {time_remaining} ث")
            # جدولة التذكير التالي بعد 5 ثوانٍ
            threading.Timer(5, send_reminder, [chat_id]).start()
        else:
            # معالجة انتهاء الوقت
            bot.send_message(chat_id, "انتهى الوقت! دز /play و عيد اللعبة")
            del user_data[chat_id]
            del message_ids[chat_id]

def create_markup(chat_id):
    question = questions[user_data[chat_id]['question_index']]
    markup = types.InlineKeyboardMarkup()

    # أزرار الاختيارات
    for answer in question['answers']:
        markup.add(types.InlineKeyboardButton(answer, callback_data=answer))

    # زر عرض الرصيد
    markup.add(types.InlineKeyboardButton(f"فلوسك : {user_data[chat_id]['money']} دولار", callback_data='show_balance'))

    return markup

def create_message_text(chat_id):
    question = questions[user_data[chat_id]['question_index']]
    return question['question']

def send_question(chat_id, question_index):
    if not questions:  # تحقق إذا كانت قائمة الأسئلة فارغة
        bot.send_message(chat_id, "لا توجد أسئلة في القائمة.")
        return

    question = questions[question_index]
    markup = create_markup(chat_id)
    message_text = create_message_text(chat_id)
    
    if chat_id in message_ids and message_ids[chat_id]:
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_ids[chat_id],
                text=message_text,
                reply_markup=markup
            )
        except Exception as e:
            print(f"Error editing message: {e}")
    else:
        message = bot.send_message(chat_id, message_text, reply_markup=markup)
        message_ids[chat_id] = message.message_id
    
    # تعيين وقت بداية المؤقت
    user_data[chat_id]['start_time'] = time.time()
    
    # بدء إرسال تذكيرات الوقت
    send_reminder(chat_id)

def update_user_stats(chat_id, win):
    if chat_id not in user_stats:
        user_stats[chat_id] = {"plays": 0, "wins": 0}

    user_stats[chat_id]["plays"] += 1
    if win:
        user_stats[chat_id]["wins"] += 1

    save_stats()

# التعامل مع بدء التفاعل مع البوت
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    stats = user_stats.get(chat_id, {"plays": 0, "wins": 0})
    bot.send_message(message.chat.id, f"دز /play حته تلعب (تلعب اللعبة مو تلعب بي) \n عدد مرات اللعب: {stats['plays']}\nعدد مرات الفوز: {stats['wins']} \n ارسل /rules لرؤية القوانين \n -")

@bot.message_handler(commands=['play'])
def play(message):
    if not questions:  # تحقق إذا كانت قائمة الأسئلة فارغة
        bot.send_message(message.chat.id, "صيانة")
        return

    # اختيار سؤال عشوائي
    question_index = random.randint(0, len(questions) - 1)
    
    user_data[message.chat.id] = {
        'question_index': question_index,
        'money': 0,
        'start_time': time.time()  # تعيين وقت بداية المؤقت
    }
    update_user_stats(message.chat.id, False)  # زيادة عدد مرات اللعب
    send_question(message.chat.id, question_index)

# التعامل مع ضغط الأزرار
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    if chat_id not in user_data:
        bot.answer_callback_query(call.id, "دز /play حته تلعب لك.")
        return
    
    user_info = user_data[chat_id]
    question_index = user_info['question_index']
    selected_answer = call.data
    
    # تحقق من انتهاء الوقت
    current_time = time.time()
    if current_time - user_info['start_time'] > 40:
        bot.answer_callback_query(call.id, "انتهى الوقت!")
        bot.send_message(chat_id, "انتهى الوقت! دز /play و عيد اللعبة")
        del user_data[chat_id]
        del message_ids[chat_id]
        return
    
    if selected_answer == 'show_balance':
        # عرض الرصيد الحالي
        bot.answer_callback_query(call.id, f"فلوسك : {user_info['money']} دولار")
        return

    correct_answer = questions[question_index]['correct']
    
    if selected_answer == correct_answer:
        user_info['money'] += 100000
        bot.answer_callback_query(call.id, "عفية *بصوت صدام*")
        
        update_user_stats(chat_id, True)  
        
        # التحقق من الرصيد
        if user_info['money'] >= 1000000:
            bot.send_message(chat_id, f"مبروك كملت اللعبة")
            del user_data[chat_id]
            del message_ids[chat_id]
            return
        
        # اختيار سؤال عشوائي جديد
        next_question_index = random.randint(0, len(questions) - 1)
        user_info['question_index'] = next_question_index
        user_info['start_time'] = time.time()  # إعادة تعيين وقت بداية المؤقت
        send_question(chat_id, next_question_index)
    else:
        bot.answer_callback_query(call.id, "غلط")  # إشعار تفاعلي
        bot.send_message(chat_id, "دز /play و عيد اللعبة يا فاشل")
        del user_data[chat_id]
        del message_ids[chat_id]

# التعامل مع الأوامر الخاصة
@bot.message_handler(commands=['stats'])
def stats(message):
    chat_id = message.chat.id
    stats = user_stats.get(chat_id, {"plays": 0, "wins": 0})
    bot.send_message(
        chat_id,
        f"عدد مرات اللعب: {stats['plays']}\nعدد مرات الفوز: {stats['wins']}"
    )

@bot.message_handler(commands=['rules'])
def show_rules(message):
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("رجوع", callback_data='back'))
    bot.send_message(chat_id, "قوانين اللعبة:\n1. أجب على الأسئلة بشكل صحيح لتحصل على النقاط.\n2. إذا انتهى الوقت دون إجابة، سيتم إنهاء اللعبة.\n3. حاول جمع أكبر عدد من النقاط!", reply_markup=markup)

# التعامل مع الأزرار الداخلية
@bot.callback_query_handler(func=lambda call: call.data == 'back')
def back(call):
    bot.send_message(call.message.chat.id, "الرجوع للصفحة الرئيسية.")

# تشغيل البوت
bot.polling()

