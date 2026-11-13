Myanmar Sign Language (MSL) Project — Team Member လမ်းညွှန် (အစအဆုံး)
အားလုံးပဲ မင်္ဂလာပါ။ ကိုယ့်ရဲ့ လက်ဟန် Data တွေကို စုဆောင်းပြီး GitHub ပေါ် တင်ပေးရမယ့် အဆင့်တွေကို အလွယ်ကူဆုံး ဖြစ်အောင် စီစဉ်ပေးထားပါတယ်။ အောက်ပါ အဆင့် ၄ ဆင့်အတိုင်း တစ်ဆင့်ချင်းစီ လိုက်လုပ်ပေးကြပါနော်။

အဆင့် (၁) - တစ်ခါသာ လုပ်ရမည့် Setup (First-Time Setup)
GitHub Invite လက်ခံပါ:

ကိုယ့် Gmail ထဲကို GitHub ကနေ ပို့ထားတဲ့ Invitation Email ကိုဖွင့်ပြီး Accept invitation ကို နှိပ်ပါ။

Project ကို စက်ထဲ ဆွဲချပါ (Clone):

ကိုယ့်ကွန်ပျူတာမှာ Folder တစ်ခု ဖွင့်ပါ (ဥပမာ - D:\Projects)၊ အဲ့ဒီ Folder ထဲမှာ Right-click → Open in Terminal (သို့မဟုတ် VS Code Terminal) ကို ဖွင့်ပြီး အောက်က command ကို ရိုက်ထည့်ပါ-

PowerShell
git clone https://github.com/MinKhant30/msl-prototype.git
cd msl-prototype
Python Environment နှင့် Library များ သွင်းပါ:

အောက်က command ၃ ကြောင်းကို တစ်ကြောင်းချင်းစီ run ပေးပါ-

PowerShell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
(မှတ်ချက် - .venv\Scripts\activate run လိုက်ရင် ရှေ့ဆုံးမှာ (.venv) ဆိုပြီး အစိမ်းရောင်လေး ပေါ်လာရပါမယ်။)

hand_landmarker.task ဖိုင် ထည့်ပါ:

Group Chat မှာ ပို့ပေးထားတဲ့ hand_landmarker.task ဖိုင်ကို ဒေါင်းလုဒ်ဆွဲပြီး msl-prototype\models\ folder ထဲကို ကူးထည့်ပေးပါ။

အဆင့် (၂) - နောက်ဆုံးရ Update များ ဆွဲချပြီး Data စကောက်ပါ (က၊ ခ၊ ဂ)
Project ကို Up-to-date ဖြစ်အောင် အရင်ဆွဲချပါ (Pull):

နောက်ဆုံးတင်ထားတဲ့ code အသစ်တွေနဲ့ တခြားသူတွေရဲ့ data တွေ ရအောင် Data မကောက်ခင်တိုင်း ဒီ ၂ ကြောင်းကို အရင် run ပါ-

PowerShell
git checkout main
git pull origin main
Data ကောက်မယ့် script ကို run ပါ:

PowerShell
python scripts/01_collect_data.py
Access Key ရိုက်ထည့်ပါ (ပထမဆုံး တစ်ကြိမ်သာ):

Team Leader ဆီက ရထားတဲ့ ကိုယ်ပိုင် လျှို့ဝှက် Key ကို ရိုက်ထည့်ပြီး Enter နှိပ်ပါ။ (ကိုယ့်နာမည် မှန်မမှန် စစ်ပါ။ နောက်တစ်ခါ ပြန် run ရင် Key ထပ်ရိုက်စရာ မလိုတော့ဘဲ Auto မှတ်ထားပေးပါလိမ့်မယ်။)

Camera ပွင့်လာရင် လက်ဟန် ၃ မျိုးကို တစ်မျိုးစီ အနည်းဆုံး 200 samples စီ ကောက်ပါ:

Keyboard 1 ကို ဖိထားပါ → က လက်ဟန် လုပ်ပြပါ (200 ပြည့်တဲ့အထိ)

Keyboard 2 ကို ဖိထားပါ → ခ လက်ဟန် လုပ်ပြပါ (200 ပြည့်တဲ့အထိ)

Keyboard 3 ကို ဖိထားပါ → ဂ လက်ဟန် လုပ်ပြပါ (200 ပြည့်တဲ့အထိ)

သတိထားရမည့် အချက်များ:

လက်ကို တစ်နေရာတည်း အသေမထားဘဲ ကင်မရာနဲ့ နည်းနည်း အနီး/အဝေး၊ ဘယ်/ညာ၊ ထောင့်အမျိုးမျိုး နည်းနည်းစီ ရွှေ့ပြီး ကောက်ပေးပါ။

မှားနှိပ်မိရင် Z ကို နှိပ်ပြီး နောက်ဆုံး ကောက်ထားတာကို ပြန်ဖျက် (Undo) လို့ ရပါတယ်။

၃ မျိုးလုံး 200 စီ (စုစုပေါင်း 600) ပြည့်သွားရင် Q ကို နှိပ်ပြီး ပိတ်လိုက်ပါ။

အဆင့် (၃) - ကိုယ့် Data ကို စမ်းသပ်ကြည့်ပါ (Optional)
ကိုယ်ကောက်ထားတဲ့ လက်ဟန် မှန်မမှန် စမ်းကြည့်ချင်ရင် ဒီ ၂ ကြောင်း run ပြီး Browser မှာ [http://127.0.0.1:8000](http://127.0.0.1:8000) ကို ဖွင့်စမ်းလို့ ရပါတယ်-

PowerShell
python scripts/02_train_model.py
uvicorn app.main:app --reload
(စမ်းပြီးရင် Terminal မှာ Ctrl + C နှိပ်ပြီး server ကို ပြန်ပိတ်ပါ။)

အဆင့် (၄) - GitHub ပေါ်သို့ Data တင်ပါ (Submit & Pull Request)
Git command တွေ အများကြီး ရိုက်စရာ မလိုပါဘူး။ ဒီ script တစ်ခုတည်းကို run လိုက်ရုံပါပဲ-

PowerShell
python scripts/submit_data.py
(ဒီ script က ကိုယ့်နာမည်နဲ့ Branch အသစ် အလိုအလျောက် ခွဲပေးပြီး ကိုယ့်ရဲ့ .csv ဖိုင် တစ်ဖိုင်တည်းကိုပဲ ရွေးပြီး GitHub ပေါ် တင်ပေးသွားပါလိမ့်မယ်။ ပထမဆုံးအကြိမ် Push လုပ်ချိန်မှာ Browser ပွင့်လာပြီး GitHub Sign-in တစ်ခါ လုပ်ခိုင်းနိုင်ပါတယ်။)

နောက်ဆုံးအဆင့် (Pull Request ဖွင့်ခြင်း):

Browser ကနေ [https://github.com/MinKhant30/msl-prototype](https://github.com/MinKhant30/msl-prototype) ကို သွားပါ။

အပေါ်ဆုံးမှာ အဝါရောင်တန်းလေးနဲ့ "Compare & pull request" ဆိုတဲ့ ခလုတ် ပေါ်နေပါလိမ့်မယ်။ အဲ့ဒါကို နှိပ်ပါ။

အစိမ်းရောင် "Create pull request" ခလုတ်ကို နှိပ်လိုက်ရင် ပြီးပါပြီ! Group Chat မှာ "PR ဖွင့်ပြီးပါပြီ" လို့ အကြောင်းကြားပေးပါ။

💡 မှတ်သားထားရန် (Up-to-date ဖြစ်နေစေရန်)
အဖွဲ့သားတွေရဲ့ Data အသစ်တွေ၊ Code အသစ်တွေ လိုချင်တိုင်း (သို့မဟုတ် Data အသစ် ထပ်မကောက်ခင်တိုင်း) အဆင့် (၂) ရဲ့ နံပါတ် (၁) အတိုင်း git checkout main နှင့် git pull origin main ကို အရင် run ပြီးမှ စလုပ်ပေးပါ။

Error တက်ရင် Error စာသားကို Screenshot ရိုက်ပြီး Group Chat ထဲ ပို့ပေးပါ။