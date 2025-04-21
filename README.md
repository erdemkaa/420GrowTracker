# 🌱 Cannabis Grow Tracker
AI-powered Cannabis Grow Tracker with Smart Recommendations and Feedback.

A desktop GUI application built with Python and Tkinter to help cannabis cultivators track and compare recommended vs. actual grow data weekly. Ideal for coco and soil growers using the Advanced Nutrients Sensi Grow & Bloom line.

## 📦 Features

- 🌿 Input-based grow schedule generation using:
  - Strain name
  - Sprouting date
  - Growing medium (Coco or Soil)
  - Veg time (weeks)
  - Flower time (days)
- 📅 Week-by-week tracking with autofill of:
  - EC In/Out
  - pH In/Out
  - PPFD
  - VPD
  - Supplements (as checkboxes)
- ✍️ Notes section for each week
- 📊 Comparison between recommended and actual values
- 💾 Saves progress locally to Data folder as (`grow_data.json`)
- 🔁 Auto-adjusts the veg and flower phases based on user inputs
- ✅ Soil-specific pH/EC adjustments
- 🔄 Navigation between weeks
- 📤 Export your grow log (`grow_data.json`) file, which can be shared with AI platforms like ChatGPT for personalized feedback and growth recommendations.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Tkinter (usually comes with Python)
  
### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cannabis-grow-tracker.git
   cd cannabis-grow-tracker
