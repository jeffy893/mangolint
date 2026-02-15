# Mangolint Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Start the Application
```bash
cd mangolint
source venv/bin/activate
python3.10 app.py
```
Open: **http://localhost:5001**

### 2. Try Example Text
Open `example_usages.txt` and copy this:
```
Our organic skincare line uses mango butter, turmeric extract, and coconut oil.
```

Paste into the text editor and wait 500ms (or click "Analyze Text")

### 3. Explore Results
- See underlined ingredients (mango, turmeric, coconut)
- Click underlined words to jump to details
- Review indigenous synonyms in sidebar
- Check brand insights and authenticity markers

## 📋 20 Ready-to-Use Examples

File: `example_usages.txt`

Categories:
- Single ingredients (mango, turmeric)
- Spice blends (curry, tea)
- Product descriptions (skincare, beverages)
- Recipes (traditional, modern)
- Superfoods and grains
- Aromatic descriptions

## 🧪 Run Tests

```bash
python3.10 run_tests.py
```

Results:
- ✅ 12 tests passed
- Report saved to `test_report.txt`
- Coverage: Unit + Integration tests

## 📖 What You'll See

### For "mango":
**Indigenous Synonyms:**
- Manga (Portuguese) - ripeness: verde vs madura
- Aam (Hindi) - stages: kairi (raw) vs aam (ripe)
- Māṅgāy (Tamil) - green for pickles, ripe for eating
- Mangga (Tagalog) - preference for semi-ripe

**Brand Insights:**
- Specify ripeness stage for authenticity
- Reference cultural preparation methods

**Traditional Uses:**
- Culinary: fresh, dried, pickled
- Medicinal: digestive aid, vitamin C
- Ceremonial: leaves in Hindu rituals

## 🎯 Key Features

1. **Real-time linting** - 500ms debounce after typing
2. **Visual overlays** - Colored underlines on ingredients
3. **Click interaction** - Jump to details in sidebar
4. **Cultural depth** - Etymology, traditional knowledge
5. **Brand anthropology** - Authenticity markers

## 📚 Documentation

- `README.md` - Full documentation
- `TESTING.md` - Testing guide
- `DEPLOYMENT.md` - Deployment instructions
- `example_usages.txt` - 20 examples to try

## 🔧 Troubleshooting

**Port 5000 in use?**
- Edit `.env` and change `PORT=5001`

**AWS credentials?**
- Uses `~/.aws/credentials` automatically
- No need to copy credentials to project

**Tests failing?**
- Run `python3.10 run_tests.py` for detailed report
- Check `test_report.txt` for specifics

## 💡 Pro Tips

1. Try single words first (mango, turmeric, vanilla)
2. Then try product descriptions with multiple ingredients
3. Click underlined words to explore details
4. Compare indigenous synonyms across cultures
5. Use brand insights for authentic marketing

## 🎨 Example Workflow

1. **Type**: "Traditional curry with turmeric and ginger"
2. **Wait**: 500ms for auto-analysis
3. **See**: Underlined ingredients
4. **Click**: "turmeric" to see Haldi (Hindi), Manjal (Tamil)
5. **Learn**: Ayurvedic uses, ceremonial significance
6. **Apply**: Use authentic terms in your brand story

---

**Ready to explore?** Open http://localhost:5001 and start typing!
