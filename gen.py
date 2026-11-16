#!/usr/bin/env python3
"""生成各 App 的隐私政策页和支持页（三语同页）。
用法：python3 gen.py   → 生成 <app>/privacy/index.html、<app>/index.html、index.html
新 App：在 APPS 里加一项，再运行。"""
import html, os

EMAIL = "weifan2026@icloud.com"
UPDATED = {"en": "Last updated: 16 November 2026", "ja": "最終更新日：2026年11月16日", "zh": "最后更新：2026年11月16日"}
LANGS = [("en", "English"), ("ja", "日本語"), ("zh", "简体中文")]

APPS = {
    "oshirase": {
        "name": {"en": "Paper to Plan", "ja": "おしらせ箱", "zh": "通知收纳"},
        "desc": {
            "en": "Snap a school notice, letter or bill and turn its dates, deadlines and items into calendar events and reminders. Works fully offline.",
            "ja": "学校のおしらせや手紙、請求書を撮るだけで、日付・締め切り・持ち物をカレンダーとリマインダーに。すべてオフラインで動きます。",
            "zh": "拍一张学校通知、信件或账单，把日期、截止日和要带的东西加进日历和提醒事项。全程离线。",
        },
        "uses": {
            "en": [
                "<b>Camera and photos</b>: images you take or choose are read on your iPhone to find dates, deadlines and amounts. They are never uploaded.",
                "<b>Calendar and Reminders</b>: used only to add the events and reminders you confirm. Your existing calendar events are not read. Items you add are then managed in those apps.",
                "<b>Text recognition and summaries</b>: done on your iPhone with Apple's Vision framework and Apple Intelligence on-device model. No internet connection is needed.",
            ],
            "ja": [
                "<b>カメラと写真</b>：撮影・選択した画像は iPhone 上で読み取り、日付・締め切り・金額を見つけます。アップロードはしません。",
                "<b>カレンダーとリマインダー</b>：あなたが確認した予定とリマインダーを追加するためだけに使います。既存の予定は読み取りません。追加した項目はそれぞれのアプリで管理されます。",
                "<b>文字の読み取りと要約</b>：Apple の Vision フレームワークと Apple Intelligence の端末内モデルで、iPhone 上で行います。インターネット接続は必要ありません。",
            ],
            "zh": [
                "<b>相机和照片</b>：你拍摄或选择的图片只在 iPhone 上识别日期、截止日和金额，不会上传。",
                "<b>日历和提醒事项</b>：只用来添加你确认过的日程和提醒，不读取你已有的日程。添加后的条目由日历和提醒事项 App 管理。",
                "<b>文字识别和摘要</b>：用 Apple 的 Vision 框架和 Apple Intelligence 端侧模型在 iPhone 上完成，不需要联网。",
            ],
        },
    },
    "sonae": {
        "name": {"en": "Use By", "ja": "そなえ帳", "zh": "备蓄账本"},
        "desc": {
            "en": "Track your emergency supplies and food with their use-by dates, get reminded before they expire, and see how many days your stock would last.",
            "ja": "備蓄品や食品を期限とあわせて記録し、期限前にお知らせ。家族の人数から何日分そなえているかもわかります。",
            "zh": "记录备蓄品和食品及其期限，到期前提醒，并按家庭人数算出能撑几天。",
        },
        "uses": {
            "en": [
                "<b>Camera</b>: photos of product labels are read on your iPhone to fill in the name and date. They are never uploaded.",
                "<b>Notifications</b>: expiry reminders are scheduled on your iPhone. No data is sent anywhere.",
            ],
            "ja": [
                "<b>カメラ</b>：商品ラベルの写真は iPhone 上で読み取り、品名と期限を入力します。アップロードはしません。",
                "<b>通知</b>：期限のお知らせは iPhone の中で設定され、外部には何も送信しません。",
            ],
            "zh": [
                "<b>相机</b>：商品标签的照片只在 iPhone 上识别名称和期限，不会上传。",
                "<b>通知</b>：到期提醒在 iPhone 本机设置，不向外发送任何数据。",
            ],
        },
    },
    "hitokoto": {
        "name": {"en": "Say It Coach", "ja": "ひとこと会話", "zh": "一句口语"},
        "desc": {
            "en": "Practise speaking English and Japanese with short everyday phrases, pronunciation feedback and on-device AI conversations.",
            "ja": "日常のひとことで英語・日本語を話す練習。発音のフィードバックと、端末上の AI との会話練習ができます。",
            "zh": "用日常短句练习说英语和日语，提供发音反馈和端侧 AI 对话练习。",
        },
        "uses": {
            "en": [
                "<b>Microphone and speech recognition</b>: your voice is transcribed on your iPhone to check your pronunciation. Recordings are not saved or uploaded.",
                "<b>AI conversations</b>: run on your iPhone with Apple's on-device model. Your messages never leave the device.",
            ],
            "ja": [
                "<b>マイクと音声認識</b>：あなたの声は iPhone 上で文字にして、発音をチェックします。録音は保存もアップロードもしません。",
                "<b>AI との会話</b>：Apple の端末内モデルで iPhone 上で動きます。会話の内容が端末の外に出ることはありません。",
            ],
            "zh": [
                "<b>麦克风和语音识别</b>：你的声音只在 iPhone 上转成文字来检查发音，录音不会保存也不会上传。",
                "<b>AI 对话</b>：使用 Apple 的端侧模型在 iPhone 上运行，对话内容不会离开设备。",
            ],
        },
    },
}

T = {
    "privacy": {"en": "Privacy Policy", "ja": "プライバシーポリシー", "zh": "隐私政策"},
    "support": {"en": "Support", "ja": "サポート", "zh": "技术支持"},
    "summary_h": {"en": "In short", "ja": "概要", "zh": "简要说明"},
    "summary": {
        "en": "{app} does not collect, store or share any personal data. There are no accounts, no servers, no analytics, no ads and no tracking. Everything you enter stays on your iPhone.",
        "ja": "{app} は個人データを収集・保存・共有しません。アカウント、サーバー、分析ツール、広告、トラッキングは一切ありません。入力した内容はすべてあなたの iPhone の中にとどまります。",
        "zh": "{app} 不收集、不保存、不分享任何个人数据。没有账号、没有服务器、没有统计分析、没有广告、没有追踪。你输入的内容都只留在你的 iPhone 上。",
    },
    "uses_h": {"en": "What the app uses on your iPhone", "ja": "端末内で使う機能", "zh": "App 在你的 iPhone 上使用的功能"},
    "uses_note": {
        "en": "Each permission is asked only when you first use the feature, and you can change it any time in Settings.",
        "ja": "各許可はその機能を初めて使うときにだけ求め、「設定」アプリからいつでも変更できます。",
        "zh": "每项权限只在你第一次使用该功能时询问，之后可以随时在“设置”里更改。",
    },
    "purchase_h": {"en": "Purchases", "ja": "購入について", "zh": "购买"},
    "purchase": {
        "en": "The one-time unlock is processed by Apple through the App Store. We never receive your payment details or Apple Account information.",
        "ja": "買い切りのアンロックは App Store を通じて Apple が処理します。支払い情報や Apple アカウントの情報を私たちが受け取ることはありません。",
        "zh": "一次性解锁由 Apple 通过 App Store 处理。我们不会收到你的付款信息或 Apple 账户信息。",
    },
    "delete_h": {"en": "Storage and deletion", "ja": "保存と削除", "zh": "存储与删除"},
    "delete": {
        "en": "Your data is stored only on your iPhone. Deleting the app removes all of it.",
        "ja": "データはあなたの iPhone の中だけに保存されます。アプリを削除するとすべて消去されます。",
        "zh": "你的数据只存在你的 iPhone 上，删除 App 即全部清除。",
    },
    "kids_h": {"en": "Children", "ja": "お子さまについて", "zh": "儿童"},
    "kids": {
        "en": "Because the app collects no personal data, it collects none from children either.",
        "ja": "本アプリは個人データを収集しないため、お子さまの個人データも収集しません。",
        "zh": "本 App 不收集任何个人数据，因此也不会收集儿童的个人数据。",
    },
    "changes_h": {"en": "Changes", "ja": "変更について", "zh": "政策变更"},
    "changes": {
        "en": "If this policy changes, the new version will be posted on this page with a new date.",
        "ja": "このポリシーを変更する場合は、このページに新しい日付とともに掲載します。",
        "zh": "如本政策有变更，会在本页发布新版本并更新日期。",
    },
    "contact_h": {"en": "Contact", "ja": "お問い合わせ", "zh": "联系我们"},
    "contact": {
        "en": "Questions or feedback: ",
        "ja": "ご質問・ご意見：",
        "zh": "问题或反馈：",
    },
    "faq_h": {"en": "Common questions", "ja": "よくある質問", "zh": "常见问题"},
    "faq": {
        "en": [("I bought the unlock, but the app is still locked.", "Open Settings in the app and tap Restore Purchases, using the same Apple Account you bought with."),
               ("Will I lose my data if I change iPhone?", "Data is stored on your iPhone. Moving to a new iPhone with an iCloud or computer backup restores it.")],
        "ja": [("購入したのにロックが解除されません。", "アプリの「設定」で「購入を復元」をタップしてください。購入時と同じ Apple アカウントを使ってください。"),
               ("機種変更するとデータは消えますか？", "データは iPhone の中に保存されています。iCloud またはパソコンのバックアップから新しい iPhone に移行すると引き継げます。")],
        "zh": [("已经购买了，但 App 还是没有解锁。", "在 App 的“设置”里点“恢复购买”，并确保使用的是购买时的同一个 Apple 账户。"),
               ("换手机后数据会丢吗？", "数据保存在 iPhone 本机。用 iCloud 或电脑备份迁移到新 iPhone 即可保留。")],
    },
    "email_us": {"en": "Email us", "ja": "メールで問い合わせる", "zh": "发邮件联系"},
    "reply": {"en": "We usually reply within a few days.", "ja": "通常、数日以内に返信します。", "zh": "我们通常会在几天内回复。"},
    "apps": {"en": "Apps", "ja": "アプリ", "zh": "App"},
}

CSS = """
:root{--bg:#fafaf9;--text:#1c1c1e;--muted:#6b6b70;--line:#e5e5e7;--accent:#c4553a}
@media (prefers-color-scheme:dark){:root{--bg:#161618;--text:#f2f2f4;--muted:#9a9aa0;--line:#2c2c30;--accent:#ef8a6d}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.65 -apple-system,BlinkMacSystemFont,"Hiragino Sans","PingFang SC",sans-serif}
main{max-width:680px;margin:0 auto;padding:32px 16px 64px}
nav{display:flex;gap:16px;flex-wrap:wrap;font-size:14px;margin-bottom:24px}
a{color:var(--accent)}h1{font-size:28px;line-height:1.3;margin:0 0 4px}h2{font-size:18px;margin:28px 0 8px}
section.lang{border-top:1px solid var(--line);padding-top:24px;margin-top:32px}section.lang:first-of-type{border-top:0;margin-top:0;padding-top:0}
.muted{color:var(--muted);font-size:14px}ul{padding-left:20px}li{margin:6px 0}
.btn{display:inline-block;padding:10px 18px;border-radius:10px;background:var(--accent);color:#fff;text-decoration:none;font-weight:600}
"""


def page(title, body, lang="en"):
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><style>{CSS}</style></head>
<body><main>{body}</main></body></html>
"""


def lang_nav():
    return "<nav>" + "".join(f'<a href="#{c}">{n}</a>' for c, n in LANGS) + "</nav>"


def privacy(key, app):
    parts = [lang_nav()]
    for c, _ in LANGS:
        name = app["name"][c]
        uses = "".join(f"<li>{u}</li>" for u in app["uses"][c])
        parts.append(f"""<section class="lang" id="{c}" lang="{'zh-Hans' if c == 'zh' else c}">
<h1>{name} — {T['privacy'][c]}</h1><p class="muted">{UPDATED[c]}</p>
<h2>{T['summary_h'][c]}</h2><p>{T['summary'][c].format(app=name)}</p>
<h2>{T['uses_h'][c]}</h2><ul>{uses}</ul><p>{T['uses_note'][c]}</p>
<h2>{T['purchase_h'][c]}</h2><p>{T['purchase'][c]}</p>
<h2>{T['delete_h'][c]}</h2><p>{T['delete'][c]}</p>
<h2>{T['kids_h'][c]}</h2><p>{T['kids'][c]}</p>
<h2>{T['changes_h'][c]}</h2><p>{T['changes'][c]}</p>
<h2>{T['contact_h'][c]}</h2><p>{T['contact'][c]}<a href="mailto:{EMAIL}">{EMAIL}</a></p>
</section>""")
    return page(f"{app['name']['en']} — Privacy Policy", "".join(parts))


def support(key, app):
    parts = [lang_nav()]
    for c, _ in LANGS:
        faq = "".join(f"<h2>{q}</h2><p>{a}</p>" for q, a in T["faq"][c])
        parts.append(f"""<section class="lang" id="{c}" lang="{'zh-Hans' if c == 'zh' else c}">
<h1>{app['name'][c]} — {T['support'][c]}</h1><p>{app['desc'][c]}</p>
<p><a class="btn" href="mailto:{EMAIL}?subject={html.escape(app['name']['en'])}">{T['email_us'][c]}</a></p>
<p class="muted">{EMAIL} · {T['reply'][c]}</p>
{faq}
<p><a href="privacy/">{T['privacy'][c]}</a></p>
</section>""")
    return page(f"{app['name']['en']} — Support", "".join(parts))


def index():
    items = "".join(
        f"<li><a href=\"{k}/\">{a['name']['ja']} / {a['name']['en']} / {a['name']['zh']}</a> · <a href=\"{k}/privacy/\">Privacy</a></li>"
        for k, a in APPS.items())
    return page("Apps", f"<h1>Apps</h1><ul>{items}</ul><p class=\"muted\"><a href=\"mailto:{EMAIL}\">{EMAIL}</a></p>")


def write(path, text):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    open(path, "w").write(text)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for k, a in APPS.items():
        write(f"{k}/index.html", support(k, a))
        write(f"{k}/privacy/index.html", privacy(k, a))
    write("index.html", index())
    print("ok")
