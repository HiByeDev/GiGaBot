from rubika import Bot
from json import load , dump
import time

bot = Bot("vddmrabxzptricoukjrhtoiihxckduny")
target = "g0B1tjY060604ca438ff508f0270cd82"


# Coded By : github.com/HiByeDev ~ rubika -> @Develover
# Tnx to github.com/Bahman-ahmadi
# v 1.1 (latest)




def hasAds(msg):
	links = ["rubika.ir/"] # you can develop it
	for i in links:
		if i in msg.lower():
			return True


def searchUserInGroup(guid):
	user = bot.getUserInfo(guid)["data"]["user"]["username"]
	members = bot.getGroupAllMembers(user,target)["in_chat_members"]
	if members != [] and members[0]["username"] == user:
		return True
	
	

# static variable
answered, sleeped, retries = [], False, {}

# option lists
blacklist, exemption, auto_lock , no_alerts , no_stars =  [] , [] , False , [] , []
alerts, stars = {} , {}
auto_lock , locked , gif_lock = False , False , False


# alert function
def alert(guid,user,alert_text=""):
	no_alerts.append(guid)
	alert_count = int(no_alerts.count(guid))

	alerts[user] = alert_count

	max_alert = 5    # you can change it


	if alert_count == max_alert:
		blacklist.append(guid)
		bot.sendMessage(target, "\n 🚫 کاربر [ @"+user+" ] \n ("+ str(max_alert) +") اخطار دریافت کرد ، بنابراین اکنون اخراج میشود .", msg["message_id"])
		bot.banGroupMember(target, guid)
		return

	for i in range(max_alert):
		no = i+1
		if alert_count == no:
			bot.sendMessage(target, "💢 اخطار [ @"+user+" ] \n\n"+ str(alert_text) +" شما ("+ str(no) +"/"+ str(max_alert) +") اخطار دریافت کرده اید .\n\nپس از دریافت "+ str(max_alert) +" اخطار ، از گروه اخراج خواهید شد .", msg["message_id"])
			return

# star function
def star(guid,user):
	no_stars.append(guid)
	star_count = int(no_stars.count(guid))
	stars[user] = star_count

	bot.sendMessage(target, "⭐ کاربر @"+ user +" امتیاز دریافت کرد .\n\nتعداد امتیاز های کاربر تا این لحظه = "+ str(star_count), msg["message_id"])
	return


while True:
	if auto_lock:
		if not locked and time.localtime().tm_hour == 00:
			bot.setMembersAccess(target, ["AddMember"])
			bot.sendMessage(target, "⏰ زمان قفل خودکار گروه فرا رسیده است .\n - گروه تا ساعت [ 08:00 ] تعطیل می باشد .")
			locked , sleeped = True , True

		if locked and time.localtime().tm_hour == 8:
			bot.setMembersAccess(target, ["SendMessages","AddMember"])
			bot.sendMessage(target, "⏰ زمان قفل خودکار گروه به پایان رسیده است .\n - اکنون اعضا می توانند در گروه چت کنند .")
			locked , sleeped = False , False		


	# time.sleep(15)
	try:

		admins = [i["member_guid"] for i in bot.getGroupAdmins(target)["data"]["in_chat_members"]]
		min_id = bot.getGroupInfo(target)["data"]["chat"]["last_message_id"]

		with open("learn.json","r",encoding="utf-8") as learn:
			data = load(learn)

		while True:
			try:
				messages = bot.getMessages(target,min_id)
				break
			except:
				continue

		for msg in messages:
			try:
				# Check Bot is Sleeped or Not
				if not sleeped:

					# Get Text Messages
					if msg["type"]=="Text" and not msg["message_id"] in answered:


						# Admin Commands
						if msg["author_object_guid"] in admins:

							if msg["text"] == "ربات خاموش" or msg["text"] == "/sleep" :
								sleeped = True
								bot.sendMessage(target, "💤 ربات اکنون خاموش است .", msg["message_id"])


							elif msg["text"] == "!start" or msg["text"] == "/start" :
								bot.sendMessage(target, "✨ به گیگابات خوش آمدید .\n\nبرای مشاهده لیست دستورات ربات ، کلمه (دستورات) را ارسال کنید .", msg["message_id"])
							
							elif msg["text"].startswith("یادبگیر") or msg["text"].startswith("/learn"):
								try:
									text = msg["text"].replace("یادبگیر ","").replace("/learn ","").split(":")
									word = text[0]
									answer = text[1]

									data[word] = answer
									with open("learn.json","w",encoding="utf-8") as learn:
										dump(data, learn)

									bot.sendMessage(target, "✅ ذخیره شد", msg["message_id"])
								except:
									bot.sendMessage(target, "❌ خطا در اجرای دستور", msg["message_id"])


							elif msg["text"].startswith("افزودن ادمین") or msg["text"].startswith("/add_admin") :

								try:
									user = msg["text"].replace("افزودن ادمین ","").replace("/add_admin ","")[1:]
									guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
									
									if not guid in admins :
										bot.setGroupAdmin(target, guid)
										bot.sendMessage(target, "✅ کاربر @"+ str(user) +" با موفقیت ادمین شد .", msg["message_id"])
									else:
										bot.sendMessage(target, "❌ کاربر هم اکنون ادمین میباشد", msg["message_id"])

								except:
									try:
										guid = bot.getMessagesInfo(target, [msg["reply_to_message_id"]])[0]["author_object_guid"]
										user = bot.getUserInfo(guid)["data"]["user"]["username"]
										
										if not guid in admins :
											bot.setGroupAdmin(target, guid)
											bot.sendMessage(target, "✅ کاربر @"+ str(user) +" با موفقیت ادمین شد .", msg["message_id"])
										else:
											bot.sendMessage(target, "❌ کاربر هم اکنون ادمین میباشد", msg["message_id"])
									except:
										bot.sendMessage(target, "❌ خطا در اجرای دستور", msg["message_id"])

							elif msg["text"].startswith("حذف ادمین") or msg["text"].startswith("/del_admin") :
								try:
									user = msg["text"].replace("حذف ادمین ","").replace("/del_admin ","")[1:]
									guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]

									if guid in admins :
										bot.deleteGroupAdmin(target, guid)
										bot.sendMessage(target, "✅ کاربر @"+ str(user) +" با موفقیت از ادمینی برکنار شد .", msg["message_id"])
									else:
										bot.sendMessage(target, "❌ کاربر ادمین گروه نمیباشد", msg["message_id"])

								except:
									try:
										guid = bot.getMessagesInfo(target, [msg["reply_to_message_id"]])[0]["author_object_guid"]
										user = bot.getUserInfo(guid)["data"]["user"]["username"]

										if not guid in admins :
											bot.setGroupAdmin(target, guid)
											bot.sendMessage(target, "✅ کاربر @"+ str(user) +" با موفقیت از ادمینی برکنار شد .", msg["message_id"])
										else:
											bot.sendMessage(target, "❌ کاربر ادمین گروه نمیباشد", msg["message_id"])
									except:
										bot.sendMessage(target, "❌ خطا در اجرای دستور", msg["message_id"])
							

							
							elif msg["text"].startswith("معاف") :
								try:
									guid = bot.getInfoByUsername(msg["text"].replace("معاف ","")[1:])["data"]["chat"]["abs_object"]["object_guid"]
									if not guid in admins :
										if not guid in exemption:
											exemption.append(guid)
											bot.sendMessage(target, "✅ کاربر با موفقیت معاف شد .", msg["message_id"])
										else:
											bot.sendMessage(target, "❌ کاربر هم اکنون معاف میباشد .", msg["message_id"])
								
									else :
										bot.sendMessage(target, "❌ کاربر ادمین میباشد .", msg["message_id"])
										
								except:
									try:
										guid = bot.getMessagesInfo(target, [msg["reply_to_message_id"]])[0]["author_object_guid"]
										if not guid in admins:
											if not guid in exemption:
												exemption.append(guid)
												bot.sendMessage(target, "✅ کاربر با موفقیت معاف شد .", msg["message_id"])
											else:
												bot.sendMessage(target, "❌ کاربر هم اکنون معاف میباشد .", msg["message_id"])

										else :
											bot.sendMessage(target, "❌ کاربر ادمین میباشد .", msg["message_id"])
									except:
										bot.sendMessage(target, "❌ خطا در اجرای دستور", msg["message_id"])


							elif msg["text"].startswith("حذف معاف") :
								try:
									guid = bot.getInfoByUsername(msg["text"].replace("حذف معاف ","")[1:])["data"]["chat"]["abs_object"]["object_guid"]
									if not guid in admins :
										if guid in exemption:
											exemption.remove(guid)
											bot.sendMessage(target, "✅ کاربر از معافیت حذف شد", msg["message_id"])
										else:
											bot.sendMessage(target, "❌ کاربر معاف نمیباشد .", msg["message_id"])
									else :
										bot.sendMessage(target, "❌ کاربر ادمین میباشد", msg["message_id"])
										
								except:
									try:
										guid = bot.getMessagesInfo(target, [msg["reply_to_message_id"]])[0]["author_object_guid"]
										if not guid in admins and guid in exemption:
											if guid in exemption:
												exemption.remove(guid)
												bot.sendMessage(target, "✅ کاربر با از معافیت حذف شد", msg["message_id"])
											else:
												bot.sendMessage(target, "❌ کاربر معاف نمیباشد .", msg["message_id"])

										else :
											bot.sendMessage(target, "❌ کاربر ادمین میباشد", msg["message_id"])
									
									except:
										bot.sendMessage(target, "❌ خطا در اجرای دستور", msg["message_id"])
							

							
							elif msg["text"] == "لیست امتیاز" or msg["text"] == "/star_list":
								try:
									text = "💎 لیست امتیازات کاربران گروه :\n\n"
									stars_list = ""
									for i in stars:
										stars_list += (" - @"+i+" \t= "+str(stars[i])+"\n")
									bot.sendMessage(target, text + str(stars_list), msg["message_id"])
								except:
									bot.sendMessage(target, "❌ خطا در اجرای دستور", msg["message_id"])
							
							
							elif msg["text"] == "لیست اخطار" or msg["text"] == "/alert_list":
								try:
									text = "⚠ لیست اخطارهای کاربران گروه :\n\n"
									alert_list = ""
									for i in alerts:
										alert_list += (" - @"+i+" \t= "+str(alerts[i])+"\n")
									bot.sendMessage(target, text + str(alert_list), msg["message_id"])
								except:
									bot.sendMessage(target, "❌ خطا در اجرای دستور", msg["message_id"])

							
							elif msg["text"].startswith("حذف اخطار") or msg["text"].startswith("/del_alert"):
								try:
									user = msg["text"].replace("حذف اخطار ","").replace("/del_alert ","")[1:]
									guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
									
									if guid in no_alerts:
										for i in range(no_alerts.count(guid)):
											no_alerts.remove(guid)
										alerts[user] = 0
										bot.sendMessage(target, "✅ اخطارهای کاربر حذف شد .", msg["message_id"])
									else:
										bot.sendMessage(target, "❌ کاربر اخطاری ندارد .", msg["message_id"])
										
								except:
									try:
										guid = bot.getMessagesInfo(target, [msg["reply_to_message_id"]])[0]["author_object_guid"]
										user = bot.getUserInfo(guid)["data"]["user"]["username"]

										if guid in no_alerts:
											for i in range(no_alerts.count(guid)):
												no_alerts.remove(guid)
											alerts[user] = 0
											bot.sendMessage(target, "✅ اخطارهای کاربر حذف شد .", msg["message_id"])
										else:
											bot.sendMessage(target, "❌ کاربر اخطاری ندارد .", msg["message_id"])

									except:
										bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", msg["message_id"])
								


							elif msg["text"].startswith("اخطار")  or msg["text"].startswith("/alert"):
								try:
									user = msg["text"].replace("اخطار ","").replace("/alert ","")[1:]
									guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
									
									if not guid in admins :
										alert(guid,user)
									else :
										bot.sendMessage(target, "❌ کاربر ادمین میباشد", msg["message_id"])
										
								except:
									try:
										guid = bot.getMessagesInfo(target, [msg["reply_to_message_id"]])[0]["author_object_guid"]
										user = bot.getUserInfo(guid)["data"]["user"]["username"]
										if not guid in admins:
											alert(guid,user)
										else:
											bot.sendMessage(target, "❌ کاربر ادمین میباشد", msg["message_id"])
									except:
										bot.sendMessage(target, "❌ خطا در اجرای دستور", msg["message_id"])
							
							
							
							elif msg["text"].startswith("حالت آرام") or msg["text"].startswith("/slow"):
								try:
									number = int(msg["text"].replace("حالت آرام ","").replace("/slow ",""))

									bot.setGroupTimer(target,number)

									bot.sendMessage(target, "⏰ حالت آرام برای "+str(number)+"ثانیه فعال شد", msg["message_id"])

								except:
									bot.sendMessage(target, "❌ خطا در اجرای دستور", msg["message_id"])
								
							elif msg["text"] == "حذف حالت آرام" or msg["text"] == "/off_slow":
								try:
									number = 0
									bot.setGroupTimer(target,number)

									bot.sendMessage(target, "⏰ حالت آرام غیرفعال شد", msg["message_id"])
								except:
									bot.sendMessage(target, "❌ خطا در اجرای دستور", msg["message_id"])
								
							# elif msg["text"] == "قفل گیف" or msg["text"] == "/gif_lock":
							# 	gif_lock = True
							# 	bot.sendMessage(target, "✅ قفل گیف و استیکر فعال شد .", msg["message_id"])

							
							# elif msg["text"] == "حذف قفل گیف" or msg["text"] == "/del_gif_lock":
							# 	gif_lock = False
							# 	bot.sendMessage(target, "✅ قفل گیف و استیکر غیرفعال شد .", msg["message_id"])


							elif msg["text"] == "قفل خودکار" or msg["text"] == "/auto_lock":
								try:
									auto_lock = True
									# time = msg["text"].split(" ")[2].split(":") start=time[0] , end=time[1]
									start = "00:00"
									end = "08:00"
									# open("time.txt","w").write(start +"-"+ end)
									bot.sendMessage(target, "🔒 قفل خودکار برای گروه فعال شد . \n\n گروه ساعت [ "+ start +" ] قفل خواهد شد \n و در ساعت [ "+ end +" ] باز خواهد شد .", msg["message_id"])
										
								except:
									bot.sendMessage(target, "❌ خطا در اجرای دستور", msg["message_id"])

							
							elif msg["text"] == "حذف قفل خودکار" or msg["text"] == "/del_auto_lock":
								auto_lock = False
								bot.sendMessage(target, "🔓 قفل خودکار برداشته شد .", msg["message_id"])


							elif msg["text"].startswith("اخراج") or msg["text"].startswith("/ban") :
								try:
									guid = bot.getInfoByUsername(msg["text"].replace("اخراج ","").replace("/ban ","")[1:])["data"]["chat"]["abs_object"]["object_guid"]
									if not guid in admins :
										bot.banGroupMember(target, guid)
										# bot.sendMessage(target, "✅ کاربر با موفقیت از گروه اخراج شد", msg["message_id"])
									else :
										bot.sendMessage(target, "❌ کاربر ادمین میباشد", msg["message_id"])
										
								except:
									try:
										guid = bot.getMessagesInfo(target, [msg["reply_to_message_id"]])[0]["author_object_guid"]
										if not guid in admins :
											bot.banGroupMember(target, guid)
											# bot.sendMessage(target, "✅ کاربر با موفقیت از گروه اخراج شد", msg["message_id"])
										else :
											bot.sendMessage(target, "❌ کاربر ادمین میباشد", msg["message_id"])
									except:
										bot.sendMessage(target, "❌ خطا در اجرای دستور", msg["message_id"])

							
							elif msg["text"].startswith("حذف") or msg["text"].startswith("/del"):
								try:
									number = int(msg["text"].replace("حذف ","").replace("/del ",""))
									if number > 50:
										bot.sendMessage(target, "❌ ربات فقط تا 50 پیام اخیر را پاک میکند .", msg["message_id"])
									else:
										answered.reverse()
										bot.deleteMessages(target, answered[0:number])

										bot.sendMessage(target, "✅ "+ str(number) +" پیام اخیر با موفقیت حذف شد", msg["message_id"])
										answered.reverse()

								except:
									try:
										bot.deleteMessages(target, [msg["reply_to_message_id"]])
										bot.sendMessage(target, "✅ پیام با موفقیت حذف شد", msg["message_id"])
									except:
										bot.sendMessage(target, "❌ خطا در اجرای دستور", msg["message_id"])

							
							elif msg["text"].startswith("آپدیت قوانین") or msg["text"].startswith("/update_rules"):
								rules = open("rules.txt","w",encoding='utf-8').write(str(msg["text"].replace("آپدیت قوانین","").replace("/update_rules","")))
								bot.sendMessage(target, "✅  قوانین بروزرسانی شد", msg["message_id"])
								# rules.close()
								

							
							elif msg["text"].startswith("امتیاز") or msg["text"].startswith("/star"):
								try:
									user = msg["text"].replace("امتیاز ","").replace("/star ","")[1:]
									guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
									star(guid,user)
									
								except:
									try:
										guid = bot.getMessagesInfo(target, [msg["reply_to_message_id"]])[0]["author_object_guid"]
										user = bot.getUserInfo(guid)["data"]["user"]["username"]
										star(guid,user)
									except:
										bot.sendMessage(target, "❌ خطا در اجرای دستور", msg["message_id"])

							
							
							elif msg["text"] == "قفل گروه" or msg["text"] == "/lock":
								bot.setMembersAccess(target, ["AddMember"])
								bot.sendMessage(target, "🔒 گروه قفل شد", msg["message_id"])


							elif msg["text"] == "بازکردن گروه" or msg["text"] == "/unlock" :
								bot.setMembersAccess(target, ["SendMessages","AddMember"])
								bot.sendMessage(target, "🔓 گروه اکنون باز است", msg["message_id"])
							

							elif msg["text"].startswith("افزودن") or msg["text"].startswith("/add"):
								try:
									guid = bot.getInfoByUsername(msg["text"].replace("افزودن ","").replace("/add ","")[1:])["data"]["chat"]["object_guid"]
									if guid in blacklist:
										for i in range(no_alerts.count(guid)):
											no_alerts.remove(guid)
										blacklist.remove(guid)

										bot.invite(target, [guid])
									else:
										bot.invite(target, [guid])
									
								except:
									bot.sendMessage(target, "❌ خطا در اجرای دستور", msg["message_id"])
							
							elif msg["text"] == "قوانین":
								rules = open("rules.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), msg["message_id"])
								# rules.close()
							
							elif msg["text"] == "دستورات":
								commands = open("commands.txt","r",encoding='utf-8').read()
								bot.sendMessage(target,str(commands),msg["message_id"])
								
					
						# User Commands
						else:

							if hasAds(msg["text"]) and not msg["author_object_guid"] in exemption:
								guid = msg["author_object_guid"]
								user = bot.getUserInfo(guid)["data"]["user"]["username"]
								bot.deleteMessages(target, [msg["message_id"]])
								alert(guid,user,"گذاشتن لینک در گروه ممنوع میباشد .\n\n")
							
							elif msg["text"] == "دستورات":
								commands = open("commands.txt","r",encoding='utf-8').read()
								bot.sendMessage(target,str(commands),msg["message_id"])
							
							elif msg["text"] == "قوانین":
								rules = open("rules.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), msg["message_id"])
								# rules.close()
							
							elif msg["text"].startswith("افزودن") or msg["text"].startswith("/add"):
								try:
									guid = bot.getInfoByUsername(msg["text"].replace("افزودن ","").replace("/add ","")[1:])["data"]["chat"]["object_guid"]
									if guid in blacklist:
										bot.sendMessage(target, "❌ کاربر در لیست سیاه میباشد و فقط ادمین میتواند فرد را به گروه اضافه کند .", msg["message_id"])
									else:
										bot.invite(target, [guid])
										# bot.sendMessage(target, "✅ کاربر اکنون عضو گروه است", msg["message_id"])
									
								except:
									bot.sendMessage(target, "❌ خطا در اجرای دستور", msg["message_id"])

							elif msg["text"] == "لینک":
								group = bot.getGroupLink(target)["data"]["join_link"]
								bot.sendMessage(target, "🔗 لینک گروه :\n"+str(group), msg["message_id"])

							for i in data.keys():
								if i == msg["text"]:
									bot.sendMessage(target, str(data[i]), msg["message_id"])



					elif msg["type"]=="Event" and not msg["message_id"] in answered:
						answered.append(msg["message_id"])

						name = bot.getGroupInfo(target)["data"]["group"]["group_title"]
						data = msg['event_data']
						if data["type"]=="RemoveGroupMembers":
							user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"🚨 کاربر {user} با موفقیت از گروه حذف شد .", msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						
						elif data["type"]=="AddedGroupMembers":
							user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"سلام {user} عزیز 🌹 \n • به گروه {name} خوش اومدی 😍 \n 📿 لطفا قوانین رو رعایت کن .\n 💎 برای مشاهده قوانین کافیه کلمه (قوانین) رو ارسال کنی .", msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						
						elif data["type"]=="LeaveGroup":
							user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"خدانگهدار {user} 👋 ", msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
							
						elif data["type"]=="JoinedGroupByLink":
							guid = data['performer_object']['object_guid']
							user = bot.getUserInfo(guid)["data"]["user"]["first_name"]
							bot.sendMessage(target, f"سلام {user} عزیز 🌹 \n• به گروه {name} خوش اومدی 😍 \n 📿 لطفا قوانین رو رعایت کن .\n 💎 برای مشاهده قوانین کافیه کلمه (قوانین) رو ارسال کنی .", msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
							if guid in blacklist:
								for i in range(no_alerts.count(guid)):
									no_alerts.remove(guid)
								blacklist.remove(guid)
					
					# elif msg["type"]=="Gif" or msg["type"]=="Sticker" and not msg["message_id"] in answered:
					# 	if gif_lock and not msg["author_object_guid"] in admins:
					# 		guid = msg["author_object_guid"]
					# 		user = bot.getUserInfo(guid)["data"]["user"]["username"]
					# 		bot.deleteMessages(target, [msg["message_id"]])
					# 		alert(guid,user,"ارسال گیف و استیکر در گروه ممنوع میباشد .")

					else:
						if "forwarded_from" in msg.keys() and bot.getMessagesInfo(target, [msg["message_id"]])[0]["forwarded_from"]["type_from"] == "Channel" and not msg["author_object_guid"] in exemption:
							bot.deleteMessages(target, [msg["message_id"]])
							guid = msg.get("author_object_guid")
							user = bot.getUserInfo(guid)["data"]["user"]["username"]
							bot.deleteMessages(target, [msg["message_id"]])
							alert(guid,user,"فوروارد پیام در گروه ممنوع میباشد .\n\n")
						
						answered.append(msg["message_id"])
						continue
				
				else:
					if msg["text"] == "ربات روشن" or msg["text"] == "/wakeup":
						sleeped = False
						bot.sendMessage(target, "✅ ربات اکنون روشن است .", msg["message_id"])
					
			except:
				continue

			answered.append(msg["message_id"])
			print("[" + msg["message_id"]+ "] >>> " + msg["text"] + "\n")

	except KeyboardInterrupt:
		exit()

	except Exception as e:
		if type(e) in list(retries.keys()):
			if retries[type(e)] < 3:
				retries[type(e)] += 1
				continue
			else:
				retries.pop(type(e))
		else:
			retries[type(e)] = 1
			continue
