# 🇲🇲 Myanmar Sign Language (MSL) Project — Team Member လမ်းညွှန်

> **ရည်ရွယ်ချက်:** အဖွဲ့သားတစ်ဦးချင်းစီ၏ လက်ဟန် Data များကို စုဆောင်းပြီး GitHub Repository ပေါ်သို့ စနစ်တကျ ပေးပို့နိုင်ရန် အစအဆုံး လမ်းညွှန်ဖြစ်ပါသည်။

---

## 📋 အဆင့် (၁) - တစ်ခါသာ လုပ်ရမည့် Setup (First-Time Setup)

### ၁. GitHub Invite လက်ခံပါ
* ကိုယ့် Gmail ထဲသို့ GitHub မှ ပို့ထားသော **Invitation Email** ကိုဖွင့်ပြီး **Accept invitation** ခလုတ်ကို နှိပ်ပါ။

### ၂. Project ကို စက်ထဲသို့ ဆွဲချပါ (Clone)
ကွန်ပျူတာတွင် Folder တစ်ခု ဖွင့်ပါ (ဥပမာ - `D:\Projects`)၊ ထို Folder ထဲတွင် **Right-click → Open in Terminal** (သို့မဟုတ် VS Code Terminal) ကို ဖွင့်ပြီး အောက်ပါ command ကို ရိုက်ထည့်ပါ-

```powershell
git clone [https://github.com/MinKhant30/msl-prototype.git](https://github.com/MinKhant30/msl-prototype.git)
cd msl-prototype
```

### ၃. Python Environment နှင့် Library များ သွင်းပါ
အောက်ပါ command ၃ ကြောင်းကို တစ်ကြောင်းချင်းစီ run ပေးပါ-

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

> 💡 **မှတ်ချက်:** `.venv\Scripts\activate` run ပြီးပါက Terminal ရှေ့ဆုံးတွင် `(.venv)` ဟူသော အစိမ်းရောင် စာတန်းလေး ပေါ်လာရပါမည်။

### ၄. `hand_landmarker.task` ဖိုင် ထည့်ပါ
* Group Chat တွင် ပို့ပေးထားသော **`hand_landmarker.task`** ဖိုင်ကို ဒေါင်းလုဒ်ဆွဲပြီး `msl-prototype\models\` folder ထဲသို့ ကူးထည့်ပေးပါ။

---

## 🎥 အဆင့် (၂) - Update ဆွဲချပြီး Data စတင်ကောက်ယူပါ (`က`၊ `ခ`၊ `ဂ`)

### ၁. Project ကို Up-to-date ဖြစ်အောင် အရင်ဆွဲချပါ (Pull)
နောက်ဆုံးရ code အသစ်များနှင့် အခြားအဖွဲ့သားများ၏ data များ ရရှိစေရန် Data မကောက်ခင်တိုင်း အောက်ပါ ၂ ကြောင်းကို အရင် run ပါ-

```powershell
git checkout main
git pull origin main
```

### ၂. Data ကောက်မည့် Script ကို Run ပါ

```powershell
python scripts/01_collect_data.py
```

### ၃. Access Key ရိုက်ထည့်ပါ (ပထမဆုံး တစ်ကြိမ်သာ)
* Team Leader ဆီမှ ရရှိထားသော ကိုယ်ပိုင် လျှို့ဝှက် Key ကို ရိုက်ထည့်ပြီး **Enter** နှိပ်ပါ။
* ကိုယ့်နာမည် မှန်/မမှန် စစ်ဆေးပါ။ *(နောက်တစ်ကြိမ် ပြန် run ပါက Key ထပ်ရိုက်စရာ မလိုတော့ဘဲ Auto မှတ်ထားပေးပါမည်။)*

### ၄. လက်ဟန် ၃ မျိုးကို တစ်မျိုးစီ အနည်းဆုံး `200 samples` စီ ကောက်ပါ

| Keyboard ခလုတ် | ပြရမည့် လက်ဟန် | ကောက်ယူရမည့် အရေအတွက် |
| :---: | :---: | :---: |
| **`1`** (ဖိထားပါ) | **`က`** | `200 samples` |
| **`2`** (ဖိထားပါ) | **`ခ`** | `200 samples` |
| **`3`** (ဖိထားပါ) | **`ဂ`** | `200 samples` |

> ⚠️ **Data အရည်အသွေး ကောင်းစေရန် သတိပြုရမည့် အချက်များ:**
> * လက်ကို တစ်နေရာတည်း အသေမထားဘဲ ကင်မရာနှင့် အနီး/အဝေး၊ ဘယ်/ညာ၊ ထောင့်အမျိုးမျိုး အနည်းငယ်စီ ရွှေ့ပြီး ကောက်ပေးပါ။
> * မှားနှိပ်မိပါက **`Z`** ကို နှိပ်ပြီး နောက်ဆုံး ကောက်ထားသည်ကို ပြန်ဖျက် (**Undo**) နိုင်ပါသည်။
> * ၃ မျိုးလုံး `200` စီ (စုစုပေါင်း `600`) ပြည့်သွားပါက **`Q`** ကို နှိပ်ပြီး ပိတ်လိုက်ပါ။

---

## 🧪 အဆင့် (၃) - ကိုယ့် Data ကို စမ်းသပ်ကြည့်ပါ (Optional)

ကိုယ်ကောက်ထားသော လက်ဟန် မှန်/မမှန် ကိုယ်တိုင် စမ်းသပ်ကြည့်လိုပါက အောက်ပါ ၂ ကြောင်းကို run ပြီး Browser တွင် `http://127.0.0.1:8000` ကို ဖွင့်စမ်းနိုင်ပါသည်-

```powershell
python scripts/02_train_model.py
uvicorn app.main:app --reload
```

> 💡 စမ်းသပ်ပြီးပါက Terminal တွင် **`Ctrl + C`** နှိပ်ပြီး server ကို ပြန်ပိတ်ပါ။

---

## 🚀 အဆင့် (၄) - GitHub ပေါ်သို့ Data တင်ပါ (Submit & Pull Request)

Git command များ အများကြီး ရိုက်စရာ မလိုပါ။ အောက်ပါ script တစ်ခုတည်းကို run လိုက်ရုံပါပဲ-

```powershell
python scripts/submit_data.py
```

* ဤ script က ကိုယ့်နာမည်ဖြင့် Branch အသစ် အလိုအလျောက် ခွဲပေးပြီး ကိုယ့်ရဲ့ `.csv` ဖိုင် တစ်ဖိုင်တည်းကိုသာ ရွေးချယ်၍ GitHub ပေါ်သို့ တင်ပေးသွားပါမည်။
* *(ပထမဆုံးအကြိမ် Push လုပ်ချိန်တွင် Browser ပွင့်လာပြီး GitHub Sign-in တစ်ခါ လုပ်ခိုင်းနိုင်ပါသည်။)*

### နောက်ဆုံးအဆင့် — Pull Request (PR) ဖွင့်ခြင်း
1. Browser မှ [GitHub Repository](https://github.com/MinKhant30/msl-prototype) သို့ သွားပါ။
2. အပေါ်ဆုံးတွင် အဝါရောင်တန်းလေးဖြင့် ပေါ်နေသော **"Compare & pull request"** ခလုတ်ကို နှိပ်ပါ။
3. အစိမ်းရောင် **"Create pull request"** ခလုတ်ကို နှိပ်လိုက်ပါ။
4. Group Chat တွင် *"PR ဖွင့်ပြီးပါပြီ"* ဟု အကြောင်းကြားပေးပါ။

---

## ❓ အမေးများသော အချက်များ (FAQ)

* **နောက်တစ်ခါ Data အသစ် ထပ်ကောက်ချင်ရင် ဘယ်က ပြန်စရမလဲ?**
  * အဆင့် (၁) ကို ပြန်လုပ်စရာ မလိုပါ။ **အဆင့် (၂)** ရဲ့ နံပါတ် (၁) (`git checkout main` နှင့် `git pull origin main`) ကနေ ပြန်စလုပ်ရုံပါပဲ။
* **Error တစ်ခုခု တက်ရင် ဘာလုပ်ရမလဲ?**
  * Terminal မှ Error စာသားကို Screenshot ရိုက်ပြီး Group Chat ထဲသို့ ပို့ပေးပါ။