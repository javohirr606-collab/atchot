# SIMO · 1-kun: qayta montaj (reels + 16:9)

Asl material: Telegram orqali yuborilgan «SIMO birinchi kun» montaji (`src/assets/source.mp4`, 268×480, 4:17).
Undan ikki video yig‘ilgan, diktor yo‘q: faqat tashkilotchi, talabalar va ustozlarning o‘z gaplari.

| Fayl | Format | Davomiyligi |
|---|---|---|
| `AIFU_SIMO_1-kun_reels.mp4` | 1080×1920, Reels / Shorts / TikTok | 0:49 |
| `AIFU_SIMO_1-kun_16x9.mp4` | 1920×1080, YouTube / Telegram / ekran | 1:33 |

## Tuzilishi
**Reels.** Hook: tashkilotchining savoli «Olimpiadalarda masalalar qanaqa tuziladi?» (imtihondan tez kadrlar, soat chiqillashi) →
SIMO titri → tashkilotchi: masalalar oylab oldin, mutaxassislar tomonidan tuziladi, yangi masala → «540 nafar talaba
ro‘yxatdan o‘tdi» hisoblagichi → «4,5 soat · 5 ta masala» → universitetlar: Namangan, Toshkent, Samarqand → talaba fikri →
«Fields, Abel mukofotlariga sazovor matematiklar chiqadi degan umiddamiz» (Evergreen) → yakuniy kartochka, 78 555 21 21.

**16:9.** 5 bob: 01 Ochilish, 02 Tashkilotchi, 03 Olimpiada, 04 Ishtirokchilar, 05 Kelajak. Montaj qismlarida 3 ta vertikal panel,
intervyularda chapda spiker, o‘ngda ism-lavozim va so‘zma-so‘z yonib boradigan matn.

## Ovoz
- Asl montajdagi musiqa nutqdan ajratib olingan (UVR-MDX-NET, `tools/separate.py` → `src/assets/audio/speech.m4a`).
  Har bir gap bir xil balandlikka keltirilgan, EQ va kompressor bilan tozalangan.
- Musiqa: perkussiya (hook–montaj), Evergreen (yakuniy fikr). Nutq ostida musiqa kamida 13 dB past.
- Effektlar sintez qilingan: soat chiqillashi, whoosh, boom, pop, hisoblagich, chime. Yakuniy balandlik −14 LUFS, cho‘qqi −1.5 dBTP.
- Asl faylda ovoz −9.7 LUFS va +1.2 dBFS (kesilish) edi; bu yerda tuzatilgan.

## Subtitrlar va faktlar
Matnlar nutqni avtomatik tanib olish (Omnilingual ASR) bilan olingan va qo‘lda tuzatilgan. Videoda faqat aytilgan gaplar bor.
Tekshirib olish kerak bo‘lgan joylar:
- **540 nafar talaba** — ochilish nutqidan («…oliy taʼlim muassasasidan besh yuz qirq nafar talaba roʻyxatdan oʻtdi»).
- **4,5 soat · 5 ta masala** — ustoz gapidan («bu yerda toʻrt yarim soatda beshta masala ustida bosh qotiradi»).
- **Shahnoza Abdurahimova** familiyasining yozilishi.
- Tashkilotchining ismi, «Matematika instituti»ning to‘liq nomi va ochilishda gapirgan, «Savollar darajasi…» va
  «Olimpiada masalalari…» degan ustozlarning ism-lavozimi aniqlanmadi: ularga ism yozilmagan.
- «SIMO» to‘liq nomi kadrlarda yo‘q; «Xalqaro matematika olimpiadasi» deb yozilgan (tashkilotchi «xalqaro darajadagi olimpiada» deydi, zalda bayroqlar).

## Qayta yig‘ish
```bash
./tools/frames.sh                 # src/frames/: manba kadrlari 720×1280, 30 kadr/s (7721 ta)
python3 tools/mix.py reel         # build/mix_reel.wav   (numpy kerak)
python3 tools/mix.py wide         # build/mix_wide.wav
node tools/render.mjs reel        # build/AIFU_SIMO_1-kun_reels.mp4
node tools/render.mjs wide        # build/AIFU_SIMO_1-kun_16x9.mp4
./tools/sheet.sh reel out.jpg 1 5 20   # tekshirish uchun kadrlar
```
Montaj ro‘yxati, gaplar va vaqtlar bitta faylda: `src/edit.js`. Sahifalar: `src/reel.html`, `src/wide.html`
(brauzerda ochib, probel bilan ijro etish mumkin).
