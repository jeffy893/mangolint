# Mangolint Demo Mode

## 🎭 What is Demo Mode?

Demo Mode uses a mock linter that returns predefined responses for common ingredients **without requiring AWS Bedrock credentials**. Perfect for:
- Testing the interface
- Demonstrations
- Development without AWS access
- Learning how the tool works

## ✅ Currently Running

The app is now running in **Demo Mode** at: **http://localhost:5001**

## 🧪 Supported Ingredients in Demo Mode

The mock linter recognizes these ingredients:
1. **mango** - Full response with 4 indigenous synonyms
2. **turmeric** - Ayurvedic context with Hindi/Tamil/Telugu names
3. **coconut** - Young vs mature context
4. **ginger** - Fresh vs dried variations
5. **cardamom** - Green vs black varieties
6. **vanilla** - Aztec origins and varieties
7. **corn** - Mesoamerican sacred crop
8. **cinnamon** - Ceylon vs Cassia
9. **pepper** - King of spices
10. **honey** - Floral varieties

## 📝 Try These Examples

### Example 1: Single Ingredient
```
mango
```
**Expected Result:**
- 4 indigenous synonyms (Manga, Aam, Māṅgāy, Mangga)
- Ripeness context (verde vs madura, kairi vs aam)
- Brand insights
- Traditional uses

### Example 2: Multiple Ingredients
```
Our organic skincare line uses mango butter, turmeric extract, and coconut oil.
```
**Expected Result:**
- 3 ingredients detected and underlined
- Each with full cultural context
- Click underlined words to jump to details

### Example 3: Spice Blend
```
Traditional tea blend with ginger, cardamom, and black pepper.
```
**Expected Result:**
- 3 spices analyzed
- Ayurvedic context
- Preparation methods

### Example 4: Recipe
```
Authentic recipe with corn masa, vanilla beans, and cinnamon.
```
**Expected Result:**
- Mesoamerican heritage
- Sacred crop significance
- Traditional preparation

## 🎯 How to Use

1. **Open browser**: http://localhost:5001
2. **Type or paste** any of the supported ingredients
3. **Wait 500ms** for automatic analysis
4. **See underlines** appear on detected ingredients
5. **Click underlined words** to scroll to details in sidebar
6. **Explore** indigenous synonyms, brand insights, and traditional uses

## 🔄 Switch to Real Bedrock

To use real AWS Bedrock (when you have valid credentials):

1. Edit `.env` file:
```env
USE_MOCK_LINTER=false
```

2. Ensure AWS credentials are configured in `~/.aws/credentials`

3. Restart the app:
```bash
# Stop current process (Ctrl+C)
python3.10 app.py
```

## 🐛 Troubleshooting

### Not seeing results?
- Make sure you're typing one of the supported ingredients
- Check browser console for errors (F12)
- Verify app is running at http://localhost:5001

### Underlines not appearing?
- Wait 500ms after typing
- Or click "Analyze Text" button for immediate analysis
- Check that ingredient is in the supported list above

### Want to add more ingredients?
Edit `linter_mock.py` and add new responses to `self.mock_responses` dictionary

## 📊 What You'll See

For "mango butter, turmeric extract, and coconut oil":

**Sidebar will show:**
- **Mango** card with:
  - Manga (Portuguese) - ripeness context
  - Aam (Hindi) - kairi vs aam stages
  - Māṅgāy (Tamil) - pickle vs fresh use
  - Mangga (Tagalog) - Filipino preference
  - Brand insights
  - Traditional uses
  - Authenticity markers

- **Turmeric** card with:
  - Haldi (Hindi) - wedding ceremonies
  - Manjal (Tamil) - prosperity symbol
  - Pasupu (Telugu) - ceremonial use
  - Ayurvedic context
  - Fresh vs dried

- **Coconut** card with:
  - Nariyal (Hindi) - sacred offering
  - Thengai (Tamil) - prosperity
  - Kelapa (Malay) - santan preparation
  - Young vs mature stages

## 🎨 Visual Features

- **Yellow underlines** on detected ingredients
- **Hover effect** on underlined words
- **Click to scroll** to sidebar details
- **Pulse animation** when scrolling to card
- **Color-coded badges** by category
- **Expandable sections** for synonyms, insights, uses

## 💡 Pro Tips

1. Type slowly to see real-time linting (500ms debounce)
2. Click "Analyze Text" for immediate results
3. Click underlined words to explore details
4. Try combining multiple ingredients
5. Check character/word count at bottom

---

**Ready to explore?** The app is running at http://localhost:5001 in Demo Mode!
