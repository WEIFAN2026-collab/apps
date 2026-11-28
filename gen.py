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
    "gamemannaka": {
        "name": {"en": "Kanji Center", "ja": "熟語のまんなか", "zh": "熟语填心"},
        "desc": {
            "en": "A daily kanji puzzle: find the one character that completes four Japanese words around it. Five new puzzles every day, plus stages graded from early elementary school to the full jōyō list.",
            "ja": "まんなかの一字を当てて、上下左右の4つの熟語を完成させる漢字パズル。毎日5問の新しい問題と、小学校低学年から常用漢字までの学年別ステージ。",
            "zh": "猜出中间那一个汉字，让上下左右组成 4 个日语熟语。每天 5 道新题，另有从小学低年级到常用汉字的分级关卡。",
        },
        "uses": {
            "en": [
                "<b>Reading words aloud</b>: uses the Japanese voice built into your iPhone. Nothing is sent over the internet.",
                "<b>Dictionary</b>: the word lookup button opens the dictionary built into iOS.",
                "<b>Progress</b>: your solved puzzles, streak and settings are saved only on your iPhone.",
            ],
            "ja": [
                "<b>読み上げ</b>：iPhone に内蔵された日本語の音声を使います。インターネットには何も送信しません。",
                "<b>辞書</b>：辞書ボタンは iOS に内蔵された辞書を開きます。",
                "<b>進み具合</b>：解いた問題、連続日数、設定は iPhone の中だけに保存されます。",
            ],
            "zh": [
                "<b>朗读</b>：使用 iPhone 内置的日语语音，不会通过网络发送任何内容。",
                "<b>词典</b>：查词按钮打开的是 iOS 内置词典。",
                "<b>进度</b>：已解的题目、连续天数和设置只保存在你的 iPhone 上。",
            ],
        },
    },
    "wrenchcheck": {
        "name": {"en": "WrenchCheck", "ja": "WrenchCheck", "zh": "WrenchCheck"},
        "updated": {"en": "Last updated: 28 November 2026", "ja": "最終更新日：2026年11月28日", "zh": "最后更新：2026年11月28日"},
        "desc": {
            "en": "Understand car warning lights, appliance error codes and unusual noises, check repair quotes line by line, and keep your vehicles and home appliances in one place.",
            "ja": "車の警告灯や家電のエラー表示、気になる異音から考えられる原因を調べ、修理見積りの妥当性を項目ごとに確認できるアプリです。マイカー・家電の整備履歴や保証期限もまとめて管理できます。",
            "zh": "帮你看懂汽车故障灯、家电报错码和各种异响，逐项核对维修报价单并生成礼貌沟通话术，同时集中管理车辆与大家电的维保记录与保修提醒。",
        },
        "summary": {
            "en": "{app} requires no account, contains no ads and does not track you across apps or websites. Your vehicle and appliance records stay on your iPhone. Only when you tap Diagnose or Check Quote—and only after you agree on the consent screen—are the photo, audio clip, model details or quote text you submit sent through our secure server to Google Gemini AI to generate your result.",
            "ja": "{app}はアカウント登録不要で、広告や他社アプリ・Webサイトをまたぐトラッキングはありません。マイカー・家電の記録はiPhone内に保存されます。故障診断や修理見積りチェックを実行し、事前の同意画面でご承諾いただいた場合のみ、送信した写真・録音・型番・見積り内容が当社の安全なサーバーを経由してGoogle Gemini AIへ送信されます。これらのデータは結果の作成にのみ使用されます。",
            "zh": "{app} 无需注册账号，不含广告，也不进行跨 App 或跨网站追踪。你的车家档案和维保记录均保存在 iPhone 本机。只有当你主动发起故障排查或报价核查、并在知情同意页明确同意后，你提交的照片、录音、车型型号或报价单文字才会经由我们的安全服务器交由 Google Gemini AI 处理，且仅用于生成本次结果。",
        },
        "uses": {
            "en": [
                "<b>Camera and photo library</b>: used only to capture or pick dashboard warning lights, appliance displays or repair quotes that you choose to submit for AI analysis.",
                "<b>Microphone</b>: used only when you record up to 10 seconds of a vehicle or appliance noise for AI diagnosis. Nothing is recorded in the background.",
                "<b>Cloud AI processing (Google Gemini)</b>: submitted photos, audio clips, error codes and quote text are transmitted over HTTPS via our server (Cloudflare Workers) to Google Gemini solely to produce your result. They are not used for advertising or linked to your identity. You can revoke AI upload consent at any time in Settings.",
                "<b>Anonymous device identifier</b>: a random, non-tracking device ID (not IDFA) is generated locally solely to count your 3 free AI checks per month.",
                "<b>Notifications</b>: optional local notifications scheduled on your iPhone 30 days before a recorded warranty expires.",
            ],
            "ja": [
                "<b>カメラ・写真ライブラリ</b>：故障診断や修理見積りチェックのために、ご自身で選択・撮影した警告灯・表示部・見積書の画像のみを使用します。",
                "<b>マイク</b>：異音診断のために最大10秒間の音声を録音するときのみ使用します。バックグラウンドで録音することはありません。",
                "<b>クラウドAI処理（Google Gemini）</b>：送信された写真・録音・型番・エラーコード・見積り内容は、結果の作成のみを目的として当社の安全なサーバー（Cloudflare Workers）経由でGoogle Gemini AIへHTTPS送信されます。広告目的での利用や個人との紐付けは行いません。設定画面からいつでもAIデータ送信の同意を取り消せます。",
                "<b>匿名デバイスID</b>：毎月の無料回数（月3回）をカウントするためだけに端末内でランダム生成されるID（IDFAではありません）を使用します。個人特定や追跡には使いません。",
                "<b>通知</b>：登録した保証期限の30日前に、iPhone内のローカル通知でお知らせします。",
            ],
            "zh": [
                "<b>相机与相册</b>：仅用于拍摄或选取你主动提交的仪表盘故障灯、家电显示屏或维修报价单照片。",
                "<b>麦克风</b>：仅在你主动录制最长 10 秒异响用于排查时使用，不会在后台录音。",
                "<b>云端 AI 处理（Google Gemini）</b>：你提交的照片、录音、型号故障码及报价单文字会通过 HTTPS 经我们的服务器（Cloudflare Workers）交由 Google Gemini 处理，仅用于生成本次排查或核价结果，不用于广告也不关联真实身份。你随时可在 App「设置」中撤销上传授权。",
                "<b>匿名设备标识</b>：仅在 App 内随机生成非追踪用的匿名设备 ID（非 IDFA），用于统计每月 3 次免费额度。",
                "<b>本地通知</b>：可选功能，在你设定的保修到期日前 30 天于本机触发提醒。",
            ],
        },
        "purchase": {
            "en": "WrenchCheck offers 3 free AI checks per month and an optional auto-renewing subscription (WrenchCheck Pro, annual with a 7-day free trial or weekly) processed by Apple through the App Store. We never receive your payment details or Apple Account information. Subscriptions renew automatically unless cancelled at least 24 hours before the end of the current period in your Apple Account settings.",
            "ja": "WrenchCheckは毎月3回まで無料でAI診断・見積りチェックを利用できます。回数無制限の自動更新サブスクリプション（WrenchCheck Pro：7日間無料トライアル付き年額プラン／週額プラン）の決済はApp Storeを通じてAppleが処理します。支払い情報やApple Accountの情報を当社が受け取ることはありません。期間終了の24時間前までに解約しない限り自動更新され、設定アプリのApple Accountからいつでも管理・解約できます。",
            "zh": "WrenchCheck 每月提供 3 次免费 AI 排查或核价，另提供可选的自动续期订阅（WrenchCheck Pro，含 7 天免费试用的年度方案或周度方案），由 Apple 通过 App Store 处理。我们不会获取你的付款信息或 Apple 账户信息。除非在当前周期结束前至少 24 小时取消，订阅将自动续期，你可随时在 Apple 账户设置中管理或取消。",
        },
        "delete": {
            "en": "Your garage vehicles, appliances, maintenance logs and diagnosis history are stored locally on your iPhone; deleting the app removes all local records. We do not store user accounts or keep copies of your uploaded photos, audio clips or quotes after generating your result.",
            "ja": "マイカー・家電の情報、整備履歴、診断履歴はiPhone内に保存され、アプリを削除するとすべて消去されます。当社サーバーにアカウント情報や送信済みの写真・録音・見積書を保存し続けることはありません。",
            "zh": "你的车家档案、维保记录和历史排查结果均保存在 iPhone 本机，删除 App 即全部清除。我们的服务器不保存用户账号，也不会在生成结果后留存你上传的照片、录音或报价单。",
        },
        "kids": {
            "en": "WrenchCheck is intended for general vehicle and home maintenance guidance and does not knowingly collect personal information from children.",
            "ja": "本アプリは一般的な車・家電の点検や見積り確認の参考情報を提供するものであり、お子さまの個人情報を意図的に収集することはありません。",
            "zh": "本 App 面向日常车辆与家电维护参考，不会故意收集儿童的个人信息。",
        },
        "safety_h": {"en": "Safety notice", "ja": "安全上のご注意", "zh": "安全提示"},
        "safety": {
            "en": "WrenchCheck provides general informational guidance only and does not replace an inspection by a qualified mechanic or technician. If you notice smoke, a burning smell, fluid leaks or a flashing warning light, stop using the vehicle or appliance immediately and contact a professional.",
            "ja": "本アプリの診断結果および見積りチェックは一般的な参考情報であり、専門業者による点検に代わるものではありません。異臭・発煙・液漏れ・警告灯の点滅がある場合は直ちに使用を中止し、専門業者へご連絡ください。",
            "zh": "WrenchCheck 提供的排查建议与核价参考仅供一般性参考，不能替代持证技师的专业现场检修。如出现焦味、冒烟、漏液或故障灯闪烁，请立即停止使用并联系专业维修人员。",
        },
        "faq": {
            "en": [
                ("I subscribed to WrenchCheck Pro, but my limit did not unlock.", "Open Settings in WrenchCheck and tap Restore Purchases while signed in with the same Apple Account you used to subscribe."),
                ("How do I cancel or manage my subscription?", "Open the iPhone Settings app, tap your Apple Account, then tap Subscriptions and select WrenchCheck."),
                ("How do I turn off AI data sharing?", "Open Settings inside WrenchCheck to review or revoke your AI processing consent at any time."),
                ("Will I lose my garage records if I switch iPhones?", "Your garage assets and logs are stored on your iPhone. Transferring via iCloud or encrypted computer backup preserves them."),
            ],
            "ja": [
                ("WrenchCheck Proに登録したのに制限が解除されない", "アプリ内の「設定」を開き、「購入を復元」をタップしてください。購入時と同じApple Accountでサインインしているかご確認ください。"),
                ("サブスクリプションの解約・変更方法", "iPhoneの「設定」アプリ＞「Apple Account」＞「サブスクリプション」からWrenchCheckを選択して管理・解約できます。"),
                ("AIデータ送信の同意を取り消すには", "アプリ内の「設定」画面からいつでもAIデータ送信の同意を取り消せます。"),
                ("機種変更するとマイカー・家電の記録は消えますか？", "記録はiPhone内に保存されています。iCloudまたはパソコンの暗号化バックアップから新しいiPhoneへ移行すると引き継げます。"),
            ],
            "zh": [
                ("已经订阅了 WrenchCheck Pro，但还是提示次数受限。", "请在 WrenchCheck 的“设置”中点击“恢复购买”，并确认当前登录的是订阅时使用的同一个 Apple 账户。"),
                ("如何取消或管理订阅？", "打开 iPhone“设置”→ 点击顶部 Apple 账户 →“订阅”，找到 WrenchCheck 即可管理或取消。"),
                ("如何关闭或撤销 AI 数据上传授权？", "随时可以在 WrenchCheck 的“设置”页查看并撤销 AI 处理授权。"),
                ("换手机后车家档案会丢失吗？", "档案与维保记录保存在 iPhone 本机，通过 iCloud 或电脑加密备份迁移到新 iPhone 即可保留。"),
            ],
        },
    },
    "spokebill": {
        "name": {"en": "SpokeBill", "ja": "SpokeBill", "zh": "SpokeBill"},
        "updated": {"en": "Last updated: 28 November 2026", "ja": "最終更新日：2026年11月28日", "zh": "最后更新：2026年11月28日"},
        "desc": {
            "en": "Describe a job for 20 seconds on site and get a clean, itemised estimate or invoice, or snap a handwritten note. Export PDFs and share a web approval link so clients can confirm in any browser.",
            "ja": "現場で20秒ほど話すだけで、見積書・請求書の明細を自動で作成できるアプリです。手書きメモの写真やテキスト入力にも対応します。PDFの書き出しから取引先向けのWeb承認リンク発行まで行えます。",
            "zh": "在现场说 20 秒即可自动生成带明细的报价单或发票，也支持拍摄手写草稿或文字输入。一键导出专业 PDF，并可生成网页确认链接供客户在浏览器中确认。",
        },
        "summary": {
            "en": "{app} requires no account, contains no ads and does not track you across apps or websites. Your estimates, invoices, client list and business profile (company name, logo, tax registration number and bank details) are stored locally on your iPhone. Only when you use AI drafting—and only after you agree on the consent screen—are your submitted voice clip, photo or notes sent through our managed server to Google Gemini AI to draft your document. Only when you tap Create Approval Link are the document title, client name, business details, line items and totals stored temporarily on our server to display the client approval page.",
            "ja": "{app}はアカウント登録は不要で、広告や他社アプリ・Webサイトをまたぐトラッキングはありません。作成した見積書・請求書、取引先情報、事業者情報（社名・ロゴ・適格請求書発行事業者登録番号・振込先）はすべてiPhone内に保存されます。AIによる書類作成では、事前の同意画面で承諾した場合のみ、音声・写真・補足メモを当社が管理するサーバーを経由してGoogle Gemini AIへ送信します。また、Web承認リンクを発行した場合のみ、その書類のタイトル・取引先名・事業者名・登録番号・明細・金額が承認ページ表示のために当社サーバーへ一時保存されます。",
            "zh": "{app} 无需注册账号，不含广告，也不进行跨 App 或跨网站追踪。你的报价单、发票、客户列表和企业抬头（名称、Logo、税号与收款信息）均保存在 iPhone 本机。只有当你使用 AI 开单并在知情同意页明确同意后，你提交的语音、照片或补充说明才会经由我们管理的服务器发送至 Google Gemini AI 用于生成单据草稿。只有当你主动点击“生成确认链接”时，该单据的标题、客户名、抬头、税号、明细和金额才会临时保存在我们的服务器上以展示客户确认网页。",
        },
        "uses": {
            "en": [
                "<b>Microphone</b>: used only while you actively record a voice note to draft an estimate or invoice. Nothing is recorded in the background.",
                "<b>Camera and photo library</b>: used only to capture or pick handwritten notes or receipts for drafting, and to select your business logo for PDFs.",
                "<b>Cloud AI processing (Google Gemini)</b>: submitted voice clips, photos and notes are sent over HTTPS via our managed server (Cloudflare Workers) to Google Gemini solely to draft your document. They are never used for advertising, linked to your identity or used to train third-party AI models. You can revoke AI consent anytime in the Clients tab.",
                "<b>Web approval links</b>: only when you tap Create Approval Link are the document title, client name, business name, tax registration number, line items and totals stored on our server (Cloudflare Workers KV) for up to 90 days so your client can view the quote and confirm by entering their name in a browser. Original voice recordings and photos are never included. This is a simple web confirmation record and not a statutory digital signature.",
                "<b>Anonymous device identifier</b>: a random, non-tracking device ID (not IDFA) is generated locally solely to count your 3 free AI drafts per month.",
            ],
            "ja": [
                "<b>マイク</b>：音声から見積書・請求書の下書きを作成するため、録音ボタンを押している間のみ使用します。バックグラウンドで録音することはありません。",
                "<b>カメラ・写真ライブラリ</b>：手書きメモや伝票から明細を読み取るための撮影・選択、およびPDFに掲載する社名ロゴ画像の選択にのみ使用します。",
                "<b>クラウドAI処理（Google Gemini）</b>：音声・写真・補足メモは、書類の下書き作成のみを目的として、当社が管理するサーバー（Cloudflare Workers）を経由してGoogle Gemini AIへHTTPSで送信します。広告目的や第三者のAIモデルの学習には使用せず、個人とひもづけることもありません。アプリ内の「取引先」タブからいつでも「クラウドAIへの送信」の同意を取り消せます。",
                "<b>Web承認リンク</b>：「承認リンクを発行」をタップした場合のみ、該当書類のタイトル・取引先名・事業者名・登録番号・明細・金額を当社サーバー（Cloudflare Workers KV）に最大90日間保存し、取引先がブラウザから内容を確認し、名前を入力して承認できます。元の録音音声や手書き写真は送信・保存しません。なお、本機能はWeb上で確認を記録する簡易な機能であり、公的な証明力を持つものではありません。",
                "<b>匿名デバイスID</b>：毎月の無料回数（3回）をカウントするためだけに端末内でランダムに生成されるID（IDFAではありません）を使用します。個人特定や追跡には使いません。",
            ],
            "zh": [
                "<b>麦克风</b>：仅在你主动按下录音键口述单据内容时使用，不会在后台录音。",
                "<b>相机与相册</b>：仅用于拍摄或选取手写草稿、单据照片以识别明细，以及选择用于 PDF 的企业 Logo 图片。",
                "<b>云端 AI 处理（Google Gemini）</b>：你提交的语音、照片和补充说明仅用于生成单据草稿，会经由我们管理的服务器（Cloudflare Workers）通过 HTTPS 发送给 Google Gemini AI 处理，不用于广告、不关联真实身份，也不用于第三方 AI 模型训练。你随时可在 App 内「客户与设置」页撤销授权。",
                "<b>客户网页确认链接</b>：仅当你主动点击“生成确认链接”时，该单据的标题、客户名、企业名称、税号、明细和金额会在我们的服务器（Cloudflare Workers KV）上最多保留 90 天，供客户在浏览器中查看内容并输入姓名确认。原始录音与手写照片不会被包含或保存。该功能仅为网页简易确认记录，不具法定电子签名效力。",
                "<b>匿名设备标识</b>：仅在 App 内随机生成非追踪用的匿名设备 ID（非 IDFA），用于统计每月 3 次免费 AI 开单额度。",
            ],
        },
        "purchase": {
            "en": "Manual drafting, PDF export and client management are free. Cloud AI drafting includes 3 free drafts per month, with an optional auto-renewing subscription (SpokeBill Pro: Annual with a 14-day free trial, or Monthly) for unlimited AI drafts. Payments are processed by Apple through the App Store; we never receive your payment details or Apple Account information. Subscriptions renew automatically unless cancelled at least 24 hours before the end of the current period in iPhone Settings > Apple Account > Subscriptions.",
            "ja": "SpokeBillでは、手入力での書類作成・PDF書き出し・取引先管理を無料で利用できます。AIによる書類作成は毎月3回まで無料で試せるほか、回数無制限で自動更新のサブスクリプション「SpokeBill Pro」も用意しています（14日間の無料トライアル付き年額プラン／月額プラン）。決済はApp Storeを通じてAppleが処理し、支払い情報やApple Accountの情報を当社が受け取ることはありません。現在の期間が終了する24時間前までに解約しない限り、自動更新されます。購入後の管理・解約はiPhoneの「設定」＞Apple Account＞「サブスクリプション」から行えます。",
            "zh": "SpokeBill 的手动建单、PDF 导出和客户管理均免费使用；AI 语音与拍照开单每月提供 3 次免费额度，另提供不限次数的自动续期订阅（SpokeBill Pro：含 14 天免费试用的年度订阅或月度订阅）。费用由 Apple 通过 App Store 结算，我们不会获取你的付款信息或 Apple 账户信息。除非在当前周期结束前至少 24 小时取消，订阅将自动续期，你随时可在 iPhone「设置」＞ Apple 账户 ＞「订阅」中管理或取消。",
        },
        "delete": {
            "en": "Your estimates, invoices, clients and business profile stay on your iPhone; deleting the app removes all local data. We do not store user accounts or keep copies of uploaded voice clips or photos after drafting. Shared web approval link records expire automatically after up to 90 days.",
            "ja": "見積書・請求書、取引先一覧、事業者情報はiPhone内に保存され、アプリを削除するとすべて消去されます。当社サーバーにアカウント情報や送信済みの音声・写真を保存し続けることはありません。発行済みのWeb承認リンクのデータは最大90日で自動的に削除されます。",
            "zh": "你的报价单、发票、客户列表和企业抬头均保存在 iPhone 本机，删除 App 即全部清除。我们的服务器不保存用户账号，也不会在生成草稿后留存你上传的语音或照片。已生成的客户网页确认记录将在最多 90 天后自动过期删除。",
        },
        "kids": {
            "en": "SpokeBill is a business quoting and invoicing tool and does not knowingly collect personal information from children.",
            "ja": "本アプリは業務用の見積書・請求書作成を支援するツールであり、お子さまの個人情報を意図的に収集することはありません。",
            "zh": "本 App 为面向业务场景的报价与开票工具，不会故意收集儿童的个人信息。",
        },
        "safety_h": {"en": "Important notice", "ja": "ご利用上の注意", "zh": "使用提示"},
        "safety": {
            "en": "Always review AI-drafted line items, quantities, unit prices, tax calculations and tax registration numbers before sending a document to a client. Web approval links record a client's name entered in a browser for convenience and do not constitute a legally binding statutory digital signature.",
            "ja": "AIで作成した見積書・請求書の品目・数量・単価・消費税額・登録番号は、送付前に必ず内容をご確認ください。Web承認リンクは、取引先がブラウザ上で名前を入力して確認を記録する機能です。法令に基づく署名の効力や公的な証明力はありません。",
            "zh": "请务必在向客户发送前核对 AI 生成的品目、数量、单价、税额及税号信息。客户网页确认链接仅用于在浏览器中输入姓名记录确认意向，不具备法定电子签名或公证效力。",
        },
        "faq": {
            "en": [
                ("I subscribed to SpokeBill Pro, but my AI draft limit did not unlock.", "Open the Clients tab in SpokeBill and tap Restore Purchases while signed in with the same Apple Account you used to subscribe."),
                ("How do I cancel or manage my subscription?", "Open iPhone Settings > Apple Account > Subscriptions and select SpokeBill."),
                ("How do I revoke cloud AI consent?", "Open the Clients tab in SpokeBill to revoke cloud AI upload consent at any time. Manual document creation and PDF export continue to work without AI."),
                ("Is a web approval link a legally binding digital signature?", "No. It lets your client view the quote in a browser and confirm by entering their name as a convenient record. Use a qualified signing service if a transaction requires a statutory digital signature."),
                ("Will I lose my documents and clients if I switch iPhones?", "Your records are stored on your iPhone. Transferring via iCloud or an encrypted computer backup preserves them."),
            ],
            "ja": [
                ("SpokeBill Proに登録したのに制限が解除されない", "アプリ内の「取引先」タブを開き、「購入を復元」をタップしてください。購入時と同じApple Accountでサインインしているかご確認ください。"),
                ("サブスクリプションの解約・変更方法", "iPhoneの「設定」＞Apple Account＞「サブスクリプション」からSpokeBillを選択して管理・解約できます。"),
                ("「クラウドAIへの送信」の同意を取り消すには", "アプリ内の「取引先」タブにある「クラウドAIへの送信」から、いつでも同意を取り消せます。同意を取り消した後も、手入力での書類作成やPDF書き出しは引き続き利用できます。"),
                ("Web承認リンクに公的な証明力はありますか？", "いいえ。取引先がブラウザで内容を確認し、名前を入力して承認を記録する簡易な確認機能です。法令に基づく効力が必要な取引には、別途、適切な手段をご利用ください。"),
                ("機種変更すると書類や取引先のデータは消えますか？", "データはiPhone内に保存されています。iCloudまたはパソコン上の暗号化されたバックアップから新しいiPhoneへ移行すると引き継げます。"),
            ],
            "zh": [
                ("已经订阅了 SpokeBill Pro，但还是提示次数受限。", "请在 SpokeBill 的「客户与设置」页点击「恢复购买」，并确认当前登录的是订阅时使用的同一个 Apple 账户。"),
                ("如何取消或管理订阅？", "打开 iPhone「设置」＞ Apple 账户 ＞「订阅」，找到 SpokeBill 即可管理或取消。"),
                ("如何撤销云端 AI 上传授权？", "随时可在「客户与设置」页的 AI 授权项撤销同意。撤销后，手动新建单据和 PDF 导出仍可正常使用。"),
                ("客户网页确认链接等同于法定电子签名吗？", "不是。它仅用于让客户在浏览器中查看报价并输入姓名记录确认，如需具有法定效力的电子签章，请另行使用合规电子签约服务。"),
                ("换手机后单据和客户数据会丢失吗？", "数据保存在 iPhone 本机，通过 iCloud 或电脑加密备份迁移到新 iPhone 即可完整保留。"),
            ],
        },
    },
    "pawclear": {
        "name": {"en": "PawClear", "ja": "PawClear", "zh": "PawClear"},
        "updated": {"en": "Last updated: 28 November 2026", "ja": "最終更新日：2026年11月28日", "zh": "最后更新：2026年11月28日"},
        "desc": {
            "en": "Snap a pet food ingredient label, a human food, a houseplant or a vet lab sheet and get clear, plain-language ratings tailored to your pet's allergies, plus a shareable care card for family or pet sitters.",
            "ja": "ペットフードの原材料表示や身近な食べ物・観葉植物、動物病院の検査結果を撮るだけで、気をつけたいポイントをわかりやすく確認できるアプリです。ペットのアレルギーに合わせたチェックや、家族・シッター向けのお世話カード共有にも対応しています。",
            "zh": "拍一下宠粮配料表、人类食物、室内植物或宠物医院化验单，结合毛孩子的过敏史给出清晰易懂的成分解读与问诊建议，还可一键生成宠物照护卡分享给家人或寄养店。",
        },
        "summary": {
            "en": "{app} requires no account, contains no ads and does not track you across apps or websites. Your pet profiles and scan history stay on your iPhone. Only when you start a scan—and only after you agree on the consent screen—are the photo, text note and basic pet profile context (species, age and allergies) sent through our managed server to Google Gemini AI solely to create your result. Only when you tap Share Care Card are the care card fields you chose to include stored temporarily on our server to display the read-only page.",
            "ja": "{app}はアカウント登録が不要で、広告や他社アプリ・Webサイトをまたぐトラッキングはありません。ペットのプロフィールやスキャン履歴はすべてiPhone内に保存されます。スキャンを実行し、事前の同意画面で同意した場合のみ、送信した写真・入力テキスト・ペットの基本情報（犬・猫の別、年齢、アレルギー）が当社管理のサーバーを経由してGoogle Geminiへ送信されます。また、お世話カードを共有した場合のみ、カードに掲載する項目が閲覧専用ページの表示のため当社サーバーへ一時保存されます。",
            "zh": "{app} 无需注册账号，不含广告，也不进行跨 App 或跨网站追踪。你的宠物档案与历史扫描记录均保存在 iPhone 本机。只有当你主动发起扫描并在知情同意页明确同意后，你提交的照片、补充文字及宠物基本信息（物种、年龄、过敏史）才会经由我们管理的服务器发送至 Google Gemini AI，且仅用于生成本次参考结果。只有当你主动点击「分享照护卡」时，照护卡中的展示字段才会临时保存在我们的服务器上以供只读网页访问。",
        },
        "uses": {
            "en": [
                "<b>Camera and photo library</b>: used only to capture or pick photos of pet food labels, human foods, plants or vet lab reports that you choose to check.",
                "<b>Cloud AI processing (Google Gemini)</b>: submitted photos, text notes and pet context (species, age and allergies) are sent over HTTPS via our managed server (Cloudflare Workers) to Google Gemini solely to produce your result. They are never used for advertising, linked to your identity or used to train third-party AI models. You can revoke AI consent anytime in Settings.",
                "<b>Shareable Care Card</b>: only when you create or update a care card link are the pet care details you entered (such as species, feeding notes, allergies, medications and emergency contact) stored on our server (Cloudflare Workers KV) for up to 90 days so family or a pet sitter can view the read-only page in a browser. Original scan photos are never included.",
                "<b>Anonymous device identifier</b>: a random, non-tracking device ID (not IDFA) is generated locally solely to count your 3 free scans per month.",
            ],
            "ja": [
                "<b>カメラ・写真ライブラリ</b>：原材料表示、食べ物・植物、検査結果の確認のために、ご自身で撮影・選択した画像のみを使用します。",
                "<b>クラウドAI処理（Google Gemini）</b>：送信した写真・入力テキスト・ペットの基本情報（犬・猫の別、年齢、アレルギー）は、結果の作成のみを目的として当社管理のサーバー（Cloudflare Workers）を経由してGoogle GeminiへHTTPSで送信されます。広告目的や第三者のAIモデルの学習には使用せず、個人を特定することもありません。設定画面からいつでもAIデータ送信の同意を取り消せます。",
                "<b>お世話カードの共有リンク</b>：お世話カードのリンクを作成・更新した場合のみ、入力したお世話情報（犬・猫の別、食事メモ、アレルギー、常備薬、緊急連絡先など）を当社サーバー（Cloudflare Workers KV）に最大90日間保存します。保存中は、家族やペットシッターがブラウザから閲覧できます。スキャン時の写真は含まれません。",
                "<b>匿名デバイスID</b>：毎月の無料スキャン回数（月3回）をカウントするためだけに端末内でランダムに生成されるID（IDFAではありません）を使用します。個人特定や追跡には使いません。",
            ],
            "zh": [
                "<b>相机与相册</b>：仅用于拍摄或选取你主动提交的宠粮配料表、人类食物、室内植物或医院化验单照片。",
                "<b>云端 AI 处理（Google Gemini）</b>：你提交的照片、补充文字与宠物基本信息（物种、年龄、过敏史）仅用于生成本次参考结果，会经由我们管理的服务器（Cloudflare Workers）通过 HTTPS 发送至 Google Gemini AI 处理，不用于广告、不关联真实身份，也不用于第三方 AI 模型训练。你随时可在「设置」中撤销同意。",
                "<b>宠物照护卡分享链接</b>：仅当你主动创建或更新照护卡链接时，你填写的照护信息（如物种、喂食说明、过敏史、常用药与紧急联系人）会在我们的服务器（Cloudflare Workers KV）上最多保留 90 天，供家人或寄养店通过浏览器查看只读页面。扫描上传的原始照片不会被包含。",
                "<b>匿名设备标识</b>：仅在 App 内随机生成非追踪用的匿名设备 ID（非 IDFA），用于统计每月 3 次免费扫描额度。",
            ],
        },
        "purchase": {
            "en": "PawClear includes 3 free scans every month and an optional auto-renewing subscription (PawClear Pro: Annual with a 14-day free trial, or Weekly) for unlimited scans. Payments are processed by Apple through the App Store; we never receive your payment details or Apple Account information. Subscriptions renew automatically unless cancelled at least 24 hours before the end of the current period in iPhone Settings > Apple Account > Subscriptions.",
            "ja": "PawClearは毎月3回まで無料でスキャンでき、回数無制限の自動更新サブスクリプション「PawClear Pro」（14日間の無料トライアル付き年額プラン／週額プラン）も用意しています。無料トライアル期間終了後は、期間終了の24時間前までに解約しない限り自動的に有料プランへ移行し、以降も自動更新されます。決済はApp Storeを通じてAppleが処理し、支払い情報やApple Accountの情報を当社が受け取ることはありません。購入後の管理・解約はiPhoneの「設定」＞Apple Account＞「サブスクリプション」からいつでも行えます。",
            "zh": "PawClear 每月提供 3 次免费扫描，另提供不限次数的自动续期订阅（PawClear Pro：含 14 天免费试用的年度方案或周度方案）。付款由 Apple 通过 App Store 处理，我们不会获取你的付款信息或 Apple 账户信息。除非在当前周期结束前至少 24 小时取消，订阅将自动续期，你随时可在 iPhone「设置」＞ Apple 账户 ＞「订阅」中管理或取消。",
        },
        "delete": {
            "en": "Your pet profiles and scan history are stored locally on your iPhone; deleting the app removes all local data. We do not store user accounts or keep copies of uploaded scan photos after generating your result. Shared care card pages expire automatically after up to 90 days.",
            "ja": "ペットのプロフィールとスキャン履歴はiPhone内に保存され、アプリを削除するとすべて消去されます。当社サーバーにアカウント情報や送信済みの写真を保存することはありません。共有したお世話カードのデータは最大90日で自動的に削除されます。",
            "zh": "你的宠物档案和历史扫描记录均保存在 iPhone 本机，删除 App 即全部清除。我们的服务器不保存用户账号，也不会在生成结果后留存你上传的扫描照片。已分享的宠物照护卡链接数据将在最多 90 天后自动过期删除。",
        },
        "kids": {
            "en": "PawClear is a pet care reference tool for pet owners and does not knowingly collect personal information from children.",
            "ja": "本アプリは飼い主向けのペットケア参考ツールであり、お子さまの個人情報を意図的に収集することはありません。",
            "zh": "本 App 面向宠物主人提供日常照护参考，不会故意收集儿童的个人信息。",
        },
        "safety_h": {"en": "Veterinary disclaimer", "ja": "獣医療に関するご注意", "zh": "兽医免责声明"},
        "safety": {
            "en": "PawClear provides information for reference only and does not replace a licensed veterinarian. If your pet seems unwell or may have eaten something toxic, contact your vet immediately.",
            "ja": "この結果は参考情報であり、獣医師の判断に代わるものではありません。いつもと様子が違う場合や、誤って何かを食べてしまったおそれがある場合は、早めに獣医師にご相談ください。",
            "zh": "PawClear 提供的解读结果仅供参考，不能替代持证兽医的专业判断。如宠物出现异常或疑似误食危险物品，请立即联系兽医就医。",
        },
        "faq": {
            "en": [
                ("I subscribed to PawClear Pro, but my scan limit did not unlock.", "Open Settings in PawClear and tap Restore Purchases while signed in with the same Apple Account you used to subscribe."),
                ("How do I cancel or manage my subscription?", "Open iPhone Settings > Apple Account > Subscriptions and select PawClear."),
                ("How do I revoke AI data sharing consent?", "Open Settings inside PawClear to review or revoke your cloud AI consent at any time. Your saved pet profiles and past scan history remain viewable offline."),
                ("How long does a shared Care Card link stay active?", "Each Care Card link remains viewable in a browser for up to 90 days and can be refreshed anytime from the pet's detail screen."),
                ("Will I lose my pets and scan history if I switch iPhones?", "Your records are stored on your iPhone. Transferring via iCloud or an encrypted computer backup preserves them."),
            ],
            "ja": [
                ("PawClear Proに登録したのに制限が解除されない", "アプリ内の「設定」を開き、「購入を復元」をタップしてください。購入時に使用したApple Accountでサインインしていることをご確認ください。"),
                ("サブスクリプションの解約・変更方法", "iPhoneの「設定」＞Apple Account＞「サブスクリプション」からPawClearを選択して管理・解約できます。"),
                ("AIデータ送信の同意を取り消すには", "アプリ内の「設定」画面からいつでも同意を取り消せます。同意を取り消した後も、保存済みのペット情報や過去のスキャン履歴はオフラインで確認できます。"),
                ("共有したお世話カードはいつまで閲覧できますか？", "作成したリンクは最大90日間ブラウザで閲覧できます。ペット詳細画面からいつでも最新の内容に更新できます。"),
                ("機種変更するとペット情報や履歴は消えますか？", "データはiPhone内に保存されています。iCloudまたはパソコン上の暗号化されたバックアップから新しいiPhoneへ移行すると引き継げます。"),
            ],
            "zh": [
                ("已经订阅了 PawClear Pro，但还是提示次数受限。", "请在 PawClear 的「设置」中点击「恢复购买」，并确认当前登录的是订阅时使用的同一个 Apple 账户。"),
                ("如何取消或管理订阅？", "打开 iPhone「设置」＞ Apple 账户 ＞「订阅」，找到 PawClear 即可管理或取消。"),
                ("如何撤销云端 AI 上传授权？", "随时可在 PawClear 的「设置」页查看并撤销同意。撤销后，已保存的宠物档案和历史扫描记录仍可离线查看。"),
                ("分享出去的宠物照护卡链接有效多久？", "每个照护卡链接最长可在浏览器中查看 90 天，随时可在宠物详情页重新生成最新链接。"),
                ("换手机后宠物档案和历史记录会丢失吗？", "数据保存在 iPhone 本机，通过 iCloud 或电脑加密备份迁移到新 iPhone 即可保留。"),
            ],
        },
    },
    "shelfflip": {
        "name": {"en": "ShelfFlip", "ja": "ShelfFlip", "zh": "ShelfFlip"},
        "updated": {"en": "Last updated: 28 November 2026", "ja": "最終更新日：2026年11月28日", "zh": "最后更新：2026年11月28日"},
        "desc": {
            "en": "Snap a thrift or secondhand find to check recent resale comps, calculate net profit after marketplace fees and shipping, draft ready-to-post listings, and track your inventory and monthly profit.",
            "ja": "商品の写真を1〜2枚撮るだけで、フリマ・オークションの相場と手数料・送料を引いた見込み利益をすぐ確認。出品文の作成から在庫管理、月ごとの純利益の集計までまとめて行えるアプリです。",
            "zh": "拍 1～2 张二手商品照片，几秒查询近期成交行情、自动扣除平台手续费和运费计算预计净利润，一键生成可直接粘贴的上架文案，并管理待卖库存与月度利润账本。",
        },
        "summary": {
            "en": "{app} requires no account, contains no ads and does not track you across apps or websites. Your inventory and profit ledger stay on your iPhone. Only when you run a price lookup—and only after you agree on the consent screen—are the item photos, target marketplace, item note and buy cost sent via our managed server to Google Gemini AI solely to generate your resale estimate and listing draft.",
            "ja": "{app}はアカウント登録が不要で、広告や他社アプリ・Webサイトをまたぐトラッキングはありません。在庫データや利益の記録はすべてiPhone内に保存されます。相場チェックを実行し、事前の同意画面で同意した場合のみ、送信した商品写真・出品先・商品名メモ・仕入れ値が当社管理のサーバーを経由してGoogle Geminiへ送信されます。",
            "zh": "{app} 无需注册账号，不含广告，也不进行跨 App 或跨网站追踪。你的库存清单与利润账本均保存在 iPhone 本机。只有当你主动发起行情查询并在知情同意页明确同意后，你提交的商品照片、目标平台、商品备注与买入成本才会经由我们管理的服务器发送至 Google Gemini AI，且仅用于生成本次行情参考与上架文案。",
        },
        "uses": {
            "en": [
                "<b>Camera and photo library</b>: used only to capture or pick photos of secondhand items that you choose to appraise.",
                "<b>Cloud AI processing (Google Gemini)</b>: submitted photos, target marketplace, item notes and buy cost are sent over HTTPS via our managed server (Cloudflare Workers) to Google Gemini solely to produce your resale estimate and listing draft. They are never used for advertising, linked to your identity or used to train third-party AI models. You can revoke AI consent anytime in Settings.",
                "<b>Anonymous device identifier</b>: a random, non-tracking device ID (not IDFA) is generated locally solely to count your 3 free lookups per month and enforce fair-use rate limits.",
            ],
            "ja": [
                "<b>カメラ・写真ライブラリ</b>：相場を調べるために、ご自身で撮影・選択した商品の画像のみを使用します。",
                "<b>クラウドAI処理（Google Gemini）</b>：送信した商品写真・出品先・商品名メモ・仕入れ値は、相場チェックと出品文の作成のみを目的として当社管理のサーバー（Cloudflare Workers）を経由してGoogle GeminiへHTTPSで送信されます。広告目的や第三者のAIモデルの学習には使用せず、個人を特定することもありません。設定画面からいつでもAIデータ送信の同意を取り消せます。",
                "<b>匿名デバイスID</b>：毎月の無料枠（月3回）のカウントおよびフェアユース管理のためだけに端末内でランダムに生成されるID（IDFAではありません）を使用します。個人特定や追跡には使いません。",
            ],
            "zh": [
                "<b>相机与相册</b>：仅用于拍摄或选取你主动提交估价的商品照片。",
                "<b>云端 AI 处理（Google Gemini）</b>：你提交的商品照片、目标平台、商品备注与买入成本仅用于生成本次行情参考与上架文案，会经由我们管理的服务器（Cloudflare Workers）通过 HTTPS 发送至 Google Gemini AI 处理，不用于广告、不关联真实身份，也不用于第三方 AI 模型训练。你随时可在「设置」中撤销同意。",
                "<b>匿名设备标识</b>：仅在 App 内随机生成非追踪用的匿名设备 ID（非 IDFA），用于统计每月 3 次免费查询额度与合理使用防滥用限流。",
            ],
        },
        "purchase": {
            "en": "ShelfFlip includes 3 free cloud lookups every month and an optional auto-renewing subscription (ShelfFlip Pro: Annual with a 7-day free trial, or Weekly) for daily sourcing lookups and listing drafts (fair-use limits apply). Payments are processed by Apple through the App Store; we never receive your payment details or Apple Account information. Subscriptions renew automatically unless cancelled at least 24 hours before the end of the current period in iPhone Settings > Apple Account > Subscriptions.",
            "ja": "ShelfFlipは毎月3回まで無料で相場チェックができ、日々の仕入れ・出品向けの自動更新サブスクリプション「ShelfFlip Pro」（7日間の無料トライアル付き年額プラン／週額プラン、フェアユース上限あり）も用意しています。無料トライアル期間終了後は、期間終了の24時間前までに解約しない限り自動的に有料プランへ移行し、以降も自動更新されます。決済はApp Storeを通じてAppleが処理し、支払い情報やApple Accountの情報を当社が受け取ることはありません。購入後の管理・解約はiPhoneの「設定」＞Apple Account＞「サブスクリプション」からいつでも行えます。",
            "zh": "ShelfFlip 每月提供 3 次免费查询，另提供面向日常高频淘货的自动续期订阅（ShelfFlip Pro：含 7 天免费试用的年度方案或周度方案，适用合理使用额度）。付款由 Apple 通过 App Store 处理，我们不会获取你的付款信息或 Apple 账户信息。除非在当前周期结束前至少 24 小时取消，订阅将自动续期，你随时可在 iPhone「设置」＞ Apple 账户 ＞「订阅」中管理或取消。",
        },
        "delete": {
            "en": "Your inventory items and profit ledger are stored locally on your iPhone; deleting the app removes all local data. We do not store user accounts or keep copies of uploaded item photos after generating your result.",
            "ja": "在庫データや利益の記録はiPhone内に保存され、アプリを削除するとすべて消去されます。当社サーバーにアカウント情報や送信済みの商品写真を保存することはありません。",
            "zh": "你的库存清单和利润账本均保存在 iPhone 本机，删除 App 即全部清除。我们的服务器不保存用户账号，也不会在生成结果后留存你上传的商品照片。",
        },
        "kids": {
            "en": "ShelfFlip is a resale pricing and inventory tool and does not knowingly collect personal information from children.",
            "ja": "本アプリはリセール向けの相場・在庫管理ツールであり、お子さまの個人情報を意図的に収集することはありません。",
            "zh": "本 App 为二手转卖估价与库存管理工具，不会故意收集儿童的个人信息。",
        },
        "safety_h": {"en": "Marketplace & estimate disclaimer", "ja": "相場・手数料に関するご注意", "zh": "行情与平台免责说明"},
        "safety": {
            "en": "ShelfFlip is an independent tool and is not affiliated with or endorsed by eBay, Poshmark, Depop, Mercari or Yahoo! Auctions. Price ranges, marketplace fees, shipping costs and profit estimates are for reference only.",
            "ja": "本アプリは各マーケットプレイスとは提携していない独立したツールです。表示される相場・販売手数料・送料・見込み利益は参考値であり、実際の売却価格や各サービスの最新条件は出品先にてご確認ください。",
            "zh": "ShelfFlip 为独立工具，与 eBay、Poshmark、Depop、Mercari 或 Yahoo! 拍卖无任何隶属或合作关系。页面展示的成交区间、手续费率、运费与净利润测算仅供参考，请以各平台最新规则及实际成交为准。",
        },
        "faq": {
            "en": [
                ("I subscribed to ShelfFlip Pro, but my lookups did not unlock.", "Open Settings in ShelfFlip and tap Restore Purchases while signed in with the same Apple Account you used to subscribe."),
                ("How do I cancel or manage my subscription?", "Open iPhone Settings > Apple Account > Subscriptions and select ShelfFlip."),
                ("How do I revoke AI data sharing consent?", "Open Settings inside ShelfFlip to review or revoke your cloud AI consent at any time. Your saved inventory and profit ledger remain viewable offline."),
                ("Why is there a fair-use limit on ShelfFlip Pro?", "Each lookup runs live web search grounding and AI image analysis. Fair-use daily and monthly caps are sized generously for everyday thrifting while keeping responses fast and preventing automated abuse."),
                ("Will I lose my inventory and profit records if I switch iPhones?", "Your records are stored on your iPhone. Transferring via iCloud or an encrypted computer backup preserves them."),
            ],
            "ja": [
                ("ShelfFlip Proに登録したのに制限が解除されない", "アプリ内の「設定」を開き、「購入を復元」をタップしてください。購入時に使用したApple Accountでサインインしていることをご確認ください。"),
                ("サブスクリプションの解約・変更方法", "iPhoneの「設定」＞Apple Account＞「サブスクリプション」からShelfFlipを選択して管理・解約できます。"),
                ("AIデータ送信の同意を取り消すには", "アプリ内の「設定」画面からいつでも同意を取り消せます。同意を取り消した後も、保存済みの在庫や利益の記録はオフラインで確認できます。"),
                ("Proプランにも利用回数の上限があるのはなぜですか？", "リアルタイムの相場検索と画像解析を安定して高速に提供し、不正な大量アクセスを防ぐため、日々の仕入れには十分な範囲で一定のフェアユース上限を設けています。"),
                ("機種変更すると在庫や利益データは消えますか？", "データはiPhone内に保存されています。iCloudまたはパソコン上の暗号化されたバックアップから新しいiPhoneへ移行すると引き継げます。"),
            ],
            "zh": [
                ("已经订阅了 ShelfFlip Pro，但还是提示次数受限。", "请在 ShelfFlip 的「设置」中点击「恢复购买」，并确认当前登录的是订阅时使用的同一个 Apple 账户。"),
                ("如何取消或管理订阅？", "打开 iPhone「设置」＞ Apple 账户 ＞「订阅」，找到 ShelfFlip 即可管理或取消。"),
                ("如何撤销云端 AI 上传授权？", "随时可在 ShelfFlip 的「设置」页查看并撤销同意。撤销后，已保存的库存清单和利润账本仍可离线查看。"),
                ("为什么 ShelfFlip Pro 也有合理使用额度？", "每次查价都会实时联网检索成交行情并解析商品图片。合理使用上限按日常个人淘货高频使用设计，用于保障查询速度稳定并防止异常刷量。"),
                ("换手机后库存和账本数据会丢失吗？", "数据保存在 iPhone 本机，通过 iCloud 或电脑加密备份迁移到新 iPhone 即可完整保留。"),
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
        updated = app.get("updated", UPDATED)[c]
        summary = app.get("summary", T["summary"])[c].format(app=name)
        uses = "".join(f"<li>{u}</li>" for u in app["uses"][c])
        purchase = app.get("purchase", T["purchase"])[c]
        delete = app.get("delete", T["delete"])[c]
        kids = app.get("kids", T["kids"])[c]
        safety_block = ""
        if "safety" in app:
            safety_block = f"<h2>{app['safety_h'][c]}</h2><p>{app['safety'][c]}</p>\n"
        parts.append(f"""<section class="lang" id="{c}" lang="{'zh-Hans' if c == 'zh' else c}">
<h1>{name} — {T['privacy'][c]}</h1><p class="muted">{updated}</p>
<h2>{T['summary_h'][c]}</h2><p>{summary}</p>
<h2>{T['uses_h'][c]}</h2><ul>{uses}</ul><p>{T['uses_note'][c]}</p>
<h2>{T['purchase_h'][c]}</h2><p>{purchase}</p>
<h2>{T['delete_h'][c]}</h2><p>{delete}</p>
{safety_block}<h2>{T['kids_h'][c]}</h2><p>{kids}</p>
<h2>{T['changes_h'][c]}</h2><p>{T['changes'][c]}</p>
<h2>{T['contact_h'][c]}</h2><p>{T['contact'][c]}<a href="mailto:{EMAIL}">{EMAIL}</a></p>
</section>""")
    return page(f"{app['name']['en']} — Privacy Policy", "".join(parts))


def support(key, app):
    parts = [lang_nav()]
    for c, _ in LANGS:
        faq_items = app.get("faq", T["faq"])[c]
        faq = "".join(f"<h2>{q}</h2><p>{a}</p>" for q, a in faq_items)
        safety_block = ""
        if "safety" in app:
            safety_block = f"\n<h2>{app['safety_h'][c]}</h2><p>{app['safety'][c]}</p>"
        parts.append(f"""<section class="lang" id="{c}" lang="{'zh-Hans' if c == 'zh' else c}">
<h1>{app['name'][c]} — {T['support'][c]}</h1><p>{app['desc'][c]}</p>
<p><a class="btn" href="mailto:{EMAIL}?subject={html.escape(app['name']['en'])}">{T['email_us'][c]}</a></p>
<p class="muted">{EMAIL} · {T['reply'][c]}</p>
{faq}{safety_block}
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
