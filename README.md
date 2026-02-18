# Fortune Stick

A Flask web application that simulates the traditional Chinese fortune stick divination (求籤) experience.

## Introduction

This web application recreates the authentic experience of drawing fortune sticks. Users can draw virtual fortune sticks and receive detailed divination results including poems, interpretations, and predictions for different aspects of life.

這個應用程式讓您隨時隨地體驗傳統的求籤文化。

## Features

- **Virtual Fortune Drawing**: Draw fortune sticks with animated effects
- **Traditional Poems**: 30 authentic fortune poems (籤詩)
- **Detailed Interpretations**: Comprehensive readings for:
  - Career (事業)
  - Wealth (財運)
  - Love (感情)
  - Health (健康)
- **Traditional Design**: Hong Kong temple-inspired UI with festive decorations
- **Mobile Responsive**: Works on all devices
- **Hong Kong Yearly Outlook**: Special feature to predict Hong Kong's prospects for the coming year

## Tech Stack

- **Backend**: Flask 3.0.0 (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Templates**: Jinja2
- **Styling**: Custom CSS with traditional Chinese design elements

## Installation

1. Clone the repository:
```bash
git clone git@github.com:henrychtang/fortune-stick.git
cd fortune-stick
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Flask application:
```bash
python app.py
```

2. Open your browser and visit:
```
http://localhost:5002
```

3. 誠心默念所求之事 (Sincerely focus on your question)
4. 點擊「誠心求籤」按鈕 (Click the "Draw Fortune" button)
5. 查看您的籤文和解說 (View your fortune stick and interpretation)

## Project Structure

```
fortune-stick/
├── app.py              # Flask application with fortune data
├── requirements.txt    # Python dependencies
├── static/
│   ├── style.css      # Traditional Chinese temple styling
│   └── script.js      # Interactive fortune drawing logic
└── templates/
    ├── index.html     # Main page template
    └── hk_outlook.html # Hong Kong outlook template
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main page |
| `/hk-outlook` | GET | Hong Kong yearly outlook prediction |
| `/api/draw` | GET | Draw a random fortune stick |
| `/api/draw-hk` | GET | Draw fortune stick with HK interpretation |
| `/api/all` | GET | Get all fortune sticks |

## Fortune Data

The application includes 30 traditional fortune sticks featuring:
- **籤號 (Stick Number)**: 1-30
- **籤類 (Fortune Type)**: 上籤 (Good), 中籤 (Medium), 下籤 (Challenging)
- **籤詩 (Poem)**: Traditional Chinese poetry
- **解曰 (Meaning)**: Overall interpretation
- **各方面運程 (Aspects)**: Career, wealth, love, and health predictions

## Development

### Adding More Fortune Sticks

To add more fortune sticks, edit the `FORTUNE_STICKS` list in `app.py`:

```python
{
    "number": 31,
    "type": "上籤",
    "poem": "您的籤詩...",
    "meaning": "解說...",
    "career": "事業...",
    "wealth": "財運...",
    "love": "感情...",
    "health": "健康..."
}
```

### Customizing Styles

Edit `static/style.css` to customize the traditional temple appearance.

## License

This project is open source. Feel free to use and modify for personal or educational purposes.

## Acknowledgments

- Inspired by traditional Chinese fortune stick divination
- Traditional Chinese cultural heritage
- Hong Kong temple architecture and design elements

---

**誠心誠意 · 心誠則靈**

*Sincerely focus, and your wish will come true!*
