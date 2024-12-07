import os
import json
import time
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import pytz
from datetime import datetime

TOKEN = '7378374058:AAH9opRuZfdgdAGDU97GiiNCMfOzdnjxIrs'
ADMIN_ID = [6343573113, 7371969470]
COOLDOWN_FILE = "cooldown.json"
PLAN_FILE = "plan.json"

COOLDOWN_TIME = 30

def list_admin_ids() -> list:
    admin_ids = []
    plan_data = load_json("plan.json")
    for item in plan_data:
        admin_ids.append(item["user_id"])
    return admin_ids



def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return {}

def save_json(data, file_path):
    with open(file_path, "w") as file:
        json.dump(data, file)

def check_user_plan(user_id):
    plan_data = load_json(PLAN_FILE)
    if user_id not in plan_data or plan_data[user_id]["banned"]:
        return False

    expiry_date = datetime.strptime(plan_data[user_id]["expiry"], "%Y-%m-%d %H:%M:%S")
    if datetime.now() > expiry_date:
        return False

    return True


async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in ADMIN_ID:
        await update.message.reply_text("Không Có Quyền Sử Dụng.")
        return

    if len(context.args) != 2:
        await update.message.reply_text("Cách Dùng: /add [id] [Số ngày]")
        return

    user_id = context.args[0]
    days = int(context.args[1])
    expiry_date = datetime.now() + timedelta(days=days)

    plan_data = load_json(PLAN_FILE)
    plan_data[user_id] = {
        "expiry": expiry_date.strftime("%Y-%m-%d %H:%M:%S"),
        "banned": False
    }
    save_json(plan_data, PLAN_FILE)

    await update.message.reply_text(f"Đã Cấp Quyền Cho User <code>{user_id}</code> trong <b>{days}</b> Days", parse_mode='HTML')
    
    user_text = f"Bạn đã được thêm vào danh sách được sử dụng /vip /stopvip với số ngày {days}\nCảm ơn đã ủng hộ!"
    try:
        await context.bot.send_message(chat_id=user_id, text=user_text)
    except Exception as e:
        print(f"Failed to send message to user {user_id}: {e}")


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in ADMIN_ID:
        await update.message.reply_text("Bạn Không Có Quyền Sử Dụng.")
        return

    if len(context.args) != 2:
        await update.message.reply_text("Cách Dùng: /add [id] [số ngày]")
        return

    user_id = context.args[0]
    days = int(context.args[1])
    expiry_date = datetime.now() + timedelta(days=days)

    plan_data = load_json(PLAN_FILE)
    plan_data[user_id] = {
        "expiry": expiry_date.strftime("%Y-%m-%d %H:%M:%S"),
        "banned": False
    }
    save_json(plan_data, PLAN_FILE)

    await update.message.reply_text(f"Đã Cấp Quyền Cho User <code>{user_id}</code> trong <b>{days}</b> Ngày",parse_mode='HTML')

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in ADMIN_ID:
        await update.message.reply_text("Bạn Không Có Quyền Sử Dụng.")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Cách Dùng: /ban [id]")
        return

    user_id = context.args[0]

    plan_data = load_json(PLAN_FILE)
    if user_id in plan_data:
        plan_data[user_id]["banned"] = True
        save_json(plan_data, PLAN_FILE)
        await update.message.reply_text(f"Đã ban user {user_id}.")
    else:
        await update.message.reply_text(f"User {user_id} Không Tồn Tại")

async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in ADMIN_ID:
        await update.message.reply_text("Bạn Không Có Quyền Sử Dụng.")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Cách Dùng: /unban [id]")
        return

    user_id = context.args[0]

    plan_data = load_json(PLAN_FILE)
    if user_id in plan_data:
        plan_data[user_id]["banned"] = False
        save_json(plan_data, PLAN_FILE)
        await update.message.reply_text(f"Đã unban user {user_id}.")
    else:
        await update.message.reply_text(f"User {user_id} Không Tồn Tại")
#bot_enabled = True
async def vip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    admin_id = '-4598829735' 
    if not check_user_plan(user_id):        
        await update.message.reply_text("Bạn Không Có Quyền Sử Dụng Bot\nVui Lòng Liên Hệ Admin Để Mua\n\nGiá Plan\n15K: Tuần\n30K: Tháng\nVĩnh Viễn: 100K\n Liên Hệ: @codondeptrai\nhoặc bạn có thể sử dụng lệnh /naptien để nạp mua plan vip tự động nhé")
        return 

    #if not bot_enabled:
 ##       await update.message.reply_text("Bot hiện đang offline. Vui lòng chờ admin bật bot lại.")
   #     return

#    cooldown_data = load_json(COOLDOWN_FILE)
 #   current_time = time.time()
#    cooldown_data = load_json(COOLDOWN_FILE)
 #   current_time = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
  

##  if user_id in cooldown_data and current_time.timestamp() - cooldown_data[user_id] < COOLDOWN_TIME:
  #      remaining_time = COOLDOWN_TIME - (current_time.timestamp() - cooldown_data[user_id])
   #     await   
 # if user_id in cooldown_data and current_time - cooldown_data[user_id] < COOLDOWN_TIME:

  #      remaining_time = COOLDOWN_TIME - (current_time - cooldown_data[user_id])


    if update.effective_chat.id != -1002177463101:
        await update.message.reply_text("lệnh chỉ hoạt động ở nhóm: https://t.me/natnetwork_123 .")
        return

    cooldown_data = load_json(COOLDOWN_FILE)
    current_time = time.time()
    if user_id in cooldown_data and current_time - cooldown_data[user_id] < COOLDOWN_TIME:
        remaining_time = COOLDOWN_TIME - (current_time - cooldown_data[user_id])
        await update.message.reply_text(f"Vui Lòng Chờ {int(remaining_time)} Giây Trước Khi Sử Dụng Lần Tiếp Theo")
        return
    if not bot_enabled:
        await update.message.reply_text("bot đã offline, chờ admin bật lại nhé")
        return
#f not bot_enabled:
#wait update.message.reply_text("Bot hiện đang offline. Vui lòng chờ admin bật lại")
#eturn
    if len(context.args) != 2:
        await update.message.reply_text("Cách Dùng: /vip [sdt] [số lần]")
        return

    phone_number = context.args[0]
    repeat_count = context.args[1]

    if not (phone_number.isdigit() and len(phone_number) == 10):
        await update.message.reply_text("Số Điện Thoại Phải Đủ 10 Số.")
        return


    try:
        repeat_count = int(repeat_count)
        if repeat_count > 10000:
            await update.message.reply_text("Số lần tối đa là 100. Vui lòng nhập số lần nhỏ hơn hoặc bằng 100.")
            return
    except ValueError:
        await update.message.reply_text("Số lần phải là số.")
        return

#    try:
 #       repeat_count = int(repeat_count)
  #  except ValueError:
   #     await update.message.reply_text("Số Lần Phải Là Con Số.")
 #       return
#
    cooldown_data[user_id] = current_time
    save_json(cooldown_data, COOLDOWN_FILE)

    command = f"screen -dm bash -c 'timeout 1000s python3 tlc.py {phone_number} {repeat_count}'"
    os.system(command)

    await update.message.reply_text(f"Thông Tin Tấn Công\n👾Plan: <b>Vip</b>\n📞Phone: <code>{phone_number}</code>\n⚡️Số Lần:  <b>{repeat_count}</b>\n⏳Delay: <b>20s</b>\n🔗Api: <b>100</b> ( MAX )\n📎Vòng Lặp: <b>1000</b> ( Mặc Định <b>1</b> | Max <b>10000</b> )", parse_mode='HTML')
    # Gửi thông tin số điện thoại và thông tin user đến admin
 #   # Gửi thông tin số điện thoại và thông tin user đến admin
  #  formatted_time = current_time.strftime('%d/%m/%Y %H:%M:%S')
#    await 
   # user_info = update.message.from_user
    #await context.bot.send_message(admin_id, f"Ngày: {formatted_time}\n Info Spam\n@{user_info.first_name} {user_info.last_name} (ID: {user_info.id})\nPlan: Vip\nPhone: {phone_number}\nConut: {repeat_count}")
   # user_info = update.message.from_user
    #await context.bot.send_message(admin_id, f"Inf Spam SMS\nUser: @{user_info.first_name}\nID: {user_info.last_name} (ID: {user_info.id})\nPhone: {phone_number}\nConut: {repeat_count}")
    user_info = update.message.from_user
    await context.bot.send_message(admin_id, f"Inf Spam SMS\nPlan: VIP\nUser: {user_info.first_name}\nID: {user_info.last_name} (ID: {user_info.id})\nPhone: {phone_number}\nConut: {repeat_count}")







#    user_info = update.message.from_user
 #   await context.bot.send_message(admin_id, f"Người dùng {user_info.first_name} {user_info.last_name} (ID: {user_info.id}) đã sử dụng lệnh /vip với số điện thoại: {phone_number}")


bot_enabled = True
async def spam(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    admin_id = '-4598829735'  # Thay 'admin_id_here' bằng id của admin
    cooldown_data = load_json(COOLDOWN_FILE)
    current_time = time.time()
    if user_id in cooldown_data and current_time - cooldown_data[user_id] < COOLDOWN_TIME:
        remaining_time = COOLDOWN_TIME - (current_time - cooldown_data[user_id])
        await update.message.reply_text(f"Vui Lòng Chờ {int(remaining_time)} Giây Trước Khi Sử Dụng.")
        return
    if not bot_enabled:
        await update.message.reply_text("Bot hiện đang offline. Vui lòng chờ admin bật bot lại.")
        return

#    if update.effective_chat.type != 'group':
  #      await update.message.reply_text("Lệnh này chỉ hoạt động trong nhóm.\n https://t.me/+fzo3QjDkxFA3ODk9")
 #       return
    if update.effective_chat.id != -1002177463101:
        await update.message.reply_text("Lệnh này chỉ hoạt động trong nhóm: https://t.me/natnetwork_123 .")
        return

    if len(context.args) != 2:
        await update.message.reply_text("Cách Dùng: /spam [sdt] [số lần]")
        return

    phone_number = context.args[0]
    repeat_count = context.args[1]

    if not (phone_number.isdigit() and len(phone_number) == 10):
        await update.message.reply_text("Số Điện Thoại Phải Đủ 10 Số.")
        return


    try:
        repeat_count = int(repeat_count)
        if repeat_count > 5:
            await update.message.reply_text("Số lần tối đa là 5. Vui lòng nhập số lần nhỏ hơn hoặc bằng 5.")
            return
    except ValueError:
        await update.message.reply_text("Số lần phải là số.")
        return


  #  try:
#        repeat_count = int(repeat_count)
 #       if repeat_count > 10:
   #         await update.message.reply_text("Số lần tối đa là 10. Vui lòng nhập số lần nhỏ hơn hoặc bằng 10.")
      #      return
    ##e#xcept ValueError:
        #await update.message.reply_text("Số lần phải là số.")
 #       return
#
  #  try:
#        repeat_count = int(repeat_count)
 # #  except ValueError:
    ##    await update.message.reply_text("Số Lần Phải Là Con Số.")
  #      return
##
    cooldown_data[user_id] = current_time
    save_json(cooldown_data, COOLDOWN_FILE)

    command = f"screen -dm bash -c 'timeout 250s python3 sms.py {phone_number} {repeat_count}'"
    os.system(command)

    await update.message.reply_text(f"Thông Tin Tấn Công\n👾Plan: <b>Free</b>\n📞Phone: <code>{phone_number}</code>\n⚡️Số Lần: <b>{repeat_count}</b>\n⏳Delay: <b>20s</b>\n🔗Api: <b>3x</b> ( MAX )\n📎Vòng Lặp: <b>10</b> ( Mặc Định <b>1</b> | Max <b>100</b> )", parse_mode='HTML')
    # Gửi thông tin số điện thoại và thông tin user đến admin
  #  user_info = update.message.from_user
###    await context.bot.send_message(admin_id, f"Info Spam {user_info.first_name} {user_info.last_name} (ID: {user_info.id})\nPlan: Free\nPhone: {phone_number}\nConut: {repeat_count}")
  #  user_info = update.message.from_user
#    await context.bot.send_message(admin_id, f"Inf Spam SMS\nUser: @{user_info.first_name}\nID: {user_info.last_name} (ID: {user_info.id})\nPhone: {phone_number}\nConut: {repeat_count}")
    user_info = update.message.from_user
    await context.bot.send_message(admin_id, f"Inf Spam SMS\nPlan: FREE\nUser: {user_info.first_name}\nID: {user_info.last_name} (ID: {user_info.id})\nPhone: {phone_number}\nConut: {repeat_count}")


bot_enabled = True

async def call(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    admin_id = '-4598829735'  # Thay 'admin_id_here' bằng id của admin
    cooldown_data = load_json(COOLDOWN_FILE)
    current_time = time.time()
    if user_id in cooldown_data and current_time - cooldown_data[user_id] < COOLDOWN_TIME:
        remaining_time = COOLDOWN_TIME - (current_time - cooldown_data[user_id])
        await update.message.reply_text(f"Vui Lòng Chờ {int(remaining_time)} Giây Trước Khi Sử Dụng.")
        return

    if not bot_enabled:
        await update.message.reply_text("Bot hiện đang offline. Vui lòng chờ admin bật bot lại.")
        return

    if update.effective_chat.id != -1002177463101:
        await update.message.reply_text("Lệnh này chỉ hoạt động trong nhóm: https://t.me/natnetwork_123 .")
        return
   # if update.effective_chat.type != 'group':
    #    await update.message.reply_text("Lệnh này chỉ hoạt động trong nhóm.\n https://t.me/+fzo3QjDkxFA3ODk9")
     #   return


    if len(context.args) != 2:
        await update.message.reply_text("Cách Dùng: /call [sdt] [số lần]")
        return

    phone_number = context.args[0]
    repeat_count = context.args[1]

    if not (phone_number.isdigit() and len(phone_number) == 10):
        await update.message.reply_text("Số Điện Thoại Phải Đủ 10 Số.")
        return



    try:
        repeat_count = int(repeat_count)
        if repeat_count > 5:
            await update.message.reply_text("Số lần tối đa là 5. Vui lòng nhập số lần nhỏ hơn hoặc bằng 5.")
            return
    except ValueError:
        await update.message.reply_text("Số lần phải là số.")
        return

#    try:
 #       repeat_count = int(repeat_count)
  #  except ValueError:
    #    await update.message.reply_text("Số Lần Phải Là Con Số.")
   #     return

    cooldown_data[user_id] = current_time
    save_json(cooldown_data, COOLDOWN_FILE)

    command = f"screen -dm bash -c 'timeout 250s python3 sms.py {phone_number} {repeat_count}'"
    os.system(command)

    await update.message.reply_text(f"Thông Tin Tấn Công\n👾Plan: <b>Free</b>\n📞Phone: <code>{phone_number}</code>\n⚡️Số Lần: <b>{repeat_count}</b>\n⏳Delay: <b>20s</b>\n🔗Api: <b>3x</b> ( MAX )\n📎Vòng Lặp: <b>10</b> ( Mặc Định <b>1</b> | Max <b>100</b> )", parse_mode='HTML')
    # Gửi thông tin số điện thoại và thông tin user đến admin
#    user_info = update.message.from_user
 #   await context.bot.send_message(admin_id, f"Info Spam {user_info.first_name} {user_info.last_name} (ID: {user_info.id})\nPlan: Free\nPhone: {phone_number}\nConut: {repeat_count}")
    user_info = update.message.from_user
    await context.bot.send_message(admin_id, f"Inf Spam SMS\nPlan: FREE\nUser: {user_info.first_name}\nID: {user_info.last_name} (ID: {user_info.id})\nPhone: {phone_number}\nConut: {repeat_count}")

bot_enabled = True

async def sms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    admin_id = '-4598829735'  # Thay 'admin_id_here' bằng id của admin
    cooldown_data = load_json(COOLDOWN_FILE)
    current_time = time.time()
    if user_id in cooldown_data and current_time - cooldown_data[user_id] < COOLDOWN_TIME:
        remaining_time = COOLDOWN_TIME - (current_time - cooldown_data[user_id])
        await update.message.reply_text(f"Vui Lòng Chờ {int(remaining_time)} Giây Trước Khi Sử Dụng.")
    if not bot_enabled:
        await update.message.reply_text("Bot hiện đang offline. Vui lòng chờ admin bật bot lại.")
        return

    #update.effective_chat.type != 'group':
      #  await update.message.reply_text("Lệnh này chỉ hoạt động trong nhóm.\n https://t.me/+fzo3QjDkxFA3ODk9")
     #   return

    #    return

    if update.effective_chat.id != -1002177463101:
        await update.message.reply_text("Lệnh này chỉ hoạt động trong nhóm: https://t.me/natnetwork_123 .")
        return

    if len(context.args) != 2:
        await update.message.reply_text("Cách Dùng: /sms [sdt] [số lần]")
        return

    phone_number = context.args[0]
    repeat_count = context.args[1]

    if not (phone_number.isdigit() and len(phone_number) == 10):
        await update.message.reply_text("Số Điện Thoại Phải Đủ 10 Số.")
        return

    try:
        repeat_count = int(repeat_count)
        if repeat_count > 5:
            await update.message.reply_text("Số lần tối đa là 5. Vui lòng nhập số lần nhỏ hơn hoặc bằng 5.")
            return
    except ValueError:
        await update.message.reply_text("Số lần phải là số.")
        return

 #   try:
   #     repeat_count = int(repeat_count)
  #  except ValueError:
#        await update.message.reply_text("Số Lần Phải Là Con Số.")
    #    return

    cooldown_data[user_id] = current_time
    save_json(cooldown_data, COOLDOWN_FILE)

    command = f"screen -dm bash -c 'timeout 250s python3 sms.py {phone_number} {repeat_count}'"
    os.system(command)

    await update.message.reply_text(f"Thông Tin Tấn Công\n👾Plan: <b>Free</b>\n📞Phone: <code>{phone_number}</code>\n⚡️Số Lần: <b>{repeat_count}</b>\n⏳Delay: <b>20s</b>\n🔗Api: <b>3x</b> ( MAX )\n📎Vòng Lặp: <b>10</b> ( Mặc Định <b>1</b> | Max <b>100</b> )", parse_mode='HTML')
    # Gửi thông tin số điện thoại và thông tin user đến admin
 #   user_info = update.message.from_user
#    await context.bot.send_message(admin_id, f"Info Spam {user_info.first_name} {user_info.last_name} (ID: {user_info.id})\nPlan: Free\nPhone: {phone_number}\nConut: {repeat_count}")
    user_info = update.message.from_user
    await context.bot.send_message(admin_id, f"Inf Spam SMS\nPlan: FREE\nUser: {user_info.first_name}\nID: {user_info.last_name} (ID: {user_info.id})\nPhone: {phone_number}\nConut: {repeat_count}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)

    all_commands = {
        "/id": "GET ID TELEGRAM",
        "/them": "Cộng thêm số ngày cho tất cả user id",
        "/sent": "Gửi thông báo đến một người dùng cụ thể bằng ID người dùng và nội dung",
        "/send": "Gửi nội dung tin nhắn đến tất cả user ID",
        "/add": "Thêm người dùng vào danh sách sử dụng lệnh /vip",
        "/ban": "xoá người dùng khỏi danh sách sử dụng lệnh /vip",
        "/unban": "xoá bỏ lệnh /ban và cho phép người dùng sử dụng lại lệnh /vip\n",

        "/vip": "Gửi tin nhắn sms - call cực nhanh đến số điện thoại và không giới hạn - VIP",
        "/spam": "Gửi tin nhắn spam đến số điện thoại cho số lần nhất định - FREE",
        "/call": "Gửi tin nhắn spam đến số điện thoại cho số lần nhất định - FREE",
        "/sms": "Gửi tin nhắn spam đến số điện thoại cho số lần nhất định - FREE",
        "/plan": "kiểm tra gói plan",
        "/check": "kiểm tra gói plan người khác bằng user id",
        "/uptime": "thời gian bot online",
        "/check": "danh sách tất cả user id đã mua gói plan /vip ",
        "/stop": "stop sdt plan free",
        "/stopvip": "stop sdt plan vip",
        "/list_ids": "check danh sách user id đã mua vip",
        "/naptien": "nạp tiền để mua plan vip tự động 100%"
    }  # Danh sách tất cả các lệnh và mô tả của chúng

    if len(context.args) > 0:
        command = context.args[0]
        if command in all_commands:
            await update.message.reply_text(f"<b>{command}</b>: {all_commands[command]}", parse_mode='HTML')
        else:
            await update.message.reply_text("Lệnh không hợp lệ. Vui lòng kiểm tra lại.")
    else:
        message = "Dưới đây là danh sách các lệnh của bot:\n\n"
        message += "<b>Tất cả các lệnh:</b>\n"
        for cmd, desc in all_commands.items():
            message += f"{cmd}: {desc}\n"

        await update.message.reply_text(message, parse_mode='HTML')


async def stdjart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("helo đây là tất cả lệnh\n/spam - spam sms - free\n/call - call and sms - free\n/sms - spam full sms - free\n/vip - spam maxspeed sms+call - có phí\n/plan - check plan\n/check - check plan người khác bằng id\n/stop - stop sdt\n/uptime - uptime bot\n/naptien - nạp tiền auto\n/list_ids - check list id plan vip\n\nMua Vip Liên Hệ: @codondeptrai | @quanganh207\n 30K THÁNG / 100K VĨNH VIỄN")

#  async def check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  #  active_phones = []
    
   # for session in asyncio.all_tasks():
    #    command = session.get_command()
      #  if command == "sms.py":
     #       args = session.get_args()
       ##     phone_number = args[ÊNx
         #   active_phones.append(phone_number)
    
   # if len(active_phones) == 0:
    #    await update.message.reply_text("Không có số điện thoại nào đang chạy spam.")
   # else:
     #   phone_list = "\n".join(active_phones)
    #    await update.message.reply_text(f"Danh sách số điện thoại đang chạy spam:\n{phone_list}")
#sync def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
 #   user_id = str(update.effective_user.id)

    # Kiểm tra xem người dùng có quyền dừng quá trình không
  #  if check_user_permissions(user_id):
   #     # Dừng file sms.py bằng lệnh kill
 #       os.system("pkill -f sms.py")
  #      await update.message.reply_text("Đã dừng quá trình gửi tin nhắn.")
#

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)

  #  cooldown_data = load_json(COOLDOWN_FILE)
   # current_time = time.time()
    #if user_id in cooldown_data and current_time - cooldown_data[user_id] < COOLDOWN_TIME:
   #     remaining_time = COOLDOWN_TIME - (current_time - cooldown_data[user_id])
  #      await update.message.reply_text(f"Vui LÃ²ng Chá» {int(remaining_time)} GiÃ¢y TrÆ°á»c Khi Sá»­ Dá»¥ng.")
    #    return

    if len(context.args) != 1:
        await update.message.reply_text("Cách Dùng: /stop [Số Điện Thoại]")
        return

    phone_number = context.args[0]

    if not (phone_number.isdigit() and len(phone_number) == 10):
        await update.message.reply_text("đủ 10 số.")
        return

    command = f"pkill -f sms.py"
    os.system(command)

    await update.message.reply_text(f"Stop Done | Phone: <code>{phone_number}</code>", parse_mode='HTML')

#async def list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
 #   admin_ids = list_admin_ids()
#   } if admin_ids:
  ##    admin_ids_str = "\n".join(str(id) for id in admin_ids)
  #}     await update.message.reply_text(f"Danh sách các user ID đã được thêm vào plan.json:\n{admin_ids_str}")
    #lse:
    #    await update.message.reply_text("Chưa có user ID nào được thêm vào plan.json.")


#async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
 #   user_id = str(update.effective_user.id)
#
 ##   # Kiểm tra xem người dùng có quyền truy cập danh sách người dùng không
   # if check_user_permissions(user_id):
    ##    user_ids = load_user_ids_from_file("plan.json")
      #  users_list = "\n".join(user_ids)
       ### await update.message.reply_text(f"Danh sách user ID đã được thêm vào plan.json:\n{users_list}")
     #   await update.message.reply_text("Bạn không có quyền truy cập danh sách người dùng.")

#ad_user_ids_from_file(file_path: str) -> List[str]:
    #try:
 # #      with open(file_path, "r") as file:
       ##     data = json.load(file)
  #          user_ids = [str(user_id) for user_id in data["users"]]
      #      return user_ids
    #pt FileNotFoundError:
     #   return []
    #cept json.JSONDecodeError:
     #   return []


#app.add_handler(CommandHandler("list", list))

#a#sync def plan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   # user_id = str(update.effective_user.id)
 #   
    #with open('plan.json', 'r') as file:
     #   plan_data = json.load(file)

    # user_id in plan_data:
     #   expiry_date = plan_data[user_id]["expiry"]
      ##  banned_status = plan_data[user_id]["banned"]
        #if banned_status:
         #   status = "Đã bị cấm"
        #lse:
           # status = "Chưa bị cấm"
        
        #it update.message.reply_text(f"Thông tin kế hoạch của bạn:\nExpiry: {expiry_date}\nTrạng thái: {status}")
    
    #    await update.message.reply_text("Không tìm thấy thông tin kế hoạch của bạn trong hệ thống.")


async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    
    with open('plan.json', 'r') as file:
        plan_data = json.load(file)

    if user_id in plan_data:
        expiry_date = plan_data[user_id]["expiry"]
        banned_status = plan_data[user_id]["banned"]
        if banned_status:
            status = "VIP ❌"
        else:
            status = "VIP ✅"
        
        await update.message.reply_text(f"Thông tin kế hoạch của bạn:\nID: {user_id}\nExpiry: {expiry_date}\nStatus: {status}")
    else:
        await update.message.reply_text("Thông tin kế hoạch của bạn: Không Có")

async def hcheck(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    user_input = ' '.join(context.args)

    if not user_input:
        await update.message.reply_text("Vui lòng nhập id của người dùng sau lệnh /check.")
        return

    if re.match(r'^@[\w]+$', user_input):
        user = await context.bot.get_chat(user_input)
        user_id = str(user.id)
    elif user_input.isdigit():
        user_id = user_input

    with open('plan.json', 'r') as file:
        plan_data = json.load(file)

    if user_id in plan_data:
        expiry_date = plan_data[user_id]["expiry"]
        banned_status = plan_data[user_id]["banned"]
        if banned_status:
            status = "VIP ❌"
        else:
            status = "VIP ✅"
        
        await update.message.reply_text(f"Thông tin kế hoạch của người dùng có id: {user_id}\nExpiry: {expiry_date}\nTrạng thái: {status}")
    else:
        await update.message.reply_text("Không tìm thấy thông tin kế hoạch của người dùng trong hệ thống.")



async def check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user_input = ' '.join(context.args)

    if not user_input:
        await update.message.reply_text("Vui lòng nhập id của người dùng sau lệnh /check.")
        return

    user_id = user_input

    with open('plan.json', 'r') as file:
        plan_data = json.load(file)

    if user_id in plan_data:
        expiry_date = plan_data[user_id]["expiry"]
        banned_status = plan_data[user_id]["banned"]
        if banned_status:
            status = "VIP ❌"
        else:
            status = "VIP ✅"
        
        await update.message.reply_text(f"Thông tin kế hoạch của người dùng có id: {user_id}\nExpiry: {expiry_date}\nTrạng thái: {status}")
    else:
        await update.message.reply_text("Không tìm thấy thông tin kế hoạch của người dùng trong hệ thống.")
start_time = datetime.now()
async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    current_time = datetime.now()
    uptime = current_time - start_time
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    await update.message.reply_text(f"STATUS - ONLINE ✅\nUP-TIME - BOT\n Giờ {hours}\n Phút: {minutes}\n Giây {seconds}")


#update.message.reply_text(f"Bot đã hoạt động được {hours} giờ {minutes} phút {seconds} giây.")



import random
import string
from telegram import Update
from telegram.ext import ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
import requests


async def naptien(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #update.message.chat.type != ChatType.PRIVATE:
      #  await update.message.reply_text(
     #       "Lệnh này chỉ có thể được sử dụng trong cuộc trò chuyện riêng với bot.\n"
 # #          "Vui lòng gửi lệnh /naptien trong tin nhắn riêng."
    #    )
  #      return

    if update.message.chat.type != 'private':
        await update.message.reply_text(
            "Lệnh này chỉ có thể được sử dụng trong tin nhắn riêng với bot."
        )
        return

    if len(context.args) != 2:
        await update.message.reply_text(
            "Vui lòng nhập đúng cú pháp: /naptien <số_tài_khoản_nạp> <số_tiền>\n"
            "Ví dụ: /naptien 0123456789 15000\nsố tài khoản nạp là số tài khoản của bạn nạp tiền lòng nhập đúng\n\nGiá Plan:\n15K - Tuần\n30K: - Tháng\n100K: Vĩnh Viễn\n\nhướng dẫn nạp tiền: https://t.me/feedbackvipplan/108"
        )
        return

    so_tai_khoan_nguoi_dung = context.args[0]
    so_tien = context.args[1]
    user_id = str(update.effective_user.id)

    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=7))

    noi_dung_nap_tien = f"{user_id}-{random_string}"

    tai_khoan_thu_huong = "0763270353"  
    ngan_hang_thu_huong = "MBBANK"  

    message = (
        f"Thông tin nạp tiền:\n"
   #     f"Số tiền: {so_tien} VNĐ\n"
       # f"Số tài khoản member yêu cầu nạp: {so_tai_khoan_nguoi_dung}\n\n"
       # f"Nội dung nạp tiền: {noi_dung_nap_tien}\n" 
      #  f"--------------------------------------------\n\n"
        f"Số tài khoản: {tai_khoan_thu_huong}\n"
        f"Nội dung nạp tiền: {noi_dung_nap_tien}\n"
        f"Số tiền: {so_tien} VNĐ\n"
#        f"Nội dung nạp tiền: {noi_dung_nap_tien}\n"
        f"Ngân hàng: {ngan_hang_thu_huong}\n\n"
        f"Vui lòng nạp đúng nội dung và số tiền để hệ thống auto duyệt sau 20s - 1 phút\n\n-Lưu Ý: vui lòng nạp tiền xong hãy bấm vào nút phía dưới để kiểm tra, nếu chưa nạp mà bấm trước sẽ bị lỗi, admin không hỗ trợ . vui lòng đọc kỹ hoặc xem video hướng dẫn: https://t.me/feedbackvipplan/109." 
    )

    keyboard = [
        [InlineKeyboardButton("bấm vào nút dưới đây nếu đã nạp tiền xong", callback_data=f"confirm_{user_id}_{so_tai_khoan_nguoi_dung}_{so_tien}_{noi_dung_nap_tien}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(message, reply_markup=reply_markup)






async def check_transaction(transaction_data):
    url = "https://api.dichvudark.vn/api/ApiMbBank"
    headers = {
        "Code": "rVejrvb6qt4NevN294ytu8P6NCz7q5JPEGVtEgWdPf64d36Tyy5jsSngPcefxHMkwsU2r2QDpacmhGRw3LTVrtwRxWJmvRvJuGZSdNs3YdXvVQRRu5tN3c8dZbC985bn5JTDaqnG24LWg7XN87SYwH9aQYMWeJcKeHaJ8fLKkPSG8daEr3ZNU3mKTrA9rbmMPJwELN5xjfTYSDJFYjHpNsYbCNbFFheZgEZmcgnXYUdXxFGUBK79pqhG9DJt3cvhf4aEbwaLK9bVQkRF3q4rPCnP9mfRKqrEvFYmjLfdvnpavqRUzaQp2dPUffNTVLXTDuPbqZ5HmBtPJ47sMP6nGAyg8AeSJ8zDBywuGQpwg9FVfrUA7LuyD4VLB3dVdUmjr7mvDj2bj7KdRZsRFdmUPruQkwYrmVzF889RfaQdjzdMhAbXMUjXcY3hTrSRAz26XSdkB3G9jn2aDk6gZC6HAUqx7JBahtE2k7uCyVpVLy5FScWeM7P8brcTSSaMcUdNgLzW8srFfwak6WB6XfJN6nEzn6Fj639AQWbFse7e3m3F4KfrwHaswPCj55ffdGkbcV4zEfm8YgwVvGMp3DXTqJSWhpsQmeV7krab37AxjvNp2qgVjGuhxLrnshgxSeQ69UYntgV3hgYzPJbCemwmsc3np2qENZFygEasmk7HqcVpAUHJHZfvUK5XWcKhKVTd32bZDkvXfMVVfPBewng6YVbzt368DW9SQe8rfcaZHfpMQgHnKYxenweP9vHXwcJU6f3aCPwt5cFGaBcg872fpbGZknMbD9chw4tKjfCCSXYbgr9BJF5dchS6DQdknjjUMbzaQnec3BNhYZV2jBmgULSa6fWcUmXEKRbcsvXWNSg8nfVhJ3e6BRrzV86hcTu9wz22hqTRedzgTDDVmtS5uRRmYNxWKSwWtep5ngELxZDKv3m8QVkyErGRZwksHUxxrbdfgcNGv5M6HaqzPNuXkcDXmjUDV3rqg5AKeDtteYxg4jqgtztRxrVqtpMYnR5UE2mpACER2QAW29LFm2Q6QvXr3W62QRsSVqSZeeENjJ7KAxu2m2GBMTH5zCnzVHCMm5eG64XAaJYxHLaxuK4HKUWahYa2NAAkaqy5kXJLkCPxrGcb4HrA9qgtkmdSk6HaPpsCae9pfPVK6UddGcHFuAPtNqMMFB9g9EXkLuCUhyQPKnBpYp4mkFYnzHXn4MSHAUr8QL5a3J29t4UgH4hJVSM348HREfmC8guGGbdBW8dPtr7vaP3CrLYhjCQEuVUXsasTY9UGskMtt2QL9e8qM6hFTHYQ8rR46Tbh7TMy2bMxCEQpbF3yMCxXytnL2tUwS5YVWNTExqr82KCCeQjmwk63uwZ2tb9wCmFZTpR82NLBB2PyjhGAth4vR5DaknqX7XaDX3wgnx5FJXxHfnCMNFuXBEkbNszAdwWE79EDGaqUntPRwzVGRXQHHE3sYG9H9PKNHWnU3QP7MBYCu4pMfp7hSD2HVZh46R4MMYJgv7Nn7dRwQQBTAmZgcjmNwa2uv3GbYaaxH3WrNfbN9pCr8YtqgsWpXW7DeEDSv7kmbb6yHBg3hadHF69u6s2NQDjrQfFSe95frF8YtTDRMjtU6LzQ9HWJW8myA83C2G4Myzb9X2cnD8Qg2PhnV8tuwAGwukbp5sxUu4Ej4jDbfvq7G4PjKZCFNEQqMBmSBSbBLe6MYKReHySGE9BdB9jS7aD4JLSQAhzJmzVKLGLKCpG7r5GBpp6TRmLCCdUeA6fb3Cyn93xJqJUrGFBEmP43fxJvQS6rkVBHBnG9d6XZYXN5bSazV7uFG27Nu9y4hQpMJ54hMVRNsDGrV6hjeQDtmDRVVYJLrDkhPsgvEQ3DvePBWVVrXeeSrEq2mp7KuJt5zEzgGSbvPubdVnELqp7zb7tujyZDG3Fc4jEBwV6JHwA34KdAvVqu9kmqdEkKWGJKftFeSTuVNgyDXh2fJLnhtF28s7xVumyqYyzNVRjTCG8e3yag8hTc3UhPFUyfatSGYeEP8mBsDRtekAgBTymnAMTR",
        "Token": "rstmNHAVyheidLlSOGfRcMXFaxIujCbYZvQEJUKpkqoWgDzTPBnw",
        "Stk": "0763270353"
    }

    data_post = {
        "Loai_api": "lsgdv2"
    }

    try:
        response = requests.post(url, data=data_post, headers=headers, verify=False)
        if response.status_code == 200:
            response_data = response.json()
            transaction_history = response_data.get("transactionHistoryList", [])
            for transaction in transaction_history:
                if (transaction["creditAmount"] == transaction_data["so_tien"] and 
                    transaction_data["noi_dung_nap_tien"].lower() in transaction["description"].lower()):
                    return True, transaction  
        return False, None  
    except Exception as e:
        print(f"Error in check_transaction: {str(e)}")
        return False, None

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data.split('_')
    user_id = data[1]
    so_tai_khoan = data[2]
    so_tien = data[3]
    noi_dung_nap_tien = data[4]

    file_name = f"{user_id}_nap.json"
    nap_data = {
        "user_id": user_id,
        "so_tai_khoan": so_tai_khoan,
        "so_tien": so_tien,
        "noi_dung_nap_tien": noi_dung_nap_tien,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(nap_data, f, ensure_ascii=False, indent=4)

    await query.edit_message_text(text="Đang kiểm tra giao dịch...\nVui lòng chờ trong giây lát !\nHệ thống có thể mất 3-5 phút để kiểm tra giao dịch")

    task = asyncio.create_task(check_and_notify(update, context, query, nap_data))
    await task


async def check_and_notify(update, context, query, nap_data):
    max_checks = 10  
    check_count = 0  

    admin_id = "-4727809242"  

    while check_count < max_checks:
        await asyncio.sleep(10)

        is_valid, transaction_info = await check_transaction(nap_data)

        if is_valid:
            so_tien = int(nap_data["so_tien"])
            if so_tien == 15000:
                added_days = 7
            elif so_tien == 30000:
                added_days = 30
            elif so_tien == 100000:
                added_days = 9824
            else:
                added_days = 0  

            file_name = "plan.json"
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    plans = json.load(f)
            except FileNotFoundError:
                plans = {}

            user_id = nap_data["user_id"]
            current_plan = plans.get(user_id)

            if current_plan:
                expiry_date = datetime.strptime(current_plan["expiry"], "%Y-%m-%d %H:%M:%S")
                new_expiry = expiry_date + timedelta(days=added_days)
                current_plan["expiry"] = new_expiry.strftime("%Y-%m-%d %H:%M:%S")
            else:
                new_expiry = datetime.now() + timedelta(days=added_days)
                plans[user_id] = {
                    "expiry": new_expiry.strftime("%Y-%m-%d %H:%M:%S"),
                    "banned": False
                }

            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(plans, f, ensure_ascii=False, indent=4)

            message = f"Giao dịch hợp lệ!\n\nThông tin giao dịch:\n{json.dumps(transaction_info, indent=4)}\n\n"
            message += f"Bạn đã được cộng {added_days} ngày vào plan của mình\nvà có quyền sử dụng lệnh /vip."

            await query.edit_message_text(text=message)

            admin_message = f"Người dùng {user_id} đã nạp thành công {so_tien} VND.\n"
            admin_message += f"Số ngày đã cộng vào kế hoạch: {added_days}\n"
            admin_message += f"Thông tin giao dịch: {json.dumps(transaction_info, indent=4)}"

            await send_message_to_admin(update, context, -4727809242, admin_message)

            return  

        check_count += 1  

    await query.edit_message_text(text="Không tìm thấy giao dịch hợp lệ.\nVui lòng liên hệ ADMIN để được giải quyết")

async def send_message_to_admin(update, context, admin_id, message):
    await context.bot.send_message(chat_id=admin_id, text=message)


#async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
 #   query = update.callback_query
  #  await query.answer()
#
 #  data = query.data.split('_')
#}  user_id = data[1]
  # }so_tai_khoan = data[2]
 #  #s#o_tien = data[3]
   # no}i_dung_nap_tien = data[
    #file_name = f"{user_id}_nap.json"
   # nap_data = {
     #   "user_id": user_id,
      ##"so_tai_khoan": so_tai_khoan,
        #"so_tien": so_tien,
       ## "noi_dung_nap_tien": noi_dung_nap_tien,
       #timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    

    #ith open(file_name, 'w', encoding='utf-8') as f:
    #    json.dump(nap_data, f, ensure_ascii=False, indent=4)

 #   await query.edit_message_text(text="Đang kiểm tra giao dịch...\nVui lòng chờ trong giây lát !\nHệ thống có thể mất 3-5 phút để kiểm tra giao dịch")
#
  #ask = asyncio.create_task(check_and_notify(query, nap_data))
  #  await task

#c def check_and_notify(query, nap_data):
    #x_checks = 10  
 #  ## check_count = 0  

  ##  while check_count < max_checks:

     ##   await asyncio.sleep(10)
#
       ## is_valid, transaction_info = await check_transaction(nap_data)
###
   ##     if is_valid:

     #       so_tien = int(nap_data["so_tien"])
      #      if so_tien == 15000:
       #         added_days = 7
        #    elif so_tien == 30000:
         #       added_days = 30
          #  elif so_tien == 100000:
           #     added_days = 730
            #else:
#               added_days = 0  
#
  #}          file_name = "plan.json"
  #        try:
 #               with open(file_name, 'r', encoding='utf-8') as f:
     #               plans = json.load(f)
  ###          except FileNotFoundError:
   ##             plans = {}  
#
 #           user_id = nap_data["user_id"]
      #      current_plan = plans.get(user_id)
#
    #        if current_plan:
###
   #             expiry_date = datetime.strptime(current_plan["expiry"], "%Y-%m-%d %H:%M:%S")
     #           new_expiry = expiry_date + timedelta(days=added_days)
      #          current_plan["expiry"] = new_expiry.strftime("%Y-%m-%d %H:%M:%S")
       #     else:
###}
     #           new_expiry = datetime.now() + timedelta(days=added_days)
 #### #              plans[user_id] = {
      #              "expiry": new_expiry.strftime("%Y-%m-%d %H:%M:%S"),
  ###  #                "banned": False
    ####   #         }
##
 #####           with open(file_name, 'w', encoding='utf-8') as f:
       #         json.dump(plans, f, ensure_ascii=False, indent=4)
##
 ##     #      message = f"Giao dịch hợp lệ!\n\nThông tin giao dịch:\n{json.dumps(transaction_info, indent=4)}\n\n"
   #      #   message += f"Bạn đã được cộng {added_days} ngày vào plan của mình.\n/plan để check nhé."
###
 #           await query.edit_message_text(text=message)
    #        return  

     #   check_count += 1  

    #wait query.edit_message_text(text="Không tìm thấy giao dịch hợp lệ.\nVui lòng liên hệ ADMIN @condondeptrai để được giải quyết")




async def vip1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    admin_id = '-4598829735' 
    if not check_user_plan(user_id):
        await update.message.reply_text("Bạn Không Có Quyền Sử Dụng\n Mua Inbox @codondeptrai : 30K Tháng / 100K Vĩnh Viễn")
        return   

##  if user_id in cooldown_data and current_time.timestamp() - cooldown_data[user_id] < COOLDOWN_TIME:
  #      remaining_time = COOLDOWN_TIME - (current_time.timestamp() - cooldown_data[user_id])
   #     await   
 # if user_id in cooldown_data and current_time - cooldown_data[user_id] < COOLDOWN_TIME:
  #      remaining_time = COOLDOWN_TIME - (current_time - cooldown_data[user_id])
    cooldown_data = load_json(COOLDOWN_FILE)
    current_time = time.time()
    if user_id in cooldown_data and current_time - cooldown_data[user_id] < COOLDOWN_TIME:
        remaining_time = COOLDOWN_TIME - (current_time - cooldown_data[user_id])
        await update.message.reply_text(f"Vui Lòng Chờ {int(remaining_time)} Giây Trước Khi Sử Dụng Lại Lần Tiếp Theo")
        return

    if len(context.args) != 2:
        await update.message.reply_text("Cách Dùng: /vip1 [sdt] [Số Lần]")
        return

    phone_number = context.args[0]
    repeat_count = context.args[1]

    if not (phone_number.isdigit() and len(phone_number) == 10):
        await update.message.reply_text("Số Điện Thoại Phải Đủ 10 SỐ.")
        return

    try:
        repeat_count = int(repeat_count)
    except ValueError:
        await update.message.reply_text("Số lần phải là con số.")
        return

    cooldown_data[user_id] = current_time
    save_json(cooldown_data, COOLDOWN_FILE)

    command = f"screen -dm bash -c 'timeout 650s python3 vip1.py {phone_number} {repeat_count}'"
    os.system(command)

    await update.message.reply_text(f"Thông Tin Tấn Công\n👾Plan: <b>Vip</b>\n📞Phone: <code>{phone_number}</code>\n⚡️Số Lần:  <b>{repeat_count}</b>\n⏳Delay: <b>20s</b>\n🔗Api: <b>1xx</b> ( MAX )\n📎Vòng Lặp: <b>1000</b> ( Mặc Định <b>1</b> | Max <b>10000</b> )", parse_mode='HTML')
   # user_info = update.message.from_user
    #await context.bot.send_message(admin_id, f"NgÃ y: {formatted_time}\n Info Spam\n@{user_info.first_name} {user_info.last_name} (ID: {user_info.id})\nPlan: Vip\nPhone: {phone_number}\nConut: {repeat_count}")
   # user_info = update.message.from_user
    #await context.bot.send_message(admin_id, f"Inf Spam SMS\nUser: @{user_info.first_name}\nID: {user_info.last_name} (ID: {user_info.id})\nPhone: {phone_number}\nConut: {repeat_count}")
    user_info = update.message.from_user
    await context.bot.send_message(admin_id, f"Inf Spam SMS\nPlan: VIP\nUser: {user_info.first_name}\nID: {user_info.last_name} (ID: {user_info.id})\nPhone: {phone_number}\nConut: {repeat_count}")

async def vip2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    admin_id = '-4598829735' 
    if not check_user_plan(user_id):
        await update.message.reply_text("Bạn Không Có Quyền Sử Dụng\n Mua Inbox @codondeptrai : 30K Tháng / 100K Vĩnh Viễn")
        return   

##  if user_id in cooldown_data and current_time.timestamp() - cooldown_data[user_id] < COOLDOWN_TIME:
  #      remaining_time = COOLDOWN_TIME - (current_time.timestamp() - cooldown_data[user_id])
   #     await   
 # if user_id in cooldown_data and current_time - cooldown_data[user_id] < COOLDOWN_TIME:
  #      remaining_time = COOLDOWN_TIME - (current_time - cooldown_data[user_id])
    cooldown_data = load_json(COOLDOWN_FILE)
    current_time = time.time()
    if user_id in cooldown_data and current_time - cooldown_data[user_id] < COOLDOWN_TIME:
        remaining_time = COOLDOWN_TIME - (current_time - cooldown_data[user_id])
        await update.message.reply_text(f"Vui Lòng Chờ {int(remaining_time)} Giây Trước Khi Sử Dụng Lại Lần Tiếp Theo")
        return

    if len(context.args) != 2:
        await update.message.reply_text("Cách Dùng: /vip2 [sdt] [Số Lần]")
        return

    phone_number = context.args[0]
    repeat_count = context.args[1]

    if not (phone_number.isdigit() and len(phone_number) == 10):
        await update.message.reply_text("Số Điện Thoại Phải Đủ 10 SỐ.")
        return

    try:
        repeat_count = int(repeat_count)
    except ValueError:
        await update.message.reply_text("Số lần phải là con số.")
        return

    cooldown_data[user_id] = current_time
    save_json(cooldown_data, COOLDOWN_FILE)

    command = f"screen -dm bash -c 'timeout 650s python3 vip2.py {phone_number} {repeat_count}'"
    os.system(command)

    await update.message.reply_text(f"Thông Tin Tấn Công\n👾Plan: <b>Vip</b>\n📞Phone: <code>{phone_number}</code>\n⚡️Số Lần:  <b>{repeat_count}</b>\n⏳Delay: <b>20s</b>\n🔗Api: <b>1xx</b> ( MAX )\n📎Vòng Lặp: <b>1000</b> ( Mặc Định <b>1</b> | Max <b>10000</b> )", parse_mode='HTML')
   # user_info = update.message.from_user
    #await context.bot.send_message(admin_id, f"NgÃ y: {formatted_time}\n Info Spam\n@{user_info.first_name} {user_info.last_name} (ID: {user_info.id})\nPlan: Vip\nPhone: {phone_number}\nConut: {repeat_count}")
   # user_info = update.message.from_user
    #await context.bot.send_message(admin_id, f"Inf Spam SMS\nUser: @{user_info.first_name}\nID: {user_info.last_name} (ID: {user_info.id})\nPhone: {phone_number}\nConut: {repeat_count}")
    user_info = update.message.from_user
    await context.bot.send_message(admin_id, f"Inf Spam SMS\nPlan: VIP\nUser: {user_info.first_name}\nID: {user_info.last_name} (ID: {user_info.id})\nPhone: {phone_number}\nConut: {repeat_count}")

async def list_ids(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    with open('plan.json', 'r') as file:
        plan_data = json.load(file)

    if not plan_data:
        await update.message.reply_text("Không có ID nào được thêm vào plan.json")
        return

    message = "Danh Sách ID Và Số Ngày Còn Lại Của GÓI VIP:\n"
    for user_id, data in plan_data.items():
        expiry_date = data["expiry"]
        message += f"ID: {user_id}, Số ngày: {expiry_date}\n"

    await update.message.reply_text(message)



async def them(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    admin_id = "5145402317"  

    if user_id != admin_id:
        await update.message.reply_text("Bạn không có quyền sử dụng lệnh này.")
        return

    if len(context.args) < 1:
        await update.message.reply_text("Cách dùng: /add [số ngày]")
        return

    try:
        days_to_add = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Số ngày phải là một số nguyên.")
        return

    try:
        with open('plan.json', 'r') as file:
            plan_data = json.load(file)
        
        for user_id, plan_info in plan_data.items():
            plan_info['expiry_date'] += datetime.timedelta(days=days_to_add)

        with open('plan.json', 'w') as file:
            json.dump(plan_data, file, indent=4)

        await update.message.reply_text(f"Đã cộng thêm {days_to_add} ngày cho tất cả user trong plan.json")

    except Exception as e:
        await update.message.reply_text("Không thể cộng thêm ngày cho plan.json. Lỗi: {}".format(str(e)))

async def sent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    admin_ids = ["6343573113", "6343573113"]  # Thay đổi để định nghĩa user_id của admin

    user_id = str(update.effective_user.id)

    if user_id not in admin_ids:
        await update.message.reply_text("Chỉ admin mới có quyền sử dụng chức năng này.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("Cách dùng: /sent [ID người dùng] [nội dung tin nhắn]")
        return

    target_user_id = context.args[0]
    message = " ".join(context.args[1:])

    try:
        await context.bot.send_message(chat_id=int(target_user_id), text=message)
        await update.message.reply_text("Thông báo đã được gửi đến người dùng có ID: {}".format(target_user_id))
    except Exception as e:
        await update.message.reply_text("Không thể gửi thông báo đến người dùng có ID: {}. Lỗi: {}".format(target_user_id, str(e)))

async def send(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)

    if user_id != "6343573113":  # Thay "1234567890" bằng user ID của admin
        await update.message.reply_text("Chỉ admin mới có quyền sử dụng chức năng này.")
        return

    if not check_user_plan(user_id):
        await update.message.reply_text("Bạn không có quyền sử dụng bot hoặc plan đã hết hạn.")
        return

    if len(context.args) < 1:
        await update.message.reply_text("Cách dùng: /send [nội dung tin nhắn]")
        return

    message = " ".join(context.args)

    try:
        with open('plan.json', 'r') as file:
            plan_data = json.load(file)
        
        for user_id in plan_data:
            try:
                await context.bot.send_message(chat_id=user_id, text=message)
            except Exception as e:
                print(f"Lỗi khi gửi tin nhắn cho user ID {user_id}: {str(e)}")

        await update.message.reply_text("Thông báo đã được gửi đến tất cả user ID trong plan.json")
    
    except Exception as e:
        await update.message.reply_text("Không thể đọc tệp plan.json. Lỗi: {}".format(str(e)))

async def stopvip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)

    if not check_user_plan(user_id):
        await update.message.reply_text("Chỉ Người Dùng Vip Mới Có Thể Sử Dụng")
        return   

  #  cooldown_data = load_json(COOLDOWN_FILE)
   # current_time = time.time()
    #if user_id in cooldown_data and current_time - cooldown_data[user_id] < COOLDOWN_TIME:
   #     remaining_time = COOLDOWN_TIME - (current_time - cooldown_data[user_id])
  #      await update.message.reply_text(f"Vui LÃÂ²ng ChÃ¡Â»Â {int(remaining_time)} GiÃÂ¢y TrÃÂ°Ã¡Â»Âc Khi SÃ¡Â»Â­ DÃ¡Â»Â¥ng.")
    #    return

    if len(context.args) != 1:
        await update.message.reply_text("Cách Dùng: /stop [Số điện thoại]")
        return

    phone_number = context.args[0]

    if not (phone_number.isdigit() and len(phone_number) == 10):
        await update.message.reply_text("Số Điện Thoại Phải Đủ 10 Số")
        return

    command = f"pkill -f tlc.py"
    os.system(command)

    await update.message.reply_text(f"Stop Done | Phone: <code>{phone_number}</code>", parse_mode='HTML')



async def off(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    admin_id = '6343573113'  # Thay 'admin_id_here' bằng id của admin

    if str(update.effective_user.id) != admin_id:
        await update.message.reply_text("Bạn không có quyền sử dụng lệnh này.")
        return
    
    global bot_enabled
    bot_enabled = False
    await update.message.reply_text("Bot đã được tắt.")


async def on(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    admin_id = '6343573113'  # Thay 'admin_id_here' bằng id của admin

    if str(update.effective_user.id) != admin_id:
        await update.message.reply_text("Bạn không có quyền sử dụng lệnh này.")
        return
    
    global bot_enabled
    bot_enabled = True
    await update.message.reply_text("Bot đã được bật trở lại.")



async def list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    admin_id = '6343573113'  # Thay 'admin_id_here' bằng id của admin

    if not check_user_plan(user_id):
        await update.message.reply_text("Bạn Không Có Quyền Sử Dụng Bot\nVui Lòng Liên Hệ Admin Để Mua\n\nGiá Plan\n15K: Tuần\n30K: Tháng\nVĩnh Viễn: 100K\n Liên Hệ: @codondeptrai")
        return

    cooldown_data = load_json(COOLDOWN_FILE)
    current_time = time.time()
    if user_id in cooldown_data and current_time - cooldown_data[user_id] < COOLDOWN_TIME:
        remaining_time = COOLDOWN_TIME - (current_time - cooldown_data[user_id])
        await update.message.reply_text(f"Vui Lòng Chờ {int(remaining_time)} Giây Trước Khi Sử Dụng Lần Tiếp Theo")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Cách Dùng: /list [sdt1|sdt2|sdt3] tối đa 10 số cùng lúc\nví dụ: /list 0123456789|0987654321 mỗi số cách nhau 1 dấu |")
        return

    phone_numbers = context.args[0].split('|')
    if len(phone_numbers) > 10:
        await update.message.reply_text("Chỉ Cho Phép Tối Đa 10 Số Điện Thoại")
        return

    for phone_number in phone_numbers:
        if not (phone_number.isdigit() and len(phone_number) == 10):
            await update.message.reply_text("Số Điện Thoại Phải Đủ 10 Số.")
            return

    cooldown_data[user_id] = current_time
    save_json(cooldown_data, COOLDOWN_FILE)

    for phone_number in phone_numbers:
        command = f"screen -dm bash -c 'timeout 650s python3 tlc.py {phone_number} 35'"
        os.system(command)

    await update.message.reply_text(f"Đã Gửi Cuộc Tấn Công Đến Tất Cả Số Điện Thoại", parse_mode='HTML')

    # Gửi thông tin số điện thoại và thông tin user đến admin
    #info = update.message.from_user
    #wait context.bot.send_message(admin_id, f"Người dùng {user_info.first_name} {user_info.last_name} (ID: {user_info.id}) đã sử dụng lệnh /list với các số điện thoại: {', '.join(phone_numbers)}")

async def id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    await update.message.reply_text(f"ID của bạn là: {user_id}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("vip", vip))
app.add_handler(CommandHandler("add", add_user))
app.add_handler(CommandHandler("ban", ban_user))
app.add_handler(CommandHandler("unban", unban_user))
app.add_handler(CommandHandler("spam", spam))

app.add_handler(CommandHandler("call", call))

app.add_handler(CallbackQueryHandler(button))

app.add_handler(CommandHandler("sms", sms))

app.add_handler(CommandHandler("stop", stop))

app.add_handler(CommandHandler("plan", plan))
#dd_handler(CommandHandler("list", list))
#d_handler(CommandHandler("list_users", list_users))
app.add_handler(CommandHandler("check", check))

app.add_handler(CommandHandler("naptien", naptien))

app.add_handler(CommandHandler("uptime", uptime))

app.add_handler(CommandHandler("vip1", vip1))
app.add_handler(CommandHandler("vip2", vip2))
app.add_handler(CommandHandler("list_ids", list_ids))

app.add_handler(CommandHandler("them", them))
app.add_handler(CommandHandler("sent", sent))
app.add_handler(CommandHandler("send", send))


app.add_handler(CommandHandler("stopvip", stopvip))


app.add_handler(CommandHandler("off", off))
app.add_handler(CommandHandler("on", on))
app.add_handler(CommandHandler("list", list))
app.add_handler(CommandHandler("id", id))
print('Screen')


app.run_polling()

